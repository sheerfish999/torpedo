# -*- coding: utf-8 -*-

import sys,os
import codecs

########################  本脚本用于载入变量设置和业务用例


def openfiles(filename):

	paths=os.getcwd()    #绝对路径  , os.getcwd()  代替  sys.path[0]
	all_the_text = codecs.open(paths + "/"+ filename,'r','utf-8').read( )

	return(all_the_text)


######  获得驱动类型

def  drivertype():

	drivertypef= open("./drivertype", "r")   
	drivertypes = drivertypef.readline()
	drivertypes=drivertypes.strip('\n')
	drivertypef.close()

	return(drivertypes)


######  获得环境变量

def getenvs(string):

	try:
		envs=os.environ[string]   
		return envs
	except:
		return ""	   







