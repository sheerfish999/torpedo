# -*- coding: utf-8 -*-

################################    本脚本用于封装基础的元素判断操作

#pip install -U selenium
from selenium import webdriver    
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

import os,time,datetime,sys
import chardet
import traceback


import Xlib.display as ds     # pip install python-xlib
import Xlib.X as X
import Xlib.ext.xtest as xtest


import platform
sysstr = platform.system()   


sys.path.append(os.getcwd() + "/modules/")   #python 2.7 对   modules.  的方式兼容不好;    os.getcwd()   取代  sys.path[0] 
from record import *    ##  用于录像
from reportit import *   ## 用于报告
from frame import *   ## 用于获得驱动类型



########################  所有的基础动作, 都建议用该脚本中的封装方法,  减少问题,  并提供更多的内置框架功能


################     特别情况下设置鼠标位置 及一些位置属性, 注意屏幕坐标和浏览器坐标是不同的

class mouse():   #http://blog.chinaunix.net/uid-52437-id-3068595.html
	'''mouse class which contains couple of mouse methods'''
	def __init__(browser):
		browser.display = ds.Display()

	def goto_xy(browser,x, y):   
		'''move to position x y'''
		xtest.fake_input(browser.display, X.MotionNotify, x = x, y = y)
		browser.display.flush()

	def pos(browser):
		'''get mouse position'''
		coord = browser.display.screen().root.query_pointer()._data
		return (coord["root_x"],coord["root_y"])



#################  一些必要的封装函数


######### 基础等待

#### 查找等待元素出现 并挪到对应位置
def findfor_ele(browser,xpath,waittime=20,alerts=0):   # alerts==1:   #忽略弹出窗体,  针对一些场景

	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser)
	except:
		pass

	## 等待元素出现
	browser.implicitly_wait(waittime)
	lastele=browser.find_element_by_xpath(xpath)

    # 向下滑动直到找到元素(如果有滑块)
	try:
		browser.execute_script("arguments[0].scrollIntoView(true)",lastele)
	except:
		pass

	return lastele


#### 等待渲染完成
def waitfor_ele(browser,xpath,waittime=20,alerts=0):   # alerts==1:   #忽略弹出窗体,  针对一些场景

	## 等待元素出现
	lastele=findfor_ele(browser,xpath,waittime=waittime,alerts=alerts)

	"""
	#这种判断无效
	if displayedwait==0 or displayedwait==2:   ## 仍然要判断元素是否已经存在     
		try:
			WebDriverWait(browser, waittime).until(lambda the_driver: the_driver.find_element_by_xpath(xpath))     # ------  这种判断无效
		except TimeoutException:
			timeoutlog(browser,xpath, waittime)
	"""

	## 等待显示
	try:
		WebDriverWait(browser, waittime).until(lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())    
	except UnexpectedAlertPresentException:
		if alerts==1:   #忽略弹出窗体, 如果出现就 accept
			maybealert(browser, 0.5)
	except:
		timeoutlog(browser,xpath, waittime)		

	## 等待元素可定位
	try:
		WebDriverWait(browser, waittime).until(EC.presence_of_element_located((By.XPATH, xpath)))
	except TimeoutException:
		timeoutlog(browser,xpath, waittime)

	return lastele


## 调整到可供录像位置，并标识	
def showfor_record(browser,lastele,xpath,waittime=20):

	## 最终用于操作的元素位置
	try:		
		location = lastele.location
	except:			#### 有可能页面发生了改变 需要重新定位
		lastele=browser.find_element_by_xpath(xpath)
		location = lastele.location

	#显示位置调整
	y=location['y']-250
	if y<0 :
		y=0

	js="var q=document.documentElement.scrollTop=" + str(y) +";"
	browser.execute_script(js)


	## 等待元素可再次定位
	try:
		WebDriverWait(browser, waittime).until(EC.presence_of_element_located((By.XPATH, xpath)))
	except TimeoutException:
		timeoutlog(browser,xpath, waittime)

	## 最终用于操作的元素位置
	try:		
		location = lastele.location
	except:			#### 有可能页面发生了改变 需要重新定位
		lastele=browser.find_element_by_xpath(xpath)
		location = lastele.location
	

	#展现操作位置
	browser.execute_script("arguments[0].style.border=\"2px solid red\";", lastele)

	return location


