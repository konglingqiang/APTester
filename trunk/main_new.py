# -*- coding: gbk -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from trunk.logic import MyForm
from trunk.myui import Ui_frmMain
import decimal
decimal.__version__
from trunk.myhelper import *

def start():
    app = QApplication(sys.argv)  # 创建窗体 参数为输入的值
    # print(sys.argv)
    # print(app)
    myapp = MyForm()
    myapp.on_btnMenu_Max_clicked()
    translator = QTranslator()
    translator.load(":/image/qt_zh_CN.qm")
    app.installTranslator(translator)
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)#创建窗体 参数为输入的值
    # print(sys.argv)
    # print(app)
    myapp=MyForm()
    myapp.on_btnMenu_Max_clicked()
    translator = QTranslator()
    translator.load(":/image/qt_zh_CN.qm")
    app.installTranslator(translator)
    myapp.show()
    sys.exit(app.exec_())

