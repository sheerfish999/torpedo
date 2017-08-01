# -*- coding: utf-8 -*-


################################   本脚本用于生成基本输出和pdf 报告

import os,time,sys
from time import sleep

import platform
sysstr = platform.system()   

if sysstr == "Linux":
        import hues   ## pip install hues

if sysstr == "Windows":
        import winhues as hues


sys.path.append(os.getcwd() + "/modules/")   #python 2.7 对   modules.  的方式兼容不好;    os.getcwd()   取代  sys.path[0] 
from record import *         ##  用于录像 (获得插图抓屏)

## 以下用于特别引用
from frame import *   #### 用于载入变量设置和业务用例

from sendmails import *  ##### 用于邮件发送

from dodoc import *  #### 用于文档处理 


### mupdf (linux) pdf 阅读器  
# zypper in libjpeg-devel  ### 还需要一些其他库，根据提示进行
# https://github.com/muennich/mupdf


class documents:
	doc=None   ## 文档句柄
	ids=1   ## 用例号



"""
关于路径混淆:  
有意使用了  reports文件夹和 reportit 模块文件名进行区分
经测试在同名情况下,  某些版本的python(如 2.7.5) 会 将文件夹误认为模块, 造成好像找到模块, 但却找不到函数的情况  (在识别 extend 路径前, 优先识别本地路径) 

"""

###############################################    关于外部参数的可支持性:

"""
当环境(如 shell) 具备以下参数时,  将默认使用对应值而不使用配置文件值,  以便 jenkins 等使用:
$maillist       收件人地址


"""

###############################################


########### 生成日志报告文件    标准检查点日志

## 动作名称/目的, 前置条件, 预期, 实际结果, 判定, 附属信息

def logs(aims, conditions, wants,  res, yesorno, others=""):

	"""
	0  失败
	1  成功
	2  警告

	"""

	####################################  命令行即时输出

	if yesorno==0:
		yesornostr=u"测试点验证未通过, 请查阅具体记录" + others
		colorstr="\033[1;31;40m"   #红色
	if yesorno==1:
		yesornostr=u"测试点验证通过" + others
		colorstr="\033[1;32;40m"     #绿色

	if yesorno==2:
		yesornostr=u"警告, 请查阅具体记录" + others
		colorstr="\033[1;33;40m"       #橙黄色


	closecolor="\033[0m"

	##### 非LINUX不支持以上模式的彩色日志输出
	if platform.system()!="Linux":
		colorstr=""
		closecolor=""
	
	######

	print("---------------------------------------------------------")
	print(u"动作名称/目的: " + aims  +"  " + u"前置条件/判断类型:" +" " + conditions)

	outputlog=  u"预期: " + wants + "  " + u"实际结果:"  + " "+  res  + "  " +u"\n判定: " +   yesornostr
	#print(colorstr  + outputlog +  closecolor )   ##  这种模式不兼容 windows , 因此暂时停止使用

	### 暂时使用以下模式  	#hues.log   hues.info   hues.error   hues.warn    hues.success

	if yesorno==0:	
		hues.error(outputlog)

	if yesorno==1:
		hues.success(outputlog)

	if yesorno==2:
		hues.warn(outputlog)

	##################################################   报告输出

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()


	##### 报告标记位正常
	if str(reports)!="0":

		doc=documents.doc

		doc.insert_text("\n")

		#   插入表格

		doc.insert_text(u"★ 用例及记录 " + str(documents.ids) + u" 判定")



		###### 颜色定义

		gray=0xcdc9c9  #灰色

		green=0x228b22 #绿色

		if platform.system()=="Linux":
			red=0xff4500   	  #红色
			yellow=0xffd700   #黄色

		if platform.system()=="Windows":
			red=0x0045ff   	  #红色
			yellow=0x00d7ff   #黄色


		######  结论 表格 在最上方

		mytable0= doc.insert_table(3,1)

		doc.table_setattr(mytable0,"A1","BackColor",gray)
		doc.insert_tabletext(mytable0,"A1",u"自动化判定结果")


		#  时间
		times=time.strftime('%Y-%m-%d %X', time.localtime())
		doc.insert_tabletext(mytable0,"A2",times)


		if yesorno==0:    ### 错误时的突出显示
			doc.table_setattr(mytable0,"A3","BackColor",red)		 #  红色  
		if yesorno==1: 
			doc.table_setattr(mytable0,"A3","BackColor",green)		 # 绿色     
		if yesorno==2: 
			doc.table_setattr(mytable0,"A3","BackColor",yellow)		#  黄色


		doc.insert_tabletext(mytable0,"A3",yesornostr)

		#####  前提 表格
		mytable1= doc.insert_table(2,2)

		doc.table_setattr(mytable1,"A1","BackColor",gray)
		doc.table_setattr(mytable1,"B1","BackColor",gray)

		doc.insert_tabletext(mytable1,"A1",u"动作名称/目的")
		doc.insert_tabletext(mytable1,"B1",u"前置条件/判断类型")
		doc.insert_tabletext(mytable1,"A2",aims)
		doc.insert_tabletext(mytable1,"B2",conditions)


		##### 预期和返回 表格
		mytable2= doc.insert_table(2,2)

		doc.table_setattr(mytable2,"A1","BackColor",gray)
		doc.table_setattr(mytable2,"B1","BackColor",gray)

		doc.insert_tabletext(mytable2,"A1",u"自动化用例预期")
		doc.insert_tabletext(mytable2,"B1",u"自动化获取结果")
		doc.insert_tabletext(mytable2,"A2",wants)
		doc.insert_tabletext(mytable2,"B2",res)

		### 用例号
		documents.ids=documents.ids+1




	#############  最后:  错误即抛出异常,以便捕获

	if yesorno==0:
		raise ValueError('测试用例识别到错误')



