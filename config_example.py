

### 用于单独文件调试时的引用
import random
from randomid import *    #####  生成各种随机量唯一值
from frame import *         #####  取系统环境变量

################################################  测试的业务流

testName="test"  ## 用于快速测试框架基本功能

############ 涉及业务功能点操作的封装

from testbaidu import *     #######  测试使用

# from XXXX import *


###############################################  驱动初始化信息:

thetimes=1   #  循环次数    失败的话会 中断本个业务流, 然后继续下个循环

get_record=0    #录像   0 不录像,  1 录像    (非linux不录像)   需要 ffmpeg 支持
get_report=0    #生成报告   0  不生成,  1 生成   (非linux不生成报告)   需要 uno 支持 , 需要 python3.  
			#支持报告即支持邮件. 邮件列表位于 maillists , #注释, 附件列表位于 attachlist, 内容 mailcontent


######  模式见下文说明

#get_type=0      # 本地 firefox    #####   gecko  驱动例如点击, 抓图等环节很多还不稳定  Action 不支持
get_type=1     # 本地 chrome       ####  目前推荐  调试使用  chromedriver版本对应关系：http://blog.csdn.net/huilan_same/article/details/51896672
#get_type=2     # 本地 ie          #### 需要将 ie 安全 "安全模式"，全部调整为相同（关闭或打开），某些产品只能使用该驱动。但速度较慢, 某些API不支持
#get_type=5	    # 本地 phantomjs   ###### 服务器使用, 某些API不支持, js弹窗不支持，需要注入解决

#get_type=10    # 本地 firefox 容器   , 通常情况下, 调试与演示建议使用10, 因为0 firefox 模式后台创建产品存在500问题,   远程自动模式推荐  5 phantomjs 
#get_type=11    # 本地 chrome 容器

#get_type=20   # 远程 firefox
#get_type=21   # 远程 chrome

######



## 容器或远程地址,  可以适应不同的情况,  当不使用容器或远程时, 这些参数无效 

"""

注意远程仍需要安装  firefox  chrome  gecko  chromedriver phantomjs   等 （都可以通过 cnpm install -g 安装，不可行则官网下载源码编译）

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
1  本地 chrome     (需要chromedriver)  
2  本地 ie  		(需要IEDriverServer)
5  本地 phantomjs   (需要phantomjs)    #  注意:  半支持系统 js 弹出alert , 需要针对性的调试

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


不打算支持:
Opera (本地的驱动不好找, 远程意义不大, 浏览器份额较小,  selenium 和 Opera 官方似乎都不再明确支持对应驱动)

还未支持：
safari

"""


###########################################  测试框架用的一些变量  ###############

testUrl="https://www.baidu.com/"
Urls=testUrl   ### 如果后文没有业务流或者没有标记，则按测试URL标记


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




##################################### 业务中需要引用的变量





