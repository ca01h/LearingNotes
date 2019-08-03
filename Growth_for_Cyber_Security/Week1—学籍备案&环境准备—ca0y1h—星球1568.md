## Week1 环境搭建&服务器加固——2019.08.02

#### 0x00 个人资料

- 知识星球编号：NO.1568

  ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g5lqh0szxjj20mb0kpq5j.jpg)

- 常用名：C@0y1h

- 联系方式：QQ：511965738

- 目前职业：在职（一年）（考研二战，今年9月份南邮信安专业）

- 所在地区：武汉/南京

- 熟悉的编程语言：Python

- 自我介绍：

  讲真，仰慕了很久信安专业，虽然本科很早就开始跟着导师一起做Linux内核安全加固，也小小小有成就，但是心里却一直梦想着CTF、网络对抗这种更富有激情的方向。于是乎，选择考研继续深造，第一年落败，第二年报名相同的学校相同的专业，但是仍然没能成功......当时斟酌了很久很久，还是毅然选择了非全这条路，为的就是想真正进入到这个圈子里面。很羡慕那些小有名气的学长学姐们，尝试了很多方法，也买了些相关的书籍，但还是感觉没有入门，还在门外摸索。 myh0st给了这个机会，一年的时间希望能当成两年来用，真的感觉自己相对于同行业的同龄人，落后的太远。（非全学费一万块，星球入会费我都是闭着眼睛按指纹Orz哈哈哈）





#### 0x01 本周目标

- **任务目标：**准备学习环境，搭建Web服务器，并做相应的服务器加固学习
- **推荐环境：**linux+nginx+php-fpm+mysql
- **预期结果：**能够运行 php 代码并且可以使用 php 连接 mysql，成功执行 mysql 的语句
- **拓展实验：**可以搭建基于 Apache 的环境、基于 Windows Server 的 IIS 环境等

------

#### 0x02 基本环境

- VMware Workstation Player 15
- Ubuntu 18.04.2 LTS

------

#### 0x03 环境搭建

##### 一、 安装Nginx

1. ###### Install Nginx

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

   使用下面命令查看是否安装成功：

   ```bash
   sudo service nginx status
   ```

   如果Nginx启动成功，会有如下显示：

   ```bash
   ● nginx.service - A high performance web server and a reverse proxy server
      Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: en
      Active: active (running) since Sat 2019-07-27 13:12:44 CST; 39s ago
        Docs: man:nginx(8)
    Main PID: 5836 (nginx)
       Tasks: 2 (limit: 3433)
      CGroup: /system.slice/nginx.service
              ├─5836 nginx: master process /usr/sbin/nginx -g daemon on; master_pro
              └─5837 nginx: worker process
   ```

2. ###### Configure Firewall

   > [ubuntu官方文档](https://help.ubuntu.com/lts/serverguide/firewall.html)有对ufw进行简单的介绍

   配置ufw允许ssh、http、https连接：

   ```bash
   sudo ufw allow ssh
   sudo ufw allow http
   sudo ufw allow https
   ```

   启动ufw：

   ```bash
   sudo ufw enable
   ```

   使用下面命令检查防火墙状态：

   ```bash
   sudo ufw status
   
   Status: active
   
   To                         Action      From
   --                         ------      ----
   22/tcp                     ALLOW       Anywhere                  
   80/tcp                     ALLOW       Anywhere                  
   443/tcp                    ALLOW       Anywhere                  
   22/tcp (v6)                ALLOW       Anywhere (v6)             
   80/tcp (v6)                ALLOW       Anywhere (v6)             
   443/tcp (v6)               ALLOW       Anywhere (v6)  
   ```

   在这里，可以看到端口22（SSH），80（https）和443（https）对IPv4和IPv6都是开放的。

3. ###### Test Nginx

   使用`ifconfig`查看本机IP地址`192.168.11.131`

   在浏览器中访问本机IP地址`http://192.168.11.131/`：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g5echydw86j20l00dr0tf.jpg)

##### 二、 安装MySQL

