# -*- coding: utf-8 -*-
__author__ = 'hero'
import sys
sys.path.append("..")
from myconfig import TestConf
import exchangeData

###设备相关操作###
class DeviceOper(object):

    def __init__(self):
        testconf = TestConf()
        self.telnetObj = testconf.get_default_ip()
        username = testconf.get_username()
        password = testconf.get_password()
        self.telnetObj.read_until("login: ")
        self.telnetObj.write(username+'\n')
        self.telnetObj.read_until("Password: ")
        self.telnetObj.write(password +'\n')

    def getTelentObj(self):
        if self.telnetObj is None:
            self.telnetInit()
        return self.telnetObj

    ###校验SN合法性###
    def checkSN(self,inputSN):
        showSNCmd = 'ar_protest --MB-SN -r'
        self.getTelentObj()
        self.telnetInit.write(showSNCmd+'\n')
        snStr = self.telnetObj.read_until("~#")

        ###需要解析返回数据，读取SN条码###

        if inputSN==snStr:
            return True
        return False

    ###校验老化时间###
    def checkAgeTest(self):
        eData = exchangeData.ExchangeData()
        max_hour = eData.loadTestConfig(exchangeData.ExchangeData.CONFIGTYPE_AGETEST,None)
        ##命令行取设备老化时间以及其它老化数据###
        ##Ram TEST
        ##Flash Test
        ##Enthernet Test
        ##Test Hour

        return True




if __name__ == '__main__':
    do = DeviceOper()
    do.checkSN('0112016011')
