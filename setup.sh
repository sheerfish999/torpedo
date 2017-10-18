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

#apt install xdg-utils xvfb x11-xkb-utils  # debian
yum install xdg-utils xorg-x11-server-Xvfb xorg-x11-xkb-utils # centos
pip install -U xvfbwrapper

pip install -U imagehash


