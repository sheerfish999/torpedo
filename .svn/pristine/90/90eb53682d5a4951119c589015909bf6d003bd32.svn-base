# -*- coding: utf-8 -*-

#################   本脚本用户生成各种随机量唯一值

import random
import time
import datetime
import uuid
import hashlib


################# 用户名

def getname():

	uuids=uuid.uuid1()   # uuid1单一不能实现随机

	m = hashlib.md5()    #md5 非对称
	m.update(str(uuids).encode('utf-8'))
	names= m.hexdigest()   

	names=names[:8]    #截取
	names="t"+ names   #首字符为字母

	#print("Name: " + names)

	return(names)


#################  手机号

def getphone():

	phone=random.choice(['131','132','133','134','135','136','137','138','139','188','185','151','158'])+"".join(random.choice("0123456789") for i in range(8))

	#print("Phone: " + phone)

	return(phone)

################ 身份证号  2.0    准确率比较低

def getdistrictcode(): 

	DC_PATH="districtcode.txt"   #### 区码文件

	with open(DC_PATH) as file:    
		data = file.read() 
		districtlist = data.split('\n') 
	for node in districtlist: 
		#print node 
		if node[10:11] != ' ': 
			state = node[10:].strip() 
		if node[10:11]==' 'and node[12:13]!=' ': 
			city = node[12:].strip() 
		if node[10:11] == ' 'and node[12:13]==' ': 
			district = node[14:].strip() 
			code = node[0:6] 
			codelist.append({"state":state,"city":city,"district":district,"code":code})

def getcardid_2(): 

	global codelist 
	codelist = [] 
	if not codelist:
		getdistrictcode()
	id = codelist[random.randint(0,len(codelist))]['code'] #地区项 
	id = id + str(random.randint(1930,2013)) #年份项 
	da = datetime.date.today()+ datetime.timedelta(days=random.randint(1,366)) #月份和日期项 
	id = id + da.strftime('%m%d') 
	id = id+ str(random.randint(100,300))#，顺序号简单处理 

	i = 0
	count = 0
	weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #权重项
	checkcode ={'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'5','9':'3','10':'2'} #校验码映射 
	for i in range(0,len(id)): 
		count = count +int(id[i])*weight[i] 
		id = id + checkcode[str(count%11)] #算出校验码 
		return id


################  身份证号  3.0   未测试 

def getcardid_3():

	id = '110108' #地区项
	id = id + str(random.randint(1930,2016)) #年份项 
	da = date.today()+timedelta(days=random.randint(1,366)) #月份和日期项 
	id = id + da.strftime('%m%d') 
	id = id+ str(random.randint(100,300))#，顺序号简单处理 
	#     print '身份证前17位:',id
	count = 0
	weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2] #身份证前17数字的权重项 
	checkcode ={'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'4','9':'3','10':'2'} #余数映射校验码字典
	n = len(id)
	for i in range(n): 
		count = count +int(id[i])*weight[i] #求出身份证号前17位数字，每一位数字与权重相乘后的总和
	#     print count    
	id = id + checkcode[str(count%11)] #总和对11取余数，根据余数映射的验证码字典，得出校验码 
	return id



################  身份证号  1.0   不是非常准确

def getcardid():

	ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
	LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')

	t = time.localtime()[0]
	x = '%02d%02d%02d%04d%02d%02d%03d' %(random.randint(10,99),
	random.randint(1,99),
	random.randint(1,99),
	random.randint(t - 80, t - 18),
	random.randint(1,12),
	random.randint(1,28),
	random.randint(1,999))

	y = 0
	for i in range(17):          #### 校验码
		y += int(x[i]) * ARR[i]

	cardids='%s%s' %(x, LAST[y % 11])
	#print("ID card: " + cardids)

	return(cardids)


################## 农行卡卡号


def getfarmbankid():

	cardtag="622848"

	# 622848后   0987654320000, 共 13 位

	x ='%04d%04d%04d%d' %(random.randint(1,9999),
		random.randint(1,9999),
		random.randint(1,9999),
		random.randint(0,9))
	
	farmbankid=cardtag+x

	#print("FarmBank Cardid: " + farmbankid)

	return(farmbankid)




##################  测试


if __name__ == '__main__':  

	for i in range(1,5):
		print(str(i)+":")
		print(getname())
		print(getphone())
		print(getcardid())
		print(getfarmbankid())












