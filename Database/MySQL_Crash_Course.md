###一、简单检索数据
单个列：`SELECT prod_name FROM products;`
多个列：`SELECT pro_id, prod_name, prod_price FROM products;`
所有列：`SELECT * FROM products;`
不同值的行：`SELECT DISTINCT vend_id FROM products;`
指定某一区间的行：`SELECT prod_name FROM products LIMIT 5 OFFSET 5;`

###二、排序检索数据
按单列排序数据：`SELECT prod_name FROM products ORDER_BY prod_name;`
按多列排序数据：`SELECT prod_id, prod_price, prod_name FROM products ORDER BY prod_price DESC, prod_name;`PS:指定prod_price降序排列，prod_name升序排列。
求最大值或最小值：`SELECT prod_price FROM products ORDER BY prod_price DESC limit 1;`

###三、过滤数据（ORDER BY子句位于WHERE子句后面）
操作符类型：=, <>, <, <=, >, >=, BETWEEN, IS NULL, AND, OR
其中AND操作符的优先级大于OR操作符，例如：`SELECT prod_name, prod_price FROM products WHERE vend_id = 1002 OR vend_id = 1003 AND prod_price >= 10;` 其结果为：
![](https://upload-images.jianshu.io/upload_images/11397602-4a14e3ec1b92320b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
IN操作符：`SELECT prod_name, prod_price FROM products WHERE vend_id IN (1002, 1003);`
IN操作符与OR操作符的作用相当，但是IN操作符有以下几点优势：
- IN操作符的语法更直观简洁；
- IN操作符一般比OR操作符执行更快；
- IN操作符最大优点是可以包含其他SELECT语句，使得能够更动态的创建WHERE子句。

###四、通配符
1、百分号（`%`）通配符：`SELECT prod_id, prod_name FROM  products WHERE prod_name LIKE '%anvil%';`
注意：`%`通配符无法匹配NULL；`%`通配符还能匹配0个字符。
2、下划线（`_`）通配符：用途跟`%`通配符一样，但是`_`通配符只能匹配单个字符。

###五、创建计算字段
1、拼接字段（Concat()函数）：`SELECT Concat(vend_name, '(' , vend_country, ')') FROM vendors ORDER BY vend_name;`
![](https://upload-images.jianshu.io/upload_images/11397602-a26d319331b89656.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Trim()函数：删除数据两侧多余的空格来整理数据
`SELECT Concat(RTrim(vend_name), '(', RTrim(vend_country), ')' ) FROM vendors ORDER BY vend_name;`
2、使用别名：`SELECT Concat(vend_name, '(' , vend_country, ')') AS vendor_title FROM vendors ORDER BY vend_name;`
![](https://upload-images.jianshu.io/upload_images/11397602-77e6a3849355621f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
3、算术计算：`SELECT prod_id, quantity, item_price, quantity*item_price AS expanded_price FROM orderitems WHERE order_num = 20005;`
![](https://upload-images.jianshu.io/upload_images/11397602-e73be3ae2f0472d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###六、汇总数据
1、五种聚集函数：
- AVG():返回某列的平均值
`SELECT  AVG(prod_price) AS avg_price FROM products WHERE vend_id = 1003;`
- COUNT():返回某列的行数
用法1：COUNT(*)对表中行的数目进行计数，不管表列中包含的是空值（NULL）还是非空值；
`SELECT COUNT(*) AS num_cust FROM customers;`
用法2：COUNT(column)对特定列中具有值的行进行计数，忽略NULL值。
`SELECT COUNT(cust_email) AS num_cust FROM customers;`
- MAX():返回**指定列**中的最大值（忽略值为NULL的行）
`SELECT MAX(prod_price) AS max_price FROM products;`
- MIN():返回**指定列**中的最小值（忽略值为NULL的行）
`SELECT MIN(prod_price) AS mIin_price FROM products;`
- SUM():返回**指定列**值的和
`SELECT SUM(quantity*item_price) AS total_price FROM orderitems WHERE order_num = 20005;`
2、聚集不同值
以上的五个聚集函数都可以如下使用：
- 对所有行执行计算指定ALL参数或不给参数（ALL是默认行为）
- 只包含不同的值，指定DISTINCT参数
`SELECT AVG(DISTINCT prod_price) AS avg_price FROM products WHERE vend_id = 1003;`
3、组合聚集函数
```
SELECT COUNT(*) AS num_items
MIN(prod_price) AS price_min,
MAX(prod_price) AS price_max,
AVG(prod_price) AS price_avg,
FROM products;
```

###七、分组数据
1、创建分组
`SELECT vend_id, COUNT(*) AS num_prods FROM products GROUP BY vend_id;`
GROUP BY子句指示MySQL按vend_id排序并且分组数据，这导致对每个vend_id而不是整张表计算num_prods一次。
注意事项：
- GROUP BY 子句中列出的每个列都必须是检索列或有效的表达式
(但不能是聚集函数)。如果在 SELECT 中使用表达式,则必须在
GROUP BY 子句中指定相同的表达式，不能使用别名。
- 除聚集计算语句外, SELECT 语句中的每个列都必须在 GROUP BY 子
句中给出给出相应的列名。
- 如果分组列中具有 NULL 值,则 NULL 将作为一个分组返回。如果列
中有多行 NULL 值,它们将分为一组。
- GROUP BY 子句必须出现在 WHERE 子句之后, ORDER BY 子句之前。

2、过滤分组
`SELECT cust_id, COUNT(*) AS orders FROM orders GROUP BY cust_id HAVING COUNT(*) >= 2;`
HAVING 非常类似于 WHERE 。事实上,目前为止所学过的所有类型的 WHERE 子句都可以用 HAVING 来替代。唯一的差别是WHERE 过滤行,而 HAVING 过滤分组。
**WHERE 和 HAVING的差别：**WHERE在数据分组前进行过滤，HAVING在数据分组后进行过滤。

`SELECT vend_id, COUNT(*) AS num_prods FROM products WHERE prod_price >= 10 GROUP BY vend_id  HAVING COUNT(*) >=2;`
![](https://upload-images.jianshu.io/upload_images/11397602-9a412436558ab949.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

WHERE 子句过滤所有 prod_price 至少为 10 的行。然后按 vend_id 分组数据, HAVING 子句过滤计数为 2 或 2 以上的分组。如果没有 WHERE 子句,将会多检索出两行(供应商 1002 ,销售的所有产品价格都在 10 以下;供应商 1001 ,销售3个产品,但只有一个产品的价格大于等于 10 )。
`SELECT vend_id, COUNT(*) AS num_prods FROM products GROUP BY vend_id  HAVING COUNT(*) >=2;`
![](https://upload-images.jianshu.io/upload_images/11397602-14ca7d388e91fbe5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、SELECT子句顺序
SELECT----------FROM----------WHERE----------GROUP BY----------HAVING----------ORDER BY----------LIMIT

###八、使用子查询