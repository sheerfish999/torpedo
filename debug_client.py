# -*- coding: utf-8 -*-

import sys
import socket

sys.path.append(sys.path[0] + "/modules/")    #python 2.7 对   modules.  的方式兼容不好
from frame import *   #### 用于载入变量设置和业务用例

##### 载入配置变量
config=openfiles("config.py")
exec(config)

mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mysocket.connect((degbug_host,debug_port))

cmdstr=openfiles("debug_content.py")

cmd=bytes(cmdstr,encoding='utf-8')

mysocket.send(cmd) 

try:
	data=""
	data=str(mysocket.recv(20480),encoding = "utf-8")
except:
	pass

print(data)

mysocket.close()



