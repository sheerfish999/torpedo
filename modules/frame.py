# -*- coding: utf-8 -*-

import sys,os
import codecs

import glob
import time

import traceback

if sys.version_info.major==2:   #python2
	import HTMLParser  #pip install HTMLParser

if sys.version_info.major==3:   #python3
	from html import parser as HTMLParser


########################  本脚本用于载入变量设置和业务用例 等通用操作


######  载入文本内容

def openfiles(filename):


	paths=os.getcwd()    #绝对路径  , os.getcwd()  代替  sys.path[0]
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

	xpath_list=getall_xpath(browser.page_source)

	#这里用作进一步处理

	text=""
	filename="debug.log"
	for i in range(len(xpath_list)):
		text=text + xpath_list[i]       

	#savefiles(filename,text)      #------ 这里什么情况  为什么不能写入文件


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


	## 生成规则： 同一个叶子生成规则为短路径到长路径，然后逐个枚举叶子。所以按照这个规则，可以从头（从短）整理生成序号

	########################## 标识序号

	for i in range(len(path_list)):


		x=1
		index=i
		strs=""

		# 列举后面(到下一个之前）的成员，并逐个修改
		for ii in range(i+1,len(path_list)):  

			if path_list[i]==path_list[ii]:   # 完全相同则逐个标记

				strs=path_list[i] # 存储特征, 且存在过相同内容

				## 上一标记和本次标记之间的位置，将相同路径进行标记
				for iii in range(index,ii):

					temp=path_list[iii]
					
					if temp[:len(strs)]==strs:   # 有前端相同特征

						temp=strs + "[" + str(x) + "]" # 前串
						if len(path_list[iii])-len(strs) !=0:  # 不是当前
							path_list[iii]=temp + path_list[iii][-1*(len(path_list[iii])-len(strs)):]  # 后串
						else:
							path_list[iii]=temp

				x = x + 1  # 标号增加
				index=ii  #记录本次的位置


			## 最后一个标记到末尾的位置，将相同路径进行标记
			if ii==len(path_list)-1 and strs!="":

				for iii in range(index,len(path_list)):   # 上升一个标记位置到结束

					temp=path_list[iii]

					if temp[:len(strs)]==strs:   # 有前端相同特征

						temp=strs + "[" + str(x) + "]" # 前串
						if len(path_list[iii])-len(strs) !=0:  # 不是当前
							path_list[iii]=temp + path_list[iii][-1*(len(path_list[iii])-len(strs)):]  # 后串
						else:
							path_list[iii]=temp



	return path_list

	


