# -*- coding: utf-8 -*-

#####################  本脚本用于集中封装一些初始化和退出清理的操作

import os,time,datetime,sys
import subprocess
import traceback

from selenium import webdriver    
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# xvfb 没涉及
#from xvfbwrapper import Xvfb  # pip install xvfbwrapper
#vdisplay = Xvfb()
#vdisplay.start()
#vdisplay.close()


sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好

from record import *    ##  用于录像
from finddoit import *    ##  用于基础动作

## 用于报告, 使用公共变量
import reportit

import platform


from frame import *   #### 用于载入变量设置和业务用例

############################################   初始化环境的判断

def initdriver(dockerinitsh, remotedriverip, get_record, get_report , get_type):

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

	if platform.system()=="Linux":
		os.system("rm -rf ./pic/*.jpg")
		os.system("rm -rf ./pic/id")
	if platform.system()=="Windows":
		os.system("del pic\*.jpg")
		os.system("del pic\id")

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

	if platform.system()=="Linux" and str(reports)!="0":
		(reportit.documents.document,  reportit.documents.cursor)=reportit.opendoc()


	##########  清空附件列表文件
	attachlist=open('attachlist','w')   ## 邮件附件清单文件
	attachlist.close()


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

	if get_type==0:   ## firefox
		profile = FirefoxProfile()
		#profile=profileset(profile,  getimgflash, get_type)
		profile.set_preference("capability.policy.default.Window.frameElement.get","allAccess")   # 避免一些权限问题 如 gecko 驱动的问题
		browser = webdriver.Firefox(profile)  
		#browser = webdriver.Firefox()    ## 这里没有使用配置文件
		return(browser)

	if get_type==1:   ## chrome   http://mvnrepository.com/artifact/org.seleniumhq.selenium/selenium-chrome-driver
		chromeOptions = webdriver.ChromeOptions()
		#chromeOptions=profileset(chromeOptions, getimgflash, get_type)
		chromeOptions.add_argument("--privileged")
		chromeOptions.add_argument("--no-sandbox")

		chromedriver = "chromedriver"   ## path()
		#os.environ["webdriver.chrome.driver"] = chromedriver

		browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

		return(browser)


	if get_type==5:         ##  本地 PhantomJS    注意不支持 系统 js 弹出alert 的业务流
		browser = webdriver.PhantomJS()
		return(browser)


	#####################


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
		    	return(browser)   #成功



	if get_type==11 or get_type==21:      # docker chrome 或远程 chrome

		#chromeOptions=profileset(chromeOptions, getimgflash, get_type)

		capabilities=DesiredCapabilities.CHROME
		# DesiredCapabilities capabilities.setCapability("webdriver.chrome.args", Arrays.asList("--whitelisted-ips=''"));   不能解决远程连接的可访问性问题
		# capabilities["webdriver.chrome.args"]="--whitelisted-ips=''"


		try:    ## 反复重试
			if get_type==11:	
				browser =webdriver.Remote(command_executor=command_executors, desired_capabilities=capabilities)		
			if get_type==21:	
				browser =webdriver.Remote(command_executor=command_executors, desired_capabilities=capabilities)
			
		except:
			traceback.print_exc()
			return(0)
		else:
		    	return(browser)   #成功



	if get_type==15 or get_type==25:      # docker htmlunit 或远程 htmlunit

		try:    ## 反复重试
			browser =webdriver.Remote(command_executor=command_executors, desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
		except:
			traceback.print_exc()
			return(0)
		else:
		    	return(browser)   #成功




########################  退出的一些整理的操作

def cleanenv(browser,Urls,timestart,savenamestr,get_type):

	now = int(time.time()) 
	timeArray = time.localtime(now)
	times = time.strftime("%Y%m%d%H%M%S", timeArray)

	savename=""
	savename=  savenamestr + times

	###################  生成录像
	if get_type!=15 and get_type!=25:      # docker htmlunit 或远程 htmlunit 不支持 录像
		catchpicsave(savename)

	##################  生成文档

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')
	reportf.close()

	if platform.system()=="Linux" and str(reports)!="0":
		reportit.closedoc(savename)

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

	### 存在报告标记并且为 Linux
	if platform.system()=="Linux" and str(reports)!="0":
		sendmaillist(mail_host,mail_user,mail_pass,mail_postfix, u"自动化测试报告 [本报告自动触发,请勿直接回复,疑问请联系测试人员]")	

	##################

	##效率计算
	print("---------------------------------------------------------")
	timesend = datetime.datetime.now()
	print("用时: " + str(timesend-timestart) +  "    测试时间点:" +  str(timestart) +  "    目标地址:" + Urls)

	#time.sleep(3)

	try:   ##关闭页面是否出现异常,没有任何捕获意义
		browser.close()
	except:
		pass

	browser.quit()

	####

	sys.exit() 







	
