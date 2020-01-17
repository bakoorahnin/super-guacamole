import requests
import json
import sys


def login():
	url_login='https://api.zoomeye.org/user/login'
	data={
	  "username": "你的账号",
	  "password": "你的密码"
	}
	data = json.dumps(data)  #把上面数据转换为json格式
	r=requests.post(url=url_login,data=data)  #获取到access_token
	
	return(json.loads(r.content)['access_token'])#取出access_token值
	

def main(keyword):
	url='https://api.zoomeye.org/host/search?query=%s'%(keyword)
	headers={'Authorization':'JWT '+login()}
	r=requests.get(url=url,headers=headers)
	datas=json.loads(r.content)['matches']#把json格式转换为普通格式
	# print(datas)
	for data in datas:
		print(data['portinfo']['service']+'://'+data['ip']+':'+str(data['portinfo']['port']))
		with open('ip.txt','a+',encoding='utf8') as f:
			f.write(data['portinfo']['service']+'://'+data['ip']+':'+str(data['portinfo']['port'])+'\n')


if __name__ =='__main__':
	print('''*Atuhor : tdcoming.
                                       
                                            
    ''')
	if len(sys.argv)!=2:
		print('enter:python %s keyword'%sys.argv[0])
		sys.exit(-1)
	else:
		main(sys.argv[1])
