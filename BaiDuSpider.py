#-*_coding:utf8-*-
from bs4 import BeautifulSoup 
import requests
import re
import sys
import queue
import threading

hea={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
   'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
   'Connection' : 'keep-alive',
   'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'X-Forwarded-For':'120.239.169.74'}

class BaiduSpider(threading.Thread):
	"""docstring for BaiduSpider"""
	def __init__(self, q):
		threading.Thread.__init__(self)
		self.q = q
	def run(self):
		while not self.q.empty():
			url=self.q.get()
			try:
				self.spider(url)
			except Exception as e:
				print(e)
				pass

	def spider(self,url):
		r = requests.get(url=url,headers=hea).content
		soup = BeautifulSoup(r,'lxml')
		urls=soup.find_all(name='a',attrs={'data-click':re.compile('.'),'class':None})
		for url in urls:
			r_get_url = requests.get(url=url['href'],headers=hea,timeout=8)
			if r_get_url.status_code==200:
				print(r_get_url.url)
				with open('url.txt','a+') as f:
					f.write(r_get_url.url+'\n')
					f.close


def main(keyword):
	q=queue.Queue()
	for i in range(0,760,10):# #wd是控制的参数，每一页pn加10，最大页码为750
		q.put('https://www.baidu.com/s?wd=%s&pn=%s'%(keyword,str(i)))
	threads = []
	threads_count=20
	for t in range(threads_count):
		threads.append(BaiduSpider(q))
	for t in threads:
		t.start()
	for t in threads:
		t.join()


if __name__ == '__main__':
	print('''
*Made by  :tdcoming
*QQ Group :256998718
*For More :https://t.zsxq.com/Ai2rj6E
*MY Heart :https://t.zsxq.com/A2FQFMN




			  _______   _                         _               
			 |__   __| | |                       (_)              
			    | |  __| |  ___  ___   _ __ ___   _  _ __    __ _ 
			    | | / _` | / __|/ _ \ | '_ ` _ \ | || '_ \  / _` |
			    | || (_| || (__| (_) || | | | | || || | | || (_| |
			    |_| \__,_| \___|\___/ |_| |_| |_||_||_| |_| \__, |
			                                                 __/ |
			                                                |___/ 


		''')
	if len(sys.argv) !=2:
		print('>>>>>>>>>>>Enter：%s keword<<<<<<<<<<<<<<'%sys.argv[0])
		sys.exit(-1)
	else:
		main(sys.argv[1])



			







	