############ 超时时的日志封装   (最常见的用例判断外的异常)

def timeoutlog(browser,xpath, waittime):

	if sys.version_info.major==2: 
		reload(sys)
		sys.setdefaultencoding('utf-8')

	#  保存超时页面的截图
	browser.save_screenshot("./logs/timeout.png")

	#  动作名称/目的, 前置条件, 预期, 实际结果, 判定
	logs(u"返回时间判断", u"预定时间: " + str(waittime) + u"s" , str(waittime) + u"s 内找到元素", u"元素 " + xpath + u" 没有在指定时间返回, 请查找元素所在的测试用例" , 0)



########### 辅助性质的记录输出 和 报告信息

def infos(strs, crlf=0):    # 默认前面不换行

	####################################  命令行即时输出

	colorstr="\033[1;34;40m"
	closecolor="\033[0m"

	##### 非LINUX不支持彩色日志输出
	if platform.system()!="Linux":
		colorstr=""
		closecolor=""
	
	######

	print("---------------------------------------------------------")
	#print(colorstr  + strs +  closecolor )  ##  这种模式不兼容 windows , 因此暂时停止使用

	### 暂时使用以下模式  	#hues.log   hues.info   hues.error   hues.warn    hues.success
	hues.info(strs)
	

	##################################################   报告输出

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()



	##### 报告标记位正常
	if str(reports)!="0":

		doc=documents.doc


		#   插入表格
		if crlf==1:   #换行
			doc.insert_text("\n")

		mytable3=doc.insert_table(1,1)

		doc.table_setattr(mytable3,"A1","BackColor",0xcdc9c9)   # 灰色
		doc.insert_tabletext(mytable3,"A1",strs)



#################  向报告中插入截图 

### 插入指定位置的图片  图片位置  ./reports/insertpic.jpg
def insertpic():   

	##################################################   报告输出

	#####  获得是否报告的标记位
	reportf = open("./reportset", "r")
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()


	##### 报告标记位正常

	if str(reports)!="0":

		doc=documents.doc

		doc.insert_text("\n")
		#insert_text(u"▼用例及记录 " + str(documents.ids) + " 自动截屏▼")   ### 可能有顺序错乱
		doc.insert_text(u"▼上下文场景自动截屏▼")

		doc.insert_break()

		#   插入图片

		paths=sys.path[0]    #必须使用绝对路径
		imgpath= 'file://'+ paths + '/reports/insertpic.jpg'

		print(imgpath)
		doc.insert_img(imgpath,16000,8000)


####  抓图并插入截图 
def insertthepic(browser,location,size=0):    #size!=0   调用的是第二种方法抓图, 不依赖于 selenium的元素定位

	paths=sys.path[0]    #必须使用绝对路径
	savepath=paths + '/reports/insertpic.jpg'
	catchthepics(browser,location,savepath,size)

	sleep(0.5)  ## 写入

	insertpic()


##################  新建文档的初始化动作

