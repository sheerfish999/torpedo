# -*- coding: utf-8 -*-

#####################  测试用脚本  百度操作封装


import os,time,sys

from selenium import webdriver    
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好
from getids import *    ####  获得各种服务器脚本映射到页面的信息
from finddoit import *    #####   用于封装基础的元素判断操作
from randomid import *    #####  生成各种随机量唯一值

## 用于报告, 使用公共变量
import reportit


######################################  百度基本操作

def searchbaidu(browser,testUrl):

	loads(browser,testUrl)  

	send_keys(browser,".//*[@id='kw']","123")   #正确情况
	#send_keys(browser,".//*[@id='kw111']","123")
	clicks(browser,".//*[@id='su']")

	## 截图插入报告
	xpath=".//*[@id='kw']"
	lastele=browser.find_element_by_xpath(xpath)
	location = lastele.location
	insertthepic(browser,location)


	#  动作名称/目的, 前置条件, 预期, 实际结果, 判定
	reportit.logs(u"框架功能测试",  u"百度操作"  ,  u"操作预期" ,  u"操作结果"  ,1)

	






