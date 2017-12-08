# -*- coding: utf-8 -*-

####### 本文件用于图像高级处理相关功能

from PIL import Image   # pip install pillow
import imagehash   # pip install imagehash

import time,datetime

from randomid import *
from finddoit import *

########## 在图像对象中查找图像的坐标 （对象需要相同的分辨率下抓取的对象）

"""
颜色特征越明显越容易查找
块越大越容易查找

"""

"""
在 img2 中查找 img1 ;  
block 查找像素跳跃度，越低越慢精度越高. 一般按钮需要3-4，有时更高能准确识别但时间更长，这个数字和被识别的对象的大小有关，越大、像素越明显越容易识别，块跳跃往往可越大; 
pre 可接受精度, 最大为1 完全匹配，最低为0，一般默认在0.8以上才能认为相同，在可接受精度内没有发现，则返回为 (-1,-1), 否则返回最优的坐标 (x,y)， 默认为 0.8
zoom 缩放提高效率比，越大速度越快，识别率越低, 默认>=1 , 完全不压缩则 =1
onlyonce 是否选择第一个达到匹配的对象，默认为1 速度最快但可能出错， 反之为0，表示选择范围内最匹配对象 

建议使用调试模式， browser.save_screenshot(pic) 截取图像后，在对应截图中抓取对应的对象图像，保持分辨率一致

"""

def getpic_pos(img1,img2,block=4,pre=0.8,zoom=1.2,onlyonce=1):

	print(u"进行图像搜索.")
	timestart = datetime.datetime.now()

	(x1,y1)=img1.size   # 小图片
	(x2,y2)=img2.size   # 大图片

	#### 缩放图片，提高效率

	width=int(x2/zoom)
	height=int(y2/zoom)
	img2 = img2.resize((width, height),Image.ANTIALIAS)

	width=int(x1/zoom)
	height=int(y1/zoom)
	img1= img1.resize((width, height),Image.ANTIALIAS)

	(x1,y1)=img1.size   # 小图片
	(x2,y2)=img2.size   # 大图片

	#####

	hash1 = imagehash.average_hash(img1)

	thex=-1
	they=-1
	bestret=36
	pre=(1-pre)*36    # 完全不同为 36, 完全相同为 0

	if block<1:
		block=1

	for x in range(0,x2,block):
 
		if x+x1-1>x2:  # 超出比较范围
			break

		for y in range(0,y2,block):

			if y+y1-1>y2:  # 超出比较范围
				break

			region = (x,y,x+x1,y+y1)
			#裁切图片

			cropImg = img2.crop(region)
			hash2 = imagehash.average_hash(cropImg)
			ret=hash2-hash1

			if ret<=pre and ret<bestret:   # 最优

				thex=x
				they=y

				bestret=ret

				#print(ret,thex,they)

				if onlyonce==1:
					break


	if thex!=-1:

		### 调试

		"""

		region = (thex,they,thex+x1,they+y1)

		#裁切图片
		cropImg = img2.crop(region)

		# 解决一个pillow兼容性问题 IOError: cannot write mode RGBA as JPEG
		if cropImg.mode in ('RGBA', 'LA'):
			cropImg = cropImg.convert("RGB")

		cropImg.save(r'./reports/imgext_get.jpg')  ## 调试输出位置

		"""

		##### 恢复到原始比例

		thex=int(thex*zoom)
		they=int(they*zoom)

		timesend = datetime.datetime.now()
		ret=str(round((timesend-timestart).total_seconds(),2))

		print(u"搜索用时:",ret,"s")

	else:

		print(u"没有搜索到图像.")




	return(thex,they)


def getpic_pos_fromfile(imgfile1,imgfile2,block=4,pre=0.8,zoom=1.2,onlyonce=1):  

	img1=Image.open(imgfile1)
	img2=Image.open(imgfile2)


	(x,y)=getpic_pos(img1,img2,block,pre,zoom,onlyonce)


	return x,y


##### 按照图像模式识别的对象

class img_ele():

	left=-1
	top=-1
	width=-1
	height=-1
	driver=None
	xpath=None

	def click(self):

		if self.left!=-1:

			"""
			x=int((self.left+self.width)/2)
			y=int((self.top+self.height)/2)
			"""

			try:
				clicks(self.driver, self.xpath)
			except:
				pass


# parent_element 是父对象的xpath, 如果能找到这个对象将极大提升查找对应图片的查找速度
def getpic_pos_fromdriver(browser,imgfile,block=4,pre=0.8,zoom=1.2,onlyonce=1, parent_element_xpath=""):

	wholepic="./logs/wholeget.png"
	browser.save_screenshot(wholepic)

	left=0
	top=0

	img1=Image.open(imgfile)

	if parent_element_xpath!="":   # 某个元素范围内查找

		### 可能是隐形范围，不需要 located displayed
		#lastele=waitfor_ele(browser,parent_element_xpath)
		#location=showfor_record(browser,lastele,parent_element_xpath)

		lastele=browser.find_element_by_xpath(parent_element_xpath)
		location = lastele.location		


		im = Image.open(wholepic)

		size = lastele.size
		left = location['x']
		top = location['y']
		right = left + size['width']
		bottom = location['y'] + size['height']
		im = im.crop((left,top,right,bottom))
		
		#im.save(wholepic) #调试
		img2=im

	else:
		img2=Image.open(wholepic)


	(x,y)=getpic_pos(img1,img2,block,pre,zoom,onlyonce)

	if x!=-1:  # 否则返回空元素

		(x1,y1)=img1.size   # 小图片

		imgele=img_ele()
		imgele.left=x+left   # 加上相对位置
		imgele.top=y+top   # 加上相对位置
		imgele.width=x1
		imgele.height=y1
		imgele.driver=browser

		tempid=show_where_imgele(browser,imgele)   # 显示并 返回 id
		imgele.xpath="//*[@id='"+tempid + "']"

		return imgele



#### 使用坐标显示某个坐标范围 或已经识别的对象  增加一个透明的 div 元素

def show_where(browser,left,top,width,height):

	tempid='img'+getname()  ## 设定id 用于操作

	### 边距在外、 最下，避免无法操作实际元素
	if left-5>0:
		left=left-5

	if top-5>0:
		top=top-5

	js="var Odiv=document.createElement('div');Odiv.setAttribute('id','"+tempid+"');"
	js=js+"Odiv.style.cssText='width:" + str(width+10) + "px;height:" + str(height+10) +"px;left:" + str(left) + "px;top:" + str(top) +"px;position:absolute;border:1px solid #F00;z-index:0';"
	js=js+"document.body.appendChild(Odiv);"

	#print(js)

	browser.execute_script(js)

	return tempid


def show_where_imgele(browser,imgele):
	
	if imgele.left!=-1:
		tempid=show_where(browser,imgele.left,imgele.top,imgele.width,imgele.height)

		return tempid



################################################  测试

if __name__ == '__main__':

	(x,y)=getpic_pos_fromfile('./test/getimg2.png','./test/getimg1.png')
	print(x,y)



