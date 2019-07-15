## DataCon 方向一 DNS恶意流量检测 WriteUp Review
<!-- MarkdownTOC -->

- 一、题目说明
- 二、知识储备
- 三、解题过程
    - 1.子域名爆破攻击
    - 2. DDOS反射放大攻击
    - 3. 非法DNS 动态更新攻击
    - 4. 非法DNS域传输攻击
    - 5. DNSSec NSec 域名遍历攻击
- 四、Q&A
- 五、总结与反思

<!-- /MarkdownTOC -->

------



#### 一、题目说明

1. **题目背景**
   假如你是某网络的管理员，近日接到告警称，网络中存在 DNS 攻击行为，希望你进行调查。现捕获到网络中的 DNS 流量，请对其中的攻击行为进行分析。
2. **题目要点**
   DNS是互联网中重要的基础设施之一，对网络的稳定运行有至关重要的作用。然而，由于设计缺陷，DNS 存在诸多脆弱点，因此可被利用与诸多攻击。本题对常见的 DNS 安全问题进行考察。

-----------------------------------------------------------------------------------------

#### 二、知识储备

1. **DNS协议及报文格式**

   这篇[文章](https://jocent.me/2017/06/18/dns-protocol-principle.html#_label2)对于DNS讲的还比较透彻，在此基础做一点摘要。
   
    + 域名层次结构
       ![域名层次](http://ww1.sinaimg.cn/large/6e4e7200ly1g4r8j4pn8xj20tm0ar74y.jpg)
   
    + 域名服务器
    ![域名服务器](http://ww1.sinaimg.cn/large/6e4e7200ly1g4r8nxtahtj20qt09zaap.jpg)
   另外还有一个本地域名服务器：当一个主机发出DNS查询请求的时候，这个查询请求首先就是发给本地域名服务器的。
    
    + 域名解析过程
    
   以查询`jocent.me`为例，其中10.74.36.90为主机IP，10.74.1.11为本地DNS服务器：<br/>
    ①主机10.74.36.90先向本地域名服务器10.74.1.11进行递归查询<br/>
    ②本地域名服务器采用迭代查询，向一个根域名服务器进行查询<br/>
    ③根域名服务器告诉本地域名服务器，下一次应该查询的顶级域名服务器`dns.me`的IP地址<br/>
    ④本地域名服务器向顶级域名服务器`dns.me`进行查询<br/>
    ⑤顶级域名服务器me告诉本地域名服务器，下一步查询权限服务器`dns.jocent.me`的IP地址<br/>
 ⑥本地域名服务器向权限服务器`dns.jocent.me`进行查询<br/>
    ⑦权限服务器`dns.jocent.me`告诉本地域名服务器所查询的主机的IP地址<br/>
    ⑧本地域名服务器最后把查询结果告诉 10.74.36.90<br/>
    其中有两个概念递归查询和迭代查询:
    **递归查询**：本机向本地域名服务器发出一次查询请求，就静待最终的结果。如果本地域名服务器无法解析，自己会以DNS客户机的身份向其它域名服务器查询，直到得到最终的IP地址告诉本机。<br/>
     **迭代查询**：本地域名服务器向根域名服务器查询，根域名服务器告诉它下一步到哪里去查询，然后它再去查，每次它都是以客户机的身份去各个服务器查询。
    
    + 报文格式
    ![DNS协议报文格式](http://ww1.sinaimg.cn/large/6e4e7200ly1g4r98y58kmj20ob0bc3z6.jpg)
   
2. <a id='ANY'> **DNS资源记录ANY类型**
  为什么在DDOS方法攻击的时候需要指定ANY类型参数，我们使用dig命令来看一下具体情况：
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4sps2a7apj20tm0i1q8t.jpg)
  可以看到，DNS服务器返回了该服务器中所有关于`163.com`的资源记录，包括类型A，NS，MX，TXT，这样就使得响应数据包远远大于请求数据包。
  我们不妨再往深层次想一想，已知UDP数据包的最大长度是512字节，也就是说当DNS响应数据大于512字节的时候，数据只返回512字节，剩余的数据将被丢弃。为什么在这个地方DNS的响应数据可以返回大于2000字节的数据呢？可以去查看请求数据包中的Additional Records有一条OPT类型的资源记录，OPT类型是一种一个“伪 DNS记录类型”以支持 EDNS协议，其中`UDP Payload Size`字段可以指定DNS返回报文的最大长度。[这里](http://blog.hnxiezan.com/blog/post/1/)对EDNS有比较详细的解释。

3. **DNS攻击类型**

  [这里](https://securitytrails.com/blog/most-popular-types-dns-attacks)有对DNS的各种攻击类型的介绍。

4. `dns.flags.opt`**常见的值**
  - dns.flags.opcode=0(只显示DNS常规查询消息，以及相应的DNS响应消息)

  - dns.flags.opcode=1(只显示DNS逆向查询消息，以及相应的DNS响应消息)

  - dns.flags.opcode=2(只显示DNS服务器状态请求查询消息，以及相应的DNS服务器状态响应消息)

  - dns.flags.opcode=5(只显示DNS动态更新查询消息，以及相应的DNS动态更新响应消息）
5. **DNS资源记录（RR）类型——NS和SOA**

   [NS和SOA的区别](https://www.cnblogs.com/comefuture/p/7543752.html)

   **SOA**，即Start Of Authority，放在 zone file 中，用于描述这个 zone 负责的 name server，version number…等资料，以及当 slave server 要备份这个 zone 时的一些参数。每个 zone file 中必须有且仅有一条 SOARR ，并在 zone file 中作为第一条资源记录保存。

6. **DNS资源记录（RR）类型——AXFR和IXFR**

   AXFR（完全区域传输 252）：由主域名服务器转移整个区域文件至辅助域名服务器。

   IXFR（增量区域传输 251）：请求只有与先前流水式编号不同的特定区域的区域转移。此请求有机会被拒绝，如果权威服务器由于配置或缺乏必要的数据而无法履行请求，一个完整的（AXFR）会被发送以作回应。

   [详细介绍](https://www.cnblogs.com/cyjaysun/p/4265240.html)

7. **DNSSEC协议**

   [浅谈DNS域名安全扩展协议DNSSEC](https://bbs.huaweicloud.com/blogs/1f0fba3f514e11e9bd5a7ca23e93a891)

-----------------------------------------------------------------------------------------

#### 三、解题过程

##### 1.子域名爆破攻击
- 攻击原理
  
[链接](https://www.secpulse.com/archives/55823.html)
  
- 发现过程
  首先，用 Wireshark 打开 pcap 包，绘制 IO Graphs：
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rdg2cpa3j211g0b1jun.jpg)
  可见，在 5500 - 6000s 中出现了异常的峰值流量，将5500s到6000s所有请求、响应提取到新的 pcap文件。

  接下来使用 协议分级 查看哪些协议占比最多：
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rdzspy3ej20us05u0tm.jpg)
  可以看到，切出来的包里面仅有DNS协议，而且用户主动发送的数据包占比最大。
  查看分组长度
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rer19tc2j20m7081gmo.jpg)<br/>
  **长度为1280~2559字节的数据包通常表示数据传输，长度较小的数据包则表示协议控制序列**

  以请求数量从高到低的 IP 地址进行排序。
  **方法一(速度很慢)：**
  使用wireshark的统计功能，并且用`dns.flags.response == 0`进行筛选(只看DNS查询报文)：
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rfgmc1aoj20mb0ckmz3.jpg)<br/>
  **方法二：**

  使用tshark命令行进行筛选`tshark -r timeTop.pcap -T fields -e ip.src -e ip.dst | tr "\t" "\n" | sort | uniq -c | sort -nr > ipRank.txt`
  
  参数解释：
  
  -r 指定目标文件
  
  -Y 指定过滤规则
  
  -T pdml|ps|text|fields|psml,设置解码结果输出的格式，包括text,ps,psml和pdml，默认为text
  
  -e  如果-T fields选项指定，-e用来指定输出哪些字段
  
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rfi2f16nj20p00gsjsm.jpg)
  首先查看第一个IP 45.80.170.1：
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rlk5wk9bj211k09iaci.jpg)
  可以看到这个IP地址是一个DNS服务。
  再来查看第二个IP 144.202.64.226：
  
![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rlqt02paj211i0e5n0s.jpg)
  144.202.64.226 发起了大量针对`b0e.com.cn`域名的查询请求，且大部分相应结果均为 No such name，因此判断此类攻击为子域名爆破攻击。
  通过观察，可以发现，前 10 个请求并不是域名爆破攻击，去掉该 10 个请求后，第一类攻击共有 34184 个。
  
- 分析结果


##### 2. DDOS反射放大攻击
- 攻击原理
![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4rm7yrtvbj20970adwek.jpg)
    + 流量放大：利用回复包比请求包大的特点
    + 地址伪造：伪造请求包的源地址为攻击目标
    + 分布式：多个 DNS 同时向攻击目标返回大量响应
  
- 攻击特征
  - 通过递归查询从而放大流量，因此recursion=1，ANY参数（[为什么必须是ANY参数](#ANY)）。
  - 要求返回包远远大于发送包，一般返回包的要求大于3000。即dns.rr.udp_payload_size>=3000。

- 发现过程
  通过攻击特征可以得出筛选条件`dns.flags.response == 0 && dns.flags.recdesired == 1 && dns.qry.type == 255 && dns.rr.udp_payload_size >= 3000`，再对筛选后的IP地址进行统计：`tshark -r q1_final.pcap -Y "dns.flags.recdesired==1 && dns.flags.response==0 && dns.rr.udp_payload_size>=3000 && dns.qry.type==255" -T fields -e ip.src -e ip.dst | sort | uniq -c| sort -nr|more`
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4v0zdtr9lj20u4092113.jpg)
  这样就过滤出了 DNS 服务响应数据了，一共有188.141.167.218，187.199.129.12，70.85.232.160，45.80.170.1四个DNS服务器，接着排除不支持 **ANY** 的 DNS 服务器，也就是 Refused：

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4v2thmc2lj20rm0a2acr.jpg)

  排查之后，可知攻击IP（也就是排除目的IP为45.80.170.1的源IP）：127.130.104.152，175.222.102.169，105.191.150.205。

##### 3. 非法DNS 动态更新攻击

- 攻击原理

  [这里](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc771255(v=ws.11))对DNS Dynamic Update有比较详细的介绍。简单地来说，DNS 客户端在 IP 地址或名称出现更改的任何时候都可利用 DNS 服务器来注册和动态更新其资源记录，攻击者可以利用 IP 欺骗伪装成 DNS 服务器信任的主机对区数据进行添加、删除和替换。

- 攻击特征：

  - `dns.flags.opt==5`显示DNS动态更新查询消息，以及相应的DNS动态更新响应消息

- 发现过程

  使用tshark命令筛选：`tshark -r q1_final.pcap -Y "dns.flags.opcode==5 && dns.flags.response==0" -T fields -e ip.src -e ip.dst | sort | uniq -c | sort -nr|more `
  
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4v5ml7ag3j20u1034wgx.jpg)
  
  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4v5m8avcnj20u103lwhb.jpg)
  
  可以看到，有四个攻击IP：19.220.251.87 414，200.152.141.106 15，18.100.48.86 4091，237.205.156.233 535
  
- 检测结果

##### 4. 非法DNS域传输攻击

- 攻击原理

  辅 DNS 服务器，需要与主 DNS 服务器进行通信，加载数据信息，称为区域传送（Zone Transfer）。AXFR 请求，常导致全区域传送，需要花费大量的时间与带宽。

  大量的 AXFR 、IXFR请求，可导致 DDoS。权限配置不当，可导致信息泄露（测试域名、内部域名）。

- 攻击特征

  `dns.flags.repsonse==0 && dns.qry.type==252 || dns.qry.type==251`

- 发现过程

  我们用过滤器`dns.qry.type in {251 252}`把AXFR和IXFR过滤出来，查看有哪些疑似攻击IP

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4xcp6egw1j20u602n76f.jpg)

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4xcpjs2jmj20u1025abs.jpg)

  有两个221.223.19.169 和一个129.191.74.107 发来的域传送请求包，以及大量的96.199.230.176 发来的域传送请求包。仔细检查一下前两个IP地址的数据包后，我们认为前面两个有可能是管理员配置不当等造成的，
  而最后的一个大量的请求数据包显然就是域传送攻击了。

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4xg9i185aj210q0fsq4l.jpg)

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4xgkoujpxj20pn0cldgg.jpg)

