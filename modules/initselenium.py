# -*- coding: utf-8 -*-

#####################  本脚本用于集中封装一些初始化和退出清理的操作

import os,time,datetime,sys
import subprocess
import traceback

import socket
import threading

from selenium import webdriver    
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# 虚拟界面终端
try:
	from xvfbwrapper import Xvfb  # pip install xvfbwrapper   only linux
	xvfb = Xvfb()
except:
	pass

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好

from record import *    ##  用于录像
from finddoit import *    ##  用于基础动作

## 用于报告, 使用公共变量
import reportit

import platform


from frame import *   #### 用于载入变量设置和业务用例


################################  远程调试模式

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


############################################   初始化环境的判断

def initdriver(dockerinitsh, remotedriverip, get_record, get_report, get_type, degbug_host, debug_port):

	####  将模式保存到文件,便于根据该情况进行判断
	os.system("echo " + str(get_type) + " > drivertype")


	if get_type>=10 and get_type<20:   ##容器模式
		#  初始化启动本地容器
		os.system(dockerinitsh)         #注意必须 root 权限执行本 py 脚本


	#  是否录像操作, 设置配置文件标记位
	if get_record==0:
		os.system("echo 0 > recordset")
	else:
		os.system("echo 1 > recordset")


	#  是否报告操作, 设置配置文件标记位
	if get_report==0:
		os.system("echo 0 > reportset")
	else:
		os.system("echo 1 > reportset")

	
	#  录像和报告 错误日志文件夹初始化

	os.system("echo touches > ./pic/touchs.jpg")

	if os.path.exists("./pic") ==False:
		os.makedirs("./pic")

	'''
	if platform.system()=="Linux":
		os.system("rm -rf ./pic/*.jpg")
		os.system("rm -rf ./pic/id")
	if platform.system()=="Windows":
		os.system("del pic\*.jpg")
		os.system("del pic\id")
	'''
	delete_files('./pic/', '*.jpg')
	delete_files('./pic/', 'id')

	os.system("echo 1 > ./pic/id")

	if os.path.exists("./reports") ==False:
		os.makedirs("./reports")

	if os.path.exists("./logs") ==False:
		os.makedirs("./logs")

	############ 鼠标位置调整, 避免无故触发
	
	## 实际鼠标减少误触   goto_xy(0,0)
	if get_type<5 or (get_type>10 and get_type<15)   or (get_type>20 and get_type<25):    #  各种本地显示调试模式
		try:
			m=mouse()
			m.goto_xy(0,0)
		except:    #不支持该方法的场合
			pass


	###########  selenium 服务连接

	browser=0
	while browser==0:
		#print("Try to connect...")
		browser=trytoconnect(remotedriverip ,get_type)     ## 各种类型模式  不仅包括容器和远程
		if browser==0:
			print("Retry for Driver_Connection.....")

			if get_type>=10 and get_type<20:   ##容器模式  则重新初始化容器
				#  初始化启动本地容器
				os.system(dockerinitsh)         #注意必须 root 权限执行本 py 脚本



	browser.maximize_window()  # 如果是docker或远程, 其大小判断来自远程端, 需要 x-server 设置


	#browser.set_window_size(1024, 768)


	WebDriverWait(browser, 20, poll_frequency=0.1, ignored_exceptions=None)    # 这里设置通用的超时时间(非主动限定), 以及轮询时间(轮询时间对效率的影响不大)


	###########  uno 文档生成的初始化

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()

	if str(reports)!="0":  ### 进行记录报告

		reportit.documents.doc=reportit.opendoc()

		##### windows 下 psr 辅助操作记录，selnium 之外记录一些内容操作
		if platform.system()=="Windows":

			os.system("psr.exe /stop")

			paths=os.getcwd()    #绝对路径  , os.getcwd()  代替  sys.path[0]
			outputpath="\"" + paths +"\\reports\\psrassist.zip\""
			cmd="psr.exe /start /gui 0 /output " + outputpath

			#os.system(cmd)  # 阻塞
			os.popen(cmd)


	##########  清空附件列表文件
	attachlist=open('attachlist','w')   ## 邮件附件清单文件
	attachlist.close()


	#########  开启远程调试模式

	socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 端口重用, 同一进程内有效
	socks.bind(("0.0.0.0",debug_port)) 
	socks.listen(500)

	global thread_remote_cmd
	thread_remote_cmd =threading.Thread(target=remote_cmd,args=(socks,browser,))
	thread_remote_cmd.setDaemon(True)  ### 不检查即可退出
	thread_remote_cmd.start()


	##效率计算
	timestart = datetime.datetime.now()
	return(browser,timestart)