#########  click   按照 xpath 

def clicks(browser,xpath,alert=0,waittime=20):           # alerts==1:   #忽略弹出窗体,  针对一些场景


	## 等待元素出现
	timestart = datetime.datetime.now()
	
	## 等待出现并渲染完成
	lastele=waitfor_ele(browser,xpath,alerts=alert,waittime=waittime)

	## 等待元素可点击
	try:
		WebDriverWait(browser,waittime).until(expected_conditions.element_to_be_clickable((By.XPATH,xpath)))
	except TimeoutException:
		timeoutlog(browser,xpath, waittime)


	## 调整到可供录像位置，并标识
	location=showfor_record(browser,lastele,xpath,waittime)	

	### 录像抓图
	recordpic(browser,location)

	## 页面中认为的焦点移到对应的元素上方, 减少误触, 并且模拟实际焦点情况
	action = ActionChains(browser)

	try:			## 存在元素不支持的情况
		action.move_to_element(lastele).perform()
	except:
		pass

	 # 操作
	browser.set_page_load_timeout(waittime)


	try:     ### 出问题则重试
		lastele.click()
	except:    ### 不仅仅是TimeoutException 的情况  
		#traceback.print_exc()
		#print("Error in:" + xpath)
		clicks(browser,xpath)    ## 再次尝试, 这里不排除会在这里出现问题, 比如上一步点击后, 原元素已经找不到了,  今后考虑可以使用 url, 再次失败则 log

	#删除展现操作位置  有可能页面已经发生跳转
	try:
		browser.execute_script("arguments[0].style.border=\"\";", lastele)
		#browser.execute_script("arguments[0].style=arguments[1]", lastele, "border: 1px dashed black")  #会影响图像比较
	except:
		pass


	# 返回页面载入时间
	timesend = datetime.datetime.now()
	ret=str(round((timesend-timestart).total_seconds(),2))
	return(ret)         #返回值为时间, 用于性能比较


#########  sendkeys     输出内容封装  (注意封装了 clear)

def send_keys(browser,xpath, value):

	#  获得 driver 属性
	drivertypes = drivertype()

	## 等待出现并渲染完成
	lastele=waitfor_ele(browser,xpath)


	""" 
	#以下修改可写和显示的方法已经过时

	lastele=browser.find_element_by_xpath(xpath)
	js="arguments[0].style=arguments[1]"
	js2="display: 'block';"         		#js2="display: '';"
	#js2="readonly: 'False';" 

	if drivertypes==5:     ###  phantomjs 情况比较特殊 ,  selenium 对元素上执行 js 的方法, phantomjs 找不到元素

		changeattrbyjs(browser,xpath,"style" ,"display:'block'")
		changeattrbyjs(browser,xpath,"style" ,"readonly:'block'")

	else:
		browser.execute_script(js, lastele, js2)    # dir(webdriver.Firefox.webdriver.WebDriver)   ,  browser.execute_async_script(js, lastele, js2)    是异步的
	
	"""
	
	delattrbyjs(browser,xpath,"display")
	delattrbyjs(browser,xpath,"readonly")	
	#browser.save_screenshot("./logs/runjs.jpg")    # 调试js执行效果


	## 调整到可供录像位置，并标识	
	location=showfor_record(browser,lastele,xpath)


	## 录像抓图
	recordpic(browser,location)

	## 移到对应的元素上方, 减少误触
	action = ActionChains(browser)
	try:  ##存在元素不支持的情况
		action.move_to_element(lastele).perform()
	except:
		pass

	# 操作

	### 注意该封装先进行了清空
	try:    ## 某些元素没有 clear 性质
		browser.find_element_by_xpath(xpath).clear()	
	except:
		pass


	if sys.version_info.major!=3:   ## python2 编码问题
		reload( sys )
		sys.setdefaultencoding('utf-8')
		valuestr=str(value).decode('utf-8')
		browser.find_element_by_xpath(xpath).send_keys(valuestr)
	else:
		browser.find_element_by_xpath(xpath).send_keys(value)


	## 操作之后的录像抓图
	recordpic(browser,location)

	#删除展现操作位置
	browser.execute_script("arguments[0].style.border=\"\";", lastele)
	#browser.execute_script("arguments[0].style=arguments[1]", lastele, "border: 1px dashed black")  #会影响图像比较


