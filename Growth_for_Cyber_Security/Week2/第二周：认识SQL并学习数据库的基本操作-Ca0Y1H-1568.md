## Week2 认识SQL并学习数据库的基础操作

> 主要以《MySQL必知必会》（《MySQl Crash Course》）为参考

#### 0x00 任务目标

- 什么是关系型和⾮关系型数据库
- 选择⼀种关系型数据库进⾏学习
- 学习数据库中的字段类型并创建库和⽤⼾表，需要包含所有字段类型
- 学习数据库的增删改查，记录学习过程

#### 0x01 SQL&NoSQL

1. 关系型数据库
   - 关系型数据库是以关系模型来创建的数据库。
   - 关系模型就是指二维表格模型。
   - 一个关系型数据库就是由二维表及其之间的联系组成的一个数据组织。
   - 常见的关系型数据库有：
     Mysql、Oracle、PostgreSQL、SQLServer、MicrosoftAccess
2. 非关系型数据库
   - 非关系型数据库是以非关系模型来创建的数据库。
   - 非关系模型有列模型、键值对模型、文档类模型。
   - 常见的关系型数据库有：
     MongoDB、Redis、MemcacheDB、HBase

#### 0x02 数据类型

| 名称         | 类型           | 说明                                                         |
| :----------- | :------------- | :----------------------------------------------------------- |
| INT          | 整型           | 4字节整数类型，范围约+/-21亿                                 |
| BIGINT       | 长整型         | 8字节整数类型，范围约+/-922亿亿                              |
| REAL         | 浮点型         | 4字节浮点数，范围约+/-1038                                   |
| DOUBLE       | 浮点型         | 8字节浮点数，范围约+/-10308                                  |
| DECIMAL(M,N) | 高精度小数     | 由用户指定精度的小数，例如，DECIMAL(20,10)表示一共20位，其中小数10位，通常用于财务计算 |
| CHAR(N)      | 定长字符串     | 存储指定长度的字符串，例如，CHAR(100)总是存储100个字符的字符串 |
| VARCHAR(N)   | 变长字符串     | 存储可变长度的字符串，例如，VARCHAR(100)可以存储0~100个字符的字符串 |
| BOOLEAN      | 布尔类型       | 存储True或者False                                            |
| DATE         | 日期类型       | 存储日期，例如，2018-06-22                                   |
| TIME         | 时间类型       | 存储时间，例如，12:20:59                                     |
| DATETIME     | 日期和时间类型 | 存储日期+时间，例如，2018-06-22 12:20:59                     |

#### 0x02 样例表设计

- vendors表

  vendors表存储销售产品的供应商。每个供应商在这个表中有一个记录，供应商ID（vend_id）列用来匹配产品和供应商。

  |      列      |       说明       |
  | :----------: | :--------------: |
  |   vend_id    |     供应商ID     |
  |  vend_name   |     供应商名     |
  | vend_address |   供应商的地址   |
  |  vend_city   |   供应商的城市   |
  |  vend_state  |    供应商的州    |
  |   vend_zip   | 供应商的邮政编码 |
  | vend_country |   供应商的国家   |

- products表

  products表包含产品目录，每行一个产品。每个产品有唯一的ID（prod_id列），通过vend_id（供应商的唯一ID）关联到它的供应商。

  |     列     |     说明     |
  | :--------: | :----------: |
  |  prod_id   |    产品ID    |
  |  vend_id   | 产品供应商ID |
  | prod_name  |    产品名    |
  | prod_price |   产品价格   |
  | prod_desc  |   产品描述   |

- customers表

  customers表存储所有顾客的信息。每个顾客有唯一的ID（cust_id列）。

  |      列      |      说明      |
  | :----------: | :------------: |
  |   cust_id    |     顾客ID     |
  |  cust_name   |    顾客姓名    |
  | cust_address |   顾客的地址   |
  |  cust_city   |   顾客的城市   |
  |  cust_state  |    顾客的州    |
  |   cust_zip   | 顾客的邮政编码 |
  | cust_country |   顾客的国家   |
  | cust_contact | 顾客的联系方式 |
  |  cust_email  |   顾客的邮箱   |

- orders表

  orders表存储顾客订单（但不是订单细节）。每个订单唯一地编号（order_num列）。订单用cust_id列（它关联到customer表的顾客唯一ID）与相应的顾客关联。

  |     列     |    说明    |
  | :--------: | :--------: |
  | order_num  | 唯一订单号 |
  | order_date |  订单日期  |
  |  cust_id   | 订单顾客ID |

- orderitems表

  orderitems表存储每个订单中的实际物品，每个订单的每个物品占一行。对orders中的每一行，orderitems中有一行或多行。每个订单物品由订单号加订单物品（第一个物品、第二个物品等）唯一标识。订单物品通过order_num列（关联到orders中订单的唯一ID）与它们相应的订单相关联。此外，每个订单项包含订单物品的产品ID（它关联物品到products表）

  |     列     |                说明                 |
  | :--------: | :---------------------------------: |
  | order_num  | 订单号（关联到orders表的order_num） |
  | order_item |  订单物品号（在某个订单中的顺序）   |
  |  prod_id   | 产品ID（关联到products表的prod_id） |
  |  quantity  |              物品数量               |
  | item_price |              物品价格               |

