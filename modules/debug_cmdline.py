# -*- coding: utf-8 -*-

import sys
import socket
import traceback

from frame import *   #### 用于载入变量设置和业务用例

##### 载入配置变量
config=openfiles("config.py")
exec(config)


while 1:
	try:

		try:  #网络类错误直接退出
			mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			mysocket.connect((degbug_host,debug_port))
		except:
			traceback.print_exc() 
			break

		## send
		cmdstr = input("Selenium Command >>> ")
		cmd=bytes(cmdstr,encoding='utf-8')
		mysocket.send(cmd)

		## recv
		data=""
		data=str(mysocket.recv(20480),encoding = "utf-8")

		if data:
			print(data, end='')
		else:
			break   ## 为空 则代表断开

	except:
		traceback.print_exc() 

	mysocket.close()


mysocket.close()



