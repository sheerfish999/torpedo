# -*- coding: utf-8 -*-

import sys,os
import codecs

import glob
import time
import datetime

import traceback

import keyboard # pip install keyboard  同时支持 windows linux

if sys.version_info.major==2:   #python2
	import HTMLParser  #pip install HTMLParser

if sys.version_info.major==3:   #python3
	from html import parser as HTMLParser


########################  本脚本用于载入变量设置和业务用例 等通用操作


######  载入文本内容

def openfiles(filename):


	#paths=os.getcwd()    #绝对路径  , os.getcwd()  代替  sys.path[0]
	paths=os.path.split(os.path.realpath(__file__))[0]   # 这个才是脚本的实际路径
	
	all_the_text = codecs.open(paths + "/"+ filename,'r','utf-8').read( )

	if sys.version_info.major==2: 
		all_the_text=all_the_text.encode('utf8','ignore')    ### windows 下编写的用例可能需要转码

	return(all_the_text)

#####  存储文本内容，用于快速调试

def savefiles(filename,text):

	paths=os.getcwd()    #绝对路径  , os.getcwd()  代替  sys.path[0]
	filename=paths + "\\" + filename

	f=open(filename,"w")
	f.write(text)
	f.close()


######  获得驱动类型

def  drivertype():

	drivertypef= open("./drivertype", "r")   
	drivertypes = drivertypef.readline()
	drivertypes=drivertypes.strip('\n')
	drivertypef.close()

	return(float(drivertypes))


######  获得是否进行报告的标记

def get_reports_tag():

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reports=reports.strip(' ')

	reports=int(reports)

	reportf.close()

	return reports


######  获得是否进行录像的标记

def get_records_tag():

	recordf = open("./recordset", "r")
	records = recordf.readline()
	records=records.strip('\n')
	records=records.strip(' ')

	records=int(records)

	recordf.close()

	return records


######  获得环境变量 (一般 jenkins 使用)

def getenvs(string):

	try:
		envs=os.environ[string]   
		return envs
	except:
		return ""	   


#####  删除某个路径下通配符匹配的文件

# delete_files('./1/', '*.txt')

def files(curr_dir, ext ):

    for i in glob.glob(os.path.join(curr_dir, ext)):
        yield i

def delete_files(curr_dir, ext):

	for i in files(curr_dir, ext):
		os.remove(i)



############################### 临时断点当前代码，用于远程调试

## 来自网络调试线程函数，利用公共标记位进行处理

debug_thread_tag=""      # 网络调试进程获得内部消息的标记位，供各个函数临时处理

def pause():

	global debug_thread_tag

	while True:

		if debug_thread_tag=="unpause":
			break

		time.sleep(2)  # 否则会占用大量的cpu时间（同局锁）


	debug_thread_tag=""
	

def unpause():

	global debug_thread_tag

	debug_thread_tag="unpause"



###########  

#  重写输出缓冲的类，用于给调试端返回信息
class TextArea(object):

	lastbuffer = ""

	def __init__(self):  
		self.buffer = "" 

	def write(self, *args, **kwargs):

		self.buffer=args
		self.lastbuffer=self.buffer

		text_area, sys.stdout = sys.stdout, stdout    ## 释放
		print(self.buffer[0], end='')
		connection.send(bytes(self.buffer[0], encoding = "utf8"))  	 ### 正常情况远程提供输出 
		sys.stdout = self			## 收集

	def flush(self):
		pass


def remote_cmd(socks,browser):

	while True:

		global connection   ### 连接提供给其他方法，以供对调试客户端输出信息使用
		connection,address = socks.accept()

		try:
			data=""
			data=connection.recv(1024)
		except:
			traceback.print_exc()

		if data:

			msgdata=data
			msgdata=msgdata.decode('utf-8').strip('\n')   
			msgdata=msgdata.strip('\r')

			#print(msgdata)

			global stdout    ### 输出进行缓冲控制，以便两端均能获得输出信息
			stdout = sys.stdout  
			sys.stdout = TextArea()    ## 收集缓冲

			try:
				exec(msgdata)
			except:
				text_area, sys.stdout = sys.stdout, stdout    ## 停止收集缓冲
				traceback.print_exc()

				backlog=traceback.format_exc()
				try:
					connection.send(bytes(backlog, encoding = "utf8"))         ### 远程提供异常信息
				except:
					pass


			text_area, sys.stdout = sys.stdout, stdout    ## 停止收集缓冲

			connection.close()


##########################  debug  显示元素定位等信息


