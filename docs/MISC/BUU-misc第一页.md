!!! 提示
    本文用于buu的misc分类第一页解题思路参考




## 大白

> 看不到图？ 是不是屏幕太小了 
>
> 注意：得到的 flag 请包上 flag{} 提交

提示改图片分辨率

用010把分辨率改成512 画图强行打开

![image-20220411210721872](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112107927.png)

flag{He1l0_d4_ba1}

## 乌镇峰会种图

010打开 flag在文件尾

![image-20220411210925584](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112109629.png)

flag{97314e7864a8f62627b26f3f998c37f1}

## 文件中的秘密

​	

![image-20220411213107396](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112131543.png)

在文件信息里

flag{870c5a72806115cb5439345d8b014396}

## wireshark

> 黑客通过wireshark抓到管理员登陆网站的一段流量包（管理员的密码即是答案) 
>
> 注意：得到的 flag 请包上 flag{} 提交

直接搜字符串flag

![image-20220411213338822](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112133919.png)

flag{ffb7567a1d4f4abdffdb54e022f8facd}

## LSB

stegslove查看LSB RGB三个的0层是PNG头

![image-20220411213951804](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112139856.png)

保存为flag.png

![image-20220411214016108](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112140133.png)

是一个二维码 扫码得到flag

cumtctf{1sb_i4_s0_Ea4y}

包上flag{1sb_i4_s0_Ea4y}

## rar

> 这个是一个rar文件，里面好像隐藏着什么秘密，但是压缩包被加密了，毫无保留的告诉你，rar的密码是4位纯数字。 
>
> 注意：得到的 flag 请包上 flag{} 提交

用ARCHPR爆破

![image-20220411214408241](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112144283.png)

![image-20220411214415787](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112144824.png)

flag{1773c5da790bd3caff38e3decd180eb7}

## zip伪加密

![image-20220411215759556](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112157597.png)

两个全局标记位全是09 00 还以为是我记错了

都改成00就能解压了

![image-20220411215907890](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204112159920.png)

flag{Adm1N-B2G-kU-SZIP}

## qr

一个签到题，扫二维码就有flag

 Flag{878865ce73370a4ce607d21ca01b5e59}

## 被嗅探的流量

> 某黑客潜入到某公司内网通过嗅探抓取了一段文件传输的数据，该数据也被该公司截获，你能帮该公司分析他抓取的到底是什么文件的数据吗？ 
>
> 注意：得到的 flag 请包上 flag{} 提交

wireshark打开 跟踪tcp流

能看到传输过一个flag.jpg

flag在图片尾![](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121312911.png)

## 镜子里面的世界

文件名是steg 用zsteg跑一下

![image-20220412131907224](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121319263.png)

得到flag{st3g0_saurus_wr3cks}

## ningen

> 人类的科学日益发展，对自然的研究依然无法满足，传闻日本科学家秋明重组了基因序列，造出了名为ningen的超自然生物。某天特工小明偶然截获了日本与俄罗斯的秘密通信，文件就是一张ningen的特写，小明通过社工，知道了秋明特别讨厌中国的六位银行密码，喜欢四位数。你能找出黑暗科学家秋明的秘密么？ 
>
> 注意：得到的 flag 请包上 flag{} 提交

用binwalk解出来一个压缩包 带密码

四位数字密码爆破

![image-20220412132305714](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121323741.png)

解压得到flag

## 小明的保险箱

> 小明有一个保险箱，里面珍藏了小明的日记本，他记录了什么秘密呢？。。。告诉你，其实保险箱的密码四位纯数字密码。（答案格式：flag｛答案｝，只需提交答案） 
>
> 注意：得到的 flag 请包上 flag{} 提交

binwalk跑出来一个rar

四位数字爆破

![image-20220412132611110](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121326134.png)

得到flag

## 爱因斯坦

一个jpg

用binwalk跑出来一个带密码的zip

![](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121331500.png)

没有密码提示

用exiftools看一下信息

![image-20220412133231762](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121332807.png)

得到密码

解压得flag

## easycap



直接追踪tcp流就能得到flag

![image-20220412133458263](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121334289.png)

## 隐藏的钥匙

> 路飞一行人千辛万苦来到了伟大航道的终点，找到了传说中的One piece，但是需要钥匙才能打开One Piece大门，钥匙就隐藏在下面的图片中，聪明的你能帮路飞拿到钥匙，打开One Piece的大门吗？ 
>
> 注意：得到的 flag 请包上 flag{} 提交

直接010打开 搜flag

![image-20220412135623898](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121356925.png)

base64解密

## 另外一个世界

010查看文件尾

![image-20220412140445879](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121404907.png)

有一串二进制数 是8的倍数

8位一组转ASCII码

