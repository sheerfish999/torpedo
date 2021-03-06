

# 本文件改名为  config.py 即可使用



### 用于单独文件调试时的引用
import random
from randomid import *    #####  生成各种随机量唯一值
from frame import *         #####  取系统环境变量

try:
	sys.path.append(sys.path[0] + "/../")   # 涉及一些特殊情况的路径包含，比如调试模式
except:
	pass

sys.path.append(sys.path[0] + "/case/")  ## 测试用例的路径

################################################  测试的业务流    ################## 请配置这段


############ 1 测试框架的入口，测试用例留.   如用例名称为  case/test.py 则  testName="test"

testName="test"  

############ 2 涉及业务功能点操作的其它封装库  (建议放置于 case 目录下)

from testbaidu import *

############ 3 起始地址信息  ###############

testUrl="https://www.baidu.com/"
Urls=testUrl


###############################################  驱动初始化信息: 

thetimes=1   #  循环次数    失败的话会 中断本个业务流, 然后继续下个循环

get_record=0	#录像   0 不录像,  1 录像      需要 ffmpeg 支持
get_report=0	#生成报告   0  不生成,  1 生成  linux 需要 openoffice + pyuno 支持 ; windows 需要 ms-office  
				#支持报告即支持邮件. 邮件列表位于 maillists , #注释, 附件列表位于 attachlist, 内容 mailcontent


######  可用驱动配置，模式依赖及更多模式见下文说明

if getenvs('get_type')=="":   ## 使用环境变量地址

	# 0-10 本地浏览器
	#get_type=0      # 本地 firefox    #####   gecko  驱动例如点击, 抓图等环节很多还不稳定  Action 不支持
	#get_type=0.1    # 本地 firefox 无头模式
	get_type=1     	 # 本地 chrome       ####  目前推荐  调试使用  chromedriver版本对应关系：http://blog.csdn.net/huilan_same/article/details/51896672
	#get_type=1.1    # 本地 chrome 无头模式
	#get_type=2     # 本地 ie  windows #### 参考 support 中如何支持 ie 。速度较慢, 某些API不支持. 
	#get_type=5	    # 本地 phantomjs   ###### 服务器使用, 某些API不支持, js弹窗不支持，需要注入解决.  selenium 官方已经不再推荐

	# 10-19 本地容器
	#get_type=10    # 本地 firefox 容器   , 通常情况下, 调试与演示建议使用10, 因为0 firefox 模式后台创建产品存在500问题,   远程自动模式推荐  5 phantomjs 
	#get_type=11    # 本地 chrome 容器

	# 20-30 远程模式
	#get_type=20   # 远程 firefox
	#get_type=21   # 远程 chrome

else:
	get_type=float(getenvs('get_type'))

######

## 用于动态调试的地址   执行：debug_client.py   调试：debug_content.py
degbug_host="127.0.0.1"
debug_port=18000

######


## 容器或远程地址,  可以适应不同的情况,  当不使用容器或远程时, 这些参数无效 

"""

注意远程仍需要安装  firefox  chrome  gecko  chromedriver phantomjs   等 （都可以通过 cnpm install -g 安装，不可行则官网下载源码编译）
建议使用 selenium-alone 的容器，可避开包的依赖关系

server:
wget https://selenium-release.storage.googleapis.com/3.4/selenium-server-standalone-3.4.0.jar
启动 java -jar selenium-server-standalone-3.4.0.jar
或者
npm install selenium-standalone@latest -g
selenium-standalone install
selenium-standalone start   # jdk 版本太低：java.lang.UnsupportedClassVersionError: org/openqa/grid/selenium/GridLauncherV3 : Unsupported major.minor version 52.0

默认操作及控制台端口 http://ip:4444   

"""

remotedriverip="192.168.4.126"
remotedriverport="4444"
remotedriverip=remotedriverip+":" + remotedriverport    ## 完整地址

## 容器调用前的初始化命令或脚本名
dockerinitsh=""

########

"""  测试模式和驱动说明    get_type   注意已经定义的, 勿修改, 涉及较多位置关联
本地模式:
0  本地 firefox  (3.0 以上版本 firefox需要geckodriver, 并且较新 注意版本与浏览器的匹配会影响操作: https://github.com/mozilla/geckodriver/releases/)
0.1 本地 firefix 无头模式 (firefox>56)
1  本地 Chrome  (需要chromedriver)
1.1 本地 Chrome 无头模式 (chrome>59) 
2  本地 Ie  	(需要IEDriverServer windows)
3  本地 Opera  	(需要operadriver)      # 暂时没有明确测试, 且不推荐使用，受支持较少
4  本地 Safari  					   # 暂时没有明确测试
5  本地 phantomjs   (需要phantomjs)    #  注意:  半支持系统 js 弹出alert , 需要针对性的调试

虚拟界面终端模式：  linux 特有
6  本地 Firefox 虚拟界面终端 (需要xvfb)   # 暂时没有明确测试
7  本地 Chrome 虚拟界面终端 (需要xvfb)    # 暂时没有明确测试
8  本地 Opera  虚拟界面终端 (需要xvfb)    # 暂时没有明确测试

容器模式:  避免了driver 版本以及 python 库\浏览器的版本对应关系造成出现的莫名其妙的问题, 可供日常显示调试和演示
10  本地firefox容器  (容器需要docker支持和设置)  
11  本地chrome容器   (容器需要docker支持和设置)   	
15  本地htmlunit 容器 不显示页面, 速度更快    ### 暂时没有明确测试

远程模式:    selenium-server-standalone  -role hub  或   -role node  -hub http://localhost:4444/grid/register   
或使用 官方容器 hub, 可避开phantomjs不支持的情况, 支持多并发(适合jenkins, 免转ghostdriver的模式).  

20  远程firefox		比 phantomjs 要慢, 注意暂时抓图不正确, 还未进行调研和修改
21  远程chrome		比 phantomjs 要慢, 注意暂时抓图不正确, 还未进行调研和修改

25  远程 htmlunit   貌似意义不大
# 需要htmlunit特别的 jar : htmlunit-driver-standalone   https://github.com/SeleniumHQ/htmlunit-driver/releases    --- 调试中 
# jar 包权限:  644,   java -cp htmlunit-driver-standalone-2.21.jar:selenium-server-standalone-2.53.0.jar org.openqa.grid.selenium.GridLauncher



"""

########################################### 百度云OCR

# 通过百度云创建OCR应用获得 (免费日500)
ocr_client_id="3567is0MyuhRQeUP0QdYgMZt"
ocr_client_secret="scbzdg9mMsZLEaL7nd8s2DxItD50OKLH"


######################################   邮件  ##########################

## 可能被 子函数 exec, 这种情况下必须 global

global mail_host
global mail_user
global mail_pass
global mail_postfix

mail_host="mail.xxxxx.com"   
mail_user="xxxxxx"   
mail_pass="xxxxxxxx"   
mail_postfix="xxxxx.com"  #发件箱的后缀




