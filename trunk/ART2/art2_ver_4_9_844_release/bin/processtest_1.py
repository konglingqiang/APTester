#coding=utf-8
import sys
import os
import subprocess

print os.getcwd()
popen = subprocess.Popen(["cart.exe"],stdout=subprocess.PIPE)
# #写入命令数据
# artin=popen.stdin
# artin.writelines("help")
# #先做一下简单的验证，看是否能得到结果，命令是否生效等。
# desc=['----------------------------------------------------------------------------------']

special_a=""
while True:
    try:
        aout = popen.stdout.readline()
        #
        if '----------------------------------------------------------------------------------' in aout:
            special_a = aout
            aout = "4000"
        elif 'Tester 1 SN:	IQXL' in aout:
            popen.stdout.readline()
            aout = special_a.replace(
                '----------------------------------------------------------------------------------',
                popen.stdout.readline())
            # aout=aout.replace("\r","")
        if "" == aout:
            break
    except Exception as e:
        print "error"
    print aout



