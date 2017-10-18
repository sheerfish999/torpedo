# -*- coding: utf-8 -*-

##### 本文件用于编写动态调试代码， 对象名称  browser
##### 修改后成后执行 debug_content.sh 或  debug_content.bat  即可实现在线调试


browser.get("http://www.baidu.com")

show_where(browser,".//*[@id='su']")


#unpause()  ## 继续运行

