# -*- coding: utf-8 -*-

#pip install -U selenium
#npm install phantomjs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import traceback

import time
import threading

"""
本模块用于 selenium 获取指定信息，但由于网速等原因整体页面加载时间过长而导致的 实际信息已经返回，但driver整体过慢的情况
一般情况用于取代页面爬虫的爬取功能或直接的接口操作等，减少开发和调试时间，且支持动态页面

注意本模块中的函数使用后，达到预期目的后会自动强制终止页面加载，不适用于页面整体操作，只适用于获取特定信息

"""


def doload(driver,url):

	try:
		driver.get(url)
	except:
		#traceback.print_exc()
		pass

def doclick(driver,xpath):

	element = driver.find_element_by_xpath(xpath)

	try:
		element.click()
	except:
		#traceback.print_exc()
		pass



## xpath1 首要判断出现的元素， 出现则返回 1
## xpath2 次要判断出现的次要元素，出现则返回 2

# 快速载入
def fastload(driver,url,xpath1,xpath2=""):    ## 优先级  或的关系

	driver.get("about:blank")  ## 先打开一个空页面，避免页面未跳转前停止，错误判断元素信息

	ret=fastdo(driver,"load",url,xpath1,xpath2)

	return ret

#快速点击
def fastclick(driver,xpath,xpath1,xpath2=""):   ## 优先级  或的关系

	ret=fastdo(driver,"click",xpath,xpath1,xpath2)

	return ret

#快速
def fastget(driver,url,xpath,types=""):      ##  type为属性值名称，如 href, 空默认取 text. 本函数适合确定稳定的xpath目标的情况

	
	ret=fastload(driver,url,xpath)  ## 首先等待载入返回

	if ret==1:

		ele = driver.find_element_by_xpath(xpath)

		# 得到
		if types=="":
			values=ele.text
		else:
			values=ele.get_attribute(types)


	else:
		values=""

	return values


def fastdo(driver,types,url_xpath,xpath1,xpath2=""):

	if types=="load":
		thread = threading.Thread(target=doload,args=(driver,url_xpath,))
	
	if types=="click":
		thread = threading.Thread(target=doclick,args=(driver,url_xpath,))


	thread.start()

	getit=0

	while True:

		#time.sleep(0.01)  # 避免CPU 满载,适用于低性能持续运行

		# 尝试查找指定主要元素
		try:
			WebDriverWait(driver, 0.001).until(lambda x : x.find_element_by_xpath(xpath1))
			getit=1
			break

		except:

			# 尝试查找指定次要元素
			if xpath2!="":
				try:
					WebDriverWait(driver, 0.001).until(lambda x : x.find_element_by_xpath(xpath2))   
					getit=2
					break
				except:
					pass

		if thread.is_alive()==False:
			break


	driver.execute_script("window.stop();")  # 终止浏览器继续加载，子线程结束


	return getit



############################## 

if __name__ == '__main__':

	driver = webdriver.PhantomJS()

	url="http://mvnrepository.com/artifact/commons-io/commons-io/2.6"
	xpath1=".//*[@id='maven-a']"


	############

	print("Start test:")

	ret=fastload(driver,url,xpath1)
	print(ret)

	ret=fastget(driver,url,xpath1)
	print(ret)


	###########

	driver.close()
	driver.quit()
