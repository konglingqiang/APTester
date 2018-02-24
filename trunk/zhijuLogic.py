# -*- coding: utf-8 -*-
from trunk.myconfig import MyConf
from trunk.zhijuFrm import *
__author__ = 'Manager'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
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

class ZhijuDiaLog(QDialog):

    exit_str = 0
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.location = self.geometry()
        self.Max = False
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect(self.ui.btnOk, SIGNAL("clicked()"),self.btn_OK_action)

        self.ui.label.setFocus()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def btn_OK_action(self):
        self.btnOk_clicked()


    def btnOk_clicked(self):
        flag = self.check_line()
        if flag:
            self.close()

    def check_line(self):
        zhijuId = self.ui.lineEdit.text()
        if zhijuId.isNull() or zhijuId.isEmpty() :
            self.ui.label_2.setText(u"请输入治具标识码")
            return False
        else:
            myconf = MyConf()
            myconf.set_zhiju_id(zhijuId)
            return True