def debug(browser):

	global path_list
	global tagstack

	path_list=[]
	tagstack = []

	# 得到 xpath
	xpath_list=getall_xpath(browser.page_source)

	# 有效 xpath
	xpath_list=available_xpath(browser,xpath_list)
	

	#这里用作进一步处理
	
	text=""
	for i in range(len(xpath_list)):
		text=text+ xpath_list[i][0] + " " +  str(xpath_list[i][1]['y'])  + " " + str(xpath_list[i][1]['x']) + " " + str(xpath_list[i][2]['height']) + " " +  str(xpath_list[i][2]['width']) +"\n"

	filename="./debug.log"
	savefiles(filename,text) 
	
	#print(text)      ## 由于采用debug模式缓冲区大小原因，输出不完整 建议文件调试 


	mouse_js(browser) # 注入脚本
	print("Use Ctrl to get Xpath in current page, Shift to release, then debug(browser) to refresh Xpath list in current page step.")

	keyboard.add_hotkey('ctrl', getpos_event, args=(browser,xpath_list))
	keyboard.add_hotkey('shift', rel_getpos_event, args=())


### 遍历 xpath ， 但没有 序号信息，需要再处理

class ShowStructure(HTMLParser.HTMLParser):

	def handle_endtag(self, tag): tagstack.pop()

	def handle_starttag(self, tag, attrs):

		tagstack.append(tag)

		this_path="/"

		for tags in tagstack:
			
			this_path=this_path+"/"+tags

		path_list.append(this_path)


		return path_list


def getall_xpath(html):

	############################

	ShowStructure().feed(html)  


	path_list=xpath2indexpath()


	return path_list


##### 普通 xpath 生成带序号的标准 xpath

## 生成规则： 同一个叶子生成规则为短路径到长路径，然后逐个枚举叶子。所以按照这个规则，可以从头（从短）整理生成序号
# 注意  不同浏览器同一个元素的 绝对路径 xpath 可能是不同的， 可能与 driver 解析有关 （和agent无关也不是针对浏览器的构造、多数情况一致），因此多采用 相对路径

def xpath2indexpath():

	## 生成 xpath list

	for i in range(len(path_list)):

		for ii in range(i+1,len(path_list)):

			if path_list[i]==path_list[ii] and path_list[i][-1:]!="]":   ## 完全相同的分支且没设置过，则累加  

				add=1
				strs=path_list[i]  ## 记录下来  以此为基准比较  避免值改变发生影响

				path_list[i]=xpath_setindex(path_list[i],1)
				path_list[ii]=xpath_setindex(path_list[ii],2)

				for iii in range(ii+1,len(path_list)):  ## 修改该分支下的部分 对应节点标记都累加

					if path_list[iii]==strs:  # 再次相同，则累加数增加
						add=add+1

					if path_list[iii].find(strs)==0:

						newxpath_node= xpath_addindex(strs,add)  # 再次增加
						path_list[iii]=path_list[iii].replace(strs,newxpath_node)   # 替换


	## 补丁

	for i in range(len(path_list)):

		## 算法漏洞 ， 即 /a/b/c[1]/d  中的 c[1] 没有进行生成， 要再进行处理一下
		if path_list[i][-3:]=="[1]":

			xpath_old=path_list[i][:-3]

			for ii in range(i+1,len(path_list)):

				if path_list[ii].find(xpath_old+"[2]/")==0:  # 出现新的就不再添加
					break

				path_list[ii]=path_list[ii].replace(xpath_old,xpath_old+"[1]")


		## 算法漏洞  结尾会有 [1][2] 这样的序号
		if path_list[i].find("[1][")>0:

			path_list[i]=path_list[i].replace("[1][","[")


	return path_list	



## xpath序号设置与递增  注意：如果没有则设置为 1

# 获得
def xpath_getindex(xpath):

	num=int(xpath.split("[")[-1].split("]")[0]) # 当前值

	return num

# 设置
def xpath_setindex(xpath,sets):

	if xpath[-1:]!="]":  ## 没设置过
		xpath=xpath+"[" + str(sets) + "]"
	else:

		num=xpath_getindex(xpath) # 当前值
		oldnum_str="[" + str(num) + "]"
		lens=len(oldnum_str)*-1

		xpath=xpath[:lens] +"[" + str(sets) + "]"

	return xpath

# 增加
def xpath_addindex(xpath,add=1):

	if xpath[-1:]!="]":  ## 没设置过
		xpath=xpath+"[1]"


	num=xpath_getindex(xpath) # 当前值
	oldnum_str="[" + str(num) + "]"
	lens=len(oldnum_str)*-1

	num=num+add

	xpath=xpath[:lens] +"[" + str(num) + "]"

	return xpath



### 去掉无意义的 xpath

def available_xpath(browser,xpath_list):


	# list 得到坐标、大小 并进行过滤
	lastpathlist=[]

	for i in range(len(xpath_list)):

		## 过滤特别 xpath
		if xpath_list[i]=="//html" or  xpath_list[i]=="//html/body":
			continue

		if xpath_list[i].find("/script[") >0 or xpath_list[i][-7:]=="/script":
			continue

		## 过滤无意义的 ele
		ele=browser.find_element_by_xpath(xpath_list[i])

		location=ele.location
		size=ele.size

		height=size['height']
		width=size['width']

		if height==0 and width==0:
			continue

		lastpathlist.append([xpath_list[i],location,size])


	return lastpathlist


