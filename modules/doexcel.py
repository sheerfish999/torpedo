# -*- coding: utf-8 -*-


#########################  本文件用于封装基本的 XLSX 操作  (操作已经存在文件)


import os,sys


import platform
sysstr = platform.system()   ### 判断操作系统类型   Windows   Linux    .   本脚本函数入口, 统一以 LINUX 为准, 其后在函数内进行转换


if sysstr == "Linux":

	"""
	####  关于 linux 平台的  uno
	#  LINUX: python3 还是 python2 根据所在发行版的源中依赖包的支持决定， 一般只支持其中一个 （centos7 支持2 ， arch/ kali 支持 3, 2016.12）
	#  具体安装过程 参考对应发行版的 uno 支持方法（不是 pip install uno , 会导致冲突）

	例如；
	suse11: zypper in openoffice-pyuno   ### 适合 python2
	centos7: yum install python-openoffice  ### 适合 python2

	"""

	import uno   
	from com.sun.star.beans import PropertyValue

if sysstr == "Windows":
	"""

	VBA 与 UNO 的 关键差别：
	1） UNO 所有行列及sheet, 第一个是0， VBA 第一个都是1
	2） UNO 函数参数次序：col, row . VBA：row,col
	3)  判断合并窗体， UNO 只有第一cell认为是 merged, VBA 认为被合并cell都是 merged,但其它cell值均为None
	4)  uno 有自己的高度和宽度单位， 基本换算比为 4.4:1000 (vba:uno)  ,  uno 自身为（openoffice:uno)  4.45:1000


	"""

	#http://analysistabs.com/vba-code
	from win32com.client import Dispatch   ### pip install pywin32  
	import win32com.client


### 入口为相对路径

def docsave(doc):    ###  文件保存  这里需要特别判断  有异常情况

	try:
		if sysstr == "Linux":
			doc.store()
		if sysstr =="Windows":
			doc.Save()
	except:
		print(u"EXCEL结果文件可能为只读不可写,请对原用例文件'另存为'后再试.")        #####  注意目前只有这里
		sys.exit()   ## 强行退出

	

