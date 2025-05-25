# 文件包含

!!! note
      期待补充


漏洞和简析

 

**内容主要是php包含文件的函数漏洞**

其原理是服务器解析执行php文件时能够通过包含函数加载另外一个文件中的php代码，当被包含的文件中存在木马时，也就意味着木马程序会在服务器上加载执行。 

只要将一些重复使用的函数写到单个文件中，需要使用某个函数时就可以直接调用此文件，而无需再次编写，其中文件调用的过程一般被称为文件包含。  （功能类似`python`中的`import`，~~应该都学了吧~~

## php的四种包含函数如下



| 函数 | 功能 |
| :------------: | :----------------------------------------------------------: |
| equire()       | 只要程序一运行就包含文件，找不到被包含的文件时会产生致命错误，并停止脚本 |
| include()      | 执行到include时才包含文件，找不到被包含文件时只会产生警告，脚本将继续执行 |
| include_once() | 若文件中代码已被包含则不会再次包含                           |
| require_once() | 若文件中代码已被包含则不会再次包含                           |

除此之外还有`fopen()`，`readfile()` 

当使用前4个函数包含一个新的文件时，只要文件内容符合PHP语法规范，那么任何扩展名都可以被PHP解析

## 分类



1. **远程包含与本地包含**
   1. **远程文件包含**，需要`php.ini`开启了`allow_url_fopen`和`allow_url_include`的配置。包含的是第三方服务器的文件。
   2. **本地文件包含**就是包含本地服务器的文件

2. **远程与本地包含的区别**
   1. **本地文件包含**就是通过浏览器包含web服务器上的文件，这种漏洞是因为浏览器包含文件时没有进行严格的过滤允许遍历目录的字符注入浏览器并执行。
   2. **远程文件包含**就是允许攻击者包含一个远程的文件,一般是在远程服务器上预先设置好的脚本。此漏洞是因为浏览器对用户的输入没有进行检查，导致不同程度的信息泄露、拒绝服务攻击，甚至在目标服务器上执行代码。
   3. **本地文件包含**与**远程文件包含**有着相同的原理，但前者只能包含服务器上存在的文件，而后者可以包含远程服务器上的文件。



## 危害



1、读取web配置文件以及敏感的数据

2、web服务器的文件被外界浏览导致信息泄露;

3、与文件上传漏洞组合getshell，将恶意代码执行解析



## 漏洞利用



### 伪协议

#### file:// 协议

>  参考：`http`协议适合需要远程访问和动态内容的场景，而`file`协议适合快速访问本地静态文件。



用于访问本地文件系统，通常用来**读取本地文件**的且在php中使用不受`allow_url_fopen`与`allow_url_include`的影响。
`include()` `require()` `include_once()` `require_once()`参数可控的情况下，如导入为非`.php`文件，则仍按照php语法进行解析，这是`include()`函数所决定的。