`koekj3s`

flag{koekj3s}

## FLAG

png stegslove查看rgb第0层数据

![image-20220412144615802](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121446844.png)

PK头  保存为zip

解压得到一个ELF文件

运行得flag

![image-20220412144724831](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121447858.png)

> 注意：请将 hctf 替换为 flag 提交，格式 flag{}

## 假如给我三天光明

两个文件 一个图片一个压缩包 压缩包带密码

![pic](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204101456360.jpg)

盲文解密 `kmdonowg`  是压缩包密码



![image-20220410150825905](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204101508949.png)

morse

```
-.-./-/..-./.--/.--././../-----/---../--.../...--/..---/..--../..---/...--/-../--../
```

解出来是ctfwpei08732?23dz

套上flag{} 删ctf

flag{wpei08732?23dz}

## 神秘龙卷风

> 神秘龙卷风转转转，科学家用四位数字为它命名，但是发现解密后居然是一串外星人代码！！好可怕！ 
>
> 注意：得到的 flag 请包上 flag{} 提交

一个rar 4位数字爆破

![image-20220412151059308](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121510338.png)

![image-20220412151210560](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121512610.png)

brainfuck解密

`flag{e4bbef8bdf9743f8bf5b727a9f6332a8}`

## 后门查杀

> 小白的网站被小黑攻击了，并且上传了Webshell，你能帮小白找到这个后门么？(Webshell中的密码(md5)即为答案)。 
>
> 注意：得到的 flag 请包上 flag{} 提交

新思路 卷宝提供的

直接拖进火绒扫描

![image-20220412151707541](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121517580.png)

![image-20220412151714363](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121517388.png)

## 数据包中的线索

> 公安机关近期截获到某网络犯罪团伙在线交流的数据包，但无法分析出具体的交流内容，聪明的你能帮公安机关找到线索吗？ 
>
> 注意：得到的 flag 请包上 flag{} 提交

跟踪TCP流  第7个

![image-20220412153035383](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121530460.png)

再跟踪http流

把数据base64解密后再存为图片

![image-20220412153335033](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121533160.png)

flag{209acebf6324a09671abc31c869de72c}

## 荷兰宽带数据泄露

conf.bin

用RouterPassView打开

搜索username

就是flag{053700357621}

## 来首歌吧

一个mp3

看声道 morse电码

...../-.../-.-./----./..---/...../-..../....-/----./-.-./-.../-----/.----/---../---../..-./...../..---/./-..../.----/--.../-../--.../-----/----./..---/----./.----/----./.----/-.-./

5bc925649cb0188f52e617d70929191c

换成大写

解出来flag{5BC925649CB0188F52E617D70929191C}

## webshell后门

火绒扫一下

![image-20220412163653424](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121636477.png)

搜pass

![image-20220412163704238](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121637269.png)

flag{ba8e6c6f35a53933b871480bb9a9545c}

## 面具下的flag

一个jpg

用binwalk分离出来flag.vmdk

用7z解压出来 

```
7z x flag.vmdk
```

![image-20220412165634950](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121656997.png)

flag分为两部分

第一部分是brainfuck

flag{N7F5_AD5

第二部分是ook!

_i5_funny!}

合起来flag{N7F5_AD5_i5_funny!}

## 九连环

binwalk 分离出来一个jpg和一个带密码的zip

密码应该在图片里  试了一圈是steghide

![image-20220412171212908](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121712938.png)

分类出一个txt 里面是压缩包密码

flag{1RTo8w@&4nK@z*XL}

## 被劫持的神秘礼物

> 某天小明收到了一件很特别的礼物，有奇怪的后缀，奇怪的名字和格式。小明找到了知心姐姐度娘，度娘好像知道这是啥，但是度娘也不知道里面是啥。。。你帮帮小明？找到帐号密码，串在一起，用32位小写MD5哈希一下得到的就是答案。 链接: https://pan.baidu.com/s/1pwVVpA5_WWY8Og6dhCcWRw 提取码: 31vk 
>
> 注意：得到的 flag 请包上 flag{} 提交

流量包 查看tcp流

一眼flag

![image-20220412192650059](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121926150.png)

adminaadminb

用md5转一下 加上flag{

flag{1d240aafe21a86afc11f38a45b541a49}



## 刷新过的图片

> 浏览图片的时候刷新键有没有用呢 
>
> 注意：得到的 flag 请包上 flag{} 提交

刷新提示就是F5隐写

用F5-steganography解出来 

![image-20220412193420967](https://jingneifile.oss-cn-qingdao.aliyuncs.com/typecho/202204121934043.png)

是一个pk头 改成zip解压

有伪加密 binwalk跑出来flag.txt

flag{96efd0a2037d06f34199e921079778ee}
