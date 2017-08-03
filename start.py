# -*- coding: utf-8 -*-
###  由于根据需要使用不同的 python 版本, 所以不设定 python 运行变量 :    #!/usr/bin/env python

import os,time,datetime,sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

import traceback

import platform

############## 基础框架

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好
from frame import *   #### 用于载入变量设置和业务用例
from initselenium import *   ######   一些初始化封装 driver 的操作
from finddoit import *    #####   用于封装基础的元素判断操作
from record import *    ##  用于录像

############ 业务辅助

from getids import *    ####  获得各种服务器脚本映射到页面的信息
from randomid import *    #####  生成各种随机量唯一值


################################################   本脚本用于最初重建用户的情况

if __name__ == '__main__':  


	if sys.version_info.major==2: 
		reload(sys)
		sys.setdefaultencoding('utf-8')


	##### 载入配置变量
	config=openfiles("config.py")
	exec(config)

	#####  初始化

	if platform.system()=="Linux":
		if get_type<20 and getenvs('DISPLAY')=="":    ## 没获取到, 异常, 就是 linux 服务器终端模式, 同时非远程模式，即只能使用无头模式
			print(u"#### 识别为服务器脚本模式") 
			get_type=5   # 无头
	
	(browser,timestart)=initdriver(dockerinitsh, remotedriverip, get_record, get_report, get_type)            ###   每个业务流脚本都需要初始化一次

	###################  起始

	##### 邮件信息
	attachlist=open('attachlist','w')   ## 邮件附件清单文件
	contentfile=open('mailcontent','w')   ## 邮件正文


	###导入业务流
	run=openfiles(testName+".py")

	Successful=0  ## 成功次数

	for i in range(thetimes):  ## 循环次数

		print(u"#### 当前循环: " + str(i+1)+ " " + u"已成功:"+ str(Successful))

		try:   ##内建异常(在log=0的位置),  一个功能点有异常, 则整个业务流提前终止

				browser.delete_all_cookies()   ## 清除 cookie
				exec(run)     ## 执行业务流
				exec(config)   ## 有些动态变量要每次循环都进行载入, 静态的不受影响
				Successful=Successful+1

		except:

			#  出错一刻的抓图

			# 生成
			now = int(time.time())
			timeArray = time.localtime(now)
			times = time.strftime("%Y%m%d%H%M%S", timeArray)

			if get_type!=15 and get_type!=25:      #  htmlunit 不具备抓图模式
				errorjpg="./logs/error"+ times +".jpg"
				browser.save_screenshot(errorjpg)
				time.sleep(1)   #等待文件生成

			 #异常存储到文件
			errorlog='./logs/error'+ times +'.log'
			traceback.print_exc(file=open(errorlog,"w"))  

			#当时的页面源码存储到文件
			source=browser.page_source
			sourcelog='./logs/source'+ times +'.log'
			#fo = open(sourcelog, "w",encoding = 'utf-8')
			fo = open(sourcelog, "w")
			fo.writelines(source)
			fo.close()

			errstrings=u"测试提前结束, 请查阅 logs目录: " + errorjpg  + u" 及 " + errorlog 
			print(errstrings + u" 错误触发操作位置:")
			print(u"\n========================自动化调试信息=======================\n")
			traceback.print_exc()    ## 供调试, 演示条件下可注释
			print(u"\n========================自动化调试信息结束====================\n")

			#  动作名称/目的, 前置条件, 预期, 实际结果, 判定 , 附属信息
			logs(u"完整测试业务流完成", "" , u"完整测试业务流完成", u"测试业务流未完成", 2, "(" + errorjpg + " " + errorlog + ")" )   ## 警告级别, 不抛出异常, 以便继续后续下一个循环


			##### 写入附件清单文件和邮件正文
			attachlist.write(errorjpg +'\n')
			attachlist.write(errorlog+'\n')
			contentfile.write(errstrings+'\n')


		##### 继续下个业务流
		exec(config)   ## 有些动态变量要每次循环都进行载入, 静态的不受影响
		#continue


	attachlist.close()	
	contentfile.close()	

	#################   结束收尾
	
	savename=testName

	cleanenv(browser,Urls,timestart,savename,get_type)

	













