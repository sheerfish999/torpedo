# -*- coding: utf-8 -*-

import sys
import socket
import traceback

import struct


from frame import *   #### 用于载入变量设置和业务用例

##### 载入配置变量
config=openfiles("config.py")
exec(config)



#########################################

if __name__ == '__main__':  


	while True:
		try:

			try:  #网络类错误直接退出
				mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				mysocket.connect((degbug_host,debug_port))
			except:
				traceback.print_exc() 
				break

			## send
			cmdstr = input("\nSelenium Command >>> ")
			cmd=bytes(cmdstr.strip(), encoding='utf-8')  ## 这种模式需要去除空格
			mysocket.send(cmd)

			## recv
			data=""
			data=str(mysocket.recv(65534),encoding = "utf-8")   #### 指定接收的最大调试长度  

			if data:
				print(data, end='')

			## 会导致错误判断而断开，某些情况没有返回
			"""
			else:
				break   ## 为空 则代表断开 (不一定)
			"""
			

		except:
			traceback.print_exc() 

		mysocket.close()


	mysocket.close()