- 检测结果

##### 5. DNSSec NSec 域名遍历攻击

- 攻击原理

  [DNSSec的概念与作用](https://www.cloudxns.net/Support/detail/id/1309.html)

  [NSEC：Walking a DNS zone](https://info.menandmice.com/blog/bid/73645/Take-your-DNSSEC-with-a-grain-of-salt)

  NSEC枚举这是针对DNSSEC的一种攻击，在未使用NSEC3的DNSSEC中，若查询区文件中不存在的域名，会以NSEC记录的形式提供靠近其的最近的下一条域名，这就造成了可能构造特殊请求，来遍历区文件，造成区文件的泄露。

- 攻击特征

  域名遍历攻击依赖于NSec资源记录类型，可以使用``dns.resp.type==47`进行初步筛选

- 发现过程

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4zkhyihryj210q0exwgu.jpg)

  可以看到我们把ANY反射型Dos攻击也筛选出来了，于是再加上`not dns.qry.type==255`条件就可以得到DNSSec NSec 域名遍历攻击IP：6.116.183.244

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g4zjhnxh23j210s0etmzh.jpg)

- 检测结果

-----------------------------------------------------------------------------------------

#### 四、Q&A

1. pacp包文件过大，Wireshark加载失败

   解决办法：使用 `editcap -c <packets per file> 原始文件.pcap 输出文件.pcap` 命令；或者使用`tcpdump -r old_file -w new_files -C 10`，在这个例子中，每个文件的大小是10 million字节。

2. bash管道格式化输出命令

   - [tr](https://blog.csdn.net/u010003835/article/details/80752797)
   - [sort -nc](https://www.jianshu.com/p/291632a11ede)
   - [sort | uniq -c](https://blog.csdn.net/u014756827/article/details/78949924)
   - [awk](https://www.cnblogs.com/xiaoleiel/p/8349487.html)
   - [more](https://www.runoob.com/linux/linux-comm-more.html)
   - [wc](https://www.cnblogs.com/blogoflee/archive/2012/02/10/2344939.html)
   
3. 几个经常用到的DNS显示过滤器的实例

   - `dns.flags.response=0`(DNS查询消息)
   - `dns.flags.response=1`(DNS响应消息)
   - `dns.flags.rcode=0`(显示RCODE字段值为0(Noerror)的DNS应答消息)
   - `dns.flags.rcode=3`(显示RCODE字段值为3(NXDomain,表示域名不存在)的DNS应答消息)
   - `dns.flags.opcode=0`(显示DNS常规查询消息，以及相应的DNS响应消息)
   - `dns.flags.opcode=1`(显示DNS逆向查询消息，以及相应的DNS响应消息)
   - `dns.flags.opcode=2`(显示DNS服务器状态请求查询消息，以及相应的DNS服务器状态响应消息)
   - `dns.flags.opcode=5`(显示DNS动态更新查询消息，以及相应的DNS动态更新响应消息)
   - `dns.flags.recdesired=1`(RD标记位置1的DNS查询消息一般为主机发出，目的是要求接受该消息的DNS服务器执行递归查询)
   - `dns.flags.recdesired=0`(显示RD标记位置0的DNS递归反复查询及响应消息)
   
4. 常用的查询字段

   | 字段                    | 描述                 | 字段                    | 描述                     |
   | ----------------------- | -------------------- | ----------------------- | ------------------------ |
   | frame.len               | 数据长度             | dns.flags.authenticated | 服务器是否为域权威服务器 |
   | ip.src                  | 源IP                 | dns.flags.checkisable   | 非认证数据是否可接收     |
   | ip.dst                  | 目的IP               | dns.flags.rcode         | DNS reply code           |
   | udp.srcport             | 源udp端口号          | dns.count.quires        | 数据包中DNS请求数        |
   | udp.dstport             | 目的udp端口号        | dns.count.answers       | 数据包中DNS回答数        |
   | eth.src                 | 源MAC地址            | dns.count.auth_rr       | 数据包中权威记录数       |
   | eth.dst                 | 目的MAC地址          | dns.count.add_rr        | 数据包中额外记录数       |
   | dns.id                  | DNS Transaction ID   | dns.qry.name            | DNS请求名                |
   | dns.flags.response      | DNS请求/现有响应标志 | dns.qry.class           | DNS请求类型              |
   | dns.flags.opcode        | DNS opcode           | dns.resp.name           | DNS响应名                |
   | dns.flags.authoritative | 应答是否被服务器认证 | dns.resp.type           | DNS回复类型              |
   | dns.flags.truncated     | 消息是否被截断       | dns.resp.ttl            | DNS响应生存时间          |
   | dns.flags.recdesired    | 是否递归查询         | dns.resp.z.do           | DNS是否支持DNSSEC        |
   | dns.flags.reavail       | 服务器是否能递归查询 | frame.time_relative     | frame相对时间            |

5. 常用查询字段类型

   | TYPE  | 值   | 含义                    |
   | ----- | ---- | ----------------------- |
   | A     | 1    | 主机地址                |
   | NS    | 2    | 权威服务器              |
   | CNAME | 5    | 别名的正则名称          |
   | SOA   | 6    | 标记权威区域的开始      |
   | PTR   | 12   | 域名指针                |
   | MX    | 15   | 邮件交换                |
   | TXT   | 16   | 文本字符串              |
   | DS    | 43   | 委托签发者              |
   | IXFR  | 251  | 增量区域转移            |
   | AXFR  | 252  | 权威区域转移            |
   | *     | 255  | 所有解析记录，也成为ANY |

------

#### 五、总结与反思