#########  click_enter          # 另一种点击, 通过转到焦点后回车,  适用于一些能找到元素,  click 点击无效的情况

def click_enter(browser,xpath):

	send_keys(browser,xpath,Keys.DOWN) 
	send_keys(browser,xpath,Keys.ENTER) 


#########  click_action   # 另一种点击, 通过 ActionChains  来进行操作,  适用于一些能找到元素,  click 点击无效的情况   (未封装)
##  not working in geckodriver  (firefox)

def click_action(browser,xpath): 

	## 等待出现并渲染完成
	lastele=waitfor_ele(browser,xpath)

	hov = ActionChains(browser).click(lastele)
	hov.perform()


######### select    单选模式

def selects(browser,xpath, value):       ########  列表选择 ,  注意  value 可能是里面显示的 txt, 可能是个id ， 要具体看html

	## 等待出现并渲染完成
	lastele=waitfor_ele(browser,xpath)

	## 调整到可供录像位置，并标识
	location=showfor_record(browser,lastele,xpath)

	## 录像抓图
	recordpic(browser,location)

	## 移到对应的元素上方, 减少误触
	action = ActionChains(browser)
	try:	## 存在元素不支持的情况
		action.move_to_element(lastele).perform()
	except:
		pass


	# 操作
	select = Select(browser.find_element_by_xpath(xpath))
	select.select_by_value(value)


	## 操作之后的录像抓图
	recordpic(browser,location)

	#删除展现操作位置
	browser.execute_script("arguments[0].style.border=\"\";", lastele)
	#browser.execute_script("arguments[0].style=arguments[1]", lastele, "border: 1px dashed black")  #会影响图像比较



######## 隐藏封装的 多选list 的点击


def clicks_multi_list(browser,inputxpath, comboboxxpath, ids):


	clicks(browser,inputxpath)
	list_xpath=comboboxxpath+"/div[" + str(ids) + "]"


	# 定位到checkbox
	## 等待元素出现
	lastele=findfor_ele(browser,list_xpath)

	menu=browser.find_element_by_xpath(inputxpath)
	ActionChains(browser).move_to_element(menu).click(hiddmenu).perform()


    #### 没有进行抓图录像所需定位等操作



#############  页面载入的封装 (失败则反复重试)

