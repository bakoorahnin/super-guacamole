利用模拟器安装好APP,然后进行BURP抓包分析

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFJnjLlY2ibcCbgib5SV32d1BwtvMQlvpyzAvwUlauTQsCUgD0qC0dicOdA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

通过各种手工分析,找到**某处SQL注入漏洞**.

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFpl2FFqIOS3eprHCEMnkqnhCVIBicSu4O69GSuVIEBeCgNZjJNIjgkJA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

之前信息收集的时候已经知道目标开放1433端口(爆破失败) 因此注入的时候,直接 `--dbms=mssql` 加快速度.

注入点类型:

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFuzjKDk0elIoD9w2pFSibYrcX0D6VnPibgYbPzZA8kC9H0M5NIkBOSv0g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

SA权限的注入点,原谅我菜,目前还没找到后台地址,数据库实在太特么乱了,虽然只有几个数据表,但是我不想一个一个的去翻,直接读sa密码解密失败,行吧,尝试下`--os-shell` 结果如上图,告诉我不支持,那我们改下类型,指定跑 `stack queries` 试试

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFLKibJBfpf8eia438wzEjbA25cAQlTSKL687mThxocTmT2iaQavWztibqjA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

成功跑出,并且没有降权,连提权都省了,我这RP![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCF311niaQBrkSfdibCbKCzunjAIOiae4eqzw28vrSiavCJVkCuKUtkVZYtlw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

接下来就是找绝对路径,然后写shell,拿到shell就方便多了,为什么不直接加用户上服务器呢?因为现在的服务器都是各种云警报,我还深刻的记得某天晚上凌晨4点上某服务器,结果管理员3分钟不到开机叫我衮蛋的事,所以呢,能不上服务器还是别上服务器的好.

已知服务器容器为:IIS7.5 08服务器

获取绝对路径方式: `type C:\Windows\System32\inetsrv\config\applicationHost.config`

不过由于注入点变成了延时的,所以速度超级超级慢,我这尿性忍不了,读文件读到一半放弃了.换了个思路

`dir/s/b d:\initial.aspx` 搜索网站的这个文件的路径,得到2个路径,目测不会用中文,所以猜测第一个是绝对路径,然后echo 123试试,发现正确,然后直接写一句话,成功getshell

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFssR9HA75K3KOvX9Rviau8TVDWu2zJZh7Ric8ibnUmgVH2LZvNqhv26Ozg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFW4nQ04LoakyJ3D5fZlECnakMu741ExPmIQCvwBlPtzwCtZVxeSDXbQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

马在根目录不好,上菜刀第一件事先换个隐蔽点的地方在说别的

然后在获得SA密码

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCF7Pr5MKuBAIaKmicSQhVb1WrwNibcohNOJUxassInNDeMnTjROkRibsVyQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

得到sa密码之后我只想说,我为什么会天真的想着去爆破? 用脑子想想也能猜到密码肯定是超级复杂的,我也是服了自己,浪费我流量.

然后继续之前的,读取配置文件,获得后台和代理后台地址:

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFqCUZwSoktkFQbcd3VqJI0Kehn2SOF1hfesCRCBdXGafTO7rxCl2ia2Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFl88E3WFENtNia7Z6aEZFzNxMq8icqP4QqrNjDoFaqiaaEv8ricBhdsORqg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFN3lr9zIuAJGFfherofkOguj5Gn50fOibJ2oqIW2ia9oBbJDWZibEPsS9Q/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

接下来通过数据库查到密码登陆进去瞧瞧涨什么鸟样

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFX4nYxMOlXIS7rgJ6qT15L5pIiaZkPsOAvkzZyXLyBK3k3sIbBExiahMQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

三万多用户,赌博有啥好玩的,为什么这么多人玩,这玩意真的能赢钱?

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFqmXA4Kga62cBib8WuZ8p2x6NscpYd9tKOW5ibZ7S3TkqX2bM7SFH55bA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

钱买排骨它不香吗?

全程下来,总结一下就是一个注入点引发的血案,太尼玛普通了,我也想来点曲折离奇的故事,但是RP不允许![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFSpYjFB73emcapc1qiamhIiamRtHSO2xzOAq6E5YCJ5qric1mmfHU73y1A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

本来想来波代码审计下的,结果发现看球不懂,菜是原罪

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCF38p1VJkYibhUk7iadXAgjdSpsjJlK7hg6EW4QNwGiaM8wvzlA1kmMwSRA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

另外头像处,总感觉有点问题,头像目录没有限制执行权限,然后这个APP是微信登陆抓取微信头像,并且登陆后还可以自定义上传头像,感觉这里有点问题,不过我模拟器还有手机上传抓包APP都卡蹦了,始终抓不到上传包,反编译想找上传接口尝试的,结果还是那句话,菜是原罪,看不懂....

![img](https://mmbiz.qpic.cn/mmbiz_png/Uq8Qfeuvou9e0NtLFgdeEPjj73BXnmCFZF0iaTS8rRiaOKoXKs8Dj3ich6mzicvNjOqSh8TVOf7NKTXHgp68FvPQLg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

本文至此告辞.