**说明**：
`file://` 文件系统是 PHP 使用的默认封装协议，用于展现本地文件系统(当然不止只有php存在file协议)。使用 CLI 的时候，目录默认是脚本被调用时所在的目录。(了解一下相对路径和绝对路径）。在某些函数里，例如 `fopen()` 和 `file_get_contents()`，`include_path() `会可选地搜索，也作为相对的路径。



#### php:// 协议

前提

`php://input php://stdin php://memory php://temp` 需要`allow_url_include:on` 



`php://` 用于访问各个输入/输出流（I/O流）

在CTF中经常使用的是`php://filter`和`php://input` 

`php://filter`用于**读取源码**，`php://input`用于**执行php代码**。



| 协议                    | 作用                                                         |
| ----------------------- | ------------------------------------------------------------ |
| php://input             | 可以访问请求的原始数据的只读流，在POST请求中访问POST的`data`部分，在`enctype="multipart/form-data"` 的时候`php://input `是无效的。 |
| php://output            | 只写的数据流，允许以 `print` 和 `echo` 一样的方式写入到输出缓冲区。 |
| php://fd                | (>=5.3.6)允许直接访问指定的文件描述符。例如 `php://fd/3` 引用了文件描述符 3。 |
| php://memory php://temp | (>=5.1.0)一个类似文件包装器的数据流，允许读写临时数据。两者的唯一区别是 `php://memory` 总是把数据储存在内存中，而 `php://temp` 会在内存量达到预定义的限制后（默认是 `2MB`）存入临时文件中。临时文件位置的决定和 `sys_get_temp_dir()` 的方式一致。 |
| php://filter            | (>=5.0.0)一种元封装器，设计用于数据流打开时的筛选过滤应用。对于一体式`（all-in-one）`的文件函数非常有用，类似 `readfile()`、`file()` 和 `file_get_contents()`，在数据流内容读取之前没有机会应用其他过滤器。 |



##### php://input

举个例子

URL：

`http://localhost/include/file.php?file=php://input`



POST：

`<?php system('ipconfig');?>`



会把POST的请求内容当作php代码执行



##### php://filter

在ctf中使用的比较广（主要目的是获取flag，所以读取文件源码的功能就很必要）



**参数详解**

举个例子

`php://filter/convert.base64-encode/resource=./flag.php`

会读取当前目录的`flag.php`文件的源码，并且以base64编码的形式展示出来，防止自动渲染



tips：可以**包含日志文件**

几乎所有网站都会将用户的访问记录到访问日志中，ctf赛题不一定



| php://filter 参数                     | 描述                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| resource=<要过滤的数据流>             | 必须项。它指定了你要筛选过滤的数据流。                       |
| read=<读链的过滤器>                   | 可选项。可以设定一个或多个过滤器名称，以管道符（/）分隔。    |
| write=<写链的过滤器>                  | 可选项。可以设定一个或多个过滤器名称，以管道符（/）分隔。    |
| convert.base64-encode<两个链的过滤器> | 任何没有以 *read=* 或 *write=* 作前缀的筛选器列表会视情况应用于读或写链。 |



| 字符串过滤器      | 作用                                        |
| ----------------- | ------------------------------------------- |
| string.rot13      | 等同于`str_rot13()`，rot13变换              |
| string.toupper    | 等同于`strtoupper()`，转大写字母            |
| string.tolower    | 等同于`strtolower()`，转小写字母            |
| string.strip_tags | 等同于`strip_tags()`，去除html、PHP语言标签 |





| 转换过滤器                                                   | 作用                                                       |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| convert.base64-encode & convert.base64-decode                | 等同于`base64_encode()`和`base64_decode()`，base64编码解码 |
| convert.quoted-printable-encode & convert.quoted-printable-decode | quoted-printable 字符串与 8-bit 字符串编码解码             |



| 压缩过滤器                        | 作用                                                         |
| --------------------------------- | ------------------------------------------------------------ |
| zlib.deflate & zlib.inflate       | 在本地文件系统中创建 gzip 兼容文件的方法，但不产生命令行工具如 gzip的头和尾信息。只是压缩和解压数据流中的有效载荷部分。 |
| bzip2.compress & bzip2.decompress | 同上，在本地文件系统中创建 bz2 兼容文件的方法。              |





| 加密过滤器 | 作用                   |
| ---------- | ---------------------- |
| mcrypt.*   | libmcrypt 对称加密算法 |
| mdecrypt.* | libmcrypt 对称解密算法 |

[更多过滤器](https://www.php.net/manual/zh/filters.php)

#### data:// 协议

前提

`allow_url_fopen:on`  以及`allow_url_include:on`  `PHP>=5.2.0`



可以使用`data://`数据流封装器，以传递相应格式的数据。

通常可以用来执行PHP代码

`data://text/plain,<?php%20phpinfo();?>`



举个例子：

Payload

**直接执行命令**

`data:text/plain,<?php system(whoami)?>`

`data:text/plain;base64,PD9waHAgc3lzdGVtKHdob2FtaSk/Pg==`

**图片马执行命令**



Payload：

`data://image/jpeg;base64,..... #图片马的base64`



#### phar:// 协议

其实严格来说是php反序列化的漏洞，不过不需要`unserialize()`

**phar的文件结构**

**stub（引导头）**

可以理解为一个标志，类似ELF文件的魔数，也就是文件头

格式为`xxx<?php xxx; __HALT_COMPILER();?>`，以`__HALT_COMPILER();?>`来结尾，

phar扩展以这个标志来识别文件是否为phar文件



##### **manifest(**元数据)

这里存放核心数据

文件信息（文件名、大小、权限等

主要这部分会以**序列化**的形式存储用户自定义的`meta-data`

解析Manifest时自动调用`unserialize()`，漏洞触发点



##### **contents(文件内容)**

一些被压缩的资源，图片，php等



##### **signature(签名)**

用于验证文件完整性的签名



主要漏洞出现在`manifest`中的`meta-data`,反序列化漏洞的部分放到反序列化来讲(挖坑，这里跳转到phar反序列化继续)



## 漏洞bypass



### **00字符截断**

**(PHP<5.3.4)**

[文件上传有写](./从零开始的Web之路-文件上传篇.md/#00)

用于截断file变量之后的字符串

`../etc/passwd`

通过web输入时

`../etc/passwd%00`






[参考](https://segmentfault.com/a/1190000018991087#/)