class openexcel():

	full_path=""
	document=None

	### 判断进程是否已经启动成功
	
	def __isRunservice(self):
	
		if sysstr == "Linux":

			ret=False
	
			result1= os.popen("ps -ef | grep soffice | grep -v grep").read() 
			result2= os.popen("netstat -apn | grep 2002 | grep LISTEN").read()  
			if result1!="" and result2!="":
				ret=True

			return ret

		if sysstr == "Windows":
			pass  ### windows 不需要


	### 初始化
	def __init__(self, filename):
	
		if sysstr == "Linux":

			## 只会启动一个，因此不必担心关闭问题.  但注意该端口如果不退出， 会导致之后 libreoffice 不能正常启动 （进程通过该端口操作）
			cmd="nohup soffice --headless --accept='socket,host=localhost,port=2002;urp;' --norestore --nologo --nodefault --invisible >/dev/null 2>log & "
			res=os.system(cmd)

			ret=False
			while ret==False:
				ret=self.__isRunservice()
	
			# connect   连接
			local = uno.getComponentContext()
			resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
			context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
			desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
		
			localpath=os.getcwd()+"/"
			self.full_path="file://"+ localpath + filename

			self.document = desktop.loadComponentFromURL(self.full_path ,"_blank", 0, ())
		
			if self.document==None:
				print(u"文件类型无法识别，或文件已经被程序打开并独占, 请检查 " + localpath + filename )


		if sysstr == "Windows":
			
			self.full_path=os.path.abspath(filename)
			
			#app=win32com.client.Dispatch('Excel.Application')
			app=win32com.client.DispatchEx('Excel.Application')   ### 独立进程，不影响其它进程
			
			app.Visible = 0    ## 默认为0    某些场景无效，原因不明
			app.DisplayAlerts=False    ## 不进行提示，一切按默认进行

			self.document=app.Workbooks.Open(self.full_path)
			
			if self.document==None:
				print(u"文件类型无法识别，请检查 " + self.full_path)
			

	#### 返回对应的值
	def get(self,column,row,sheet=0):


		if sys.version_info.major==2:   ## 3 默认 utf-8
			reload(sys)
			sys.setdefaultencoding('utf-8')

		value=""

		if self.document!=None:
		
			if sysstr == "Linux":
		
				sheets=self.document.getSheets().getByIndex(sheet)
				value=sheets.getCellByPosition(column,row).getString()
				
			if sysstr == "Windows":
			
				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet)
				
				#第一个是1  ， 不是 0
				row=row+1
				column=column+1

				value=sheets.Cells(row,column).Value
			
		return value



	#### 返回对应 cell 是否是合并的单元格, 注意只是首个单元格是 True
	def getmerge(self,column,row,sheet=0):


		if self.document!=None:
		
			if sysstr == "Linux":		
				sheets=self.document.getSheets().getByIndex(sheet)
				Merged=sheets.getCellByPosition(column,row).getIsMerged()
					 
	
			if sysstr == "Windows":
			
				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet)
				
				#第一个是1  ， 不是 0
				row=row+1
				column=column+1
				
				if sheets.Cells(row,column).MergeCells==True and  sheets.Cells(row,column).value!=None:   ## VBA 所有合并CELL 均能判断,但只有第一个的值非None
					Merged=True
				else:
					Merged=False
		
		
		return Merged

	#### 设置对应的值
	def set(self,column,row,value,sheet=0):


		if sys.version_info.major==2:   ## 3 默认 utf-8
			reload(sys)
			sys.setdefaultencoding('utf-8')
	

		if self.document!=None:
		
			if sysstr == "Linux":
				sheets=self.document.getSheets().getByIndex(sheet)
				sheets.getCellByPosition(column,row).setString(value)
				
				docsave(self.document)


			if sysstr == "Windows":

				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet)   			

				#第一个是1  ， 不是 0
				row=row+1
				column=column+1

				sheets.Cells(row,column).Value=value
				
				docsave(self.document)
			

	#### 设置背景颜色
	def setbgcolor(self,column,row,color,sheet=0):


		if self.document!=None:
		
			if sysstr == "Linux":	
				
				sheets=self.document.getSheets().getByIndex(sheet)
			
				if color=="green":
					sheets.getCellByPosition(column,row).setPropertyValue("CellBackColor", 0x228b22)       # 绿色
				elif color=="red":
					sheets.getCellByPosition(column,row).setPropertyValue("CellBackColor", 0xff4500)        #  红色
				elif color=="yellow":
					sheets.getCellByPosition(column,row).setPropertyValue("CellBackColor", 0xffd700)         #  黄色

				docsave(self.document)


			if sysstr == "Windows":
			
				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet)   

				#第一个是1  ， 不是 0
				row=row+1
				column=column+1

				if color=="green":
					#sheets.Cells(row,column).Interior.ColorIndex=43  ## GREEN
					sheets.Cells(row,column).Interior.Color="&H00FF00"
				elif color=="red":
					#sheets.Cells(row,column).Interior.ColorIndex=46  ## RED
					sheets.Cells(row,column).Interior.Color="&H0000FF"

				elif color=="yellow":
                                        #sheets.Cells(row,column).Interior.ColorIndex=44  ## YELLOW
					sheets.Cells(row,column).Interior.Color="&H00FFFF"
				
				docsave(self.document)


	####  设置列宽
	def setcolwidth(self,column,width=-1,sheet=0):



		if self.document!=None:
		
			if sysstr == "Linux":
			
				sheets=self.document.getSheets().getByIndex(sheet)
				oColumn=sheets.getColumns().getByIndex(column)

				if width<0:
					oColumn.setPropertyValue("OptimalWidth", True)
				else:
					#换算
					width=int(width/4.45 *1000)
					oColumn.setPropertyValue("Width", width)

				docsave(self.document)


			if sysstr == "Windows":
			
				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet)   

				#第一个是1  ， 不是 0
				column=column+1

				if width<0:
					return
				else:
					try:
						sheets.Columns(column).ColumnWidth=width
					except:
						print(u"列宽数值设置错误")

				docsave(self.document)



	#### 设置行高
	def setrowheight(self,row,height=-1,sheet=0):

		if self.document!=None:
		
			if sysstr == "Linux":
			
				sheets=self.document.getSheets().getByIndex(sheet)
				oRow=sheets.getRows().getByIndex(row)

				if height<0:
					oRow.setPropertyValue("OptimalHeight", True)
				else:
					#换算
					height=int(height/4.45 *1000)
					oRow.setPropertyValue("Height", height)

				docsave(self.document)


			if sysstr == "Windows":
				
				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet)   

				#第一个是1  ， 不是 0
				row=row+1

				if height<0:
					return
				else:
					try:
						sheets.Rows(row).RowHeight=height

					except:
						print(u"行高数值设置错误")
                                                
				docsave(self.document)



	#### 得到 sheet 数量
	def getsheetcount(self):


		if self.document!=None:
		
			if sysstr == "Linux":
				count=self.document.getSheets().getCount()

			if sysstr == "Windows":
				count=self.document.Worksheets.Count

		return count
		
		
	#### 得到对应 sheet 页名字
	def getsheetname(self,sheet=0):

		if self.document!=None:
		
			if sysstr == "Linux":
		
				sheets=self.document.getSheets().getByIndex(sheet)
				name=sheets.getName()

			
			if sysstr == "Windows":
			
				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet) 
				
				name=sheets.Name				


		return name

	#### 激活对应的 sheet 页
	def activesheet(self,sheet=0):

		if self.document!=None:
		
			if sysstr == "Linux":
			
				sheets=self.document.getSheets().getByIndex(sheet)
				controller = self.document.getCurrentController()
				controller.setActiveSheet(sheets)

				docsave(self.document)

			if sysstr == "Windows":
				
				sheet=sheet+1		### 第一个是1  ， 不是 0
				sheets=self.document.Worksheets(sheet)   

				sheets.Activate()

				docsave(self.document)


	#### 退出
	def quit(self):
	

		if self.document!=None:
		
			if sysstr == "Linux":
				try:
					docsave(self.document)
					self.document.dispose()
				except:
					pass	

			if sysstr == "Windows":
				try:
					self.document.Close(SaveChanges=1)     ### 这里可能有只读的特例没有处理
				except:
					pass	
		



################################################  测试

if __name__ == '__main__':  


	xlsx=openexcel("./test/example.xlsx")
	
	xlsx.set(2,30,"1234",0)
	
	print(xlsx.get(0,1))
	print(xlsx.getmerge(0,1))
	print(xlsx.getsheetcount())

	print(xlsx.getsheetname())

	xlsx.setcolwidth(0,9)
	xlsx.setrowheight(0)


	xlsx.setbgcolor(8,8,"green")
	xlsx.setbgcolor(9,8,"red")
	xlsx.setbgcolor(10,8,"yellow")

	xlsx.activesheet()

	xlsx.quit()










	
