# -*- coding: utf-8 -*-

##### 本脚本用于处理 doc 

"""
linux:
1) openoffice

2) python-office

同一个系统中(linux), 一般uno要么支持  python 2.7 , 要么支持 python 3
这是因为系统源中的支持包被安装在了其中一个, 不取决于 pip 版本. 因此同一设备支持一个python版本即可

例如；suse11
zypper in openoffice-pyuno   ### 适合 pythno2
非以下
#pip install pyoo
#pip install unotools

另一种方法：直接导入 openoffice的库路径  # https://stackoverflow.com/questions/4270962/using-pyuno-with-my-existing-python-installation

os.environ['URE_BOOTSTRAP'] ='vnd.sun.star.pathname:/usr/lib64/ooo3/program/fundamentalrc'
os.environ['UNO_PATH'] ='/usr/lib64/ooo3/program/'
os.environ['PATH'] = '$PATH;/usr/lib64/ooo3/ure/bin;/usr/lib64/ooo3/basis3.2/program;'

sys.path.append('/usr/lib64/ooo3/basis3.2/program')

遇到 uno.py 的 python 版本语法冲突时，再进行uno.py修改, 主要是 except

如果报：
ImportError: dynamic module does not define module export function  说明python版本不兼容


"""

#####  不同系统操作doc模式不同

import sys,os

import platform

if platform.system()=="Linux":

	"""
	os.environ['URE_BOOTSTRAP'] ='vnd.sun.star.pathname:/usr/lib64/ooo3/program/fundamentalrc'
	os.environ['UNO_PATH'] ='/usr/lib64/ooo3/program/'
	os.environ['PATH'] = '$PATH;/usr/lib64/ooo3/ure/bin;/usr/lib64/ooo3/basis3.2/program;'

	sys.path.append('/usr/lib64/ooo3/basis3.2/program')
	"""

	import uno   
	from com.sun.star.beans import PropertyValue
	from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK

if platform.system() == "Windows":
	#http://analysistabs.com/vba-code
	from win32com.client import Dispatch   ### pip install pywin32  
	import win32com.client


################### linux


"""
centos 安装字体：
cp arial.ttf /usr/share/fonts/
fc-cache -fv

"""


########################################################


######## 新建文档

def openthedoc():

	if platform.system()=="Linux":   

		soffice="nohup soffice --headless --accept='socket,host=localhost,port=2002;urp;' --norestore --nologo --nodefault --invisible "

		soffice=soffice + " >/dev/null 2>log &"
		os.system(soffice)

		sleep(1)  #稍等启动, 需要进行等待

		# connect   连接
		local = uno.getComponentContext()
		resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
		context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

		# load new   一个新文档
		desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
		document = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
		cursor = document.Text.createTextCursor()


	if platform.system()=="Windows":

		document=win32com.client.DispatchEx('Word.Application')   ### 独立进程，不影响其它进程
		#document=win32com.client.Dispatch('Word.Application')

		document.Visible = 0         ## 默认为0    某些场景无效，原因不明
		#document.WindowState = 2   #1表示正常，2表示最小化，3表示最大化
		document.DisplayAlerts=0    ## 不进行提示，一切按默认进行

		doc=document.Documents.Add()

		cursor=doc.Range(0,0)

	return(document,cursor)


######  插入字符

def doc_insertstring(document,cursor,strs):

	if platform.system()=="Linux":

		document.Text.insertString(cursor, strs, 0)

	if platform.system()=="Windows":

		cursor.InsertAfter(strs)


######  插入章节分隔符

def doc_insertbreak(document,cursor):

	if platform.system()=="Linux":

		xText = document.getText()
		xText.insertControlCharacter(cursor, PARAGRAPH_BREAK, False)





###### 插入图片

def doc_insertimg(document,cursor,imgpath,imgwidth,imgheight):

	if platform.system()=="Linux":

		img = document.createInstance('com.sun.star.text.TextGraphicObject') 

		img.GraphicURL = imgpath
		img.Width = imgwidth
		img.Height = imgheight

		document.Text.insertTextContent(cursor, img, False)


####### 插入表格

def doc_inserttable(document,cursor,linecount,colcount):

	if platform.system()=="Linux":

		mytable= document.createInstance("com.sun.star.text.TextTable")
		mytable.initialize(linecount, colcount)
		document.Text.insertTextContent(cursor, mytable, 0)

	return mytable

###### 表格插入字符

def table_insertstring(table,pos,strs):

	if platform.system()=="Linux":

		table.getCellByName(pos).setString(strs)


###### 表格设置属性

def table_setattr(table,pos,attrname,attrvalue):

	if platform.system()=="Linux":

		table.getCellByName(pos).setPropertyValue(attrname, attrvalue)


####### 保存文档

def savetopdf(document,savename):


	# 保存
	paths=sys.path[0]    #必须使用绝对路径

	if platform.system()=="Linux":  

		# 转换  已经废弃
		#document.storeAsURL("file://" +  paths + "/reports/" + savename + ".odt",())   
		#os.system("python3 DocumentConverter.py  ./reports/"+ savename +".odt" + " " + "./reports/" + savename + ".pdf")
		## 清理
		#os.system("rm -f  ./reports/"+ savename +".odt")


		# 转换
		property = (PropertyValue( "FilterName" , 0, "writer_pdf_Export" , 0 ),)
		savenames="./reports/" + savename + ".pdf"
		document.storeToURL("file://" +  paths + "/" + savenames ,property)

		document.dispose()


	if platform.system()=="Windows":

		savename= paths + "/" + savename +".pdf"
		document.ActiveDocument.SaveAs(savename,FileFormat=17)

		wc = win32com.client.constants
		document.Documents.Close(0)
		document.Quit()


################################################  测试

if __name__ == '__main__':  

	savename="./reports/test"

	(document,cursor)=openthedoc()

	doc_insertstring(document,cursor,"1111111111111")
	doc_insertstring(document,cursor,"2222222222222")


	savetopdf(document,savename)