1. ###### Install MySQL

   输入以下命令安装MySQL：

   ```bash
   sudo apt install mysql-server
   ```

   可以按如下方式测试MySQL服务器：

   ```bash
   sudo mysql
   
   Welcome to the MySQL monitor.  Commands end with ; or \g.
   Your MySQL connection id is 2
   Server version: 5.7.27-0ubuntu0.18.04.1 (Ubuntu)
   
   Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.
   
   Oracle is a registered trademark of Oracle Corporation and/or its
   affiliates. Other names may be trademarks of their respective
   owners.
   
   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
   
   mysql> show databases;
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | mysql              |
   | performance_schema |
   | sys                |
   +--------------------+
   4 rows in set (0.00 sec)
   ```

2. ###### Configure MySQL Security

   默认情况下，MySQL服务器只有一个用户：`root`。如果您是Linux系统上的root用户*并*执行`mysql`命令，则只能使用此用户登录数据库，无需输入密码，也不需要输入密码。

   为了确保安装，MySQL附带了一个脚本，该脚本将询问我们是否要修改一些不安全的默认值。键入以下命令启动脚本：

   ```bash
   sudo mysql_secure_installation
   ```

   此脚本将询问您是否要配置`VALIDATE PASSWORD PLUGIN`：

   ```bash
   ca0y1h@ubuntu18042:~$ sudo mysql_secure_installation
   
   Securing the MySQL server deployment.
   
   Connecting to MySQL using a blank password.
   
   VALIDATE PASSWORD PLUGIN can be used to test passwords
   and improve security. It checks the strength of password
   and allows the users to set only those passwords which are
   secure enough. Would you like to setup VALIDATE PASSWORD plugin?
   
   Press y|Y for Yes, any other key for No:
   ```

   输入`y`，接下来脚本还会要求你选择密码验证级别：

   ```bash
   There are three levels of password validation policy:
   
   LOW    Length >= 8
   MEDIUM Length >= 8, numeric, mixed case, and special characters
   STRONG Length >= 8, numeric, mixed case, special characters and dictionary file
   
   Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG:
   ```

   输入`1`选择中等密码强度，接下来，系统会要求您提交并确认root密码：

   ```bash
   New password: 
   
   Re-enter new password: 
   
   Estimated strength of the password: 100 
   Do you wish to continue with the password provided?(Press y|Y for Yes, any other key for No) : y
   ```

   接下来MySQL脚本将删除一些匿名用户和测试数据库，禁用远程root登录，并加载这些新规则：

   ```bash
   By default, a MySQL installation has an anonymous user,
   allowing anyone to log into MySQL without having to have
   a user account created for them. This is intended only for
   testing, and to make the installation go a bit smoother.
   You should remove them before moving into a production
   environment.
   
   Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
   Success.
   
   --snip--
   
   By default, MySQL comes with a database named 'test' that
   anyone can access. This is also intended only for testing,
   and should be removed before moving into a production
   environment.
   
   --snip--
   
   Reloading the privilege tables will ensure that all changes
   made so far will take effect immediately.
   
   Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
   Success.
   
   All done! 
   ```

   最后需要注意的是，在运行MySQL 5.7（及更高版本）的Ubuntu系统中，如果是以root身份用户启动`mysql`命令时，根MySQL用户设置为`auth_socket`默认使用插件进行身份验证，而不是使用密码进行身份验证。如果需要允许外部程序（例如phpMyAdmin）访问用户时，会出现访问受限的情况。

   这样就需要将其身份验证方法从切换`auth_socket`为`mysql_native_password`，使用以下命令检查每个MySQL用户帐户使用的身份验证方法：

   ```bash
   mysql> SELECT user,authentication_string,plugin,host FROM mysql.user;
   +------------------+-------------------------------------------+-----------------------+-----------+
   | user             | authentication_string                     | plugin                | host      |
   +------------------+-------------------------------------------+-----------------------+-----------+
   | root             |                                           | auth_socket           | localhost |
   | mysql.session    | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
   | mysql.sys        | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
   | debian-sys-maint | *A38295EEEA729FDFC0C36C8E270DDA27005B7693 | mysql_native_password | localhost |
   +------------------+-------------------------------------------+-----------------------+-----------+
   4 rows in set (0.00 sec)
   ```

   运行以下`ALTER USER`命令，更改`password`为上述步骤选择的强密码：

   ```bash
   mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
   ```

   然后，运行`FLUSH PRIVILEGES`告诉服务器重新加载授权表并使新的更改生效：

   ```bash
   mysql> FLUSH PRIVILEGES;
   ```

   配置根MySQL用户使用密码进行身份验证后，将无法再`sudo mysql`使用先前使用的命令访问MySQL 。相反，必须运行以下命令：

   ```bash
   mysql -u root -p
   ```

   输入刚刚设置的密码后，将看到MySQL提示符。

   此时，数据库系统现已设置完毕，接下来继续安装PHP。

