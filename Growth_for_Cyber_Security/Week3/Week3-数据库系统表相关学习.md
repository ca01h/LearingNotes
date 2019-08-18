## Week3 数据库系统表相关学习

### 0x00 任务目标

1. 学习数据库系统表的功能，如何利用SQL语句查询库名、表名、字段名、内容以及当前用户等基本信息；
2. 如何利用数据库的功能读写文件，需要什么样的条件才可以读写；
3. **扩展：**查询用户的哈希值，并使用hashcat来对获取的hash进行暴力破解。

### 0x01 MySQL系统表

#### 一、information_schema

**数据库元数据：**

元数据(meta data)——“data about data” 关于数据的数据，一般是结构化数据（如存储在数据库里的数据，规定了字段的长度、类型等）。所以metadata就是描述数据的数据，在MySQL中就是描述database的数据。有哪些数据库、每个表有哪些表、表有多少字段、字段是什么类型等等，这样的数据就是数据库的元数据。

综上，我们可以称`information_schema`是一个**元数据库**。它就像物业公司的信息库，对管理的每栋大厦有多少电梯、电梯型号、每个房间的长宽高等等了如指掌。

1. ##### SCHEMATA

   提供数据库信息，有哪些数据库，字符集是GBK还是UTF-8等等。

   所有字段名：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62uv0t1q0j20kp03ot97.jpg)

   其中某一条数据：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62uxo6ljvj20nw01d0so.jpg)

   **命令`SHOW DATABASES;`的结果取自此表**

2. ##### TABLES

   提供表的信息，数据库有哪些表，是什么存储引擎等等。

   所有字段名：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62v12v0n0j20jj0ct76r.jpg)

   常用字段包含：

   | 字段名       | 含义     | 备注 |
   | ------------ | -------- | ---- |
   | TABLE_SCHEMA | 数据库名 |      |
   | TABLE_NAME   | 表名     |      |
   | TABLE_TYPE   | 表的类型 |      |
   | ENGINE       | 存储引擎 |      |
   | CREATE_TIME  | 建表时间 |      |

   其中某几条记录：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62v61aw7vj20mw03x0td.jpg)

   **命令`SHOW TABLES;`的结果取自此表**

3. ##### COLUMNS

   提供字段的信息，有哪些字段字段类型是什么等等。

   所有字段名：

   ![1566038785942](C:\Users\51196\AppData\Roaming\Typora\typora-user-images\1566038785942.png)

   常用字段名：

   | 字段名      | 含义     | 备注                   |
   | ----------- | -------- | ---------------------- |
   | SCHEMA_NAME | 数据库名 |                        |
   | TABLE_NAME  | 表名     |                        |
   | COLUMN_NAME | 字段名   |                        |
   | COLUMN_TYPE | 字段类型 | 如int(10),varchar(250) |

   其中某几条记录：

   ![1566039093716](C:\Users\51196\AppData\Roaming\Typora\typora-user-images\1566039093716.png)

   **等同命令：`SHOW COLUMNS` 或者 `desc learnSQL.customers` 看emp表的具体字段。**

4. ##### STATISTICS

   这张表的单词是统计的意思，但是却是索引的信息。

   > [什么是索引](https://www.liaoxuefeng.com/wiki/1177760294764384/1218728442198976)

   所有字段名：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62vhu74ggj20ib0a0768.jpg)

   | 字段名       | 含义         | 备注         |
   | ------------ | ------------ | ------------ |
   | SCHEMA_NAME  | 数据库名     |              |
   | TABLE_NAME   | 表名         |              |
   | INDEX_SCHEMA | 也是数据库名 |              |
   | INDEX_NAME   | 索引名       |              |
   | COLUMN_NAME  | 字段名       |              |
   | INDEX_TYPE   | 索引类型     | 一般是B-Tree |

   其中几条记录：

   ![1566043823615](C:\Users\51196\AppData\Roaming\Typora\typora-user-images\1566043823615.png)

   **等同于命令：`SHOW INDEX;`**

5. ##### TABLE_CONSTRAINTS

   提供约束情况，我们想看看表有哪些约束？约束指的是唯一性约束、主键约束、外键约束。

   所有字段名：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62xqyr7lzj20kq0430td.jpg)

   常用字段名：

   | 字段名            | 含义         | 备注                             |
   | ----------------- | ------------ | -------------------------------- |
   | CONSTRAINT_SCHEMA | 数据库名     |                                  |
   | CONSTRAINT_NAME   | 约束名       |                                  |
   | TABLE_SCHEMA      | 也是数据库名 |                                  |
   | TABLE_NAME        | 表名         |                                  |
   | CONSTRAINT_TYPE   | 约束类型     | UNIQUE、PRIMARY KEY、FOREIGN KEY |

   其中几条记录：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62xt8hqe4j20qc07c3zm.jpg)

   >  唯一约束和主键约束，我们在前面的索引中一样可以查到

