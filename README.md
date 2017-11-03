# torpedo web UI 测试框架
## 本框架基于 selenium 封装以下功能：

### 1） 同时兼容 linux 及 windows ,  python2.7 与 python3

### 2） 基础操作重新封装, 鲁棒性成倍增强

### 3） 健全的日志输出及报告生成能力、录像能力, 报告完成后的邮件发送

### 4） 多种浏览器、无头浏览器的快捷切换支持

	本地模式：
	0  本地 firefox
	1  本地 Chrome
	1.1 本地 Chrome 无头模式 (chrome>59)
	2  本地 Ie
	3  本地 Opera
	4  本地 Safari
	5  本地 phantomjs

	虚拟界面终端模式：  linux 特有
	6  本地 Firefox 虚拟界面终端
	7  本地 Chrome 虚拟界面终端
	8  本地 Opera  虚拟界面终端

	容器模式:
	10  本地firefox容器
	11  本地chrome容器   	
	15  本地htmlunit 容器

	远程模式: 
	20  远程firefox
	21  远程chrome
	25  远程 htmlunit

### 5） jenkins支持:

	maillists 收件人
	get_type 指定浏览器驱动类型，方便进行兼容测试


### 6） 测试过程中远程动态调试支持:

	设定 degbug_host 以及 debug_port
	修改 debug_content.py 执行 debug_content.sh / debug_content.bat 完成动态调试
	或直接使用单行命令行模式： debug_cmdline.sh / debug_cmdline.bat

### 7） 扩展的按图索骥功能：

	A 根据现有图片查找位置，并能够进行点击
	B 根据文字查找位置，并能够进行点击
	C 得到对应图片的文字

# 安装：

## 1)  基础安装

	setup.sh  linux
	setup.bat  windows

## 2)  配置文件

	config_example.py 更名为 config.py