- productnotes表

  productnotes表存储与特定产品有关的注释。并非所有产品都有相关的注释，而有的产品可能有许多相关的注释。

  |    列     |      说明      |
  | :-------: | :------------: |
  |  note_id  |     注释ID     |
  |  prod_id  |     产品ID     |
  | note_date | 增加注释的日期 |
  | note_text |   注释的内容   |

#### 0x02 样例表创建

附件中包含两个可以执行的SQL脚本文件。

- create.sql包含创建6个数据库表（包括所有主键和外键约束）的MySQL语句。
- populate.sql包含用来填充这些表的INSERT语句。

然后按照以下步骤创建样例表

- 创建一个新的数据库
- 选择新数据源（如果使用mysql命令行实用程序，用USE命令）
- 执行create.sql脚本和populate.sql脚本。如果使用mysql命令行实用程序，可给出
  source create.sql;（指定create.sql文件的完全路径）

#### 0x03 简单检索数据

- 单个列：`SELECT prod_name FROM products;`
- 多个列：`SELECT pro_id, prod_name, prod_price FROM products;`
- 所有列：`SELECT * FROM products;`
- 不同值的行：`SELECT DISTINCT vend_id FROM products;`
- 指定某一区间的行：`SELECT prod_name FROM products LIMIT 5 OFFSET 5;`

#### 0x04 排序检索数据

- 按单列排序数据：`SELECT prod_name FROM products ORDER_BY prod_name;`

- 按多列排序数据：`SELECT prod_id, prod_price, prod_name FROM products ORDER BY prod_price DESC, prod_name;`

  > 指定prod_price降序排列，prod_name升序排列。

- 求最大值或最小值：`SELECT prod_price FROM products ORDER BY prod_price DESC limit 1;`

#### 0x05 过滤数据

> （ORDER BY子句位于WHERE子句后面）

