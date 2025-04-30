# 写在前面
本人刚入门时的基础比小白还小白，学习路上逛了不少博客
各个平台上的博客无非抄来抄去，我把我认为有用的内容整合了一下
大自然的搬运工罢了
# What is Web
**what is web的内容借鉴自Landasika师傅写的文章，有删改**
## 一、WEB安全是什么
web也就是俗称的web安全，也就是大家打开浏览器的那一刻。就开始和web打交道了。我们是学网络安全的，web安全是网络中最经典的应用之一。
Web安全就是要提供证据表明，在面对敌意和恶意输入的时候，web系统应用仍然能够充分地满足它的需求
2005年06月，CardSystems，黑客恶意侵入了它的电脑系统，窃取了4000万张信用卡的资料。
2011年12月，国内最大的开发者社区CSDN被黑客在互联网上公布了600万注册用户的数据；黑客随后陆续公布了网易、人人、天涯、猫扑等多家大型网站的数据信息。
## 二、如何入门WEB安全
可以参考这篇文章：[https://zhuanlan.zhihu.com/p/409570216](https://zhuanlan.zhihu.com/p/409570216)
常见Web安全漏洞大致可以分为：信息泄露、弱口令爆破、命令执行、文件包含、php特性、文件上传、sql注入、反序列化、代码审计、XSS、jwt、SSRF、CSRF
先深入理解这些漏洞背后的原理和知识，然后运用于实战化（CTF模拟）
推荐新手刷题平台：[ctf.show](https://ctf.show/)，[https://buuoj.cn/](https://buuoj.cn/)

**有些童鞋会问，从哪里开始呢？**
大家莫慌，先从一个搭建一个网页，理解运行机理开始吧！
**本地服务器的搭建：利用phpstudy搭建一个wamp**

- 参考链接：[https://blog.csdn.net/weixin_43837883/article/details/114021104](https://blog.csdn.net/weixin_43837883/article/details/114021104)

最终实现，其实并不需要你实现安装一个wordpress博客。在网页所在的根目录找到index.html即可。
之后可以学习一下web前端html的语言构造
以及了解js是什么（在学习XSS漏洞的时候了解即可）
然后学习一下php的语言
（不需要那么精通，只需要知道有什么出题的点，能看懂代码就好）
然后就可以开始学习一些漏洞，可以从最简单的php特性开始。
在本篇中，我把php的一些特性放在了前置知识的位置，大家可以随学随看
### 三、书籍推荐

- 学web入门推荐是《web安全深度剖析》虽然内容有些老，但是对新手入门很友好。
- 《web前端黑客技术揭秘》偏向于前端黑客知识，都是些理论话的东西
- 还有是徐焱的《web安全攻防》这本书偏向于web渗透实战，手把手教你如何搭建环境。还有配套的源代码，可以边搞实战技巧边玩代码审计。
- 再然后就是道哥的《白帽子讲web安全》了，萌新读这个可能会有点困难，但是这本书不可不读，里面的思想方法值得学习。
- 中后期就是偏向于编程和脚本了，搞web首先就是要学好PHP，然后可以学python（CTF题目很多是要写脚本的）学好编程并能写一些简单的工具是web渗透的分水岭
### 方便我们使用的软件

- notepad++（力荐）
- utools
- Typora
# 前置知识
不是看完前置知识才能学习漏洞，这里仅作整理，边看边学
这份大纲会带你过一遍学习web所需的一些主要的基础知识，但是难免有疏漏的地方，大家学习的时候遇到不明白的问题多多百度，百度解决不了的随时问学长学姐，周报求质不求量，学到东西才是最重要的
## 1.http状态码
```python
 1开头的http状态码
表示临时响应并需要请求者继续执行操作的状态代码。

100   （继续） 请求者应当继续提出请求。 服务器返回此代码表示已收到请求的第一部分，正在等待其余部分。  
101   （切换协议） 请求者已要求服务器切换协议，服务器已确认并准备切换。
—————————————————————————————————————————————————————————————————————————————————————————
2开头的http状态码
表示请求成功

200     成功处理了请求，一般情况下都是返回此状态码； 
201     请求成功并且服务器创建了新的资源。 
202     接受请求但没创建资源； 
203     返回另一资源的请求； 
204     服务器成功处理了请求，但没有返回任何内容；
205     服务器成功处理了请求，但没有返回任何内容；
206     处理部分请求；
—————————————————————————————————————————————————————————————————————————————————————————
3xx （重定向） 
重定向代码，也是常见的代码

300   （多种选择）  针对请求，服务器可执行多种操作。 服务器可根据请求者 (user agent) 选择一项操作，或提供操作列表供请求者选择。 
301   （永久移动）  请求的网页已永久移动到新位置。 服务器返回此响应（对 GET 或 HEAD 请求的响应）时，会自动将请求者转到新位置。 
302   （临时移动）  服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求。 
303   （查看其他位置） 请求者应当对不同的位置使用单独的 GET 请求来检索响应时，服务器返回此代码。 
304   （未修改） 自从上次请求后，请求的网页未修改过。 服务器返回此响应时，不会返回网页内容。 
305   （使用代理） 请求者只能使用代理访问请求的网页。 如果服务器返回此响应，还表示请求者应使用代理。 
307   （临时重定向）  服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求。
—————————————————————————————————————————————————————————————————————————————————————————
4开头的http状态码表示请求出错

400    服务器不理解请求的语法。 
401   请求要求身份验证。 对于需要登录的网页，服务器可能返回此响应。 
403   服务器拒绝请求。 
404   服务器找不到请求的网页。 
405   禁用请求中指定的方法。 
406   无法使用请求的内容特性响应请求的网页。 
407   此状态代码与 401类似，但指定请求者应当授权使用代理。 
408   服务器等候请求时发生超时。 
409   服务器在完成请求时发生冲突。 服务器必须在响应中包含有关冲突的信息。 
410   如果请求的资源已永久删除，服务器就会返回此响应。 
411   服务器不接受不含有效内容长度标头字段的请求。 
412   服务器未满足请求者在请求中设置的其中一个前提条件。 
413   服务器无法处理请求，因为请求实体过大，超出服务器的处理能力。 
414   请求的 URI（通常为网址）过长，服务器无法处理。 
415   请求的格式不受请求页面的支持。 
416   如果页面无法提供请求的范围，则服务器会返回此状态代码。 
417   服务器未满足”期望”请求标头字段的要求。
—————————————————————————————————————————————————————————————————————————————————————————
5开头状态码并不常见，但是我们应该知道

500   （服务器内部错误）  服务器遇到错误，无法完成请求。 
501   （尚未实施） 服务器不具备完成请求的功能。 例如，服务器无法识别请求方法时可能会返回此代码。 
502   （错误网关） 服务器作为网关或代理，从上游服务器收到无效响应。 
503   （服务不可用） 服务器目前无法使用（由于超载或停机维护）。 通常，这只是暂时状态。 
504   （网关超时）  服务器作为网关或代理，但是没有及时从上游服务器收到请求。 
505   （HTTP 版本不受支持） 服务器不支持请求中所用的 HTTP 协议版本。  
```
## 2.正则表达式
[https://ihateregex.io/](https://ihateregex.io/)
[https://tool.oschina.net/regex](https://tool.oschina.net/regex)
### 表达式全集
| 字符 | 描述 |
| --- | --- |
| \\ | 将下一个字符标记为一个特殊字符、或一个原义字符、或一个向后引用、或一个八进制转义符。例如，“n”匹配字符“n”而“\\n”匹配一个换行符。串行“\\\\”匹配“\\”而“\\(”则匹配“(”。 |
| ^ | 匹配输入字符串的开始位置。如果设置了RegExp对象的Multiline属性，^也匹配“\\n”或“\\r”之后的位置。 |
| $ | 匹配输入字符串的结束位置。如果设置了RegExp对象的Multiline属性，$也匹配“\\n”或“\\r”之前的位置。 |
| * | 匹配前面的子表达式零次或多次。例如，zo*能匹配“z”以及“zoo”。*等价于{0,}。 |
| + | 匹配前面的子表达式一次或多次。例如，“zo+”能匹配“zo”以及“zoo”，但不能匹配“z”。+等价于{1,}。 |
| ? | 匹配前面的子表达式零次或一次。例如，“do(es)?”可以匹配“does”或“does”中的“do”。?等价于{0,1}。 |
| {_n_} | _n_是一个非负整数。匹配确定的_n_次。例如，“o{2}”不能匹配“Bob”中的“o”，但是能匹配“food”中的两个o。 |
| {_n_,} | _n_是一个非负整数。至少匹配_n_次。例如，“o{2,}”不能匹配“Bob”中的“o”，但能匹配“foooood”中的所有o。“o{1,}”等价于“o+”。“o{0,}”则等价于“o*”。 |
| {_n_,_m_} | _m_和_n_均为非负整数，其中_n_<=_m_。最少匹配_n_次且最多匹配_m_次。例如，“o{1,3}”将匹配“fooooood”中的前三个o。“o{0,1}”等价于“o?”。请注意在逗号和两个数之间不能有空格。 |
| ? | 当该字符紧跟在任何一个其他限制符（*,+,?，{_n_}，{_n_,}，{_n_,_m_}）后面时，匹配模式是非贪婪的。非贪婪模式尽可能少的匹配所搜索的字符串，而默认的贪婪模式则尽可能多的匹配所搜索的字符串。例如，对于字符串“oooo”，“o+?”将匹配单个“o”，而“o+”将匹配所有“o”。 |
| . | 匹配除“\\_n_”之外的任何单个字符。要匹配包括“\\_n_”在内的任何字符，请使用像“(.&#124;\\n)”的模式。 |
| (pattern) | 匹配pattern并获取这一匹配。所获取的匹配可以从产生的Matches集合得到，在VBScript中使用SubMatches集合，在JScript中则使用$0…$9属性。要匹配圆括号字符，请使用“\\(”或“\\)”。 |
| (?:pattern) | 匹配pattern但不获取匹配结果，也就是说这是一个非获取匹配，不进行存储供以后使用。这在使用或字符“(&#124;)”来组合一个模式的各个部分是很有用。例如“industr(?:y&#124;ies)”就是一个比“industry&#124;industries”更简略的表达式。 |
| (?=pattern) | 正向肯定预查，在任何匹配pattern的字符串开始处匹配查找字符串。这是一个非获取匹配，也就是说，该匹配不需要获取供以后使用。例如，“Windows(?=95&#124;98&#124;NT&#124;2000)”能匹配“Windows2000”中的“Windows”，但不能匹配“Windows3.1”中的“Windows”。预查不消耗字符，也就是说，在一个匹配发生后，在最后一次匹配之后立即开始下一次匹配的搜索，而不是从包含预查的字符之后开始。 |
| (?!pattern) | 正向否定预查，在任何不匹配pattern的字符串开始处匹配查找字符串。这是一个非获取匹配，也就是说，该匹配不需要获取供以后使用。例如“Windows(?!95&#124;98&#124;NT&#124;2000)”能匹配“Windows3.1”中的“Windows”，但不能匹配“Windows2000”中的“Windows”。预查不消耗字符，也就是说，在一个匹配发生后，在最后一次匹配之后立即开始下一次匹配的搜索，而不是从包含预查的字符之后开始 |
| (?<=pattern) | 反向肯定预查，与正向肯定预查类拟，只是方向相反。例如，“(?<=95&#124;98&#124;NT&#124;2000)Windows”能匹配“2000Windows”中的“Windows”，但不能匹配“3.1Windows”中的“Windows”。 |
| (?<!pattern) | 反向否定预查，与正向否定预查类拟，只是方向相反。例如“(?<!95&#124;98&#124;NT&#124;2000)Windows”能匹配“3.1Windows”中的“Windows”，但不能匹配“2000Windows”中的“Windows”。 |
| x&#124;y | 匹配x或y。例如，“z&#124;food”能匹配“z”或“food”。“(z&#124;f)ood”则匹配“zood”或“food”。 |
| [xyz] | 字符集合。匹配所包含的任意一个字符。例如，“[abc]”可以匹配“plain”中的“a”。 |
| [^xyz] | 负值字符集合。匹配未包含的任意字符。例如，“[^abc]”可以匹配“plain”中的“p”。 |
| [a-z] | 字符范围。匹配指定范围内的任意字符。例如，“[a-z]”可以匹配“a”到“z”范围内的任意小写字母字符。 |
| [^a-z] | 负值字符范围。匹配任何不在指定范围内的任意字符。例如，“[^a-z]”可以匹配任何不在“a”到“z”范围内的任意字符。 |
| \\b | 匹配一个单词边界，也就是指单词和空格间的位置。例如，“er\\b”可以匹配“never”中的“er”，但不能匹配“verb”中的“er”。 |
| \\B | 匹配非单词边界。“er\\B”能匹配“verb”中的“er”，但不能匹配“never”中的“er”。 |
| \\cx | 匹配由x指明的控制字符。例如，\\cM匹配一个Control-M或回车符。x的值必须为A-Z或a-z之一。否则，将c视为一个原义的“c”字符。 |
| \\d | 匹配一个数字字符。等价于[0-9]。 |
| \\D | 匹配一个非数字字符。等价于[^0-9]。 |
| \\f | 匹配一个换页符。等价于\\x0c和\\cL。 |
| \\n | 匹配一个换行符。等价于\\x0a和\\cJ。 |
| \\r | 匹配一个回车符。等价于\\x0d和\\cM。 |
| \\s | 匹配任何空白字符，包括空格、制表符、换页符等等。等价于[ \\f\\n\\r\\t\\v]。 |
| \\S | 匹配任何非空白字符。等价于[^ \\f\\n\\r\\t\\v]。 |
| \\t | 匹配一个制表符。等价于\\x09和\\cI。 |
| \\v | 匹配一个垂直制表符。等价于\\x0b和\\cK。 |
| \\w | 匹配包括下划线的任何单词字符。等价于“[A-Za-z0-9_]”。 |
| \\W | 匹配任何非单词字符。等价于“[^A-Za-z0-9_]”。 |
| \\x_n_ | 匹配_n_，其中_n_为十六进制转义值。十六进制转义值必须为确定的两个数字长。例如，“\\x41”匹配“A”。“\\x041”则等价于“\\x04&1”。正则表达式中可以使用ASCII编码。. |
| \\_num_ | 匹配_num_，其中_num_是一个正整数。对所获取的匹配的引用。例如，“(.)\\1”匹配两个连续的相同字符。 |
| \\_n_ | 标识一个八进制转义值或一个向后引用。如果\\_n_之前至少_n_个获取的子表达式，则_n_为向后引用。否则，如果_n_为八进制数字（0-7），则_n_为一个八进制转义值。 |
| \\_nm_ | 标识一个八进制转义值或一个向后引用。如果\\_nm_之前至少有_nm_个获得子表达式，则_nm_为向后引用。如果\\_nm_之前至少有_n_个获取，则_n_为一个后跟文字_m_的向后引用。如果前面的条件都不满足，若_n_和_m_均为八进制数字（0-7），则\\_nm_将匹配八进制转义值_nm_。 |
| \\_nml_ | 如果_n_为八进制数字（0-3），且_m和l_均为八进制数字（0-7），则匹配八进制转义值_nm_l。 |
| \\u_n_ | 匹配_n_，其中_n_是一个用四个十六进制数字表示的Unicode字符。例如，\\u00A9匹配版权符号（©）。 |

### 常用正则表达式
| 用户名 | /^[a-z0-9_-]{3,16}$/ |
| --- | --- |
| 密码 | /^[a-z0-9_-]{6,18}$/ |
| 十六进制值 | /^#?([a-f0-9]{6}&#124;[a-f0-9]{3})$/ |
| 电子邮箱 | /^([a-z0-9_\\.-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,6})$/
`/^[a-z\\d]+(\\.[a-z\\d]+)*@([\\da-z](-[\\da-z])?)+(\\.{1,2}[a-z]+)+$/` |
| URL | /^(https?:\\/\\/)?([\\da-z\\.-]+)\\.([a-z\\.]{2,6})([\\/\\w \\.-]*)*\\/?$/ |
| IP 地址 | /((2[0-4]\\d&#124;25[0-5]&#124;[01]?\\d\\d?)\\.){3}(2[0-4]\\d&#124;25[0-5]&#124;[01]?\\d\\d?)/
/^(?:(?:25[0-5]&#124;2[0-4][0-9]&#124;[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]&#124;2[0-4][0-9]&#124;[01]?[0-9][0-9]?)$/ |
| HTML 标签 | /^<([a-z]+)([^<]+)*(?:>(.*)<\\/\\1>&#124;\\s+\\/>)$/ |
| 删除代码\\\\注释 | (?<!http:&#124;\\S)//.*$ |
| Unicode编码中的汉字范围 | /^[\\u2E80-\\u9FFF]+$/ |

## 3.常见的HTTP头部信息
Accept: 允许哪些媒体类型
Accept-Charset: 允许哪些字符集
Accept-Encoding: 允许哪些编码
Accept-Language: 允许哪些语言
Cache-Control: 缓存策略，如no-cache，详见官方文档
Connection: 连接选项，例如是否允许代理。
Host: 请求的主机
If-None-Match: 判断请求实体的Etag是否包含在If-None-Match中，如果包含，则返回304，使用缓存，见Etag
If-Modified-Since: 判断修改时间是否一致，如果一致，则使用缓存
If-Match: 与If-None-Match相反
If-Unmodified-Since: 与If-Modified-Since相反
Referer: 表明这个请求发起的源头
User-Agent: 这个大家相信应该很熟悉了，就是经常用来做浏览器检测的userAgent。
Cache-Control: 缓存策略，如max-age:100，详见官方文档
Connection: 连接选项，例如是否允许代理
Content-Encoding: 返回内容的编码，如gzip
Content-Language: 返回内容的语言
Content-Length: 返回内容的字节长度
Content-Type: 返回内容的媒体类型，如text/html
Data: 返回时间
Etag: entity tag，实体标签，给每个实体生成一个单独的值，用于客户端缓存，与If-None-Match配合使用
Expires: 设置缓存过期时间，Cache-Control也会相应变化
Last-Modified: 最近修改时间，用于客户端缓存，与If-Modified-Since配合使用
Pragma: 似乎和Cache-Control差不多，用于旧的浏览器
Server: 服务器信息。
Vary: WEB服务器用该头部的内容告诉 Cache 服务器，在什么条件下才能用本响应所返回的对象响应后续的请求。假如源WEB服务器在接到第一个请求消息时，其响应消息的头部为：Content-Encoding: gzip; Vary: Content-Encoding那么 Cache 服务器会分析后续请求消息的头部，检查其 Accept-Encoding，是否跟先前响应的 Vary 头部值一致，即是否使用相同的内容编码方法，这样就可以防止 Cache 服务器用自己 Cache 里面压缩后的实体响应给不具备解压能力的浏览器
## 4.url编码集
| ASCII 字符 | URL-编码 |
| --- | --- |
| space | %20 |
| ! | %21 |
| " | %22 |
| # | %23 |
| $ | %24 |
| % | %25 |
| & | %26 |
| ' | %27 |
| ( | %28 |
| ) | %29 |
| * | %2A |
| + | %2B |
| , | %2C |
| - | %2D |
| . | %2E |
| / | %2F |
| 0 | %30 |
| 1 | %31 |
| 2 | %32 |
| 3 | %33 |
| 4 | %34 |
| 5 | %35 |
| 6 | %36 |
| 7 | %37 |
| 8 | %38 |
| 9 | %39 |
| : | %3A |
| ; | %3B |
| < | %3C |
| = | %3D |
| > | %3E |
| ? | %3F |
| @ | %40 |
| A | %41 |
| B | %42 |
| C | %43 |
| D | %44 |
| E | %45 |
| F | %46 |
| G | %47 |
| H | %48 |
| I | %49 |
| J | %4A |
| K | %4B |
| L | %4C |
| M | %4D |
| N | %4E |
| O | %4F |
| P | %50 |
| Q | %51 |
| R | %52 |
| S | %53 |
| T | %54 |
| U | %55 |
| V | %56 |
| W | %57 |
| X | %58 |
| Y | %59 |
| Z | %5A |
| [ | %5B |
| \\ | %5C |
| ] | %5D |
| ^ | %5E |
| _ | %5F |
| ` | %60 |
| a | %61 |
| b | %62 |
| c | %63 |
| d | %64 |
| e | %65 |
| f | %66 |
| g | %67 |
| h | %68 |
| i | %69 |
| j | %6A |
| k | %6B |
| l | %6C |
| m | %6D |
| n | %6E |
| o | %6F |
| p | %70 |
| q | %71 |
| r | %72 |
| s | %73 |
| t | %74 |
| u | %75 |
| v | %76 |
| w | %77 |
| x | %78 |
| y | %79 |
| z | %7A |
| { | %7B |
| &#124; | %7C |
| } | %7D |
| ~ | %7E |
|   | %7F |
| ` | %80 |
|  | %81 |
| ‚ | %82 |
| ƒ | %83 |
| „ | %84 |
| … | %85 |
| † | %86 |
| ‡ | %87 |
| ˆ | %88 |
| ‰ | %89 |
| Š | %8A |
| ‹ | %8B |
| Œ | %8C |
|  | %8D |
| Ž | %8E |
|  | %8F |
|  | %90 |
| ' | %91 |
| ' | %92 |
| " | %93 |
| " | %94 |
| • | %95 |
| – | %96 |
| — | %97 |
| ˜ | %98 |
| ™ | %99 |
| š | %9A |
| › | %9B |
| œ | %9C |
|  | %9D |
| ž | %9E |
| Ÿ | %9F |
|   | %A0 |
| ¡ | %A1 |
| ¢ | %A2 |
| £ | %A3 |
| ¤ | %A4 |
| ¥ | %A5 |
| ¦ | %A6 |
| § | %A7 |
| ¨ | %A8 |
| © | %A9 |
| ª | %AA |
| « | %AB |
| ¬ | %AC |
|   | %AD |
| ® | %AE |
| ¯ | %AF |
| ° | %B0 |
| ± | %B1 |
| ² | %B2 |
| ³ | %B3 |
| ´ | %B4 |
| µ | %B5 |
| ¶ | %B6 |
| · | %B7 |
| ¸ | %B8 |
| ¹ | %B9 |
| º | %BA |
| » | %BB |
| ¼ | %BC |
| ½ | %BD |
| ¾ | %BE |
| ¿ | %BF |
| À | %C0 |
| Á | %C1 |
| Â | %C2 |
| Ã | %C3 |
| Ä | %C4 |
| Å | %C5 |
| Æ | %C6 |
| Ç | %C7 |
| È | %C8 |
| É | %C9 |
| Ê | %CA |
| Ë | %CB |
| Ì | %CC |
| Í | %CD |
| Î | %CE |
| Ï | %CF |
| Ð | %D0 |
| Ñ | %D1 |
| Ò | %D2 |
| Ó | %D3 |
| Ô | %D4 |
| Õ | %D5 |
| Ö | %D6 |
| × | %D7 |
| Ø | %D8 |
| Ù | %D9 |
| Ú | %DA |
| Û | %DB |
| Ü | %DC |
| Ý | %DD |
| Þ | %DE |
| ß | %DF |
| à | %E0 |
| á | %E1 |
| â | %E2 |
| ã | %E3 |
| ä | %E4 |
| å | %E5 |
| æ | %E6 |
| ç | %E7 |
| è | %E8 |
| é | %E9 |
| ê | %EA |
| ë | %EB |
| ì | %EC |
| í | %ED |
| î | %EE |
| ï | %EF |
| ð | %F0 |
| ñ | %F1 |
| ò | %F2 |
| ó | %F3 |
| ô | %F4 |
| õ | %F5 |
| ö | %F6 |
| ÷ | %F7 |
| ø | %F8 |
| ù | %F9 |
| ú | %FA |
| û | %FB |
| ü | %FC |
| ý | %FD |
| þ | %FE |
| ÿ | %FF |

## 5.windows系统python2，3版本共存问题
编写python脚本是后期各方向解题的重要手段（如sql注入漏洞利用方式中的盲注极其耗费时间精力，纯人力几乎无法完成）但是部分工具对python有版本限制，或python2，3版本会得到不同结果（如在flask框架的SSTI漏洞中python2与python3内置的索引值不同）
目前，Python3和Python2互相并不完全兼容，这就造成了很多Python代码或者是脚本在版本不对应的情况下无法执行，所以说，在一台电脑上同时拥有Python2和Python3是很有必要的，也能更高效的处理工作，节省时间。
其实要解决Python2和Python3共存也很简单，提供如下方案：
### 1、下载Python2和Python3的安装包(或者叫解释器)
下载地址：[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
根据自己需要的版本下载即可，安装包都比较小。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667987900810-c4c16e03-ac73-4212-ae19-3140ba7e8403.png#clientId=uc4c7c51b-e896-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=KHKsg&margin=%5Bobject%20Object%5D&name=image.png&originHeight=2090&originWidth=3456&originalType=url&ratio=1&rotation=0&showTitle=false&size=640270&status=done&style=none&taskId=u2418c492-4214-45b9-b102-16b10ce7afe&title=)
下载后，直接安装即可。
安装过程注意安装路径，默认是安装到C盘，可以根据需要进行更改安装路径。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667987900606-f6222d67-08c7-4fa9-a06c-9396dd1852ca.png#clientId=uc4c7c51b-e896-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=BTK6V&margin=%5Bobject%20Object%5D&name=image.png&originHeight=272&originWidth=1293&originalType=url&ratio=1&rotation=0&showTitle=false&size=34913&status=done&style=none&taskId=u261805bd-ed6c-495c-bb19-290d3373ffc&title=)
### 2、设置环境变量
由于我们安装了两个版本的Python，因此为了方便系统能够准确识别到指定的Python版本，所以我们需要设置环境变量。
将Python安装路径及其安装路径下的Scripts设置到Path变量里。
这里设置Scripts文件夹的目的是为了方便识别pip。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667987900517-42cf9800-3692-4ae4-8779-8c8c10c0479d.png#clientId=uc4c7c51b-e896-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=lnu3P&margin=%5Bobject%20Object%5D&name=image.png&originHeight=353&originWidth=1201&originalType=url&ratio=1&rotation=0&showTitle=false&size=43640&status=done&style=none&taskId=uf1bc7b66-1773-42cb-a228-dae54e9e88a&title=) 
### 3、修改Python编译器的名字
为了能够准确定位Python2和Python3，我们需要将默认的Python编辑器的名称进行修改。
**NO.1. **修改Python2安装目录下：python.exe修改为python2.exe，pythonw.exe修改为pythonw2.exe
**NO.2. **修改Python3安装目录下：python.exe修改为python3.exe，pythonw.exe修改为pythonw3.exe
修改完成后，在cmd命令行下分别输入python2和python3就可以进入对应版本的python环境。
### 4、设置pip
python环境在安装包的时候需要使用到包管理工具——pip，而pip也是需要对应版本的。在python的安装目录Scripts下可以看到 默认是存在pip的，但是在命令行下，并不能直接定位到，因此需要重新分别安装两个版本对应的pip，使得两个python版本的pip也能够共存。
#### python2：
`python2 -m pip install --upgrade pip`
#### python3:
`python3 -m pip install --upgrade pip`
安装完成之后，可以使用pip2 -V 或者pip3 -V查看对应的pip版本了。
## 6.关于靶场环境搭建
web的十大漏洞当中有很多漏洞在github上都能找到大师傅制作出来供学习用的靶场，这里针对一些可能出现的问题供大家参考
首先大家需要了解LAMP和LNMP，也就是linux，apache/nginx，mysql，php
这里Linux环境的实现需要用到虚拟机，也就是VMware，大家使用社团给的kali镜像，自行百度一下安装教程配置即可
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1670728188672-33f2cd44-b174-4a56-bd0b-004a4e42c402.png#clientId=ufeb3e999-f58d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=901&id=udaa712de&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1351&originWidth=2160&originalType=binary&ratio=1&rotation=0&showTitle=false&size=493408&status=done&style=none&taskId=ude5259c9-828d-4015-9dc1-fdad21b5487&title=&width=1440)
mysql是数据库的一种，对于专业开发人员可以使用navicat去管理数据库，这里仅作了解，对于环境搭建，使用PHPstudy即可满足我们全部的需求
phpstudy集成了php，mysql和apache、nginx两个web中间件（不知道什么是中间件的自己去百度），需要使用时按需求随时启停即可
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1670728101927-96a6e0d7-25f9-4730-ae56-7c30975e2773.png#clientId=ufeb3e999-f58d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=630&id=ub422b90f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=945&originWidth=1200&originalType=binary&ratio=1&rotation=0&showTitle=false&size=113570&status=done&style=none&taskId=ub825c629-6e8e-4c63-b20e-dc391dfb18b&title=&width=800)
那么如何搭建一个新环境呢
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1670728557152-f035162d-a9da-4c34-ba20-31e5bb503031.png#clientId=ufeb3e999-f58d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=630&id=u51e8922a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=945&originWidth=1200&originalType=binary&ratio=1&rotation=0&showTitle=false&size=113984&status=done&style=none&taskId=u1538d13d-8f7b-4b5f-be9d-5a6103274e0&title=&width=800)
phpstudy的目录下默认有一个WWW目录，下有一个localhost，即本地网站
想要创建新网站，遵照图中的几个步骤即可
域名设置起来除了不要有中文和符号之外非常自由，其实质就是在根目录下创建一个可以访问目录下资源的文件夹，这一点很好理解
端口设置为默认即可，若想改变端口，记得避开其他服务占用的端口，phpstudy提供了端口检测的功能，能够方便地测试和查看端口是否被占用，避免冲突
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1670940234774-607921c0-b864-4235-815d-1e6c593a9648.png#clientId=ua17198eb-70a7-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=630&id=u431719d3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=945&originWidth=1200&originalType=binary&ratio=1&rotation=0&showTitle=false&size=75061&status=done&style=none&taskId=u20103def-02bd-4123-83df-1090dc1a9ef&title=&width=800)
根目录可以自定义，默认会设定为软件安装路径的WWW目录下，比如我这里的目录是D:/phpstudy_pro/WWW/，设在E盘F盘也都是可以的（就是别放C盘）
建议不同漏洞的靶场
至于php版本问题，是一个非常值得说的点，这里暂不展开说，在后面的漏洞学习当中还会分别提到，在网站使用过程中，也可以对版本进行修改
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1670942055295-e56231e8-1b1e-4c97-be19-5f64342a9857.png#clientId=ubb6928da-eb0d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=198&id=ub9c6a179&margin=%5Bobject%20Object%5D&name=image.png&originHeight=297&originWidth=334&originalType=binary&ratio=1&rotation=0&showTitle=false&size=18794&status=done&style=none&taskId=udb58d283-55ff-4cd1-a44d-c5e3231a95b&title=&width=222.66666666666666)
除了php版本，其他软件的版本管理可以在下面找到
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1670942094171-fbf840d7-c572-44b0-92f3-e19029915980.png#clientId=ubb6928da-eb0d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=630&id=u15e641ee&margin=%5Bobject%20Object%5D&name=image.png&originHeight=945&originWidth=1200&originalType=binary&ratio=1&rotation=0&showTitle=false&size=136065&status=done&style=none&taskId=ue8028d4d-ce45-4514-bbeb-783599262c3&title=&width=800)
需要注意的是，无论更改了哪一项服务的版本，都需要重新启动才能生效
一些情况下还需要修改php的配置文件，每个版本对应一个ini文件，用txt打开即可
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1670942237079-60e99f5b-3c59-4866-92b5-a1fef4bda887.png#clientId=ubb6928da-eb0d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=630&id=u14e8cca4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=945&originWidth=1200&originalType=binary&ratio=1&rotation=0&showTitle=false&size=79355&status=done&style=none&taskId=u9b359638-dde1-42bc-b560-0a21c10d01f&title=&width=800)
**重头戏之php函数，特性（如下）**
## 7.PHP代码安全
PHP相关题目一般是CTF竞赛中Web类题目考察最多的，PHP语言具有很多特性，这些特性通常会造成预料之外的安全问题，也是很多CTF竞赛考查的知识点。
### 一、浮点数精度问题
### 理论知识
在用PHP进行浮点数的运算中,经常会出现一些和预期结果不一样的值，这是由于浮点数的精度有限。尽管取决于系统，PHP 通常使用 IEEE 754 双精度格式，则由于取整而导致的最大相对误差为 1.11e-16。非基本数学运算可能会给出更大误差，并且要考虑到进行复合运算时的误差传递。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477134064-1caf3cd8-9890-4a93-8014-d7ee12d56889.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=ua0c46fbd&margin=%5Bobject%20Object%5D&name=image.png&originHeight=354&originWidth=645&originalType=url&ratio=1&rotation=0&showTitle=false&size=269045&status=done&style=none&taskId=u23b0a048-a54f-463b-a508-a0f1e23fa5f&title=)
以十进制能够精确表示的有理数如 0.1 或 0.7，无论有多少尾数都不能被内部所使用的二进制精确表示，因此不能在不丢失一点点精度的情况下转换为二进制的格式。这就会造成混乱的结果：例如，floor((0.1+0.7)*10) 通常会返回 7 而不是预期中的 8，因为该结果内部的表示其实是类似 7.9999999999999991118…。
### 例子
#### 题目代码
```php
<?php
    if($_GET['num']<>""){
        $num = $_GET['num'];
        if(strstr($num,'1')){
            die("Sorry");
        }elseif($num <> 1){
            echo "Try to num = 1";
        }
        if($num == 1 ){
            echo 'flag{xxxxxxxx}';
        }
    }
```
#### payload
num=0.9999999999999999999999999999999999999999999999
## 二、类型转换问题
### 理论知识
#### 常见转换
常见的转换主要就是int转换为string，string转换为int。
转换方式：
```php
$var = 5;
方式1：$item = (string)$var;
方式2：$item = strval($var);
```
常见的PHP数学运算：
```php
<?php
var_dump(0 == '0'); // true
var_dump(0 == 'abcdefg'); // true
var_dump(0 === 'abcdefg'); // false
var_dump(1 == '1abcdef'); // true
var_dump(intval('3389a'));//输出3389
```
当有一个比较参数是整数的时候，会把另一个参数强制转换为整数。
#### 0e转换问题
在松散模式的比较下，PHP会将0e这类字符串识为科学技术法表示的数字。
通常会以md5()作为考考查。
**字符串加密后md5为0exxxx的字符串(x必须是10进制数字)列表**

| 字符串 | md5 |
| --- | --- |
| QNKCDZO | 0e830400451993494058024219903391 |
| 240610708 | 0e462097431906509019562988736854 |
| aabg7XSs | 0e087386482136013740957780965295 |
| aabC9RqS | 0e041022518165728065344349536299 |
| s878926199a | 0e545993274517709034328855841020 |

### 例子（1）
#### 题目代码
```php
<?php
    error_reporting(0);
    $flag = 'flag{1S_numer1c_Not_S4fe}';
    $id = $_GET['id'];
    is_numeric($id)?die("Sorry...."):NULL;    
    if($id>665){
        echo $flag;
    } 
?>
```
#### payload
id=666a
### 例子（2）
#### 题目代码
```php
<?php
    $md5_1 = md5('QNKCDZO');
    $a = @$_GET['a'];
    $md5_2 = @md5($a);
    if(isset($a)){
        if ($a != 'QNKCDZO' && $md5_1 == $md5_2) {
            echo "flag{*****************}";
        } else {
            echo "false!!!";
        }
    }
    else{
        echo "please input a";
    }
?>
```
#### payload
a=240610708
## 三、松散判断问题
### 理论知识
#### 1. 变量的松散比较问题
php比较相等性的运算符有两种，一种是严格比较 ===，另一种是松散比较 ==。
PHP 会根据变量的值，自动把变量转换为正确的数据类型。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477134197-08663759-fe02-4ded-b295-c0b27f70ada6.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=ud0e2955e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=454&originWidth=1027&originalType=url&ratio=1&rotation=0&showTitle=false&size=491220&status=done&style=none&taskId=uc2798905-0739-4f95-9e32-5235f8632e4&title=)
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477134209-9fac049e-32ea-4400-b5ef-92cec4591ade.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u612400b2&margin=%5Bobject%20Object%5D&name=image.png&originHeight=458&originWidth=1025&originalType=url&ratio=1&rotation=0&showTitle=false&size=462809&status=done&style=none&taskId=u25c0698b-5d6e-4249-bdae-6bd2dbe8323&title=)
#### 2. 数组的松散问题
```php
<?php
$c = $_GET['c'];
$a = $_GET['a'];
if(!strcmp($c[1],$a) && $c[1]!==$a){
    echo 'flag{***********}';
}    
```
可以发现，这个分支通过strcmp函数比较，要求两者相等，且==要求两者不相等才能getflag。
这里的strcmp函数实际上是将两个变量转换成ascii然后做数学减法，返回一个int的差值。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477133981-063c5879-de2f-45e0-9e07-af36ab8e5e16.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=udab4fd78&margin=%5Bobject%20Object%5D&name=image.png&originHeight=295&originWidth=368&originalType=url&ratio=1&rotation=0&showTitle=false&size=69439&status=done&style=none&taskId=uf53ea2ca-65f9-4f85-a759-35e50ed8ddd&title=)
#### 3. 语句条件的松散判断问题
PHP的switch()使用了松散比较。
$which会被自动动intval()，如果每个case()都没有break，就会一直执行到包含的语句。
```python
<?php 
if (isset($_GET['which'])) {
    $which = $_GET['which'];
		switch ($which)      
{      
    case 0:      
	case 1: 	 
	case 2: 			
show_source( $which.'.php' );              
break;      
default:              
echo GWF_HTML::error('PHP-0817', 'Hacker NoNoNo!', false);              
break; 	
	} 
} 
?> 
```
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477133936-978b4a89-f449-4135-afb7-d6bc866ecacb.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=ufa2c7d5f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=115&originWidth=309&originalType=url&ratio=1&rotation=0&showTitle=false&size=23561&status=done&style=none&taskId=ufb4e33be-50cc-4afc-8132-cd2a9de140a&title=)
#### 4. 函数的松散判断问题
`var_dump(in_array("abc", $array)); `
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477134820-76d19a7b-476e-4f9f-8e15-39e49cf4ff04.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u4996780f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=418&originWidth=1184&originalType=url&ratio=1&rotation=0&showTitle=false&size=194134&status=done&style=none&taskId=u9a27ddde-cff6-4740-afcc-037a12bccc8&title=)
`in_array()`是PHP当中经常使用的函数，用于检查数组中是否存在某个值。默认是使用松散模式遍历数组，进行比较。松散模式，存在一定的安全问题。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477135239-260cf7ae-75c8-4466-bfaa-eaa6b1862113.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u1fdc2a59&margin=%5Bobject%20Object%5D&name=image.png&originHeight=311&originWidth=488&originalType=url&ratio=1&rotation=0&showTitle=false&size=135764&status=done&style=none&taskId=ufe0e3c2d-c4b0-4578-b69c-b30058ddcd9&title=)
## 四、加密函数问题
### 理论知识
`md5()`和`sha1()`对一个数组进行加密将返回 `NULL`。
### 例子
#### 题目代码
```php
<?php
error_reporting(0);
$flag = 'flag{I_think_that_I_just_broke_md5}';
if (isset($_GET['username']) and isset($_GET['password'])) {
    if ($_GET['username'] == $_GET['password'])
        print 'Your password can not be your username.';
    else if (md5($_GET['username']) === sha1($_GET['password']))
        die($flag);
    else
        print 'Invalid password';
}
?>
```
#### payload
username[]=1&password[]=2
## 五、字符串处理函数漏洞缺陷
### 理论知识
`strcmp()`、`ereg()`、`strpos()`三个字符串处理函数在处理数组时，会出现异常，返回`NULL`。
### 例子
#### 题目代码
```php
<?php
    error_reporting(0);
    $flag = 'flag{P@ssw0rd_1s_n0t_s4fe_By_d0uble_Equ4ls}';
    if (isset ($_GET['password'])) {  
        if (ereg ("^[a-zA-Z0-9]+$", $_GET['password']) === FALSE)  
            echo 'You password must be alphanumeric';  
        else if (strpos ($_GET['password'], '--') !== FALSE)  
            die($flag);  
        else  
            echo 'Invalid password';  
    }  
?>
```
#### payload
password[]=gg
## PHP中的各种trick
### parse_url()函数
#### 条件
< php5.4.7
#### 介绍
我们看以下测试：
```php
<?php

$url=parse_url($_SERVER['REQUEST_URI']);

var_dump($url);

parse_str($url['query'],$query);

var_dump($query);

$key_word=array("select","from","for","like");

    foreach($query as $key)

    {

        foreach($key_word as $value)

        {

            if(preg_match("/".$value."/",strtolower($key)))

            {

                die("Stop hacking by using SQL injection!");

            }

        }

    }

?>
```
先正常输入：
`http://localhost/web/trick1/parse.php?sql=select`
可以看到，被正常的过滤
H:\wamp64\www\web\trick1\parse.php:3:
    array (size=2)
    
    'path' => string '/web/trick1/parse.php' (length=21)
    
    'query' => string 'sql=select' (length=10)

H:\wamp64\www\web\trick1\parse.php:5:
    
    array (size=1)
    
    'sql' => string 'select' (length=6)

Stop hacking by using SQL injection!

但是构造这样的请求：
`http://localhost///web/trick1/parse.php?sql=select`
则
H:\wamp64\www\web\trick1\parse.php:3:boolean false
H:\wamp64\www\web\trick1\parse.php:5:

array (size=0)

  empty

可以绕过过滤，导致注入成功
因为这里用到了`parse_ur`l函数在解析url时存在的bug
通过：`///x.php?key=value`的方式可以使其返回False
#### 原理
具体可以看下parse_url()的源码，关键代码如下
```php
PHPAPI php_url *php_url_parse_ex(char const *str, size_t length)

{

    char port_buf[6];

    php_url *ret = ecalloc(1, sizeof(php_url));

    char const *s, *e, *p, *pp, *ue;

    ...snip...

} else if (*s == '/' && *(s + 1) == '/') { /* relative-scheme URL */

        s += 2;

    } else {

        just_path:

        ue = s + length;

        goto nohost;

    }

    e = s + strcspn(s, "/?#");

    ...snip...

    } else {

        p = e;

    }

    /* check if we have a valid host, if we don't reject the string as url */

    if ((p-s) 1) {

        if (ret->scheme) efree(ret->scheme);

        if (ret->user) efree(ret->user);

        if (ret->pass) efree(ret->pass);

        efree(ret);

        return NULL;

    }
```
可以看到，在函数parse_url内部，如果url是以//开始，就认为它是相对url
而后认为url的部件从url+2开始。若`p-s < 1`也就是如果url为`///x.php`，则`p = e = s = s + 2`，函数将返回 NULL。
再看`PHP_FUNCTION`,line 351：
```php
 /* {{{ proto mixed parse_url(string url, [int url_component])

   Parse a URL and return its components */

PHP_FUNCTION(parse_url)

{

    char *str;

    size_t str_len;

    php_url *resource;

    zend_long key = -1;

    if (zend_parse_parameters(ZEND_NUM_ARGS(), "s|l", &str, &str_len, &key) == FAILURE) {

        return;

    }

    resource = php_url_parse_ex(str, str_len);

    if (resource == NULL) {

        /* @todo Find a method to determine why php_url_parse_ex() failed */

        RETURN_FALSE;

}
```
若php_url_parse_ex结果为 NULL，函数parse_url将返回FALSE
但是如果输入
`http://localhost/web/trick1//parse2.php?/home/binarycloud/`
则会被当做相对url，
此时的`parse2.php?/home/binarycloud/`都会被当做是`data[‘path’]`
而不再是`query`，导致可以绕过过滤。
但是需要注意的是：
查阅官方手册后：
Example #2 A parse_url() example with missing scheme$url = '//www.example.com/path?googleguy=googley';

// Prior to 5.4.7 this would show the path as "//www.example.com/path"

var_dump(parse_url($url));

?>

#### 实例
题目来自2017swpu的一道web题
```php
<?php

error_reporting(0);

$_POST=Add_S($_POST);

$_GET=Add_S($_GET);

$_COOKIE=Add_S($_COOKIE);

$_REQUEST=Add_S($_REQUEST);

function Add_S($array){

    foreach($array as $key=>$value){

        if(!is_array($value)){          

            $check= preg_match('/regexp|like|and|\"|%|insert|update|delete|union|into|load_file|outfile|\/\*/i', $value);

            if($check)

                {

                exit("Stop hacking by using SQL injection!");

            }

        }else{

            $array[$key]=Add_S($array[$key]); 

        }

    }

return $array;

}

function check_url()

{

    $url=parse_url($_SERVER['REQUEST_URI']);

    parse_str($url['query'],$query);

    $key_word=array("select","from","for","like");

    foreach($query as $key)

    {

        foreach($key_word as $value)

        {

            if(preg_match("/".$value."/",strtolower($key)))

            {

                die("Stop hacking by using SQL injection!");

            }

        }

    }

}

?>
```
从源码中可知有一个check_url()函数会进行过滤
但是他利用了这样的获取方式
`$url=parse_url($_SERVER['REQUEST_URI']); parse_str($url['query'],$query); `
而这就导致了我们的攻击点。
### in_array()函数
#### 相关知识
查阅PHP手册：
(PHP 4, PHP 5, PHP 7)
`in_array() — 检查数组中是否存在某个值`
大体用法为：
`bool in_array ( mixed $needle , array $haystack [, bool $strict = FALSE ] )  `
而官方的解释也很有意思：
大海捞针，在大海（haystack）中搜索针（needle），如果没有设置 strict 则使用宽松的比较。
#### 漏洞问题
我们注意到
`bool $strict = FALSE  `
宽松比较如果不设置，默认是FALSE，那么这就会引来安全问题
如果设置$strict = True:则 in_array() 函数还会检查 needle 的类型是否和 haystack 中的相同。
那么不难得知，如果不设置，那么就会产生弱类型的问题
例如：
```php
<?php
$whitelist = range(1, 24);
$filename='sky';
var_dump(in_array($filename, $whitelist));
?>
```
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477135982-05fcb338-82ad-46f1-8dd2-da19c275dce2.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=ud9231c02&margin=%5Bobject%20Object%5D&name=image.png&originHeight=496&originWidth=1100&originalType=url&ratio=1&rotation=0&showTitle=false&size=72382&status=done&style=none&taskId=ua3d8de17-4703-4841-9b1a-dd3af5f37e4&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t018abb8965f13840d0.png)
此时运行结果为false
但是如果我们将filename改为1sky
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477136003-d341cd3f-b15f-4fcc-a11a-e45a0565d0ff.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u38bfe2ed&margin=%5Bobject%20Object%5D&name=image.png&originHeight=470&originWidth=1102&originalType=url&ratio=1&rotation=0&showTitle=false&size=71702&status=done&style=none&taskId=u9d1b73d6-b5af-4e95-97f0-f9f1e122e89&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t01424511a642ee1ff2.png)成功利用弱比较，而绕过了这里的检测
#### 典型案例
上面的实例已说明了问题，其实这个问题是存在于上次文件的检查的
在php-security-calendar-2017-Wish List中
```php
class Challenge {
    const UPLOAD_DIRECTORY = './solutions/';
    private $file;
    private $whitelist;

    public function __construct($file) {
        $this->file = $file;
        $this->whitelist = range(1, 24);
    }

    public function __destruct() {
        if (in_array($this->file['name'], $this->whitelist)) {
            move_uploaded_file(
                $this->file['tmp_name'],
                self::UPLOAD_DIRECTORY . $this->file['name']
            );
        }
    }
}

$challenge = new Challenge($_FILES['solution']);
```
我们不难看出，代码的意图上是想让我们只传数字名称的文件的
而我们却可以用1skyevil.php这样的名称去bypass
由于没有修改in_array的默认设置，而导致了安全问题
可能这比较鸡肋，但在后续对文件的处理中，前一步产生了非预期，可能会直接影响后一步的操作
#### 漏洞修复
将宽松比较设为true即可
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477136497-57bb47c7-aafa-4ea5-bae0-6a11368024f3.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=uc7d14c61&margin=%5Bobject%20Object%5D&name=image.png&originHeight=600&originWidth=1250&originalType=url&ratio=1&rotation=0&showTitle=false&size=99795&status=done&style=none&taskId=uf057204e-80af-4f61-80d1-8e164fbb53b&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t0115f0ad8431fa62fe.png)可以看到，搜索的时候，直接要求前两个参数均为array
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477136505-d58c4b19-f5fc-4ffe-ba95-3b7a51ab2785.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=ue5ee6b2e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=860&originWidth=1246&originalType=url&ratio=1&rotation=0&showTitle=false&size=117400&status=done&style=none&taskId=u3b034be7-9278-489b-b73d-cb40f57ae2c&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t01dfb3947529464dfa.png)此时已经不存在弱比较问题
### filter_var()函数
#### 相关知识
(PHP 5 >= 5.2.0, PHP 7)
filter_var — 使用特定的过滤器过滤一个变量
mixed filter_var ( mixed $variable [, int $filter = FILTER_DEFAULT [, mixed $options ]] )  虽然官方说这是过滤器，但是如果用这个函数进行过滤，并且相信他的结果，是非常愚蠢的
#### 漏洞问题
比较常用的当属FILTER_VALIDATE_URL了吧，但是它存在非常多的过滤bypass
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477137412-8a305d52-8408-4ff8-93d7-cc6754943912.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=uf81e3508&margin=%5Bobject%20Object%5D&name=image.png&originHeight=466&originWidth=1088&originalType=url&ratio=1&rotation=0&showTitle=false&size=74429&status=done&style=none&taskId=uae6a477c-9957-4f4d-b1c0-7fb2cc6ec64&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t01b08e5038dc6881ae.png)本应该用于check url是否合法的函数，就这样放过了可能导致SSRF的url
类似的bypass还有：
`0://evil.com:80$skysec.top:80/ 0://evil.com:80;skysec.top:80/  `
详细SSRF漏洞触发可参考这篇文章：
[http://skysec.top/2018/03/15/Some%20trick%20in%20ssrf%20and%20unserialize()/](http://skysec.top/2018/03/15/Some%20trick%20in%20ssrf%20and%20unserialize()/)
除此之外，还能触发xss
`javascript://comment%0Aalert(1)  `
#### 典型案例
```php
// composer require "twig/twig"
require 'vendor/autoload.php';

class Template {
    private $twig;

    public function __construct() {
        $indexTemplate = '<img ' .
            'src="https://loremflickr.com/320/240">' .
            '<a href="{{link|escape}}">Next slide »</a>';

        // Default twig setup, simulate loading
        // index.html file from disk
        $loader = new TwigLoaderArrayLoader([
            'index.html' => $indexTemplate
        ]);
        $this->twig = new TwigEnvironment($loader);
    }

    public function getNexSlideUrl() {
        $nextSlide = $_GET['nextSlide'];
        return filter_var($nextSlide, FILTER_VALIDATE_URL);
    }

    public function render() {
        echo $this->twig->render(
            'index.html',
            ['link' => $this->getNexSlideUrl()]
        );
    }
}

(new Template())->render();
```
这里不难看出是有模板渲染的，而模板渲染则有可能触发xss
那么寻找可控点，不难发现
public function render() {         echo $this->twig->render(             'index.html',             ['link' => $this->getNexSlideUrl()]         );     }  
这里的Link是使用了getNexSlideUrl()的结果
我们跟进这个函数
```php
public function render() {
        echo $this->twig->render(
            'index.html',
            ['link' => $this->getNexSlideUrl()]
        );
    }
```
这里的nextSlide使用就充分相信了filter_var()的过滤结果
所以导致了XSS：
`?nextSlide=javascript://comment%250aalert(1)  `
#### 漏洞修复
不要轻易的相信filter_var()，它只能当做初步验证函数，结果不能当做是否进入if的后续程序的条件
## class_exists()函数
### 相关知识
(PHP 4, PHP 5, PHP 7)
class_exists — 检查类是否已定义
bool class_exists ( string $class_name [, bool $autoload = true ] ) 检查指定的类是否已定义。
### 漏洞问题
上述操作表面上看起来似乎没有什么问题，和函数名一样，检查指定的类是否已定义
但是关键点就在于选项上，可以选择调用或不调用__autoload
更值得思考的是，该函数默认调用了__autoload
什么是__autoload？
PHP手册是这样描述的：
在编写面向对象（OOP） 程序时，很多开发者为每个类新建一个 PHP 文件。 这会带来一个烦恼：每个脚本的开头，都需要包含（include）一个长长的列表（每个类都有个文件）。
在 PHP 5 中，已经不再需要这样了。 spl_autoload_register() 函数可以注册任意数量的自动加载器，当使用尚未被定义的类（class）和接口（interface）时自动去加载。通过注册自动加载器，脚本引擎在 PHP 出错失败前有了最后一个机会加载所需的类。
那么自动调用__autoload会产生什么问题呢？
我们从下面的案例来看
### 典型案例
```php
function __autoload($className) {
    include $className;
}

$controllerName = $_GET['c'];
$data = $_GET['d'];

if (class_exists($controllerName)) {
    $controller = new $controllerName($data['t'], $data['v']);
    $controller->render();
} else {
    echo 'There is no page with this name';
}

class HomeController {
    private $template;
    private $variables;

    public function __construct($template, $variables) {
        $this->template = $template;
        $this->variables = $variables;
    }

    public function render() {
        if ($this->variables['new']) {
            echo 'controller rendering new response';
        } else {
            echo 'controller rendering old response';
        }
    }
}
```
案例同样来自php-security-calendar-2017
乍一看，这样的代码并不存在什么高危的问题，但实际上因为class_exists()的check自动调用了`__autoload()`
所以我们可以调用php的内置类实现攻击，例如SimpleXMLElement
正常来说，应该是可以这样触发render():
`http://localhost/xxe.php?c=HomeController&d[t]=sky&d[v][new]=skrskr `
可以得到回显
controller rendering new response 但此时我们可以使用SimpleXMLElement或是simplexml_load_string对象触发盲打xxe，进行任意文件读取
构造：
`simplexml_load_file($filename,'SimpleXMLElement') `
即
`c=simplexml_load_file&d[t]=filename&d[v]=SimpleXMLElement `
即可
而这里的$filename使用最常见的盲打XXE的payload即可
这就不再赘述，详细可参看
`https://blog.csdn.net/u011721501/article/details/43775691 `
### 漏洞修复
对于特点情况，可关闭自动调用
`bool $autoload = false  `
## htmlentities()函数
### 相关知识
(PHP 4, PHP 5, PHP 7)
htmlentities — 将字符转换为 HTML 转义字符
string htmlentities ( string $string [, int $flags = ENT_COMPAT | ENT_HTML401 [, string $encoding = ini_get("default_charset") [, bool $double_encode = true ]]] )  本函数各方面都和 htmlspecialchars() 一样， 除了 htmlentities() 会转换所有具有 HTML 实体的字符。
如果要解码（反向操作），可以使用 `html_entity_decode()`。
### 漏洞问题
从上述知识来看，该函数应该是用来预防XSS，进行转义的了
但是不幸的是
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477137491-2a2277d1-5ebc-4e1a-b407-309a6c6fdc85.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u07a0de5e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=980&originWidth=1634&originalType=url&ratio=1&rotation=0&showTitle=false&size=277457&status=done&style=none&taskId=u5d912fe8-bf28-49c3-ae1d-379dadf95ef&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t01421c6fd9c0b0fde3.png)该函数默认使用的是ENT_COMPAT
即不会转义单引号，那么就可能产生非常严重的问题，例如如下案例
### 典型案例
```php
$sanitized = [];

foreach ($_GET as $key => $value) {
    $sanitized[$key] = intval($value);
}

$queryParts = array_map(function ($key, $value) {
    return $key . '=' . $value;
}, array_keys($sanitized), array_values($sanitized));

$query = implode('&', $queryParts);

echo "<a href='/images/size.php?" .
    htmlentities($query) . "'>link</a>";
```
由于不会转义单引号
我们可以随意闭合
`<a href='/images/size.php?htmlentities($query)'>link</a>  `
此时我们替换htmlentities($query)为
`' onclick=alert(1) //  `
这样原语句就变成了
`<a href='/images/size.php?' onclick=alert(1) //'>link</a>  `
这样就成功的引起了xss
故此最终的payload为
`/?a'onclick%3dalert(1)%2f%2f=c  `
### 漏洞修复
必要的时候加上ENT_QUOTES选项
## openssl_verify()函数
### 相关知识
(PHP 4 >= 4.0.4, PHP 5, PHP 7)
openssl_verify — 验证签名
int openssl_verify ( string $data , string $signature , mixed $pub_key_id [, mixed $signature_alg = OPENSSL_ALGO_SHA1 ] )  openssl_verify() 使用与pub_key_id关联的公钥验证指定数据data的签名signature是否正确。这必须是与用于签名的私钥相对应的公钥。
### 漏洞问题
这个函数看起来是用于验证签名正确性的，怎么会产生漏洞呢？
我们注意到它的返回值情况
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477137356-17471838-35d6-4798-be1b-041c0649e456.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u1a86a4e7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=222&originWidth=960&originalType=url&ratio=1&rotation=0&showTitle=false&size=31708&status=done&style=none&taskId=ue4b15b3f-44ea-4a16-95cb-689c5eac382&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t0192bd3b09104db6b1.png)其中，内部发送错误会返回-1
我们知道if判断中，-1和1同样都可以被当做true
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477137573-4eed5d51-ae74-47eb-9a91-7c1ae2d07e60.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=ud0ffbcd9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=660&originWidth=726&originalType=url&ratio=1&rotation=0&showTitle=false&size=61601&status=done&style=none&taskId=u5f1a942d-940f-48e7-b46e-31af01e090b&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t018a24735d6d00f170.png)那么假设存在这样的情况
`if(openssl_verify())`
那么它出现错误的时候，则同样可以经过check进入后续程序
如何触发错误呢？
实际上只要使用另一个与当前公钥不匹配的算法生成的签名，即可触发错误
### 典型案例
```php
class JWT {
    public function verifyToken($data, $signature) {
        $pub = openssl_pkey_get_public("file://pub_key.pem");
        $signature = base64_decode($signature);
        if (openssl_verify($data, $signature, $pub)) {
            $object = json_decode(base64_decode($data));
            $this->loginAsUser($object);
        }
    }
}

(new JWT())->verifyToken($_GET['d'], $_GET['s']);
```
此时我们只需要使用一个不同于当前算法的公钥算法，生成一个有效签名，然后传入参数
即可导致openssl_verify()发生内部错误，返回-1，顺利通过验证，达成签名无效依然可以通过的目的
### 漏洞修复
if判断中使用
if(openssl_verify()===1)  
[![image.png](https://cdn.nlark.com/yuque/0/2022/png/22941704/1667477137914-4f42d543-fa9a-419f-917d-b2f49500354f.png#clientId=ua93d0166-f3e5-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u064741e2&margin=%5Bobject%20Object%5D&name=image.png&originHeight=622&originWidth=736&originalType=url&ratio=1&rotation=0&showTitle=false&size=57811&status=done&style=none&taskId=ufd0c2f4a-5458-41a8-96d8-3cc6daf70b8&title=)](http://mweb-zeal.oss-cn-qingdao.aliyuncs.com/2022/05/24/t01372e5a180c19f3b1.png)
## intval()缺陷
intval函数用于获取变量的整数值。通过使用指定的进制 base 转换（默认是十进制），返回变量 var 的 integer 数值。 intval() 不能用于 object，否则会产生 E_NOTICE 错误并返回 1。
本来想写在php函数缺陷内的，但是这个函数，往往在进行比较时使用。
intval() 在转换的时候，会从字符串的开始进行转换直到遇到一个非数字的字符。即使出现无法转换的字符串，intval() 不会报错而是返回 0 
例如：
```php
var_dump(intval('2')) // 2
var_dump(intval('3abcd')) // 3
var_dump(intval('abcd')) // 0

var_dump(0 == '0'); // true
var_dump(0 == 'abcdefg'); // true 
var_dump(0 === 'abcdefg'); // false
var_dump(1 == '1abcdef'); // true

if(intval($a) > 1000) {
    mysql_query("select * from news where id=".$a)
}
```
## strcmp函数缺陷
这个函数也经常的被使用到，也是一个经典函数。
定义:
 int strcmp ( string $str1 , string $str2 )     参数 str1第一个字符串。str2第二个字符串。如果 str1 小于 str2 返回 < 0； 如果 str1 大于 str2 返回 > 0；如果两者相等，返回 0。 漏洞：
在php5.3之前，当这个函数接受到了不符合的类型，这个函数将发生错误，显示了报错的警告信息后，将return 0。 
经典题目：
```php
<?php
$password="***************";
$a = array();
    if (strcmp($a, $password) == 0) {
        echo "Right!!!login success";
        exit();
    } else {
        echo "Wrong password..";
}
?>
结果输出 Right!!!login success。
```
## ereg()，eregi()函数缺陷

- ereg函数存在两个漏洞： 
   - %00截断，在遇到%00的时候会认为字符串结束了
   - ereg函数中的参数值如果为数组，会返回false

eregi跟ereg函数漏洞基本一样，区别在于ereg区分大小写(这里划重点，也是可以用来绕过的),eregi函数不区分大小写。
经典题目：
```php
<?php
if (isset ($_GET['password'])) {
    if (ereg ("^[a-zA-Z0-9]+$",$_GET['password']) === FALSE)    
       {
        echo '<p>You password must be alphanumeric</p>';
    }
    else if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)
    {
        if (strpos ($_GET['password'], '*-*') !== FALSE)
        {
            die('Flag: ' . $flag);
        }
        else
        {
            echo('<p>*-* have not been found</p>');
        }
    }
    else
    {
        echo '<p>Invalid password</p>';
    }
}
?>
附：payload= 1e9%00*-*
```
## strlen()函数缺陷
这个函数也是CTF函数黑魔法中的经典函数，自我矛盾。用来进行判断长度，然后结合大小比较来进行出题。
但是可以通过科学计数法的方法来进行绕过。比如：
`1e9 `
经典题目：
```php
<?php
@$a = $_GET['num'];
if(strlen($a)<4 && $a>10000){
    echo $flag;
}
else{
    echo "is too small";
}
?>
```
## preg_match()，preg_match_all()函数缺陷
先说preg_match()函数，是为了弥补ereg函数的%00截断问题，替换了ereg函数。但是，在CTF中踩了那么多坑以后，终于发现了制裁它的方法，构造数组，就可以了。
经典题目：
`payload: id[]=1 `
```php
<?php
$str = intval($_GET['id']);
$reg = preg_match('/\d/is', $_GET['id']);    //有0-9的数字 和.在内的符号
if(!is_numeric($_GET['id']) and $reg !== 1 and $str === 1){
    echo 'Flag';
}else{
    echo "no";
}// 最终输出了Flag
?>
```
preg_match()函数还存在另一个问题，preg_match 函数用于进行正则表达式匹配，返回 pattern 的匹配次数，它的值将是 0 次（不匹配）或 1 次，因为 preg_match() 在第一次匹配后将会停止搜索。如果在进行正则表达式匹配的时候，没有限制字符串的开始和结束(^ 和 $)，则可以存在绕过的问题。
经典题目：
`payload:ip=127.0.0.1 abcdasd `
```php
<?php
$ip = $_GET['ip']; // 可以绕过
if(!preg_match("/(\d+)\.(\d+)\.(\d+)\.(\d+)/",$ip)) {
  die('error');
} else {
  echo "Flag";
}
?>// Flag
```
preg_match_all()这个函数还没有单独的碰到过，碰到了再做总结吧。（我不是标题党）
## is_numeric()函数缺陷&trim()函数缺陷
is_numeric() 函数用于检测变量是否为数字或数字字符串。如果指定的变量是数字和数字字符串则返回 TRUE，否则返回 FALSE。
好，那么问题来了，对于16进制的字符串，是怎么判断的呢？
它会默认16进制的字符串为整形，这样就可以构造16进制的payload来进行函数绕过。
例题：
```php
16进制的abc=0x616263
<?php
header('content-type:text/html;charset=utf-8');
$a=$_GET['num'];
var_dump($a);
if(is_numeric($a)){
    echo "您输入的是数字";
}else{
    echo "请输入合法字符";
}
?>
```
```php
<?php
echo is_numeric(233333);       // 1
echo is_numeric('233333');    // 1
echo is_numeric(0x233333);    // 1
echo is_numeric('0x233333');    // 1
echo is_numeric('9e9');   // 1
echo is_numeric('233333abc');  // 0
?>
```
is_numeric 检测的时候会自动过滤掉前面的 ‘ ‘, ‘\t’, ‘\n’, ‘\r’, ‘\v’, ‘\f’ 等字符，但是不会过滤 ‘\0’，如果这些字符出现在字符串尾，也不会过滤，而是返回 false
trim 函数会过滤空格以及 \n\r\t\v\0，但不会过滤过滤\f
`$a = "  \n\r\t\v\0abc  \f"; var_dump(trim($a)); // abc  \f `
利用trim函数以及is_numeric函数实现绕过：
```php
<?php
    // %0c1%00
    $number = "\f1\0";
    // trim 函数会过滤 \n\r\t\v\0，但不会过滤过滤\f
    $number_2 = trim($number);
    var_dump($number_2); // \f1
    $number_2 = addslashes($number_2);
    var_dump($number_2);  // \f1
    // is_numeric 检测的时候会过滤掉 '', '\t', '\n', '\r', '\v', '\f' 等字符
    // 但是不会过滤 '\0'
    var_dump(is_numeric($number)); // false
    var_dump(strval(intval($number_2))); // 1
    var_dump("\f1" == "1"); // true
?>
```
## in_array()函数缺陷
in_array()函数用来判断字符串是否存在与数组中，但是在判断的时候，会进行类型强制转换，就会出现数字比较的情况。
经典例题：
```php
<?php
$array=[0,1,2,'3'];  
var_dump(in_array('abc', $array)); // true
var_dump(in_array('1bc', $array)); // true
?>
```
那这种情况，在SQL注入时，就可以产生很大的作用，比如：
payload: `a = 1' or 1=1--+ `
```php
<?php
@$a = $_GET['a'];
$arr = [1,2,3,4];
if(in_array($a,$arr)){
    echo "success!";// 输出success
}
?>
```
## strpos()函数缺陷
strpos() 函数查找字符串在另一字符串中第一次出现的位置（区分大小写）。
经典题目：
```php
<?php
if(strpos($_GET['a'],'abc') == 0 ){
    echo '123';
}
else{
    echo '456';
}
?>
```
传入abc或会打印123，但是传入一个数组或者不传入数据一样也会打印123。这个函数也是只解析string类型的字符串，给他个数组就不知道如何解析，于是就返回为null。Null==0！当不传入数据的时候，也是一样的道理，还是返回null。
## 变量覆盖
### extract()函数
用法：
extract() 函数从数组中将变量导入到当前的符号表。该函数使用数组键名作为变量名，使用数组键值作为变量值。针对数组中的每个元素，将在当前符号表中创建对应的一个变量。
EXTR_OVERWRITE - 默认。如果有冲突，则覆盖已有的变量。
EXTR_SKIP - 如果有冲突，不覆盖已有的变量。
EXTR_PREFIX_SAME - 如果有冲突，在变量名前加上前缀 prefix。
EXTR_PREFIX_ALL - 给所有变量名加上前缀 prefix。
EXTR_PREFIX_INVALID - 仅在不合法或数字变量名前加上前缀 prefix。
EXTR_IF_EXISTS - 仅在当前符号表中已有同名变量时，覆盖它们的值。其它的都不处理。
EXTR_PREFIX_IF_EXISTS - 仅在当前符号表中已有同名变量时，建立附加了前缀的变量名，其它的都不处理。
EXTR_REFS - 将变量作为引用提取。导入的变量仍然引用了数组参数的值。
这个函数的重点就是默认将已经有的变量给覆盖掉
其实很简单，就是变量覆盖，给个例题一看就知道了：
```php
<?php
  $auth = 'yaun';  
    extract($_GET); 
    if($auth == 1){  
        echo "private!";  
    } else{  
        echo "public!";  
    }  
?>
参数：auth=1
```
这样，输出privatel了。
经典题目：
```php
<?php

   $flag = ‘xxx’;

   extract($_GET);

   if (isset($gift)) 
  {
       $content = trim(file_get_contents($flag));

       if ($gift == $content) 
      {
            echo ‘hctf{…}’;

      } 
       else 
      {
           echo ‘Oh..’;
      }

   } 
?>
```
### parse_str()函数导致变量覆盖
parse_str() 函数用于把查询字符串解析到变量中，如果没有array 参数，则由该函数设置的变量将覆盖已存在的同名变量。 极度不建议 在没有 array参数的情况下使用此函数，并且在 PHP 7.2 中将废弃不设置参数的行为。此函数没有返回值。
```php
<?php
if(empty($_GET['id'])){
    show_source(__FILE__);
    die();
}else{
    include('flag.php');
    $a = "http://blog.51cto.com/12332766";
    $id = $_GET['id'];
    @parse_str($id);
    if($a[0] == 'yaun'){
        echo "yes is flag";
    }else{
        exit('其实很简单，其实并不难');
    }
}
?>
payload:id=a[]=yaun
```
当传递参数id=a[]=yaun的时候，经过parse_str()函数的处理将a变成变量。但是原来有同名的变量，于是就将原来的变量覆盖掉，同时覆盖的还有变量的值
### $$变量覆盖
直接上代码看：
```php
<?php
$a = 1;
$b = 2;
$c = 'a';
$$c = $b;    //   $a = $b
var_dump($a);   //   输出2
?>
```
CTF经典题目：
```php
<?php
   include “flag.php”;

   $_403 = “Access Denied”;

   $_200 = “Welcome Admin”;

   if ($_SERVER["REQUEST_METHOD"] != “POST”)
   {
         die(“BugsBunnyCTF is here :p…”);
   }
   if ( !isset($_POST["flag"]) )
   {
         die($_403);
   }
   foreach ($_GET as $key => $value)
   {
         $$key = $$value;
   }
   foreach ($_POST as $key => $value)
   {
         $$key = $value;
   }
   if ( $_POST["flag"] !== $flag )
   {
         die($_403);
   }
   echo “This is your flag : “. $flag . “\n”;
   die($_200);
?>
```
GET：_200=flag
POST：flag=abcde 
## json_decode()函数
先介绍下json字符串吧，json就是一种数据交换格式，在 JS 语言中，一切都是对象。因此，任何支持的类型都可以通过 JSON 来表示，例如字符串、数字、对象、数组等。但是对象和数组是比较特殊且常用的两种类型：
```php
对象表示为键值对
数据由逗号分隔
花括号保存对象
方括号保存数组
```
经典例题：
```php
<?php
if (isset($_POST['message'])) {
    $message = json_decode($_POST['message']);
    $key ="*********";
    if ($message->key == $key) {
        echo "flag";
    } 
    else {
        echo "fail";
    }
 }
 else{
     echo "~~~~";
 }
?>

payload: message={"key":0}
```
这个payload利用的还是php字符比较的漏洞，0==’admin’
## switch()函数漏洞
switch函数是php中的条件分支语句，通过对switch中的参数值进行判断，选择case中的代码去执行，但是会将switch中的参数转换为int类型，那么问题就来了，在进行类型转换的时候，’1admin’==’1’的。
经典题目：
```php
<?php
$i ="2abc";  
switch ($i) {  
case 0:  
case 1:  
case 2:  
echo "i is less than 3 but not negative";  
break;  
case 3:  
echo "i is 3";  
} 
// 输出了 i is less than 3 but not negative
?>
```
switch还有一个特别巧妙的坑，代码如下
```php
<?php
$a=0;
 switch($a){
    case $a>=0: echo 0;break;
    case $a>=10:echo 1;break; // 输出1
    default: echo 2;break;    
 }
?>
```
这个代码，巧妙在哪里？
第一个分支判断语句，并不会成立，因为case的条件是 0>=0 ，也就是 true ，但是参数$a为0，两者并不相等，但是第二个分支语句的case条件为 0>=10 ，也就是false，参数$a的值为0，’0’==’false’,所以case $a>=10成立。

---

**接下来进入漏洞学习篇章**

---