6. ##### KEY_COLUMN_USAGE

   有STATISTICS和TABLE_CONSTRAINTS表，为什么还需要KEY_COLUMN_USAGE？
   因为外键时没有指出参考的是哪张表的哪个字段！

   所有字段：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62xvqbu0dj20my07lmys.jpg)

   常用字段：

   | 字段名                  | 含义         | 备注                  |
   | ----------------------- | ------------ | --------------------- |
   | CONSTRAINT_SCHEMA       | 数据库名     |                       |
   | CONSTRAINT_NAME         | 约束名       | PRIMARY或列名或外键名 |
   | TABLE_SCHEMA            | 也是数据库名 |                       |
   | TABLE_NAME              | 表名         |                       |
   | COLUMN_NAME             | 列名         |                       |
   | REFERENCED_TABLE_SCHEMA | 参考的数据库 |                       |
   | REFERENCED_TABLE_NAME   | 参考的表     |                       |
   | REFERENCED_COLUMN_NAME  | 参考的列     |                       |

   其中几条记录：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g62xzsvazsj20z107z0uc.jpg)

   相比前面两个，KEY_COLUMN_USAGE这个表的信息是最全的。包括主键、外键、唯一约束。

7. ##### VIEWS

   查询数据库下所有的视图。

   所有字段名：

   ![1566044609083](C:\Users\51196\AppData\Roaming\Typora\typora-user-images\1566044609083.png)

   常用字段名：

   | 字段名          | 含义         | 备注 |
   | --------------- | ------------ | ---- |
   | TABLE_SCHEMA    | 数据库名     |      |
   | TABLE_NAME      | 表名         |      |
   | VIEW_DEFINITION | 视图定义语句 |      |

8. ##### 其他部分表

   - **ENGINES**：列举了当前数据库对InnoDB、MEMORY、MyISAM等各种存储引擎的支持情况。等同`show ENGINES`
   - **GLOBAL_VARIABLES**：服务器变量设置，一些开关和设置。等同命令`show global variables`。除了global还有session。
   - **PLUGINS**：MySQL的插件列表。可以看到存储引擎InnoDB甚至binlog都是插件！binlog是强制加载的，InnoDB是默认打开的。等同命令`show PLUGINS`
   - **PROCESSLIST**：查看正在运行的线程！比如我查这个表，就看到一个查询的线程。等同命令`show full processlist`

#### 二、Performance_schema

主要用于收集数据库服务器性能参数。并且库里表的存储引擎均为PERFORMANCE_SCHEMA，而用户是不能创建存储引擎为PERFORMANCE_SCHEMA的表。MySQL5.7默认是开启的。 

参考：[Performance_schema](https://www.cnblogs.com/zhoujinyi/p/5236705.html)

#### 三、mysql

mysql的核心数据库，类似于sql server中的master表，主要负责存储数据库的用户、权限设置、关键字等mysql自己需要使用的控制和管理信息。(常用的，在mysql.user表中修改root用户的密码)。

> 如何利用SQL语句查询库名、表名、字段名、内容以及当前用户等基本信息
>
> - 查询库名：`SELECT schema_name FROM infomation_schema.schemata;`
> - 查询表名：`SELECT table_name FROM information_schema.tables WHERE table_schema='test'`;
> - 查询字段名：`SELECT column_name FROM information_schema.columns WHERE table_name='col'`;
> - 查询记录：`SELECT * FORM test.col;`

### 0x02 读写文件

#### 一、利用数据库读取文件

1. ##### 使用system命令

   - 查看文件

     ```bash
     mysql> system cat /etc/passwd
     root:x:0:0:root:/root:/bin/bash
     daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
     bin:x:2:2:bin:/bin:/usr/sbin/nologin
     sys:x:3:3:sys:/dev:/usr/sbin/nologin
     sync:x:4:65534:sync:/bin:/bin/sync
     games:x:5:60:games:/usr/games:/usr/sbin/nologin
     man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
     lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
     mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
     news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
     uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
     proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
     www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
     backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
     list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
     irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
     gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
     nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
     systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
     systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
     syslog:x:102:106::/home/syslog:/usr/sbin/nologin
     messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
     _apt:x:104:65534::/nonexistent:/usr/sbin/nologin
     uuidd:x:105:111::/run/uuidd:/usr/sbin/nologin
     avahi-autoipd:x:106:112:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/usr/sbin/nologin
     usbmux:x:107:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
     dnsmasq:x:108:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
     rtkit:x:109:114:RealtimeKit,,,:/proc:/usr/sbin/nologin
     cups-pk-helper:x:110:116:user for cups-pk-helper service,,,:/home/cups-pk-helper:/usr/sbin/nologin
     speech-dispatcher:x:111:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/false
     whoopsie:x:112:117::/nonexistent:/bin/false
     kernoops:x:113:65534:Kernel Oops Tracking Daemon,,,:/:/usr/sbin/nologin
     saned:x:114:119::/var/lib/saned:/usr/sbin/nologin
     pulse:x:115:120:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
     avahi:x:116:122:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/usr/sbin/nologin
     colord:x:117:123:colord colour management daemon,,,:/var/lib/colord:/usr/sbin/nologin
     hplip:x:118:7:HPLIP system user,,,:/var/run/hplip:/bin/false
     geoclue:x:119:124::/var/lib/geoclue:/usr/sbin/nologin
     gnome-initial-setup:x:120:65534::/run/gnome-initial-setup/:/bin/false
     gdm:x:121:125:Gnome Display Manager:/var/lib/gdm3:/bin/false
     ca0y1h:x:1000:1000:ca0y1h,,,:/home/ca0y1h:/bin/bash
     mysql:x:122:127:MySQL Server,,,:/nonexistent:/bin/false
     ```

   - 执行命令

     ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g63nt6f27lj20jp092q4h.jpg)

   **注意：**

   - 该方法只能在本地使用，远程连接时无法使用system
   - 无法越权使用