def loads(browser,Url,timeouts=8,alerts=1):   # 默认页面重试的超时时间,   注意: 默认处理载入时的弹出窗体(JS)

	browser.set_page_load_timeout(timeouts)

	timestart = datetime.datetime.now()

	####  获得 driver 属性
	drivertypes = drivertype()


	try:   ### 任何异常, 都重试

		browser.get(Url)
		## 根据页面特点判断是否是WAP, 以便在PC端进行页面大小的调整:
		source=browser.page_source

		## 以下判断和处理办法 无法进行载入的准确判断:
		"""
		while exists(browser,"html",timeouts) ==0:      ## html 作为 xpath 进行判断
			#  某些环境该页面需要 F5刷才能刷出来, 只是请求  loads(browser,Url)  的话不行
			browser.refresh() 
		"""

		doctypepos=source.find("<html")
		source=source[:doctypepos]


		types=str(browser)

		#print(source)
		if (source.find("mobile")>=0 or source.find("Mobile")>=0)  and  "phantomjs" not in types:     # DOCTYPE 有 Mobile  字样, 并且不是 phantomjs 模式
			#print("WAP")
			browser.set_window_size(550, 960)  #调整屏幕大小  
		else:
			browser.maximize_window() 

			types=str(browser)
			if "phantomjs" in types:
				size=browser.get_window_size()  
				width=size["width"]
				height=size["height"]
				browser.set_window_size(width,height)   #phantomjs 最大化窗体仍可能是小窗体, 导致抓屏过小, 或找不到元素(phantomjs特有问题)

			## 如果是 远程或容器模式, 可能最大化或大小调整(按照远程)无效,  而且 get_window_size 会出错,  这个时候强行进行修正大小, 避免浏览器找不到元素
			if drivertypes >=10 and drivertypes <30:
				width=1024
				height=768
				browser.set_window_size(width,height)

	except:
		infos(Url + u"页面载入错误或载入时间超过 " + str(timeouts) + "s")
		traceback.print_exc()    ## 供调试, 演示条件下可注释
		maybealert(browser, 0.5)
		time.sleep(0.5)
		loads(browser,Url,timeouts,alerts)


	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser)
	except:
		pass


	## 实际鼠标减少误触   goto_xy(0,0)
	# 以下方式无法判断 htmlunit
	types=str(browser)
	#print(types)
	if "phantomjs" in types:
		pass
	else:
		try:
			m=mouse()
			m.goto_xy(0,0)
		except:    #不支持该方法的场合
			pass


	#恢复默认时间, 避免影响元素操作
	#这个属性会影响点击操作或链接操作后, 页面载入的超时时间判断, 不仅是 get
	browser.set_page_load_timeout(20) 

	# 返回页面载入时间
	timesend = datetime.datetime.now()
	ret=str(round((timesend-timestart).total_seconds(),2))
	infos(Url + u" 页面载入累计时间: " + ret + " s", 1)   # 输出时间并先换行


	return(ret)       #返回值为时间, 用于性能比较


#########  exists   元素存在的时间内即时判断

def exists(browser,xpath,timesouts):

	## 等待页面完全载入完成  #由于目标是时间段内判断，所以不能阻塞

	"""
	try:
		wait_for_page_load(browser)
	except:
		pass  
	"""

	try:

		## 等待元素出现
		browser.implicitly_wait(timesouts)
		lastele=browser.find_element_by_xpath(xpath)

	    # 向下滑动直到找到元素(如果有滑块)
		try:
			browser.execute_script("arguments[0].scrollIntoView(true);",lastele)
		except:
			pass

		###  注意有个响应时间, 本地脚本0.2, 远程返回的弹出框时间建议1-2, 对于刷新判断的页面 建议 5
		WebDriverWait(browser, timesouts).until(lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())

	except:
		return(0)
	else:
		return(1)   #存在

###### 查找并自动切换到存在元素的 iframe 上, 简易搜索一层，搜索失败则退到特定层。已经处于复杂的嵌套时不建议使用


"""
level=0  从顶层搜索，失败后退到顶层 (默认)
level=1  从当前的父一层搜索，失败后退到父一层
level=2  从当前下搜索，失败后退到当前

注意： PhantomJS/Safari/IE  由于不支持  switch_to.parent_frame ，所以不支持 12。 chrome 和 firefox 应支持

"""

