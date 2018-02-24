# -*- coding: gbk -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from msglogic import MyMSGForm

class myHelper(object):
    def ShowMessageBoxInfo(self,info):
        msg = MyMSGForm()
        msg.SetMessage(info, 0)
        return msg.exec_()
    
    def ShowMessageBoxError(self,info):
        msg = MyMSGForm()
        msg.SetMessage(info, 2)
        return msg.exec_()
    
    def ShowMessageBoxQuesion(self,info):
        msg = MyMSGForm()
        msg.SetMessage(info, 1)
        return msg.exec_()