2. ##### load_file()与load data file

   load_file()与load data file读取文件的原理都是一样的：新建一个表，读取文件为字符串形式插入表中后读取表中的数据。

   使用load_file()和load data infile()函数时，需要满足以下条件：

   - `secure_file_priv` 不为 NULL，使用 `select @@secure_file_priv`查看其值，值不为空字符串时，只能使用该目录进行文件的读写操作， 该值的设置见[附录](https://bingslient.github.io/2019/08/16/MySQL 数据库系统表的利用/#附录)；
   - 当前数据库用户具有 `FILE` 权限，使用 `show grants`查看；
   - 系统用户 `mysql` 对该文件可读（要考虑系统的访问控制策略），在Ubuntu-18.04使用 MySQL 时默认的系统用户是 `mysql`；
   - 读取文件的大小小于 `max_allowed_packet`，使用 `select @@max_allowed_packet`查看；
   - 文件存在服务器上。

   如果上述任一条件不满足，函数返回 `NULL` 值。

   查看secure_file_priv的值：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g63ycnyqg5j20dd03mq30.jpg)

   可以看到secure_file_priv的值为`/var/lib/mysql-files`

   > ① secure_file_priv为NULL时，表示不允许导入导出；
   > ② secure_file_priv指定文件夹时，表示mysql的导入导出只能发生在指定的文件夹；
   > ③ secure_file_priv没有设置时，则表示没有任何限制

   **在不改变secure_file_priv值的情况下如何读文件：**

   可以新建一个表，或者直接把要读文件的内容into到已有的字符类型的表中。

   ```mysql
   create table mytable(a VARCHAR(100), b VARCHAR(100), c VARCHAR(100), d VARCHAR(100), e VARCHAR(100), f VARCHAR(100), g VARCHAR(100));
   ```

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g63z0tqvswj20qc01pmx7.jpg)

   使用load data infile读取文件：

   ```mysq
   LOAD DATA LOCAL INFILE "/etc/passwd" INTO TABLE mytable;
   ```

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g63z2vt4r8j20fv01n0su.jpg)

   查看刚刚读入的文件：

   ![1566121685409](C:\Users\51196\AppData\Roaming\Typora\typora-user-images\1566121685409.png)

   

   **在改变secure_file_priv值的情况下如何读文件：**

   修改MySQL配置文件`etc/mysql/my.cnf`，在[mysqld]下添加如下内容：

   ```mysql
   secure_file_priv=""
   ```

   再重启mysql服务：

   ```bash
   sudo service mysql restart
   ```

   在mysql命令行中查看`secure_file_priv`的值：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g63zybibb1j20bl03kq2y.jpg)

   修改成功！

   使用load_file()读取文件：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g641rti54aj20ae04m74d.jpg)

   > **在Ubuntu-18.04使用 MySQL 时默认的系统用户是 `mysql`，所以必须把要读取的文件的所有者和用户组修改为`mysql`**

#### 二、利用数据库写入文件

`SELECT INTO OUTFILE` 和 `LOAD DATA` 这两条语句是完全互补的，一个写文件，一个读文件，语句的语法也很相似。

**前提条件：**

