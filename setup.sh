#!/bin/bash

cp ./support/simsun.ttc /usr/share/fonts/
fc-cache -fv

localedef -c -f UTF-8 -i zh_CN zh_CN.utf8

pip install -U pip
pip install -U selenium
pip install -U hues
pip install -U pyscreenshot
pip install -U python-xlib
pip install -U pillow

yum install python-devel zbar-devel  # centos
pip install -U zbarlight

 
