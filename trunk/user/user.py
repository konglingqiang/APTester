# -*- coding: utf-8 -*-
from trunk.bdplug.dbop import DataBaseOP
from trunk.myconfig import MyConf

__author__ = 'Manager'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from configui import Ui_configBox
from PyQt4 import QtGui
# from myui import *
from loginDialog import *
# from myconfig import *
import sys
import os
# from logic import *
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class LoginDiaLog(QDialog):

    exit_str = 0
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.location = self.geometry()
        self.Max = False;
        self.ui = Ui_loginDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect(self.ui.pushButton_2, SIGNAL("clicked()"),self.btn_cancel_action)
        self.connect(self.ui.pushButton, SIGNAL("clicked()"),self.btn_login_action)
        self.widget = self.ui.widget_main
        png = QtGui.QPixmap()
        png.load(os.getcwd() + "\\image\\login.png")
        palette1 = QtGui.QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(png))
        self.widget.setPalette(palette1)
        self.widget.setAutoFillBackground(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def btn_login_action(self):
        myconfig = MyConf()
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        pmgr_link = myconfig.get_pmgr_link()
        if pmgr_link == '1':
            db_connect = DataBaseOP()
            login_result = db_connect.loginApTester(username, password)
        else:
            login_result = 2
        if login_result == 0:
            #提示用户名密码错误
            self.ui.label_3.setText(u"用户名或密码错误!")
            # self.ui.label_3.setTextColor(QColor.red)
        elif login_result == 1:
            #角色为普通名员工
            myconfig.set_user_type(1)
            self.btnOk_clicked()
        else:
            #角色为高权限：
            myconfig.set_user_type(2)
            self.btnOk_clicked()


    def btn_cancel_action(self):
        # logic = MyForm()

        self.close()
        sys.exit()
    def SetIcon(self, obj, text, size):
        self.iconFont.setPointSize(size)
        obj.setFont(self.iconFont)
        obj.setText(text)


    def set_username_ini(self):
        myconf = MyConf()
        username = self.ui.lineEdit.text()
        myconf.set_username(username)
    def btnOk_clicked(self):
        self.set_username_ini()
        self.close()