- `secure_file_priv` 不为 `NULL`，使用 `select @@secure_file_priv`查看其值，值不为空字符串时，只能使用该目录进行文件的读写操作， 该值的设置见[附录](https://bingslient.github.io/2019/08/16/MySQL 数据库系统表的利用/#附录)；
- 当前数据库用户具有 `FILE` 权限，使用 `show grants`查看；
- 系统用户 `mysql` 对该文件可写（要考虑系统的访问控制策略），在Ubuntu-18.04使用 MySQL 时默认的系统用户是 `mysql`；
- 读取文件的大小小于 `max_allowed_packet`，使用 `select @@max_allowed_packet`查看；
- 文件不存在。

将数据库中的某一个记录写入`/tmp/customer.csv`文件中：

![](http://ww1.sinaimg.cn/large/6e4e7200ly1g642bna6a0j20no06gaaf.jpg)

结果如下：

![1566128262926](C:\Users\51196\AppData\Roaming\Typora\typora-user-images\1566128262926.png)

> 使用 `SELECT INTO DUMPFILE` 可将文件内容写成一行。

> 如果想把远程数据库的查询结果写到本地主机文件上, 可用：
>
> ```mysql
> >mysql -h hostname -P portnum -u username -p databsename -e "SELECT ..." > file_name
> ```

### 0x03 用户密码爆破

MySQL 用户的密码存储方式并非明文直接存储，而是经过 hash 函数加密进行存储的，从 `mysql.user`中获取到 MySQL 用户密码的哈希值后，需要使用工具进行破解。

首先查询`root`用户密码的Hash值：

![](http://ww1.sinaimg.cn/large/6e4e7200ly1g646f0wllhj20g7050t97.jpg)

**工具：**[hashcat](https://github.com/hashcat/hashcat)

> hashcat 号称最快的高级密码恢复套机（密码破解工具），支持多系统（Linux，OS，Windows），多平台（GPU，CPU，DSP等），支持多达 200 多种的 Hash 类型，支持使用同一系统的不同设备，支持分布式系统资源等，重要的是开源啊！

**使用：**

```bash
./hashcat64.exe -m 300 -a 3 hashcode -o plaintxt --outfile-format=2 ?a?a?a?a?a?a
```

参数解释：

- `-m 300`：hash 类型，300 选择的是 MySQL4/5 的hash

- `-a 3`：攻击模式，3代表爆破模式

  > 软件一共支持5种破解模式，分别为:
  >
  > 0 Straight（字典破解）
  > 1 Combination（组合破解）
  > 3 Brute-force（掩码暴力破解）
  > 6 Hybrid dict + mask（混合字典+掩码）
  > 7 Hybrid mask + dict（混合掩码+字典）
  
- `-o pliantxt` ：破解后输出到文件 plaintxt

- `--outfile-format=2`：输出文件格式，2表示只输出破解后的内容

- `?a?a?a?a?a?a`：这表示密码的掩码，所谓的掩码就是通过 ?[字符集代号]… 的格式表示密码的格式，包括密码的位数和每一位密码使用的字符集。?a 表示所有的键盘上可输入的字符，6个?a表示密码有6位。

  > hashcat 内置字符集如下：
  >
  > ?l = abcdefghijklmnopqrstuvwxyz
  >
  > ?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
  >
  > ?d = 0123456789
  >
  > ?h = 0123456789abcdef
  >
  > ?H = 0123456789ABCDEF
  >
  > ?s = !”#$%&’()*+,-./:;<=>?@[]^_`{
  >
  > ?a = ?l?u?d?s
  >
  > ?b = 0x00 - 0xff

  如果要用掩码表示小写+数字怎么办呢？这就需要用到自定义字符集这个参数了。软件支持用户最多定义4组字符集，分别用

  ```bash
  --custom-charset1 [chars]
  --custom-charset2 [chars]
  --custom-charset3 [chars]
  --custom-charset4 [chars]
  ```

  比如说我要设置自定义字符集1为小写+数字，那么就加上:

  ```bash
  -- custom-charset1 ?l?d
  ```

  对于想要破解一些未知长度的密码，希望软件在一定长度范围内进行尝试的，可以使用--increment参数，并且使用--increment-min ?定义最短长度，使用--increment-max ?定义最大长度。比如要尝试6-8位小写字母，可以这样写：

  ```bash
  --increment --increment-min 6 --increment-max 8 ?l?l?l?l?l?l?l?l
  ```

  **爆破结果：**

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g646w12n96j208u02rt8j.jpg)

  > 最新版本的MySQL在配置密码规则是要求密码长度最小为8位，但是我这破电脑用hashcat爆破8位密码预计需要1年的时间，只能强行把密码最小长度改为6位，15分钟解决问题。

  

