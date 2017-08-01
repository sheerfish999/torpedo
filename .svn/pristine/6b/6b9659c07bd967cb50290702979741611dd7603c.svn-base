# -*- coding: utf-8 -*-


###### 本脚本用于发送邮件

import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication


## 以下用于特别引用
from frame import *   #### 用于载入变量设置和业务用例


# 发送邮件动作  邮件服务器位置, 用户名, 密码, 邮箱后缀,  标题, 内容

def sendmaill(mail_host,mail_user,mail_pass,mail_postfix, to_list, sub,content):

	if sys.version_info.major==2:   ## 3 默认 utf-8
		reload(sys)
		sys.setdefaultencoding('utf-8')

	#####

	msg = MIMEMultipart('alternative')    ## 创建一个实例

	#mailtype="text"  
	mailtype="html"	

	if mailtype=="html":
		heads="<head><meta http-equiv='Content-Type' content='text/html; charset=utf-8' /> </head>"
		content=content.replace("\n","<br>")
		msgcontent = MIMEText(heads + content,_subtype='html',_charset='utf-8')    

	if mailtype=="text":
		msgcontent = MIMEText(content,_charset='utf-8')   

	msg.attach(msgcontent)

	me="Auto-Report"+"<"+mail_user+"@"+mail_postfix+">"   #发送人姓名
	msg['Subject'] = sub    #设置主题
	msg['From'] = me
	msg['To'] = ";".join(to_list)  

	### 附件列表

	attachlist="attachlist"     ### 默认的附件列表文件, 可以生成该文件

	file_object= open(attachlist)             
	attach_list = file_object.readline() 
	
	while attach_list: 

		attach_list=attach_list.replace('\n','')    #处理换行

		if len(attach_list)>1:            # 行有内容

			data = open(attach_list, 'rb') 
			file_msg = MIMEApplication(data.read( ))    ### 可以应对所有文件类型
			data.close( )

			file_msg.add_header('Content-Disposition', 'attachment', filename = attach_list)  
			msg.attach(file_msg)

		attach_list = file_object.readline() 

	file_object.close()  


	### 发送

	try:  

		#s= smtplib.SMTP()   ## 常规模式, 在禁止非常规的模式的情况下, 可能 报  SMTPAuthenticationError(550, 'User suspended')
		s = smtplib.SMTP_SSL()    ## SSL  模式
		
		print("connect....")
		s.connect(mail_host)  #连接smtp服务器
		print("login....")
		s.login(mail_user,mail_pass)  #登陆服务器
		print("send....")
		s.sendmail(me, to_list, msg.as_string())  #发送邮件
		s.close()  
		time.sleep(1)   #避免被服务器认为是攻击
		return True  
	except: 
		print(sys.exc_info())   
		return False	


		