############### 键盘捕获与匹配位置 得到对应的 xpath


# 注入js  供获得鼠标坐标
def mouse_js(browser):


	js="var Otextbox=document.createElement('div');" + \
		"Otextbox.setAttribute('id','xpath_debug');" + \
		"document.body.appendChild(Otextbox);"

	browser.execute_script(js)


	js="document.onmousemove=function(event) " + \
		"{var e = event || window.event;" + \
		"var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;"+ \
		"var scrollY = document.documentElement.scrollTop ||document.body.scrollTop;"+ \
		"var x = e.pageX || e.clientX +scrollX;var y = e.pageY || e.clientY +scrollY;" + \
		"var Otextbox= document.getElementById('xpath_debug');" + \
		"Otextbox.setAttribute('x',x);Otextbox.setAttribute('y',y); }"

	browser.execute_script(js)



########## 快捷键 输出 xpath

def getpos_event(browser,xpath_list):

	## 获得鼠标当前坐标

	ele=browser.find_element_by_id("xpath_debug")
	
	x=int(ele.get_attribute("x"))
	y=int(ele.get_attribute("y"))

	#print(x,y)

	## 根据 list 开始过滤

	lastarea=-1
	lastpath=""

	for i in range(len(xpath_list)):

		xpath=xpath_list[i][0]
		y1=xpath_list[i][1]['y']
		x1=xpath_list[i][1]['x']
		height=xpath_list[i][2]['height']
		width=xpath_list[i][2]['width']

		y2=y1+height;
		x2=x1+width;

		# 矩形范围内:
		if x>=x1 and x<=x2 and y>=y1 and y<=y2:

			area=height*width # 面积

			### 取最小面积
			if lastarea> area or lastarea==-1:
				lastarea=area
				lastpath=xpath


	times=datetime.datetime.now()
	hour=str(times.hour)
	minute=str(times.minute)
	second=str(times.second)
	the_time=hour + ":" + minute + ":" + second + " "

	print(the_time + lastpath)

	### 获取简化的路径变形，逐层向上 直到元素为 1 个

	simplifyxpath=simplify_xpath(browser,lastpath)

	if simplifyxpath!=lastpath:
		print(the_time + simplifyxpath)

	### 标识对象

	the_ele=browser.find_element_by_xpath(lastpath)
	browser.execute_script("arguments[0].style.border=\"2px solid red\";", the_ele)	


	# 以下方法会影响实际操作，因此不采用

	"""
	js="var Otextbox= document.getElementById('xpath_debug');" + \
		"Otextbox.style.cssText='width:'" + str(width) +"'px;height:'" + str(height) +"'px;left:'"+ str(x1)  +'px;top:'+ str(y1) +'px;position:absolute; background-color:#F00;opacity:0.5;z-index:9999';

	browser.execute_script(js)
	"""


####  简化 xpath , 减少全路径 xpath 长度， 减少不同浏览器的 xpath 结构不同带来的问题

def simplify_xpath(browser,xpath):

	simplifyxpath=xpath

	xpath_split_list=xpath.split("/")
	#print(xpath_split_list)

	## 所有 xpath 位置，从长到短倒序
	xpath_list=[]
	xpath_now=""
	for i  in range(len(xpath_split_list)):
		xpath_now=xpath_now  + "/" + xpath_split_list[i]

		if xpath_now!="/" and  xpath_now!="//" and  xpath_now!="///html" and  xpath_now!="///html/body":
			xpath_now=xpath_now.replace("///","//")
			xpath_list.append(xpath_now)

	xpath_list.reverse()

	## 逐个查找是否有 id 或 class,   xpath_list[0] 是完整路径

	for i in range(len(xpath_list)):

		ele=browser.find_element_by_xpath(xpath_list[i])

		text=ele.text
		ids=ele.get_attribute("id")
		classes=ele.get_attribute("class")
		
		overplus=xpath_list[0].replace(xpath_list[i],"")  ## 剩余的尾部串

		if text!="" or ids!="" or classes!="":

			if text!="":
				xpath=".//*[contains(text(),'" + text + "')]" 

			if ids!="":
				xpath=".//*[@id='" + ids + "']"

			if classes!="":
				xpath=".//*[@class='" + classes + "']"
								
			now_ele_list=browser.find_elements_by_xpath(xpath)

			if len(now_ele_list)==1:

				simplifyxpath = xpath + overplus
				break
			

	return simplifyxpath


########### 释放快捷键

def rel_getpos_event():

	keyboard.remove_hotkey('ctrl')

	print("Xpath debug mode has been finished.")