########################  尝试连接

## 浏览器配置文件设置)
def profileset(profile, getimgflash, get_type):

	## 一些特别设置(暂放)

	"""   
	禁用图片和flash   但目前没效果, 所以该参数废弃

	###  禁用图片和flash
	if getimgflash==0 and get_type==0:
		###########  适合 firefox 的配置文件  -------  这里未来还需要参数判断浏览器的类型
		## Disable CSS
		#profile.set_preference('permissions.default.stylesheet', 2)   #有影响 不能使用
		## Disable images
		profile.set_preference('permissions.default.image', 2)      #  (是否收到图片验证码不影响图片验证)   但 似乎没效果, 至少对远程是这样
		## Disable Flash
		profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')

		########### 适合 chrome 的配置文件 ------- 还没写

	"""

	return(profile)


## 初始化并连接
def trytoconnect(remotedriverip, get_type):

	if get_type==0 or get_type==6:   ## firefox

		if get_type==6:
			xvfb.start()   # 虚拟界面终端
			print(u"#### 尝试进入虚拟界面终端")

		profile = FirefoxProfile()
		#profile=profileset(profile,  getimgflash, get_type)
		profile.set_preference("capability.policy.default.Window.frameElement.get","allAccess")   # 避免一些权限问题 如 gecko 驱动的问题
		browser = webdriver.Firefox(profile)
		#browser = webdriver.Firefox()    ## 这里没有使用配置文件

		print(u"#### 驱动模式: 【本地 Firefox】")

		return(browser)

	if get_type==1 or get_type==7 or get_type==1.1:   ## chrome   http://mvnrepository.com/artifact/org.seleniumhq.selenium/selenium-chrome-driver

		if get_type==7:
			xvfb.start()   # 虚拟界面终端
			print(u"#### 尝试进入虚拟界面终端")

		chromeOptions = webdriver.ChromeOptions()
		#chromeOptions=profileset(chromeOptions, getimgflash, get_type)
		chromeOptions.add_argument("--privileged")
		chromeOptions.add_argument("--no-sandbox")

		if get_type==1.1:
			chromeOptions.add_argument("--headless")    ### 无头模式   chrome 59 以后支持
			print(u"#### Chrome 无头模式")

		chromedriver = "chromedriver"   ## path()
		#os.environ["webdriver.chrome.driver"] = chromedriver

		browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

		print(u"#### 驱动模式: 【本地 Chrome】")

		return(browser)

	if get_type==5:         ##  本地 PhantomJS    注意不支持 系统 js 弹出alert 的业务流
		browser = webdriver.PhantomJS()

		print(u"#### 驱动模式: 【本地 PhantomJS】")
		return(browser)

	if get_type==2:   ### ie
		browser = webdriver.Ie()

		print(u"#### 驱动模式: 【本地 Internet Explorer】")
		return(browser)

	if get_type==3 or get_type==8:   ### Opera

		if get_type==8:
			xvfb.start()   # 虚拟界面终端
			print(u"#### 尝试进入虚拟界面终端")

		browser = webdriver.Opera()

		print(u"#### 驱动模式: 【本地 Opera】")
		return(browser)		

	if get_type==4:   ### Safari
		browser = webdriver.Safari()

		print(u"#### 驱动模式: 【本地 Safari】")
		return(browser)



	########################  容器或远程服务连接

	command_executors='http://' + remotedriverip + '/wd/hub'
	#print(command_executors)

	if get_type==10 or get_type==20:      # docker firefox 或远程 firefox
		profile = FirefoxProfile()
		#profile=profileset(profile,  getimgflash, get_type)
		profile.set_preference("capability.policy.default.Window.frameElement.get","allAccess")   # 避免一些权限问题 如 gecko 驱动的问题

		try:    ## 反复重试
			if get_type==10:
				browser =webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX,command_executor=command_executors, browser_profile=profile)
			if get_type==20:			
				browser = webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX,command_executor=command_executors)
		except:
			traceback.print_exc()
			return(0)
		else:
			print(u"#### 驱动模式: 【远程 Firefox】")
			return(browser)   #成功



	if get_type==11 or get_type==21:      # docker chrome 或远程 chrome

		#chromeOptions=profileset(chromeOptions, getimgflash, get_type)

		capabilities=DesiredCapabilities.CHROME
		# DesiredCapabilities capabilities.setCapability("webdriver.chrome.args", Arrays.asList("--whitelisted-ips=''"));   不能解决远程连接的可访问性问题
		# capabilities["webdriver.chrome.args"]="--whitelisted-ips=''"


		try:    ## 反复重试
			browser =webdriver.Remote(command_executor=command_executors, desired_capabilities=capabilities)
		except:
			traceback.print_exc()
			return(0)
		else:
			print(u"#### 驱动模式: 【远程 Chrome】")
			return(browser)   #成功


	if get_type==15 or get_type==25:      # docker htmlunit 或远程 htmlunit

		try:    ## 反复重试
			browser =webdriver.Remote(command_executor=command_executors, desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
		except:
			traceback.print_exc()
			return(0)
		else:
			print(u"#### 驱动模式: 【远程 HtmlUnit】")
			return(browser)   #成功




########################  退出的一些整理的操作

def cleanenv(browser,Urls,timestart,savenamestr,get_type):

	now = int(time.time()) 
	timeArray = time.localtime(now)
	times = time.strftime("%Y%m%d%H%M%S", timeArray)

	savename=""
	savename=  savenamestr + times

	###################  关闭虚拟界面终端
	if get_type>5 and get_type<10:
		xvfb.stop()


	###################  生成录像
	if get_type!=15 and get_type!=25:      # docker htmlunit 或远程 htmlunit 不支持 录像
		catchpicsave(savename)

	##################  生成文档

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()

	if str(reports)!="0":  ##  进行记录
		reportit.closedoc(savename)

		##### windows 下 psr 辅助操作记录，selnium 之外记录一些内容操作
		if platform.system()=="Windows":
			os.system("psr.exe /stop")


	##################  发送邮件

	##### 增加报告文件到清单

	attachlist=open('attachlist','a')   ## 邮件附件清单文件
	attachlist.write("./reports/"  + savename + ".pdf")
	attachlist.close()

	##### 邮件的正文

	contentfile=open('mailcontent','a')   ## 邮件正文
	contentfile.write(u"测试时间: "+str(datetime.datetime.now()) + "\n" + u"更具体信息详见对应附件报告")
	contentfile.close()	


	##### 载入配置变量   
	
	config=openfiles("config.py")   
	exec(config)

	### 存在报告标记
	if str(reports)!="0":
		sendmaillist(mail_host,mail_user,mail_pass,mail_postfix, u"自动化测试报告 [本报告自动触发,请勿直接回复,疑问请联系测试人员]")	

	##################

	##效率计算
	print("---------------------------------------------------------")
	timesend = datetime.datetime.now()
	print("用时: " + str(timesend-timestart) +  "    测试时间点:" +  str(timestart) +  "    目标地址:" + Urls)

	#time.sleep(3)

	browser.quit()

		
	####

	sys.exit() 







	