def opendoc():

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()

	if str(reports)=="0":        #不报告
		return (None,None)


	doc=openthedoc()
	documents.doc=doc


	# 文档生成时间
	now = int(time.time()) 
	timeArray = time.localtime(now)
	times = time.strftime("%Y%m%d%H%M%S", timeArray)

	doc.insert_text(u"自动化测试报告-文档生成时间:" + times)
	doc.insert_text("\n")

	return doc


################  关闭文档的动作

def closedoc(savename):

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()

	if str(reports)=="0":        #不报告
		return

	doc=documents.doc

	doc.insert_text("\n")
	doc.insert_text(u"报告结束")


	######## 生成

	doc.savetopdf(savename)

	print("报告名称: " + savename)

	## 弹出文档报告
	if getenvs('DISPLAY')!="":  #linux本地模式
		os.system("nohup mupdf ./reports/"+ savename +".pdf  >/dev/null 2>log &")

	if platform.system()=="Windows":  #windows模式
		os.system("start ./reports/"+ savename +".pdf")


########################################  发送邮件 的开关等同于报告的开关  ,邮件功能的关闭也可以通过 邮件清单中注释掉所有邮件即可


def tosendmaill(mail_host,mail_user,mail_pass,mail_postfix, mailto_list, sub,content):  

	if sendmaill(mail_host,mail_user,mail_pass,mail_postfix, mailto_list, sub,content):  
		print (u"发送成功:"+mailto_list) 
	else:  
		print (u"发送失败:"+mailto_list)


#按列表发送   邮件服务器位置, 用户名, 密码, 邮箱后缀,   标题, 内容
def sendmaillist(mail_host,mail_user,mail_pass,mail_postfix, sub):

	####  获得是否报告的标记位         不报告则不涉及发送邮件
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()

	if str(reports)=="0":        #不报告
		return

	#### 发送的邮件信息

	filename="mailcontent"           ####  默认的邮件内容文件, 可以生成该文件
	file_object = open(filename)
	content = file_object.read( )	   #内容
	file_object.close()


	##### 支持外部临时环境变量的发送地址, 以便支持诸如 jenkins

	if getenvs('maillist')=="":    ## 使用配置文件列表地址
		#### 逐行提取邮件列表
		maillist = "maillists"          	     ###  默认的邮件收件人列表文件, 可以维护该文件

		file_object= open(maillist)             
		mailto_list = file_object.readline() 

		while mailto_list: 
			mailto_list=mailto_list.replace('\n','')    #处理换行
			if len(mailto_list)>1:

				if mailto_list.find('#')!= 0:   # 非注释行

					#### 发送
					tosendmaill(mail_host,mail_user,mail_pass,mail_postfix, mailto_list, sub,content)
					####

			mailto_list = file_object.readline() 

		file_object.close()  



	if getenvs('maillist')!="":   ## 使用环境变量地址

		mailto_list=getenvs('maillist')

		tosendmaill(mail_host,mail_user,mail_pass,mail_postfix, mailto_list, sub,content)



################  测试

if __name__ == '__main__':

	if sys.version_info.major==2: 
		reload(sys)
		sys.setdefaultencoding( "utf-8" )


	##############################  生成报告

	doc=opendoc()

	infos(u"响应时间: "+ "10.5s" )

	insertpic()

	## 动作名称/目的, 前置条件, 预期, 实际结果, 判定
	try:
		logs(u"这是一个文档测试1", "openoffice", u"输出文档",  u"输出了",  1)
		infos(u"响应时间: "+ "10.5s" )
		logs(u"这是一个文档测试2", "openoffice", u"输出文档",  u"输出了",  2)
		infos(u"响应时间: "+ "10.5s",1 )
		logs(u"这是一个文档测试3", "openoffice", u"输出文档",  u"输出了",  0)  
	finally:
		closedoc(u"测试文档生成模块")



	################################ 发送邮件

	"""

	##### 载入配置变量
	config=openfiles("../config.py")
	exec(config)

	####  邮件的正文
	attachlist=open('mailcontent','w')   ## 邮件附件清单文件
	attachlist.write(u"这是一个调试邮件, 测试时间: "+str(datetime.datetime.now())  + "\n" +  "这是一个测试邮件")
	attachlist.close()	


	sendmaillist(mail_host,mail_user,mail_pass,mail_postfix, u"这是一个测试邮件")

	"""













