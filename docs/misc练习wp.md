

# MISC

## 签到

关注齐鲁师院网络安全社团公众号，发送**QLNUCTF**，即可得到本题flag

## base编码

> 考点：base64编码

百度搜索**base编码**

https://the-x.cn/base64/

![image-20221115203537745](https://file.shenghuo2.top/typecho/202211152035815.png)



## 你猜它属啥

> 考点：查看文件属性

下载后右键找到属性

往下翻

![img](https://file.shenghuo2.top/typecho/202211152036145.png)

## 010的奥秘

> 考点：010editor的使用

010 editer下载链接 [https://file.shenghuo2.top/file/010%20Editor.rar](https://file.shenghuo2.top/file/010 Editor.rar)

用010查看文件最后

![img](https://file.shenghuo2.top/typecho/202211152040726.png)

## 会动的图

> 考点：GIF图片的逐帧查看

使用stegslove打开图片

![image-20221115204523247](https://file.shenghuo2.top/typecho/202211152045304.png)![image-20221115204538280](https://file.shenghuo2.top/typecho/202211152045349.png)



再使用frame browser查看，或者搜索在线gif查看器

反正只要逐帧查看图片就可以

## 表白的话

> 考点:md5值反向查询

md5解密网址：https://www.somd5.com/

md5(表白的话)=3e451fbcff5fef443993a72c66713e29

![img](https://file.shenghuo2.top/typecho/202211152049559.png)

### 社会主义好青年

> 考点：核心价值观编码

核心价值观编码

http://www.hiencode.com/cvencode.html

### 想见出题人吗？

> 考点：二维码修复

一个被从中间分开的二维码

截图	然后用PPT拼接就可以

### 好长的文本

> 考点：base64编码转图片

在线Base64编码转图片

http://www.atoolbox.net/Tool.php?Id=1024

![image-20221115211124363](https://file.shenghuo2.top/typecho/202211152111426.png)

也可以这样查看

浏览器地址栏输入**data:image/jpg;base64,要解码的值**

![image-20221115210512398](https://file.shenghuo2.top/typecho/202211152105459.png)

### 你看到我的玫瑰了吗

> 考点：url编码，w形栅栏密码

先进行url解码

http://www.hiencode.com/url.html

![image-20221115212050036](https://file.shenghuo2.top/typecho/202211152120109.png)



这道题是W形栅栏密码

http://moersima.00cha.net/shanlan.asp

不知道分栏数，可以用这个网站爆破

![image-20221115212321173](https://file.shenghuo2.top/typecho/202211152123245.png)

然后把flag{}改成QLNU{}提交即可

### bang

> 考点：压缩包密码爆破

下载之后是压缩包，打开需要密码

![img](https://file.shenghuo2.top/typecho/202211152124285.png)

可看到题目描述说密码为四位数

![img](https://file.shenghuo2.top/typecho/202211152124239.png)

[点击下载ARCHPR](https://file.shenghuo2.top/file/ARCHPR%E4%B8%AD%E6%96%87%E7%A0%B4%E8%A7%A3%E7%89%88%E5%AE%89%E8%A3%85%E5%8C%85.zip)

软件爆破得到密码

![img](https://file.shenghuo2.top/typecho/202211152124278.png)

解压得到flag

### base家族

> 考点：各种base编码

考base的各种编码

https://ctf.bugku.com/tools

可以用这里的base家族![image-20221115212907747](https://file.shenghuo2.top/typecho/202211152129834.png)

解码顺序，base64-->base85-->base32-->base64

### 假密码

> 考点：zip伪加密
>

 修改全局加密

均改为0

![img](https://file.shenghuo2.top/typecho/202211152133680.png)

重新解压

![img](https://file.shenghuo2.top/typecho/202211152133644.png)

###  后缀呢？

> 考点：常见类型文件头的辨认
>

![image-20221115214641574](https://file.shenghuo2.top/typecho/202211152146628.png)

 ![image-20221115214620056](https://file.shenghuo2.top/typecho/202211152146121.png)



![image-20221115214625162](https://file.shenghuo2.top/typecho/202211152146211.png)

![image-20221115214632547](https://file.shenghuo2.top/typecho/202211152146598.png)





flag1 flag2 flag3 flag4分别是png jpg bmp zip文件

重命名修改后打开即可

### WhoIMI

> 考点：信息收集

百度识图

找到电影相关的文章

![img](https://file.shenghuo2.top/typecho/202211152148490.png)

QLNU{主角所在团队名字_团队四人的偶像}

![img](https://file.shenghuo2.top/typecho/202211152148418.png)

 

```
QLNU{CLAY_MRX}
```

### 游戏

压缩包内bin为游戏存档	打开压缩包注释中的网址

去观察游戏界面都有什么  发现可以导入存档 左边导入存档 (即将文件给的bin导入  

在玩一玩游戏在游戏指导有 shift功能 （shift+x）挨个删删（只剩下运输器即可看清答案

![img](https://file.shenghuo2.top/typecho/202211152149410.png)

## MISC STEGANOGRAPHY

### flag在哪呢

> 考点：docx文件隐写

下载文件，docx文件

![img](https://file.shenghuo2.top/typecho/202211161117814.png)

ctrl+a全选一下文字，发现第二行有东西

![img](https://file.shenghuo2.top/typecho/202211161117785.png)

改一下字体颜色

![img](https://file.shenghuo2.top/typecho/202211161117801.png)

### 腿呢？

> 考点：修改图片宽高

下载题目，得到一张图片

发现不能正常显示	通过略缩图发现图片看不到腿，猜测为修改图片高度

![img](https://file.shenghuo2.top/typecho/202211161117970.png)

根据题目可知该图片应该有腿，用010打开，修改高度

![img](https://file.shenghuo2.top/typecho/202211161117818.png)

修改的数尽量大点，不容易出错

![img](https://file.shenghuo2.top/typecho/202211161117789.png)

修改完别忘了保存哈！！！（快捷键：**ctrl+s**）然后再次打开图片

![img](https://file.shenghuo2.top/typecho/202211161117052.png)

### 人美心善的学姐

> 考点：文件后藏的文件分离

**ctrl+f** 选择在16进制字节搜索png文件的文件头89 50 4E

各类文件头文件尾总结： http://t.csdn.cn/A1jnj

![img](https://file.shenghuo2.top/typecho/202211161117015.png)

发现有两个，可以猜测这个图片里还有一张图片（不能确定的话，可以搜一下png的文件尾，看是不是两个）

点击第二个，会自动定位，然后从此处开始到最后复制下来

![img](https://file.shenghuo2.top/typecho/202211161117046.png)

新建一个文件（推荐新建十六进制文件，因题而异）

![img](https://file.shenghuo2.top/typecho/202211161117141.png)

将复制的内容粘贴到新建的文件里，保存（快捷键：**ctrl+c复制，ctrl+v粘贴,ctrl+s保存**）

![img](https://file.shenghuo2.top/typecho/202211161117127.png)

![img](https://file.shenghuo2.top/typecho/202211161117143.png)

### 图片隐写1

> 考点：LSB隐写

下载出来一张图片

根据图片名称联想到软件**Stegsolve（**具体使用方法百度**）**

![img](https://file.shenghuo2.top/typecho/202211161117873.png)

![img](https://file.shenghuo2.top/typecho/202211161117866.png)

一般来说，基础的考法是**LSB隐写**

![img](https://file.shenghuo2.top/typecho/202211161117993.png)

![img](https://file.shenghuo2.top/typecho/202211161117088.png)

### 图片隐写2

> 考点：LSB通道隐写

下载得到图片，用**Stegsolve**打开

![img](https://file.shenghuo2.top/typecho/202211161117512.png)

通过下面两个按钮，进行颜色通道变换

![img](https://file.shenghuo2.top/typecho/202211161117296.png)

### 就是不想告诉你

> 考点：盲水印

附件有两个图面，有一个**hint.jpg**先拖到010里查看一下，在最后发现了base64字符串

![img](https://file.shenghuo2.top/typecho/202211161117699.png)

解密一下

![img](https://file.shenghuo2.top/typecho/202211161117755.png)

提示尝试一下水印，用工具**WaterMarkH**来提取

下载链接：https://file.shenghuo2.top/file/WaterMarkH.exe

![img](https://file.shenghuo2.top/typecho/202211161117753.jpeg)





## 古典密码

### 古典密码入门指北

在pdf的最后

### 我爱你！Caesar

> 考点：凯撒密码

可以使用工具枚举

https://ctf.bugku.com/tool/caesar

注意有些工具会让大小写消失，导致不正确

![image-20221115215352668](https://file.shenghuo2.top/typecho/202211152153736.png)

### 听佛说宇宙的真谛

> 考点：佛曰解密

https://www.keyfc.net/bbs/tools/tudoucode.aspx

佛曰：开头为佛曰加密的特征

![image-20221115215745132](https://file.shenghuo2.top/typecho/202211152157187.png)

将要解密内容放在下面，然后点击参悟佛所言的真意即可



### 红星闪闪放光芒

> 考点：社会主义核心价值观编码

http://www.hiencode.com/cvencode.html

![image-20221115215936512](https://file.shenghuo2.top/typecho/202211152159628.png)

### 你知道ascii的全称是什么吗

> 考点：ASCII码转换

http://www.hiencode.com/jinzhi.html

![image-20221115220233499](https://file.shenghuo2.top/typecho/202211152202581.png)

### 你看我眼熟吗

> 考点：8进制的ASCII码转换

8进制特征，只由0-7 8个数字组成

> 观看此题是一堆代码，但是很多数超过了127，所以肯定不是十进制的ascii，再发现数字都是0到7，所以判断为八进制ascll码
>
> 先转换为十进制
>
> 81 76 78 85 123 69 118 51 95 115 51 101 110 95 97 78 95 111 99 116 97 108 125
>
> 再进行转换成ascii码



![](https://file.shenghuo2.top/typecho/202211152211255.png)

可以用python写一个进制转换的脚本

```python
a = "121 114 116 125 173 105 166 63 162 137 163 63 145 156 137 141 116 137 157 143 164 141 154 175"

for i in a.split(' '):
    print(chr(int(i,8)),end='')
```



### 7、0和1第一题

> 考点：摩斯编码

观察此题，发现只有0和1组成的编码，判断此编码有两种形式输出，因此暂时判断为摩斯电码

摩斯电码由-和.组成，所以把0和1换成-和.

[https://www.tooleyes.com/app/morse.html](https://www.tooleyes.com/app/morse.html?accessToken=eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2Njg0MzExMjcsImZpbGVHVUlEIjoiNXJrOWQwTERnN2NEV3dxeCIsImlhdCI6MTY2ODQzMDgyNywiaXNzIjoidXBsb2FkZXJfYWNjZXNzX3Jlc291cmNlIiwidXNlcklkIjo3NDExMTA4NX0.0Q7LgqEgilnjiY2rjnT029Qnot-SK_4NTlX3dZ34Ajg)在线解码网站

![image-20221115221330110](https://file.shenghuo2.top/typecho/202211152213196.png)

### **0和1第二题**

> 考点：培根密码

打开此题，发现还是由0和1组成的编码，经过摩斯电码尝试，发现错误，在搜索发现是培根密码也是由两个字符构成，为A和B，

然后经过转化，在网上在线解码培根密码工具发现解不出来密码，

再经过搜索发现是第二种方式，然后一个一个对照第二个表格找就可以了

![image-20221115221358573](https://file.shenghuo2.top/typecho/202211152213656.png)

### 歪比巴卜

> 考点：BubbleBabble

http://www.hiencode.com/bubble.html

网站解密即可

### 头脑风暴

> 考点：brainfuck

http://www.hiencode.com/brain.html

![image-20221115221737527](https://file.shenghuo2.top/typecho/202211152217629.png)



### 人美心善的学姐又来了

> 考点：标准银河字母

根据文件名 银河的英语 可以联想到标准银河字母

![image-20221115221925110](https://file.shenghuo2.top/typecho/202211152219193.png)

### 维多利亚的秘密

> 考点：未知密钥的维吉尼亚密码

发现此题类似于凯撒密码，但是枚举并没有得到想要的答案

所以推断为没有秘钥的维吉尼亚密码，然后去网上搜索解密网站

[https://www.guballa.de/vigenere-solver](https://www.guballa.de/vigenere-solver)，在线爆破解密（注意语言要选English哦）



### 是base但不仅仅是base

> 考点：由base64编码的加盐加密

Rabbit TripleDES DES AES四种是以U2开头，带密钥的对称加密

http://www.esjson.com/rabbitEncrypt.html

![image-20221115222513330](https://file.shenghuo2.top/typecho/202211152225417.png)



