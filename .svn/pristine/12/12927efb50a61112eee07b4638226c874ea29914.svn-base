# -*- coding: utf-8 -*-


#########   本脚本用于获得各种服务器脚本映射到页面的信息


import socket
import os,sys

if sys.version_info.major==2:
	import httplib    #python2
if sys.version_info.major==3:
	import http.client    #python3.5

import time
import math

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from PIL import Image

import platform

if platform.system()=="Linux":   ## windows 支持较为复杂，需要 mingw 编译，可以略过 
	import zbarlight   # pip install zbarlight , yum install zbar-devel  win: https://gist.github.com/Zephor5/aea563808d80f488310869b69661f330

#import qrcode ## pip install PyQRCode  这个是识别
#import zbar   ## pacman -S zabr , pip install zbar.   python3 支持不好

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好
from reportit import *   ## 用于报告

################################################

#  获得 cookie
def getcookie(server,username,password):

	port=901

	if sys.version_info.major==2:
		conn = httplib.HTTPConnection(server + ":" + str(port))    #python2
	if sys.version_info.major==3:
		conn = http.client.HTTPConnection(server + ":" + str(port))    #python3

	conn.request("GET", "/"+username+"?"+ password)


	if sys.version_info.major==3:
		try:
			readdata = conn.getresponse()
		except http.client.HTTPException as e:         #python3                      
			cookies=str(e)                 
		else:
			cookies = readdata.read()

	if sys.version_info.major==2:
		try:
			readdata = conn.getresponse()
		except:	 #python2
			cookies=u"获取短信信息失败"         
		else:
			cookies = readdata.read()

	
	cookies=cookies.strip('\n')     ### cookies 
	cookies=cookies.strip('\r')  

	return(cookies)


	#一个登陆测试  直接使用 cookie

	"""
	browser.get(Url)
	cookie=getcookie(server,username,password)
	cookie=cookie.replace("ccat=","")
	#print(cookie)
	browser.add_cookie({'name':'ccat', 'value':cookie})   
	browser.get(Url)

	"""



################################################

def getmsg(server,Phone):   ### 临时使用

	return("123456")

#  获得短信信息  激发即产生日志(仍需要时间)
def getmsg_OK(server,Phone):

	time.sleep(2)   #给予时间

	port=1900

	###  获得 短信  

	if sys.version_info.major==2:
		conn = httplib.HTTPConnection(server + ":" + str(port))    #python2
	if sys.version_info.major==3:
		conn = http.client.HTTPConnection(server + ":" + str(port))    #python3

	conn.request("GET", "/"+Phone)   


	if sys.version_info.major==3:
		try:
			readdata = conn.getresponse()
		except Exception as e:  	   #python3
			msgdata=str(e)               
		else:
			msgdata = readdata.read()

	if sys.version_info.major==2:
		try:
			readdata = conn.getresponse()
		except:    #python2
			msgdata=u"获取短信信息失败"            
		else:
			msgdata = readdata.read()

	
	msgdata=msgdata.strip('\n')     ### 短信 
	msgdata=msgdata.strip('\r') 


	## 没有从数据中得到
	if msgdata=="Remote end closed connection without response":
		#  动作名称/目的, 前置条件, 预期, 实际结果, 判定
		#logs("短信验证码",  "",  "" ,   "无法收到短信验证码"  ,0)
		msgdata=u"无法收到短信验证码, 重新尝试获取"
		print(msgdata)
		#return(msgdata)
		#再次重试
		getmsg(server,Phone)

	## 非数字
	if msgdata.isdigit()==False:
		#  动作名称/目的, 前置条件, 预期, 实际结果, 判定
		logs(u"短信验证码",  "",  "" ,   msgdata   ,0)

	return(msgdata)


#  第一个版本的获得短信信息接收函数   如发送成功则会产生日志    已经废弃
# 某些发送有问题的情况不会触发, 应对所有类型的短信验证码处理情况比较多, 而且由于不验证手机, 有可能在频繁的情况下会出问题
def getmsgold(server):

	time.sleep(2)   #给予时间

	port=900

	###  获得 短信  
	mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	mysocket.connect((server,port))
	while 1:
		data=mysocket.recv(1024)
		if data:
			msgdata=data
			msgdata=msgdata.decode('utf-8').strip('\n') #### 
			msgdata=msgdata.strip('\r') #### 
			mysocket.close()
			break

	return(msgdata)



################################################

def getpicid(server, port):   ## 临时使用

	if port!=950:
		return("test")
	else:
		return getpicid_OK(server, port)

#  获得 前台和后台图片验证码
def getpicid_OK(server, port):

	#  注意本地环路包用  tcpdump -i  lo , 参考对应脚本

	time.sleep(1)   #给予时间

	mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	mysocket.connect((server,port))
	while 1:
		data=mysocket.recv(1024)
		if data:
			msgdata=data    
			msgdata=msgdata.decode('utf-8').strip('\n')   
			msgdata=msgdata.strip('\r')   
			mysocket.close()
			break

	return(msgdata)


################################################

## 识别二维码

#来自文件
def barstr(filename):

	file_path = filename

	with open(file_path, 'rb') as image_file:
		image = Image.open(image_file)
		image.load()

	codes = zbarlight.scan_codes('qrcode', image)
	return codes[0].decode('utf-8')

#来自xpath
def barstrfromxpath(browser,xpathstr):

	savepath="./temp.png"

	codes=None
	while codes==None:

		waittime=15
		try:
			WebDriverWait(browser, waittime).until(lambda the_driver: the_driver.find_element_by_xpath(xpathstr))    
		except TimeoutException:
			timeoutlog(browser,xpath, waittime)

		imgelement = browser.find_element_by_xpath(xpathstr)  
		location = imgelement.location
		size = imgelement.size
		browser.save_screenshot(savepath)
		time.sleep(0.5)   ### 图像没有显示出来之前 失败率较高

		im = Image.open(savepath)
		left = location['x']
		top = location['y']
		right = left + size['width']
		bottom = location['y'] + size['height']
		im = im.crop((left,top,right,bottom))

		codes = zbarlight.scan_codes('qrcode', im)
		if codes!=None:
			break
		print("二维码识别失败,再次尝试")

	return codes[0].decode('utf-8')


################################################  测试


if __name__ == '__main__':  

	server="10.17.5.151"
	port=911
	Phone="13718104161"

	#print(getmsg(server,Phone))
	#print(getpicid(server,port))
	#print(getcookie(server,"xu_lei000303","xulei777"))    

	filename="./catchme.png"
	barstrs=barstr(filename)
	print(barstrs)







