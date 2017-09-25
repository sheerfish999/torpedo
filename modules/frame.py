# -*- coding: utf-8 -*-

import sys,os
import codecs

import glob

########################  本脚本用于载入变量设置和业务用例 等通用操作


######  载入文本内容

def openfiles(filename):


	paths=os.getcwd()    #绝对路径  , os.getcwd()  代替  sys.path[0]
	all_the_text = codecs.open(paths + "/"+ filename,'r','utf-8').read( )

	if sys.version_info.major==2: 
		all_the_text=all_the_text.encode('utf8','ignore')    ### windows 下编写的用例可能需要转码

	return(all_the_text)


######  获得驱动类型

def  drivertype():

	drivertypef= open("./drivertype", "r")   
	drivertypes = drivertypef.readline()
	drivertypes=drivertypes.strip('\n')
	drivertypef.close()

	return(drivertypes)


######  获得是否进行报告的标记

def get_reports_tag():

	####  获得是否报告的标记位
	reportf = open("./reportset", "r")   
	reports = reportf.readline()
	reports=reports.strip('\n')

	reports=int(reports)

	reportf.close()

	return reports


######  获得是否进行录像的标记

def get_records_tag():

	recordf = open("./recordset", "r")   
	records = recordf.readline()
	records=records.strip('\n')

	records=int(records)

	recordf.close()

	return records


######  获得环境变量 (一般 jenkins 使用)

def getenvs(string):

	try:
		envs=os.environ[string]   
		return envs
	except:
		return ""	   


#####  删除某个路径下通配符匹配的文件

# delete_files('./1/', '*.txt')

def files(curr_dir, ext ):

    for i in glob.glob(os.path.join(curr_dir, ext)):
        yield i

def delete_files(curr_dir, ext):

	for i in files(curr_dir, ext):
		os.remove(i)



######### 临时断点当前代码，用于远程调试

def pause():

	while True:
		pass