##### 三、安装PHP&配置Nginx

1. ###### Install php-fpm

   与Apache不同，Nginx不包含本地PHP处理。为此，我们必须安装PHP-FPM（FastCGI Process Manager）。FPM是另一种PHP FastCGI实现，具有一些对重载站点有用的附加功能。另外还需要安装php-mysql以允许PHP与MySQL数据库通信。

   ```bash
   $ sudo apt install php-fpm php-mysql
   ```

   查看PHP是否安装成功：

   ```bash
   $ php --version
   PHP 7.2.19-0ubuntu0.18.04.1 (cli) (built: Jun  4 2019 14:48:12) ( NTS )
   Copyright (c) 1997-2018 The PHP Group
   Zend Engine v3.2.0, Copyright (c) 1998-2018 Zend Technologies
       with Zend OPcache v7.2.19-0ubuntu0.18.04.1, Copyright (c) 1999-2018, by Zend Technologies
   ```

2. ###### Configure Nginx for PHP

   现在已经安装了所有必需的LEMP堆栈组件，但仍需要进行一些Nginx配置更改。这是在服务器块级别完成的（服务器块类似于Apache的虚拟主机）。

   在`/etc/nginx/sites-available/`目录中打开新的服务器块配置文件。在此示例中，新服务器块配置文件命名`example.com`：

   ```bash
   $ sudo vim /etc/nginx/sites-available/example.com
   ```

   将以下内容（从默认服务器块配置文件中获取并略微修改）添加到新服务器块配置文件中：

   ```
   server {
           listen 80;
           root /var/www/html;
           index index.php index.html index.htm index.nginx-debian.html;
           server_name SERVER_IP_ADDRESS;
   
           location / {
                   try_files $uri $uri/ =404;
           }
   
           location ~ \.php$ {
                   include snippets/fastcgi-php.conf;
                   fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
           }
   
           location ~ /\.ht {
                   deny all;
           }
   }
   ```

   需要注意两个地方：

   - 在`index.html`前面添加`index.php`
   - 确保`fastcgi_pass` 套接字路径是正确的

   添加此内容后，保存并关闭该文件。通过从新服务器块配置文件（在`/etc/nginx/sites-available/`目录中）到`/etc/nginx/sites-enabled/`目录创建符号链接来启用新服务器块：

   ```bash
   $ sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
   ```

   然后，从`/sites-enabled/`目录中取消链接默认配置文件：

   ```bash
   $ sudo unlink /etc/nginx/sites-enabled/default
   ```

   > **注意**：如果您需要恢复默认配置，可以通过重新创建符号链接来执行此操作：
   >
   > ```bash
   > $ sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
   > ```

   以下命令可以测试新配置文件的语法错误：

   ```bash
   $ sudo nginx -t
   ```

   准备好后，重新加载Nginx的配置文件：

   ```bash
   $ sudo systemctl reload nginx
   ```