# xpath 比照元素的 xpath
# frametype  frame 或  iframe 的 xpath 信息
def search_switch_to_frametype(browser,xpath,frametype,level=0,timeouts=3):

	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser) 
	except:
		pass

	if level==0:
		browser.switch_to_default_content()   #### 最上层
	if level==1:
		browser.switch_to.parent_frame()   ### 父层
	if level==2:						
		pass								### 不变

	ele=[]
	ele=browser.find_elements_by_xpath(frametype)   ###  find_elements_by_xpath != find_element_by_xpath , 前者是个列表

	#print("has frame:",str(len(ele)))

	for i in range(len(ele)):

		#### 有些可能没有 name
		#names=ele[i].get_attribute("name")
		#print(names)
		#browser.switch_to_frame(names)

		browser.switch_to.frame(ele[i])

		has=exists(browser,xpath,timeouts)    ##### 快速判断

		if has==0:
			#### 以便后续查找
			if level==0:
				browser.switch_to_default_content()   #### 最上层
			if level==1:
				browser.switch_to.parent_frame()   ### 父层
			if level==2:						
				browser.switch_to.parent_frame()   ### 父层
		else:
			print(u"搜索到有效的Frame切换: " + xpath )
			return 1   ### 存在

	return 0


def search_switch_to_frame(browser,xpath,level=0,timeouts=3):      #### 存在默认在每个frame下查找元素的超时时间


	############## iframe

	frametype="//iframe"

	ret=search_switch_to_frametype(browser,xpath,frametype,level,timeouts)
	if ret==1:
		return

	############## frame

	frametype="//frame"

	ret=search_switch_to_frametype(browser,xpath,frametype,level,timeouts)
	if ret==1:
		return


##########  根据 链接输出 xpath , 以便得到父路径及推导其它xpath

## 获得后可以进行 诸如 父路径 再乡下追溯 (../xxx) , 以及兄弟节点等操作

"""
特例情况可以使用如兄弟节点的方法, 如:
兄弟节点  之后第一个div兄弟节点
//a[text()='首页- ']/../following-sibling::div[1]/div[2]/div[2]/a[2]      preceding-sibling  为之前
"""

def getlinkxpath(linkstr, eletypes="a",parentPath="//"):    # eletypes 默认元素类型 a  , parentPath 默认上层路径位于根

	# 链接  包含的方法  //a[contains(text(),'自动化测试t8ca8b8b8')]
	# 对于特别的 xml , 注意对象名必须转为小写

	if parentPath!="//":

		if parentPath[len(parentPath)-1:]=="/":   #最后一个是 / 则去掉
			parentPath=parentPath[:len(parentPath)-1]

		parentPath=parentPath+"//"


	link=parentPath + eletypes+ "[contains(text(),'" + linkstr + "')]"
	return(link)

#########  getvalues     取值的封装

def getvalues(browser,xpath,waittimes=20,types="text"):   # types 为所需获得的属性，默认为中间的文本

	## 等待出现并渲染完成
	lastele=waitfor_ele(browser,xpath,waittime=waittimes)

	## 调整到可供录像位置，并标识
	location=showfor_record(browser,lastele,xpath,waittimes)

	## 录像抓图
	recordpic(browser,location)


	# 得到
	if types=="text":
		values=lastele.text
	else:
		values=lastele.get_attribute(types)

	#删除展现操作位置
	browser.execute_script("arguments[0].style.border=\"\";", lastele)
	#browser.execute_script("arguments[0].style=arguments[1]", lastele, "border: 1px dashed black")  #会影响图像比较

	return(values)


#########  checks   检查核对动作, 直接进入报告

