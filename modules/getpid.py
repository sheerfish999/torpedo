# -*- coding: utf-8 -*-


################### 本脚本用于查找 windows 进程 pid

import os
import sys
import string
import psutil  # pip install psutil
import re

def get_pid(name):

	process_list = list(psutil.process_iter())
	regex = "pid=(\d+),\sname=\'" + name + "\'"
	#print(regex)
	pid = -1

	for line in process_list:

		process_info = str(line)
		ini_regex = re.compile(regex)
		result = ini_regex.search(process_info)

		if result != None:
			pid = int(result.group(1))
			#print(result.group())
			return pid
			#break

if __name__ == "__main__":

	pid=get_pid(sys.argv[1])
	print(pid)