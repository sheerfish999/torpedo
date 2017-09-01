# -*- coding: utf-8 -*-

#####################  本脚本用于录像 , 生成的录像  建议使用 mplayer 播放, smplayer 可能会出错

from PIL import Image  # pip install pillow
#from PIL import ImageGrab
from PIL import ImageDraw
from PIL import ImageFont

import os,time,datetime,sys

import platform

import pyscreenshot as ImageGrab   #pip install pyscreenshot

#线程,  但是效率没有提升.  python2  thread,  python3  _thread
if sys.version_info.major==2:
	import thread as _thread
if sys.version_info.major==3:
	import _thread

#from rq import Queue   #用队列提高效率   #pip3 install rq   , 只适用 redis   ,  同理  pip3 install Celery
import multiprocessing


from frame import *         #####  取系统环境变量


'''  由于抓图需要进行一定的对象控制, 所以需要在内部使用异步

各项效率对比, reguser  到 绑卡环节:

1  不抓图   1:12   , 设定元素轮询时间的影响不大
2  抓图, 不使用任何的方法   1:52
3  使用线程   1:45-1:53   略微提高
4  使用multiprocessing    1:36-:45   目前手段中相对较快的

'''


######################################


##########  录像抓图,    需要首先创建 pic 文件夹

#### 抓图动作, 支持各种系统,     如果 size!=0,  调用动作方法2 , 不依赖 selenium 和 元素坐标, 适用于没有元素的情况下, 如 alert
def catchthepics(browser,location,savepath, size=0):


	try:
		if size!=0:
			catchthepics2(browser,location,savepath,size)  #  不依赖 selenium的元素定位
		else:
			browser.save_screenshot(savepath)   # selenium 抓取的屏幕太长, 是整个浏览器的
	except:
		return(0)   ## htmlunit  不支持 抓屏


	#  ImageGrab  只适合OSX WIN , 而且抓的是外部的
	# imcatch = ImageGrab.grab()
	# imimcatch.save(savepath,'jpeg')

	im = Image.open(savepath)

	if location!=0:   # selenium 抓取的屏幕太长, 是整个浏览器的

		###   转换 JPEG  , 不压缩和转换格式的话, 合成录像有问题. selenium 输出为 png格式， ffmpeg需求为 jpg格式


		####  必须要处理长宽, 以便合成的视频宽比是对的

		width, height = im.size

		howmuch=250    #调整的尺寸
	
		#当前位置的上下
		top = location['y']-howmuch   ## 上边-
		bottom=location['y']+howmuch   ## 下边+

		if top<0 :		## 超过最上则向下
			top=0
			bottom=bottom+howmuch
	
		if bottom>height:       ## 超过最下则向上
			bottom=height
			#top=top-howmuch   ##这句由于动画问题, 可能会产生错误

		im = im.crop((0,top,width,bottom))        


	### 打印测试时间
	#  cp arial.ttf /usr/share/fonts/
	#  cd /usr/share/fonts/
	#  yum install -y fontconfig mkfontscale
	#  mkfontscale
	#  mkfontdir
	#  fc-cache -fv

	#font = ImageFont.truetype("arial.ttf",size=12)   # 字体大小设定无效  ， 且需要安装字体
	times=str(datetime.datetime.now())
	draw = ImageDraw.Draw(im)
	draw.text((0, 0),times,(255,0,0))
	draw = ImageDraw.Draw(im)

	##保存

	# 解决一个pillow兼容性问题 IOError: cannot write mode RGBA as JPEG
	if im.mode in ('RGBA', 'LA'):
		im = im.convert("RGB")

	pos=savepath.find('.png')

	filename=savepath[:pos]

	savepath=filename+".jpg"

	im.save(savepath, "JPEG",quality=100)


	#调整到指定大小可能非常模糊
	"""
	w=800
	h=550
	im.resize((w, h)).save(savepath, "JPEG",quality=100)  
	"""

####  抓图动作方法2 , 不依赖 selenium 和 元素坐标
def catchthepics2(browser,location,savepath,size):

	#locations=browser.get_window_position()
	#size=browser.get_window_size()

	x1=location['x']
	y1=location['y']

	width=size['width']
	height=size['height']

	x2=x1+width
	y2=y1+height
	im = ImageGrab.grab(bbox=(x1,y1,x2,y2))

	im.save(savepath,'png')



#### 录像用抓图, 文件名排序 , 同时使用线程的方法
def recordpicthread(browser,location):    

	####  获得是否录像的标记位
	records=get_records_tag()

	if records==0:        #不录像
		return(0)


	"""
	# 以下方式无法判断 htmlunit
	##### htmlunit  不支持录像输出
	types=str(browser)
	if "htmlunit" in types:
		return(0)
	"""


	####  获得id号
	recidf = open("./pic/id", "r")   
	recid = recidf.readline()  
	recidf.close()

	recidlong=int(recid)

	####  补齐生成文件名
	PICIDtr=str(recidlong)
	savepath=PICIDtr.zfill(8)    # 8位补齐
	  
	savepath="./pic/temp" + savepath +".png"
	#print(savepath)

	#### 抓图:
	ret=catchthepics(browser,location,savepath)
	if ret==0:
		return(0)

	###  id 号+1  写回
	recidlong=recidlong+1
	PICIDtr=str(recidlong)
	#print("rec id:" + PICIDtr)
	os.system("echo " + PICIDtr + " > ./pic/id")



def recordpic(browser,location):

	# _thread.start_new_thread(recordpicthread,(browser,location))    #使用线程, 但是效率没有明显提高
	#Queue(recordpicthread(browser,location))   #队列方式复杂化

	### windows 支持这个线程方法有点问题
	if platform.system()=="Linux":
		p = multiprocessing.Process(target=recordpicthread, args=(browser,location))    # multiprocessing  目前相对较快的方式
		p.start()
		
	if platform.system()=="Windows":
		recordpicthread(browser,location)
	####


#########  录像合成,  需要首先创建 reports 文件夹

def catchpicsave(savename):


	####  获得是否录像的标记位
	records=get_records_tag()

	if records==0:        #不录像
		return(0)


	"""
	# 以下方式无法判断 htmlunit
	##### htmlunit  不支持录像输出
	types=str(browser)
	if "htmlunit" in types:
		return(0)
	"""

	time.sleep(3)   ### 等待文件写回

	# 生成
	savename=  "./reports/" + savename + ".mp4"

	### framerate 越小，显示越慢 
	### 尺寸相当于 -s 1600*800

	cmd="ffmpeg  -framerate 3  -loglevel -8 -i ./pic/temp%08d.jpg ./"  + savename
	print(cmd)

	os.system(cmd)     # 8位文件名补齐的图片,  数字表示每秒几帧图片
	print("录像名称: " +savename)

	## 清理环境
	'''
	os.system("rm -rf ./pic/*.jpg")
	os.system("rm -rf ./pic/*.png")
	os.system("rm -rf ./pic/id")
	'''

	#delete_files('./pic/',"*.jpg")
	#delete_files('./pic/',"*.png")
	#delete_files('./pic/',"id")	



##########  抓取指定对象的截图, 用于保存用于识别等

def catchelepic(browser,xpathstr,savename):

	savepath="./pic/" +  savename + ".png"

	imgelement = browser.find_element_by_xpath(xpathstr)  
	location = imgelement.location
	size = imgelement.size
	browser.save_screenshot(savepath)

	im = Image.open(savepath)
	left = location['x']
	top = location['y']
	right = left + size['width']
	bottom = location['y'] + size['height']
	im = im.crop((left,top,right,bottom))
	im.save(savepath)