def checks(browser,xpath,txt,name,waittimes=20,include=0):     # include=0, 表示完全匹配; 1 , 部分匹配即可

	timestart = datetime.datetime.now()

	## 等待出现并渲染完成
	lastele=waitfor_ele(browser,xpath,waittime=waittimes)

	# 返回页面载入时间
	timesend = datetime.datetime.now()
	ret=str(round((timesend-timestart).total_seconds(),2))

	## 调整到可供录像位置，并标识
	location=showfor_record(browser,lastele,xpath,waittimes)

	## 录像抓图
	recordpic(browser,location)

	#删除展现操作位置
	browser.execute_script("arguments[0].style.border=\"\";", lastele)
	#browser.execute_script("arguments[0].style=arguments[1]", lastele, "border: 1px dashed black")  #会影响图像比较

	## 截图插入报告
	insertthepic(browser,location)

	 # 验证
	if include==0:   ## 完全匹配
		if lastele.text==txt:
			#  动作名称/目的, 前置条件, 预期, 实际结果, 判定
			logs(name, u"字符串信息对比" , txt, lastele.text, 1)
			return(1,ret)          ##  ret 为返回时间, 用于性能比较
		else:
			logs(name, u"字符串信息对比" , txt, lastele.text, 0)
			return(0,ret)

	if include==1:   ## 部分匹配
		if  txt in lastele.text:
			#  动作名称/目的, 前置条件, 预期, 实际结果, 判定
			logs(name, u"字符串信息对比" , txt, lastele.text, 1)
			return(1,ret)          ##  ret 为返回时间, 用于性能比较
		else:
			logs(name, u"字符串信息对比" , txt, lastele.text, 0)
			return(0,ret)	



#############  如果时间内元素没出现, 则页面反复强刷

def existrefreshs(browser,xpath,timeout):

	## 等待页面完全载入完成
	# ## 目标是强刷 所以不能阻塞
	"""
	try:
		wait_for_page_load(browser)  
	except:
		pass
	"""

	Url=browser.current_url

	while exists(browser,xpath,timeout) ==0:     
		#  某些环境该页面需要 F5刷才能刷出来, 只是请求的话不行
		infos(Url +u" 页面载入错误或时间超过 " + str(timeout) + u" s , 被脚本强制刷新",1)
		browser.refresh() 



################  alert 弹出框的等待及获得内容  注意只适用于系统弹出窗体, 而不是xpath能获得的页面

### 正常判断并点击
def getalert(browser, location=0, size=0):   #需要抓图时传入这两个参数, 出现alert时再获得会出错


	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser)
	except:
		pass

	texts=""

	"""
	## 用于类型判断, 适应一些特殊的驱动 (无法判断 htmlunit)
	types=str(browser)
	if "phantomjs" in types:
		pass
	"""	
	#  http://uniquepig.iteye.com/blog/1568197   selenium 可捕获异常类型

	timeout=30   ##默认的等待时间

	####  获得 driver 属性
	drivertypes = drivertype()

	if drivertypes ==5 or drivertypes ==15  or drivertypes ==25 :      # phantomjs ,  容器 htmlunitjs ,  远程 htmlunitjs
		# 需要在操作前提前注入脚本   acceptbyalert_beforedo_ghostdriver(browser)
		texts=u"GhostDriver模式,未获取"     ### 这里是  Phantomjs , Htmlunit (Htmlunitjs)  模式的判断返回
	else:
		try:
			alert=WebDriverWait(browser, timeout).until(EC.alert_is_present())
			#alert=browser.switch_to_alert()    ## 某些驱动的版本情况
			texts=alert.text

			### 截图插入报告    由于没有元素, 所以采用方式2抓图
			if location!=0 and size!=0 :
				insertthepic(browser,location,size)

			alert.accept()     ##进行了选择
		except TimeoutException:    
			timeoutlog(browser,xpath, waittime)

	return(texts)	