3. ###### Create a PHP file to Test Configuration

   在`/var/www/html/`下新建`info.php`文件

   ```bash
   $ sudo vim /var/www/html/info.php
   ```

   在新文件中写入以下代码：

   ```php
   <?php
   phpinfo();
   ```

   现在可以在浏览器中访问`http://Server_IP_Address/info.php/`，应该看到PHP生成的网页，其中包含有关您的服务器的信息：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g5jbfupowxj20py0ekgmy.jpg)

#### 0x04 验证结果

1. ###### Connect MySQL

   在`/var/www/html/`建立一个新文件`test_sql.php`：

   ```php
   <?php
   $servername = "localhost";
   $username = "username";
   $password = "password";
    
   // 创建连接
   $conn = new mysqli($servername, $username, $password);
    
   // 检测连接
   if ($conn->connect_error) {
       die("连接失败: " . $conn->connect_error);
   } 
   echo "连接成功";
   ?>
   ```

   运行结果：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g5jc5mudu3j20ev049weg.jpg)

2. ###### Create Database

   在上一个步骤的基础上，修改`test_sql.php`文件：

   ```php
   <?php
   $servername = "localhost";
   $username = "username";
   $password = "password";
    
   // 创建连接
   $conn = new mysqli($servername, $username, $password);
   // 检测连接
   if ($conn->connect_error) {
       die("连接失败: " . $conn->connect_error);
   } 
    
   // 创建数据库
   $sql = "CREATE DATABASE testPHP";
   if ($conn->query($sql) === TRUE) {
       echo "数据库创建成功";
   } else {
       echo "Error creating database: " . $conn->error;
   }
    
   $conn->close();
   ?>
   ```

   运行结果：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g5jc8g0seej20ff04k0sq.jpg)

3. ###### Create Table

   在上一个步骤的基础上，继续修改`test_sql.php`文件：

   ```bash
   <?php
   $servername = "localhost";
   $username = "username";
   $password = "password";
   $dbname = "testPHP";
    
   // 创建连接
   $conn = new mysqli($servername, $username, $password, $dbname);
   // 检测连接
   if ($conn->connect_error) {
       die("连接失败: " . $conn->connect_error);
   } 
    
   // 使用 sql 创建数据表
   $sql = "CREATE TABLE VIPMembers (
   id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
   firstname VARCHAR(30) NOT NULL,
   lastname VARCHAR(30) NOT NULL,
   email VARCHAR(50),
   reg_date TIMESTAMP
   )";
    
   if ($conn->query($sql) === TRUE) {
       echo "Table MyGuests created successfully";
   } else {
       echo "创建数据表错误: " . $conn->error;
   }
    
   $conn->close();
   ?>
   ```

   运行结果：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g5jcuu2hgoj20h004m0sq.jpg)

