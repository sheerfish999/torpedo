# -*- coding: utf-8 -*-

import os,sys
import base64
import json

from frame import *
from postget import *
from dodata import *


if sys.version_info.major==2:   #python2
	import urllib2    
	import cookielib
	
if sys.version_info.major==3:   #python3
	from urllib import request as urllib2  
	import http.cookiejar as cookielib           # pip3 install request


##### 载入配置变量


try:
	config=openfiles("../config.py")
	exec(config)
except:
	# 通过百度云创建OCR应用获得 (免费日500)  临时使用
	ocr_client_id="3567is0MyuhRQeUP0QdYgMZt"
	ocr_client_secret="scbzdg9mMsZLEaL7nd8s2DxItD50OKLH"	


########## 获得 token

def gettoken():

	url="https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+ocr_client_id +"&client_secret="+ocr_client_secret

	ret=posts(url)

	#print(ret)

	token=readjson(ret,"@access_token")
	
	#print(token)

	return token

############# 从图片文件OCR成 文本 list

def getocr(filename):

	token=gettoken()

	###################
	
	url="https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=" + token

	f = open(filename, 'rb')

	# 参数image：图像base64编码
	img = base64.b64encode(f.read())
	f.close()

	params = {"image": img}

	import urllib
	if sys.version_info.major==2:   #python2
		params = urllib.urlencode(params)
	if sys.version_info.major==3:   #python3
		params = urllib.parse.urlencode(params)


	header=[]
	header.append(['Content-Type', 'application/x-www-form-urlencoded'])

	content=posts(url,data=params,header=header)

	#print(content)


	hjson = json.loads(content)
	count=hjson["words_result_num"]  #获得识别的数量
	
	# 获得所有识别的内容
	textlist=[]
	for i in range(0,count):

		width=hjson["words_result"][i]["location"]["width"]
		height=hjson["words_result"][i]["location"]["height"]
		left=hjson["words_result"][i]["location"]["left"]
		top=hjson["words_result"][i]["location"]["top"]
		text=hjson["words_result"][i]["words"]

		#print(text,top,left,height,width)

		textlist.append([text,top,left,height,width])

	return textlist


############################################## 测试

if __name__ == "__main__":

	filename=(os.getcwd() + r"/test/getimg2.png")

	textlist=getocr(filename)

	print(textlist)

	for i in range(0,len(textlist)):
		print(textlist[i][0])