### 可能弹出的窗体并点击, 如果超时就继续操作
def maybealert(browser, timeout):

	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser)
	except:
		pass

	texts=""

	####  获得 driver 属性
	drivertypes = drivertype()

	if drivertypes ==5 or drivertypes ==15  or drivertypes ==25 :      # phantomjs ,  容器 htmlunitjs ,  远程 htmlunitjs.   注意: 其他模式不操作
		# 需要在操作前提前注入脚本   acceptbyalert_beforedo_ghostdriver(browser)
		texts=u"GhostDriver模式,未获取"     ### 这里是 Phantomjs 或 Htmlunit 模式判断的返回
		return (texts)	
	else:
		try:
			alert=WebDriverWait(browser, timeout).until(EC.alert_is_present())
			alert.accept()     ##进行了选择
			texts=alert.text
		except TimeoutException: 
			pass
		except NoAlertPresentException:
			pass
		finally:
			return (texts)	## 返回具体信息, 以便一些错误弹出窗体的信息判断   ,  必须在 finally 返回, 否则其它异常会抛出

	



##########  执行 js 脚本替换元素属性,  代替 selenium 的方法,  可以兼容 类似 phantomjs 结合 selenium 后元素找不到的情况, 造成js 作用失败

def changeattrbyjs(browser,xpath,attrname,attrvalue):

	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser)
	except:
		pass

	## 必须替换 " 为 '
	xpath=xpath.replace("\"","'")


	#print(xpath)   #在浏览器中调试一下 ,  是否js作用的元素对了

	###  具体脚本格式如下:
	#function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;}
	#var a = getElementByXpath("//a[contains(text(),'自动化测试t278530ab')]/../../../div[2]/form/input[2]"); a.setAttribute("style","display:'block'");
	
	jsstr=u"function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;}"
	jsstr=jsstr+ u"var thatisattr = getElementByXpath(" + u"\"" +xpath + u"\"" + u"); thatisattr.setAttribute(" + u"\""  + attrname + u"\"" + u"," + u"\""   + attrvalue + u"\""   + u")"
	#print(jsstr)
	
	browser.execute_script(jsstr)       #   代替  browser.execute_script(js, lastele, js2)    , 针对 一些driver 找不到元素的情况, 如 phantomjs


######### 执行js 删除一个属性

def delattrbyjs(browser,xpath,attrname):

	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser)
	except:
		pass

	## 必须替换 " 为 '
	xpath=xpath.replace("\"","'")

	jsstr=u"function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;}"
	jsstr=jsstr + u"var thatisattr = getElementByXpath(" + u"\"" +xpath + u"\"" + u"); thatisattr.removeAttribute(\"" + attrname + u"\")"
	#print(jsstr)
	browser.execute_script(jsstr)



##########  phantomjs 模式, 对于 alert  accept 的选择的情况,  需要先注入脚本再点击,  这样 js 才能起作用,  注意只针对 phantomjs 等 ghostdriver

def acceptbyalert_beforedo_ghostdriver(browser):

	## 等待页面完全载入完成
	try:
		wait_for_page_load(browser)
	except:
		pass

	####  获得 driver 属性
	drivertypes = drivertype()

	if drivertypes ==5 or drivertypes ==15  or drivertypes ==25 :      # phantomjs ,  容器 htmlunitjs ,  远程 htmlunitjs.   注意: 其他模式不操作

		js="window.confirm = function(){return true;}"
		browser.execute_script(js)



########## 等待页面载入完成的另类方法   并不适合页面发生点击后跳转情况, 需要 try: pass

def is_page_loaded(browser):

	if browser.execute_script("return document.readyState;") == "complete":
		return True
	else:
		return False


def wait_for_page_load(browser, freq=5):

	while True:

		if is_page_loaded(browser)==True:
			break

		print("Wait for load...")
		time.sleep(freq)


######### 临时显示元素位置

def show_where(browser,xpath):

	## 等待出现并渲染完成
	lastele=waitfor_ele(browser,xpath)
		
	#展现操作位置
	browser.execute_script("arguments[0].style.border=\"2px solid red\";", lastele)	


######################################


###  返回 xpath list 中最先出现的元素的序号   用于判断载入的页面整体情况，如跳转的页面是哪个

