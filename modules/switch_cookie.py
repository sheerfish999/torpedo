

############################################  本脚本用于接口与  selenium 之间cookie 交换的封装


from selenium import webdriver  #pip install -U selenium   npm install phantomjs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

import time
import os 


########  CookieJar 转化给 selenium,  cookiejar to selenium cookie dict ,  找到某一条 cookie


def cookiejar_2seleniumcookie(cookiejar,cookieitem_name):


	#import requests
	#cookie_dict=requests.utils.dict_from_cookiejar(cookiejar)  ## 这个值不能直接用 格式不对

	cookie_dict={}

	for item in cookiejar:

		#print(dir(item))


		"""
		未添加：
		'comment', 'comment_url', 'discard',  'domain_initial_dot', 'domain_specified', 'expires', 'get_nonstandard_attr', 
		'has_nonstandard_attr', 'is_expired', 'path_specified', 'port', 'port_specified', 'rfc2109', 'set_nonstandard_attr', 'version'

		"""

		if item.name==cookieitem_name:

			cookie_dict["name"]=item.name
			cookie_dict["value"]=item.value
			cookie_dict["domain"]=item.domain
			cookie_dict["path"]=item.path
			cookie_dict["secure"]=item.secure


	#print(cookie_dict)
	
	return cookie_dict



######## cookiejar 传递给 selenium driver

def cookiejar_2selenium_driver(driver,url,cookiejar,cookieitem_name):


	cookie_dict=cookiejar_2seleniumcookie(cookiejar,cookieitem_name)


	#必须先打开一个页面（同域名页面）才能设置cookie
	driver.get(url)  #  phantomjs 不需要先载入一个页面, 但是 chromedriver 需要

	driver.add_cookie(cookie_dict)

	driver.get(url)  # driver.refresh() 不行, 必须 get

	#print(driver.page_source)
	
	
	