4. ###### Insert Record

   在上一个步骤的基础上，继续修改`test_sql.php`文件：

   ```bash
   <?php
   $servername = "localhost";
   $username = "username";
   $password = "password";
   $dbname = "myDB";
    
   // 创建连接
   $conn = new mysqli($servername, $username, $password, $dbname);
   // 检测连接
   if ($conn->connect_error) {
       die("连接失败: " . $conn->connect_error);
   } 
    
   $sql = "INSERT INTO MyGuests (firstname, lastname, email)
   VALUES ('John', 'Doe', 'john@example.com')";
    
   if ($conn->query($sql) === TRUE) {
       echo "新记录插入成功";
   } else {
       echo "Error: " . $sql . "<br>" . $conn->error;
   }
    
   $conn->close();
   ?>
   ```

   运行结果：

   ![](http://ww1.sinaimg.cn/large/6e4e7200ly1g5jcz3rcwcj20i304kweh.jpg)

#### 0x05 服务器加固

本章主要目的是介绍如何通过优化 Nginx 默认配置，提高 Nginx Web 服务器的安全性。其中注释带有`ADD`是相对于默认配置的新增项。

```bash
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}

http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;
	
	##
	# 隐藏Nginx版本号
	##
	server_tokens off;
	
	##
	# ADD: 通过关闭慢连接来抵御一些DDOS攻击
	##
    # 读取客户端请求体的超时时间
    client_body_timeout 5s; 
    # 读取客户端请求头的超时时间
    client_header_timeout 5s;
    # 超时时间之后会关闭这个连接
    keepalive_timeout 75s;
    
    ##
    # ADD: 
    ##
    # 客户端请求的http头部缓冲区大小
    client_header_buffer_size 2k;
    # 客户端请求的一些比较大的头文件到缓冲区的最大值
    large_client_header_buffers 4 4k;
    
    ##
    # ADD: 防止恶意流量的短时间大量请求
    ##
    # 用户的IP地址$binary_remote_addr作为Key，每个IP地址每秒处理10个请求
    limit_req_zone $binary_remote_addr zone=ConnLimitZone:10m rate=10r/s;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	# ADD: 要让https和http并存，不能在配置文件中使用ssl on
	##
	
	# ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
	# ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	# ADD: 开启gzip提高页面加载速度
	##

	gzip on;

	gzip_vary on;
	gzip_proxied any;
	gzip_comp_level 6;
	gzip_buffers 16 8k;
	gzip_http_version 1.1;
	gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
	
	server {
		server_name localhost;
		listen 80;
		
		##
		# ADD: 清除不安全的HTTP响应头
		##
        more_clear_headers "X-Powered-By";
        more_clear_headers "Server";
        more_clear_headers "ETag";
        more_clear_headers "Connection";
        more_clear_headers "Date";
        more_clear_headers "Accept-Ranges";
        more_clear_headers "Last-Modified";
        
        ##
        # ADD: 避免点击劫持
        ##
        add_header X-Frame-Options "SAMEORIGIN"; 
        
        ##
        # ADD: 防XSS攻击
        ##
        add_header X-XSS-Protection "1; mode=block";
        
        ##
        # ADD: 禁用不安全的HTTP方法
        ##
        if ($request_method !~ ^(GET|HEAD|POST)$ ) {
            return 405;
        }
        
        ##
        # ADD: 静态资源
        ##
        location ~* \.(js|css|flash|media|jpg|png|gif|dll|cab|CAB|ico|vbs|json|ttf|woff|eot|map)$ {
            # 缓存30天
            add_header Cache-Control "max-age=2592000";
        }
        
        ## 
        # ADD: 静态页面
        ##
        location ~* \.html$ {
            # 不缓存
            add_header Cache-Control "no-cache";
        }
	}
}

#mail {
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
# 
#	# auth_http localhost/auth.php;
#	# pop3_capabilities "TOP" "USER";
#	# imap_capabilities "IMAP4rev1" "UIDPLUS";
# 
#	server {
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}
# 
#	server {
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}
#}
```

**Summary**：

在写这篇学习文档之前，我对Nginx服务器安全加固还是处于完全无知的状态，看到参考资料的一些配置都有些云里雾里，但是我又比较喜欢“折腾”，每个阶段成功后都会对虚拟机进行快照，防止环境无法恢复。从上面可以看到，通过修改Nginx的默认配置，可以对Nginx服务器的“先天性”缺陷进行主动防御，比如：关闭版本信息、关闭慢连接、设置静态资源和静态页面的缓存时间等等，这样就可以整体上防止服务器受到常见的攻击。

另外，还可以添加IP白名单和IP黑名单，以及设置Naxsi自定义规则。

#### 0x06 Q&A

1. Nginx中`sites-available`和`sites-enabled`的区别

   sites-available是存放当前的server配置, 在这里修改配置文件；

   sites-enabled是激活并使用的server配置（从sites_available的文件创建快捷方式到sites-enabled）

2. `ln -s`命令

   [具体使用方法](https://www.jianshu.com/p/f7746b7fdf8d)

3. Nginx服务器安全加固参考文档

   - https://www.cnblogs.com/RiwellAckerman/p/11273705.html
   - https://my.oschina.net/jiaoyanli/blog/1510174
   - https://blog.csdn.net/JY_He/article/details/52299884
   - https://bbs.ichunqiu.com/thread-36091-1-1.html

