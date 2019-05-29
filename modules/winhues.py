# -*- coding: utf-8 -*-



######################### 本脚本用于颜色化日志输出， 用于补充 hues 的 windows 部分   

##### windows 在某些版本条件下，一行只能一个颜色，本文件用于适应本种特点

"""  引用方法
import platform
sysstr = platform.system()  

if sysstr == "Linux":
        import hues

if sysstr == "Windows":
        import winhues as hues

"""

import sys
import time
import ctypes

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

####### 字体色

## 暗色
FOREGROUND_BLACK = 0x00 # 黑色
FOREGROUND_BLUE = 0x01 #  蓝色
FOREGROUND_GREEN= 0x02 #  绿色
FOREGROUND_CYAN = 0x03 # 青色
FOREGROUND_RED = 0x04 #  红色
FOREGROUND_PURPLE = 0x05 #   紫色
FOREGROUND_YELLOW = 0x06 # 褐色/黄色
FOREGROUND_WHITE = 0x07 #  白色
FOREGROUND_INTENSITY = 0x08 # 灰色

## 亮色
FOREGROUND_LIGHTBLUE = 0x09 # 亮蓝色

#######  背景色

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.  灰色



########################### 颜色输出部分


class Color:

    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
     
    def set_cmd_color(self, color, handle=std_out_handle):
        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool

    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    def printf(self,strs):
            #print(strs, end=' ')
            sys.stdout.write(strs)

    def whitecolor(self,strs):
            self.set_cmd_color(FOREGROUND_WHITE)  
            self.printf(strs)


    def syancolor(self,strs):
            self.set_cmd_color(FOREGROUND_CYAN  | FOREGROUND_INTENSITY)
            self.printf(strs)


    def greencolor(self,strs):
            self.set_cmd_color(FOREGROUND_GREEN  | FOREGROUND_INTENSITY)  
            self.printf(strs)

            
    def redcolor(self,strs):
            self.set_cmd_color(FOREGROUND_RED  | FOREGROUND_INTENSITY)  
            self.printf(strs)


    def yellowcolor(self,strs):
            self.set_cmd_color(FOREGROUND_YELLOW  | FOREGROUND_INTENSITY)  
            self.printf(strs)


    def purplecolor(self,strs):
            self.set_cmd_color(FOREGROUND_PURPLE | FOREGROUND_INTENSITY)  
            self.printf(strs)



##################### 日志部分


def gettimes():
        
        ISOTIMEFORMAT="%X"
        times=time.strftime(ISOTIMEFORMAT, time.localtime())

        return times


def warn(strs):

        clr = Color()

        ret=""

        ## 时间
        clr.yellowcolor(gettimes()+" - " + "WARN" + " - " + strs)

        ## 换行
        print("")

        clr.whitecolor("")




def info(strs):

        clr = Color()

        ret=""

        ## 时间
        clr.syancolor(gettimes()  + " - " +  "INFO" + " - " + strs )


        ## 换行
        print("")

        clr.whitecolor("")

def log(strs):

        clr = Color()

        ret=""

        ## 时间
        clr.whitecolor(gettimes()  + " - "  + strs)

        ##
        clr.whitecolor(" - ")

        ##
        clr.whitecolor(strs)

        ## 换行
        print("")

        clr.whitecolor("")

def error(strs):

        clr = Color()

        ret=""

        ## 时间
        clr.redcolor(gettimes()  + " - " +  "ERROR" + " - " + strs )


        ## 换行
        print("")

        clr.whitecolor("")


def success(strs):

        clr = Color()


        ret=""

        ## 时间
        clr.greencolor(gettimes() + " - " +  "SUCCESS" + " - " + strs )

        ## 换行
        print("")

        clr.whitecolor("")





################################################  测试

if __name__ == '__main__':  


    strs=u"这是一个测试"

    warn(strs)
    info(strs)
    log(strs)
    error(strs)
    success(strs)






