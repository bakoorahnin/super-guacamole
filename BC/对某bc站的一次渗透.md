很多人问我你日站是用手工还是工具扫？我觉得两者同时进行效率会高些，所谓双管齐下，无站不破，当然还得看人品。

前段时间经常日有颜色的站，懂得都懂，emmm哈哈哈，但都是套路，跟bc又密不可分。

于是就按着套路顺利打开下面这个站：



[![image](https://forum.90sec.com/uploads/default/optimized/2X/6/6e1da6c585cd3097f8a1330adf3af429542ba6cf_2_638x500.jpeg)image1123×879 486 KB](https://forum.90sec.com/uploads/default/original/2X/6/6e1da6c585cd3097f8a1330adf3af429542ba6cf.jpeg)



刚好正是中午的时候，准备恰饭去，先将这个站丢到某W某S里面，如果有东西就直接捡现成的，于是：

(ps:不得不承认我长得帅！)



[![image](https://forum.90sec.com/uploads/default/original/2X/0/0230475b22d92b39f758af84d089987ebf6b9bba.png)image852×138 11.1 KB](https://forum.90sec.com/uploads/default/original/2X/0/0230475b22d92b39f758af84d089987ebf6b9bba.png)



懂的都懂



[![image](https://forum.90sec.com/uploads/default/original/2X/9/92828b2b9d654202cf0cfbff110a7057bd6a1966.png)image919×374 5.11 KB](https://forum.90sec.com/uploads/default/original/2X/9/92828b2b9d654202cf0cfbff110a7057bd6a1966.png)





[![image](https://forum.90sec.com/uploads/default/original/2X/3/30d1c57e9e91b1f3dd4638e37fee8c1384a2cbc2.png)image965×456 12.9 KB](https://forum.90sec.com/uploads/default/original/2X/3/30d1c57e9e91b1f3dd4638e37fee8c1384a2cbc2.png)



猜测估计是xp_cmdshell禁用或者删除

当前权限又是dba，而且支持堆叠可以执行update ，insert，等

于是就准备开启xp_cmdshell



[![image](https://forum.90sec.com/uploads/default/original/2X/8/8fbea8b1bb277b150855e03bd2332670d7b6547f.png)image927×228 6.44 KB](https://forum.90sec.com/uploads/default/original/2X/8/8fbea8b1bb277b150855e03bd2332670d7b6547f.png)





[![image](https://forum.90sec.com/uploads/default/original/2X/b/b7ba3d6516a6738889f9dbdcd2367b3a1761a599.png)image945×302 8.01 KB](https://forum.90sec.com/uploads/default/original/2X/b/b7ba3d6516a6738889f9dbdcd2367b3a1761a599.png)



再次osshell看xp_cmdshell是否开启成功。然儿….



[![image](https://forum.90sec.com/uploads/default/original/2X/1/186cf6ff080f83ce4cdc829f22808c9483450767.png)image1323×618 24 KB](https://forum.90sec.com/uploads/default/original/2X/1/186cf6ff080f83ce4cdc829f22808c9483450767.png)



不甘心，于是来到burp，如果xp_cmdshell启用返回时间应该是>=5,然儿只有1秒多钟，

证明没有开启成功。



[![image](https://forum.90sec.com/uploads/default/optimized/2X/a/a503030e97bd49846fd2f6eb35b140dbb0a14ca6_2_690x441.png)image1261×806 49.2 KB](https://forum.90sec.com/uploads/default/original/2X/a/a503030e97bd49846fd2f6eb35b140dbb0a14ca6.png)



于是，利用burp再次开启xp_cmdshell,然儿好像还是不得行



[![image](https://forum.90sec.com/uploads/default/optimized/2X/8/8b23886ab9e6c29e3ea79a6d98999d13f42d2f12_2_690x308.png)image1072×479 43.6 KB](https://forum.90sec.com/uploads/default/original/2X/8/8b23886ab9e6c29e3ea79a6d98999d13f42d2f12.png)





[![image](https://forum.90sec.com/uploads/default/optimized/2X/c/c372ca4b57b9eed484dd7f0431fdc2619a891927_2_690x444.png)image1259×811 48.9 KB](https://forum.90sec.com/uploads/default/original/2X/c/c372ca4b57b9eed484dd7f0431fdc2619a891927.png)



Xp_cmdshell哪里=0呢看看语句是不是有毛病

看返回时间是没毛病的，在这里就纳闷了….



[![image](https://forum.90sec.com/uploads/default/optimized/2X/0/0c2b41aff5de2445d59a34f699463d9354444473_2_690x296.png)image1267×544 46.5 KB](https://forum.90sec.com/uploads/default/original/2X/0/0c2b41aff5de2445d59a34f699463d9354444473.png)



在此期间尝试了很多 ，包括沙箱等等burp跟sqlmap都尝试过，

参考文章：[https://blog.csdn.net/sircoding/article/details/78681016 28](https://blog.csdn.net/sircoding/article/details/78681016)

后面还考虑过了站库分离的情况，burp构造发包，发现不是。

想到写shell

必须满足：

1.网站绝对路径

2.目录写权限

3.数据库是Dba

但没有站点绝对路径，那岂不是要凉凉。



[![image](https://forum.90sec.com/uploads/default/optimized/2X/d/dcadb5a0899de19ad7ba5260b9e995b5066e925a_2_690x297.png)image1252×539 44 KB](https://forum.90sec.com/uploads/default/original/2X/d/dcadb5a0899de19ad7ba5260b9e995b5066e925a.png)



鼓捣了好一会儿，找到该站点真实ip，从旁站入手了，万一·····，一般bc旁站一般也是bc

只能抱着试一试心态去，果不其然，也是bc，但感觉模板是一样的，同样的注入点，再次用sqlmap来梭哈，奇迹出现了哇哈哈哈：（ps：之前的注入点也尝试过union，没幼结果）：



[![image](https://forum.90sec.com/uploads/default/original/2X/2/272b4ac416eb189d1bfbde0881fbe0991df48496.png)image968×427 9.32 KB](https://forum.90sec.com/uploads/default/original/2X/2/272b4ac416eb189d1bfbde0881fbe0991df48496.png)





[![image](https://forum.90sec.com/uploads/default/original/2X/c/c3033fe26849cb574699ef9954fc001b591aa51f.png)image993×487 13 KB](https://forum.90sec.com/uploads/default/original/2X/c/c3033fe26849cb574699ef9954fc001b591aa51f.png)



终于能执行命令了



[![image](https://forum.90sec.com/uploads/default/original/2X/e/e4f59ccb9c9a0d2be30769716ff0d7836b63cc35.png)image971×338 9.37 KB](https://forum.90sec.com/uploads/default/original/2X/e/e4f59ccb9c9a0d2be30769716ff0d7836b63cc35.png)



接下来就是cs上线，提权，不是特殊目标，不上桌面的黑客不是好黑客



[![image](https://forum.90sec.com/uploads/default/original/2X/5/53648eb18430f460bcd79614652b05a31436997a.png)image793×840 31.3 KB](https://forum.90sec.com/uploads/default/original/2X/5/53648eb18430f460bcd79614652b05a31436997a.png)



Sqlserver被降权，利用ms16-032提权，或者其他权限提升机器未安装的补丁进行提权

System



[![image](https://forum.90sec.com/uploads/default/optimized/2X/e/e5bb5d0e7dd3de8e8248e080fc64100ff646d22d_2_690x425.png)image1277×787 202 KB](https://forum.90sec.com/uploads/default/original/2X/e/e5bb5d0e7dd3de8e8248e080fc64100ff646d22d.png)



利用mimikatz dump账号密码



[![image](https://forum.90sec.com/uploads/default/original/2X/7/71819c84bd738e99bd5bc5d63f624b27affa6b50.png)image1055×672 24.2 KB](https://forum.90sec.com/uploads/default/original/2X/7/71819c84bd738e99bd5bc5d63f624b27affa6b50.png)



没有明文，可以利用mimikatz传递ntml，感觉不得行，成功率低。

命令：

```
Copy to clipboardsekurlsa::pth /user:Administrator /domain:WORKGROUP /ntlm:206ca710d5b82f1c988b301808d1016e/run:powershell.exe
```



[![image](https://forum.90sec.com/uploads/default/original/2X/4/421999935db9f8fd4704b61f260ffbe548e3e66c.png)image968×340 8.15 KB](https://forum.90sec.com/uploads/default/original/2X/4/421999935db9f8fd4704b61f260ffbe548e3e66c.png)



然而好像不得行，算了直接加帐号吧



[![image](https://forum.90sec.com/uploads/default/optimized/2X/6/61a0fd1e6ea3ee55d2c8aa1af24bfb600192f1de_2_690x313.png)image1117×508 19.9 KB](https://forum.90sec.com/uploads/default/original/2X/6/61a0fd1e6ea3ee55d2c8aa1af24bfb600192f1de.png)



登录远程终端

看了浏览器的历史记录



[![image](https://forum.90sec.com/uploads/default/optimized/2X/5/58444b4a1b0deffe8517423a069eb89000a8653f_2_690x431.png)image1411×882 82.7 KB](https://forum.90sec.com/uploads/default/original/2X/5/58444b4a1b0deffe8517423a069eb89000a8653f.png)



顺其自然的登录后台：

开始以为这个后台是另外一台服务器，结果看了iis还有域名解析才发现是当前机器。。。有点小失望emmm



[![image](https://forum.90sec.com/uploads/default/optimized/2X/9/933fc7de7fedb6d7e0e62d7534c547a4d9e27e03_2_690x337.png)image1920×938 144 KB](https://forum.90sec.com/uploads/default/original/2X/9/933fc7de7fedb6d7e0e62d7534c547a4d9e27e03.png)





[![image](https://forum.90sec.com/uploads/default/optimized/2X/a/ae101e2cc720559c78f8231d16f364af66d481eb_2_690x288.png)image1920×804 114 KB](https://forum.90sec.com/uploads/default/original/2X/a/ae101e2cc720559c78f8231d16f364af66d481eb.png)





[![image](https://forum.90sec.com/uploads/default/optimized/2X/3/3815cb45df194ac36f7896c77bfeb20463c453dd_2_690x359.png)](https://forum.90sec.com/uploads/default/original/2X/3/3815cb45df194ac36f7896c77bfeb20463c453dd.png)