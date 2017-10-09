# -*- coding: utf-8 -*-

import sys
import socket

from frame import *   #### 用于载入变量设置和业务用例

##### 载入配置变量
config=openfiles("config.py")
exec(config)

mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mysocket.connect((degbug_host,debug_port))

cmdstr=openfiles("debug_content.py")

cmd=bytes(cmdstr,encoding='utf-8')

mysocket.send(cmd)


while 1:
	try:
		data=""
		data=str(mysocket.recv(20480),encoding = "utf-8")

		if data:
			print(data, end='')
		else:
			break   ## 为空 则代表断开

	except:
		pass


mysocket.close()



