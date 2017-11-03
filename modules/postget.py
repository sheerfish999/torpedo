# -*- coding: utf-8 -*-

####################  本文件用于进行基本的 http 操作


import sys
import traceback
import ssl

import datetime
import string

import platform
sysstr = platform.system()   ### 判断操作系统类型   Windows   Linux    .   本脚本函数入口, 统一以 LINUX 为准, 其后在函数内进行转换


if sysstr == "Linux":
	import hues   ## pip install hues

if sysstr == "Windows":
	import winhues as hues


### httplib 受 python2 3 版本影响教大 ,  因此未使用

if sys.version_info.major==2:   #python2
	import urllib2    
	import cookielib
	
if sys.version_info.major==3:   #python3
	from urllib import request as urllib2  
	import http.cookiejar as cookielib           # pip3 install request


###  xml   json
from dodata import * 



cookie=cookielib.CookieJar()



################################  POST 方法  ,     data 为空时  GET

def posts(urls,data="",cookieadd="",timeouts=0,header=[]):          #   目前支持 xml   json  urlencode  

	if sys.version_info.major==2:   ## 3 默认 utf-8
		reload(sys)
		sys.setdefaultencoding('utf-8')


	### 中文处理
	urls=cn2url(urls)


	##########  请求类型

	if data !="":

		binary_data = data.encode('utf-8')
		req = urllib2.Request(urls, binary_data)

		req.get_method = lambda: 'POST'

		## 判断类型
		types=whichtypes(data)

		if types=="xml":
			req.add_header('Content-type', 'application/xml; charset=UTF-8')

		if types=="json":
			req.add_header('Content-type', 'application/json; charset=UTF-8')

		if types=="urlcode":
			req.add_header('Content-type', 'application/x-www-form-urlencoded; charset=UTF-8')
		

	else:
		req = urllib2.Request(urls) 
		req.get_method = lambda: 'GET'


	####### 请求的 cookie

	global cookie 
	handler=urllib2.HTTPCookieProcessor(cookie)
	opener=urllib2.build_opener(handler)    

	if cookieadd!="":
		#print(cookieadd)   ### 查看是否接收到 cookie 插入请求
		opener.addheaders.append(('Cookie', cookieadd))

	#######  http 头

	for i in range(len(header)): 
		#print(header[i][0])
		#print(header[i][1])
		opener.addheaders.append((header[i][0], header[i][1]))


	########### 进行请求

	try:
		#response = urllib2.urlopen(req)   ### 为支持 cookie, 不再使用此种简易方式
		
		timestart = datetime.datetime.now()

		ssl._create_default_https_context = ssl._create_unverified_context ## SSL

		if timeouts>0:
			urlopen = opener.open(req,timeout=timeouts)
		else:
			urlopen = opener.open(req)

		timeend = datetime.datetime.now()
		rettime=str(round((timeend-timestart).total_seconds(),2))

		hues.info(u"接口返回时间: "+rettime + " s")

	except:
		hues.info(u"URL地址请求失败或超时, 具体原因:")
		traceback.print_exc() 

		return None   ### 返回None 触发后续异常输出


	the_page = str(urlopen.read().decode('utf8'))

	return the_page


### 从文件 POST

def postsfile(urls,files,cookieadd="",timeouts=0,header=[]):

	data=open(files).read()  

	### 从文件内容进行判断
	"""
	if files[len(files)-4:]==".xml":
		types="xml"

	if files[len(files)-5:]==".json":
		types="json"
	"""

	returns=posts(urls,data,cookieadd,timeouts,header)

	return returns



### 返回URL 结构

def urlheader(url):      # prase 兼容 2.7 和 3 比较差
	
	url=url.replace("\\","/")

	headerpos="://"
	if url.find(headerpos)>=0:
		pos=url.find(headerpos)+3
	else:
		pos=0


	## 协议头
	header=url[:pos]

	## 地址
	temp=url[pos:]
	pos=temp.find("/")

	addr=temp[:pos]
 
	## body
	body=temp[pos:]

	#域名IP或端口
	pos=addr.find(":")
	if pos>=0:
		ipaddr=addr[:pos]
		port=int(addr[pos+1:])
	else:
		ipaddr=addr
		port=80

	######

	return header,addr,ipaddr,port,body



### 中文字符转url编码 

def cn2url(strs):

	strs=urllib2.quote(strs, safe=string.printable)
	
	return(strs)






