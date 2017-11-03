# -*- coding: utf-8 -*-

#####################  测试用脚本  百度操作封装


import os,time,sys

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好

#from getids import *    	####  获得各种服务器脚本映射到页面的信息
from finddoit import *    	#####   用于封装基础的元素判断操作
from randomid import *    	#####  生成各种随机量唯一值
import reportit				## 用于报告, 使用公共变量

from imgext import *		### 用于图片处理



######################################  百度基本操作

def searchbaidu(browser,testUrl):


	### 示例一  基本操作  并生成报告（需要配置文件打开报告模式）


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

	
	### 示例二   按图搜索并点击

	loads(browser,"https://www.baidu.com/")

	#imgele=getpic_pos_fromdriver(browser,"./test/getimg2.png")    # 整个页面中搜索
	imgele=getpic_pos_fromdriver(browser,"./test/getimg2.png",block=3,parent_element_xpath="//*[@id='head']/div/div[1]/div")  # 某个范围下搜索

	imgele.click()

	
	### 示例三  搜索指定文本并点击

	loads(browser,"https://www.baidu.com/")

	#imgele=gettext_pos_fromdriver(browser,u"百度一下")    # 整个页面中搜索
	imgele=gettext_pos_fromdriver(browser,u"百度一下",parent_element_xpath="//*[@id='head']/div/div[1]/div")  # 某个范围下搜索

	imgele.click()

	text=ocr_fromdriver(browser,".//*[@id='su']")
	print(text)


	"""

	### 示例四   动态调试

	修改 debug_content.py 执行 debug_content.sh / debug_content.bat 完成动态调试
	或直接使用单行命令行模式： debug_cmdline.sh / debug_cmdline.bat

	

	# pause()  ## 中断后可用于远程调试

	
	"""