def existlist(browser,xpathlist,timeout,cyc_time=0.001):

	### 避免页面渲染速度影响
	wait_for_page_load(browser)

	### 

	timestart = datetime.datetime.now()	

	while True:

		tag=False # 发现

		for i in range(len(xpathlist)):

			xpath=xpathlist[i]

			if exists(browser,xpath,cyc_time) !=0:
				tag=True
				break

		if tag==True:
			break
		else:
			### 总体时间判断是否超时
			timeend = datetime.datetime.now()
			rettime=round((timeend-timestart).total_seconds(),1)
			
			if rettime > timeout:
				i=-1  ## 指定时间内没有等待到
				break

	return i
	
##### 载入页面前 删除缓存  （目前只支持本地  chrome 和  firefox)

def cleancache_beforeload(browser):  

	####  获得 driver 属性
	drivertypes = drivertype()

	################# firefox

	if drivertypes>=0 and drivertypes<1:

		loads(browser,"about:preferences#privacy")

		clicks(browser,"//*[@id='clearSiteDataButton']")   # 外面的按钮

		# js执行 css 对应按钮 , 其它方式未成功

		dialog_selector = '#dialogOverlay-0 > groupbox:nth-child(1) > browser:nth-child(2)'

		accept_dialog_script = (
			f"const browser = document.querySelector('{dialog_selector}');" + \
			"browser.contentDocument.documentElement.querySelector('#clearButton').click();")   # 里一层按钮

		# wait
		WebDriverWait(browser, 5).until(lambda the_driver: the_driver.find_element_by_css_selector(dialog_selector).is_displayed())  

		# click
		browser.execute_script(accept_dialog_script)

		# wait alert
		WebDriverWait(browser, 5).until(EC.alert_is_present())
		alert = Alert(browser)
		alert.accept()

		loads(browser,"about:blank")

	################# chrome 

	if drivertypes>=1 and drivertypes<2:

		loads(browser,"chrome://settings/clearBrowserData")

		# js执行 css 对应按钮 , 其它方式未成功

		dialog_selector ='* /deep/ #clearBrowsingDataConfirm'   # 跳过 shadow roots

		# wait
		WebDriverWait(browser, 5).until(lambda the_driver: the_driver.find_element_by_css_selector(dialog_selector))

		accept_dialog_script = (
			f"const browser = document.querySelector('{dialog_selector}');" + \
			"browser.click();")

		# click
		browser.execute_script(accept_dialog_script)

		loads(browser,"about:blank")


##### 载入页面前 以文件形式删除缓存  （目前只支持本地  chrome 和  firefox)

#  注意，本地 chrome 这种方法清除缓存后，第一次载入后资源索引可能有问题，所以 load 后要 refresh 一次

def cleancache_beforeload_byfile(browser):


	####  获得 driver 属性
	drivertypes = drivertype()


	################# firefox

	if drivertypes>=0 and drivertypes<1:

		loads(browser,"about:cache")
		text=getvalues(browser,"/html/body/table[2]/tbody/tr[4]/td")

		### 强制删除缓存 

		path=text + r"\entries"

		for i in os.listdir(path):

			path_file = os.path.join(path,i) 

			if os.path.isfile(path_file):

				try:
					os.remove(path_file)
				except:
					pass


	################# chrome 

	if drivertypes>=1 and drivertypes<2:

		loads(browser,"chrome://appcache-internals/")
		text=getvalues(browser,"//*[@id='appcache-list']/div/div[1]/span[1]/span[2]")

		### 强制删除缓存 

		path=text + r"\Cache"

		for i in os.listdir(path):
			path_file = os.path.join(path,i) 

			if os.path.isfile(path_file):

				if path_file.find(r"\f_")>0:

					try:
						os.remove(path_file)
					except:
						pass

		## 新窗口
		js = "window.open('about:blank')" 
		browser.execute_script(js)
		
		## 切换到新窗口
		latest_window=browser.window_handles[-1]
		browser.close() 
		browser.switch_to.window(latest_window)

