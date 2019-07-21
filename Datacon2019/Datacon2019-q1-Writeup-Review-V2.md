### DataCon 方向一 DNS恶意流量检测 WriteUp Review-v2

> 这一轮流量分析主要是**分析**为主，以[这篇Writeup](https://github.com/shyoshyo/DataCon-9102-DNS)为参考，有关DNS的攻击类型、攻击手段和攻击特征，详见[DNS攻击流量分析识别-v1](https://github.com/caoyihuai2/LearingNotes/blob/master/Datacon2019/Datacon2019-q1-Writeup-Review.md)

##### 0x00 系统环境

- Windows10 64bit；
- wireshark 3.0.3 (v3.0.3-0-g6130b92b0ec6) ；
- TShark (Wireshark) 3.0.3 (v3.0.3-0-g6130b92b0ec6)；
- Cmder 18026 preview；
- python 3.7；
- Excel 2016

------

##### 0x01 未授权的Dynamic Update

**切入点：**粗略观察绝大部分DNS包的Opcode都是0（Standard Query），但是我们也可以分析Opcode不为零的。使用以下命令筛选：

`dns and not dns.flags.opcode==0`

![Figure1：未授权的Dynamic Update](http://ww1.sinaimg.cn/large/6e4e7200ly1g548iwinf2j210t0ezgnr.jpg)

可以看到，全部都是DNS Dynamic Update请求。接下来，使用在Cmder中使用tshark命令筛选出所有的攻击IP：

`tshark.exe -r q1_final.pcap -Y "dns.flags.opcode==5 && dns.flags.response==0" -T fields -e ip.src -e ip.dst |awk '{print $1"->"$2}' > DynamicDNSip.csv`

![](http://ww1.sinaimg.cn/large/6e4e7200ly1g54e5ws2vfj20bt0dddg2.jpg)

从图中可以看到有四个攻击来源：19.220.251.87 414，200.152.141.106 15，18.100.48.86 4091，237.205.156.233 535。**由于正常的Dynamic Update 不会发送这么多且这么频繁的请求，而且涉及到二级域名com.cn以及很多其他不同域名的更新**，因此我们认为这些都是攻击。再使用下面一行命令把他们选出来：

`tshark.exe -r q1_final.pcap -Y "dns and not dns.flags.opcode == 0 and dns.flags.response
== 0" -T fields -e frame.number -e ip.src | awk '{print $1",5"; ip[$2] += 1}' > DynamicDNS.csv`

上述命令把这些攻击包的标号和类型(5) 输出到了DynamicDNS.csv

##### 0x02 反射放大攻击

**切入点：**我们接下来再看看除了A(1) 和AAAA(28) 这两个常见类型以外的DNS 请求。使用如下命令启动
wireshark：

`wireshark -r q1_final.pcap -R "dns and not dns.query.type in {1, 28} and dns.flags.opcode == 0"`

![除了A(1) 和AAAA(28) 类型以外的DNS 请求](http://ww1.sinaimg.cn/large/6e4e7200ly1g55hio4fw8j210p0ghq5h.jpg)

如图所示，可以看到有很多杂七杂八的DNS 请求。为便于观察，我们按照请求类型排序。简单浏览一下，我们就能够发现一些攻击。例如，我们可以看到反射放大攻击：

![反射放大攻击](http://ww1.sinaimg.cn/large/6e4e7200ly1g55itxa9hqj210r0h1whb.jpg)

使用以下命令统计各IP的进/出流量：

`tshark -r q1_final.pcap -T fields -e ip.src -e ip.dst -e frame.len | awk '{send[$1]
+= $3; rece[$1] += 0; rece[$2] += $3; send[$2] += 0;} END {for(ip in send) if(rece[ip]
== 0) tmp = 1e60; else tmp = send[ip]/rece[ip]; for(ip in send) print ip, send[ip],
rece[ip], tmp; }' > send_rece.csv`

为了更容易观察这些IP的流量特征，可以使用Python的matplotlib模块作图：

```python
import matplotlib.pyplot as plt
import csv

send = []
rece = []
ip = []

with open('send_rece.csv' ,'r') as csvfile:
	plots = csv.reader(csvfile, delimiter=' ')
	for row in plots:
		if row[0] == '45.80.170.1': continue
		send.append(int(row[1]))
		rece.append(int(row[2]))
		ip.append(row[0])

fig, ax = plt.subplots()
ax.scatter(send, rece, label='')
for i, txt in enumerate(ip):
	if send[i] > 8e6 or rece[i] > 8e6:
		ax.annotate(txt, (send[i], rece[i]))

plt.xlabel('send')
plt.ylabel('receive')
plt.title('')
plt.legend()
plt.show()
```

> 为什么要排除45.80.170.1：
>
> 我们可以使用命令`wireshark -r q1_final.pcap -R "dns and ip.addr == 45.80.170.1"查看相关流量：`
>
> ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rlk5wk9bj211k09iaci.jpg)
>
> 可以看出这个IP是一个DNS服务。

![](http://ww1.sinaimg.cn/large/6e4e7200gy1g56axqdpwaj211y0in3zd.jpg)

可以看到到188.141.167.218、70.85.232.160、187.199.129.12 是反射用的递归DNS，而伪造出的源地址127,130.104.152、175.222.102.169、105.191.150.205 则都是受害者。

> 从图中，102.181.153.79也比较可以，但是使用`ip.addr==102.181.153.79`可以看出它的请求类型主要是MX、NS和CNAME。

`tshark -r q1_final.pcap -Y 'dns.qry.type in {255} and dns.flags.recdesired == 1 and
dns.qry.name in {"734a5.gov" "d1a4.cc"} and not dns.flags.response == 1 and ip.src
in {127.130.104.152 175.222.102.169 105.191.150.205}' -T fields -e frame.number -e
ip.src -e dns.qry.name | awk '{print $1",3"} > Reflect.csv`

上述命令把这些攻击包的标号和类型(3) 输出到了Reflect.csv。

##### 0x03 未授权的域传输攻击

继续浏览除了A(1) 和AAAA(28) 以外的DNS 请求，我们看到了未授权的DNS 域传送攻击。

![DNS域传送攻击](http://ww1.sinaimg.cn/large/6e4e7200ly1g55hmu5dvfj20w90gi0vb.jpg)

我们用显示过滤器`dns.qry.type in {252 251}`把AXFR 和IXFR 过滤出来：

![过滤后的DNS 域传送攻击](http://ww1.sinaimg.cn/large/6e4e7200ly1g55hpxssx8j20wl0gidi8.jpg)

可以手工验证，有两个221.223.19.169 和一个129.191.74.107 发来的域传送请求包，以及大量的96.199.230.176 发来的域传送请求包。我们认为前面两个有可能是管理员配置不当等造成的，而最后的一个大量的请求数据包显然就是域传送攻击了。使用以下命令提取出我们认为是攻击的包：

`tshark -r q1_final.pcap -Y "dns.qry.type in {251 252} and not ip.addr in {221.223.19.169
129.191.74.107} and not dns.flags.response == 1" -T fields -e frame.number -e ip.src
| awk '{print $1",4"; ip[$2] += 1}' > AXFR.csv`

上述命令把这些攻击包的标号和类型(4) 输出到了AXFR.csv。

##### 0x04 DNSSec NSec 域名遍历

继续浏览除了A(1) 和AAAA(28) 以外的DNS 请求，可以看到DNSSec 域名遍历攻击：

![DNSSec域名遍历攻击](http://ww1.sinaimg.cn/large/6e4e7200gy1g56bib7p9gj210q0ghdij.jpg)

由于域名遍历攻击依赖于NSec，我们可以重新执行

`tshark -r q1_final.pcap -R "dns.resp.type == 47 and not dns.qry.type == 255"`

从原来的所有包中重新过滤所有涉及到NSec(47) 项的响应数据包：

![](http://ww1.sinaimg.cn/large/6e4e7200gy1g56cbvlgpdj210s0g0n05.jpg)

容易手工验证，在所有的域名遍历攻击中，攻击者只有6.116.183.244 一个人。我们可以用：

`wireshark -r q1_final.pcap -R "dns and ip.addr == 6.116.183.244"`

过滤出6.116.183.244 发送的所有包：

![](http://ww1.sinaimg.cn/large/6e4e7200gy1g56d4z9fy7j210u0fzjue.jpg)

可见所有的攻击包都是SOA 或者DS 类型的。使用以下命令提取出攻击的包

`tshark -r q1_final.pcap -Y 'dns and dns.qry.type in {43 6} and dns.flags.response
== 0 and ip.src == 6.116.183.244' -T fields -e frame.number -e ip.dst | awk '{print
$1",1"}' > DNSSec.csv`

##### 0x05 Dos子域名遍历攻击

**切入点：**我们可以先统计一下DNS 查询到一个不存在的域名的次数及其请求发起人的IP，具体而言可以使用如下的命令：

`tshark -r q1_final.pcap -Y "dns and dns.flags.rcode == 3" -T fields -e ip.src -e ip.dst -e dns.qry.name | awk '{ip = $2; doname = substr($3, index($3,"."), length($3)); c_ip_doname[ip"@@@"doname] += 1} END {for(i in c_ip_doname) print i, c_ip_doname[i]}' > No_such_name.csv`

> ``substr(string, start` [`, length` ])`：Return a length-character-long substring of string, starting at character number start. The first character of a string is character number one.
>
> `index(str1, str2)： This searches the string *str1* for the first occurrences of the string *str2*, and returns the position in characters where that occurrence begins in the string *str1*

以域名为排序标准，查看No_such_name.csv：

`cat No_such_name.csv | sort -k2nr | less`

![](http://ww1.sinaimg.cn/large/6e4e7200gy1g56f5ke98sj20rl0ef3z9.jpg)

可以看到，144.202.64.226查询了30318次*b0e.com.cn下面不存在的域名，是所有IP中次数最多的。我们可以使用：

`wireshark -r q1_final.pcap -R "dns and ip.addr == 144.202.64.226"`

进一步查看144.202.64.226相关的包：

![](http://ww1.sinaimg.cn/large/6e4e7200ly1g576j59tyhj210s0efmzi.jpg)

可以看出，攻击人144.202.64.226 选了182.254.116.116 、119.29.29.29 和223.6.6.6 三个递归DNS 服务器作为中间“跳板”，攻击b0e.com.cn 的权威DNS 服务器。本来攻击者还想利用223.5.5.5 作为“跳板”的，但是看起来这台DNS 服务器没有工作，无法利用。

对于每个子域名，攻击人都访问了两次。第二次明显快于第一次，说明请求确实到达了权威DNS服务器并被递归服务器缓存。

使用下列命令可以提取出攻击的包：

`tshark -r q1_final.pcap -Y 'dns and dns.flags.response == 0 and ip.src == 144.202.64.226' -T fields -e frame.number -e ip.dst -e dns.qry.name | awk '{print $1",2"}' > DOS.csv`

使用下列命令提取“跳板机器”的dns及其被利用次数：

`tshark -r q1_final.pcap -Y 'dns and dns.flags.response == 0 and ip.src == 144.202.64.226' -T fields -e frame.number -e ip.dst -e dns.qry.name | awk '{dns[$2] += 1} END {for(ip in dns) print ip, dns[ip]'}`

> 119.29.29.29 15719
> 182.254.116.116 16227
> 223.6.6.6 2247
> 223.5.5.5 1

使用下列命令提取询问次数不是两次的域名：

`tshark -r q1_final.pcap -Y 'dns and dns.flags.response == 0 and ip.src == 144.202.64.226' -T fields -e frame.number -e ip.dst -e dns.qry.name | awk '{domain[$3] += 1} END {for(i in
domain) if(domain[i] != 2) print i, domain[i]}' > query_one_time_domain.csv`

我们发现：这些域名要么是Google 的8.8.8.8，访问了四次，用于试探四个“跳板”DNS 递归服务器是否工作；要么是没有收到响应的请求，因此只访问了一次。这间接的说明了受害者的资源已经被消耗了非常多，攻击人对于b0e.com.cn 权威服务器的DoS 攻击是成功的。

------

##### 0x06 分析思路总结

- 首先查看Opcode不为0，即非Standard Query的查询数据包 ---> 未授权的DNS Dynamic Update
- 再查看类型不为A(1)和AAAA(28)，即IPV4和IPV6的查询数据包 ---> 反射放大攻击、未授权的域传输和DNSSec NSec 域名遍历
- 最后可以统计一下返回No Such Name的响应数据包 ---> Dos子域名遍历