**操作符类型：=, <>, <, <=, >, >=, BETWEEN, IS NULL, AND, OR**
其中AND操作符的优先级大于OR操作符，例如：`SELECT prod_name, prod_price FROM products WHERE vend_id = 1002 OR vend_id = 1003 AND prod_price >= 10;` 其结果为：
![](https://upload-images.jianshu.io/upload_images/11397602-4a14e3ec1b92320b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
IN操作符：`SELECT prod_name, prod_price FROM products WHERE vend_id IN (1002, 1003);`
IN操作符与OR操作符的作用相当，但是IN操作符有以下几点优势：

- IN操作符的语法更直观简洁；
- IN操作符一般比OR操作符执行更快；
- IN操作符最大优点是可以包含其他SELECT语句，使得能够更动态的创建WHERE子句。

#### 0x06 通配符

1. 百分号（`%`）通配符：`SELECT prod_id, prod_name FROM  products WHERE prod_name LIKE '%anvil%';`
   注意：`%`通配符无法匹配NULL；`%`通配符还能匹配0个字符。
2. 下划线（`_`）通配符：用途跟`%`通配符一样，但是`_`通配符只能匹配单个字符。

#### 0x07 创建计算字段

1. 拼接字段（Concat()函数）：`SELECT Concat(vend_name, '(' , vend_country, ')') FROM vendors ORDER BY vend_name;`
   ![](https://upload-images.jianshu.io/upload_images/11397602-a26d319331b89656.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   Trim()函数：删除数据两侧多余的空格来整理数据
   `SELECT Concat(RTrim(vend_name), '(', RTrim(vend_country), ')' ) FROM vendors ORDER BY vend_name;`

2. 使用别名：`SELECT Concat(vend_name, '(' , vend_country, ')') AS vendor_title FROM vendors ORDER BY vend_name;`
   ![](https://upload-images.jianshu.io/upload_images/11397602-77e6a3849355621f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
   
3. 算术计算：`SELECT prod_id, quantity, item_price, quantity*item_price AS expanded_price FROM orderitems WHERE order_num = 20005;`
   ![](https://upload-images.jianshu.io/upload_images/11397602-e73be3ae2f0472d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 0x08 汇总数据

1. 五种聚集函数：

   - AVG():返回某列的平均值
     `SELECT  AVG(prod_price) AS avg_price FROM products WHERE vend_id = 1003;`

   - COUNT():返回某列的行数
     用法1：COUNT(*)对表中行的数目进行计数，不管表列中包含的是空值（NULL）还是非空值；
     `SELECT COUNT(*) AS num_cust FROM customers;`
     用法2：COUNT(column)对特定列中具有值的行进行计数，忽略NULL值。
     `SELECT COUNT(cust_email) AS num_cust FROM customers;

   - MAX():返回**指定列**中的最大值（忽略值为NULL的行）
     `SELECT MAX(prod_price) AS max_price FROM products;`

   - MIN():返回**指定列**中的最小值（忽略值为NULL的行）
     `SELECT MIN(prod_price) AS mIin_price FROM products;`

   - SUM():返回**指定列**值的和
     `SELECT SUM(quantity*item_price) AS total_price FROM orderitems WHERE order_num = 20005;`

2. 聚集不同值
     以上的五个聚集函数都可以如下使用：
     
     - 对所有行执行计算指定ALL参数或不给参数（ALL是默认行为）
     
     - 只包含不同的值，指定DISTINCT参数
       `SELECT AVG(DISTINCT prod_price) AS avg_price FROM products WHERE vend_id = 1003;`
     
3. 组合聚集函数

     ```sql
     SELECT COUNT(*) AS num_items
     MIN(prod_price) AS price_min,
     MAX(prod_price) AS price_max,
     AVG(prod_price) AS price_avg,
     FROM products;
     ```

#### 0x09 分组数据

1. 创建分组
   `SELECT vend_id, COUNT(*) AS num_prods FROM products GROUP BY vend_id;`
   GROUP BY子句指示MySQL按vend_id排序并且分组数据，这导致对每个vend_id而不是整张表计算num_prods一次。

   > 注意事项：
   >
   > - GROUP BY 子句中列出的每个列都必须是检索列或有效的表达式
   >   (但不能是聚集函数)。如果在 SELECT 中使用表达式,则必须在
   >   GROUP BY 子句中指定相同的表达式，不能使用别名。
   > - 除聚集计算语句外, SELECT 语句中的每个列都必须在 GROUP BY 子
   >   句中给出给出相应的列名。
   > - 如果分组列中具有 NULL 值,则 NULL 将作为一个分组返回。如果列
   >   中有多行 NULL 值,它们将分为一组。
   > - GROUP BY 子句必须出现在 WHERE 子句之后, ORDER BY 子句之前。

2. 过滤分组
   `SELECT cust_id, COUNT(*) AS orders FROM orders GROUP BY cust_id HAVING COUNT(*) >= 2;`
   HAVING 非常类似于 WHERE 。事实上,目前为止所学过的所有类型的 WHERE 子句都可以用 HAVING 来替代。唯一的差别是WHERE 过滤行,而 HAVING 过滤分组。

   > **WHERE 和 HAVING的差别**：WHERE在数据分组前进行过滤，HAVING在数据分组后进行过滤。`SELECT vend_id, COUNT(*) AS num_prods FROM products WHERE prod_price >= 10 GROUP BY vend_id  HAVING COUNT(*) >=2;`
   > ![](https://upload-images.jianshu.io/upload_images/11397602-9a412436558ab949.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
   >
   > WHERE 子句过滤所有 prod_price 至少为 10 的行。然后按 vend_id 分组数据, HAVING 子句过滤计数为 2 或 2 以上的分组。如果没有 WHERE 子句,将会多检索出两行(供应商 1002 ,销售的所有产品价格都在 10 以下;供应商 1001 ,销售3个产品,但只有一个产品的价格大于等于 10 )。
   > `SELECT vend_id, COUNT(*) AS num_prods FROM products GROUP BY vend_id  HAVING COUNT(*) >=2;`
   > ![](https://upload-images.jianshu.io/upload_images/11397602-14ca7d388e91fbe5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. SELECT子句顺序
   SELECT----------FROM----------WHERE----------GROUP BY----------HAVING----------ORDER BY----------LIMIT

#### 0x10 插入数据

```sql
INSERT INTO customers(cust_name,
                     cust_address,
                     cust_city,
                     cust_zip,
                     cust_country,
                     cust_contact,
                     cust_email)
                VAlUSE('Pep E. LaPew',
                     '100 Main Street',
                      'Los Angeles',
                      'CA',
                      '90046',
                      'USA',
                      NULL,
                      NULL);
```

在插入行时，MySQL将用VALUES列表中的相应值填入列表中的对应项。VALUES中的第一个值对应于第一个指定的列名。第二个值对应于第二个列名，如此等等。

因为提供了列名，VALUES必须以其指定的次序匹配指定的列名，不一定按各个列出现在实际表中的次序。

#### 0x11 更新和删除数据

1. 更新数据

   基本的UPDATE语句由3部分组成，分别是：

   - 要更新的表；
   - 列名和它们的新值；
   - 确定要更新行的过滤条件。

   例如：

   ```sql
   UPDATE customers
   SET cust_email = 'elmer@fudd.com'
   WHERE cust_id = 10005;
   ```

   为了删除某个列的值，可设置它为NULL（假如表定义允许NULL值）。

   ```sql
   UPDATE customers
   SET cust_email = NULL
   WHERE cust_id = 10005;
   ```

2. 删除数据

   下面的语句从customers表中删除一行：

   ```sql
   DELETE FROM customers
   WHERE cust_id = 10006;
   ```