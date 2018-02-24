# -*- coding: gbk -*-
__author__ = 'kaikai'
i = 0  #控制显示不同文字
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from configui import Ui_configBox
from PyQt4 import QtGui
# from myui import *
from trunk.user.loginDialog import Ui_loginDialog
from trunk.myconfig import *
# from logic import *
from calculate_b_xs import *
from B_power import *
from A_power import *
import os
import subprocess
from A_B_to_get_xiansun import *

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Calculate_B(QDialog):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.location = self.geometry()
        self.Max = False
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.A_powera = Worker_A()
        self.B_powerb = Worker_B()
        self.A_B_power = Worker_A_B()
        # self.xiansunTXT = XianSunTXT()
        # self.xiansunTXT.write_2g_xiansun_to_ini()
        # self.xiansunTXT.write_5g_xiansun_to_ini()
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.connect(self.ui.btnMenu_Close,SIGNAL("clicked()"),SLOT("close()"))
        self.connect(self.ui.pushButton, SIGNAL("clicked()"), self.btn_power_A)
        self.connect(self.ui.pushButton_2, SIGNAL("clicked()"), self.btn_power_B)
        self.connect(self.ui.pushButton_3, SIGNAL("clicked()"), self.btn_power_A_B)
        self.connect(self.ui.pushButton_4, SIGNAL("clicked()"), self.btn_close)
        self.connect(self.ui.pushButton_5, SIGNAL("clicked()"), self.btn_change_to_xiansun)
        self.connect(self.ui.pushButton_6, SIGNAL("clicked()"), self.btn_open_tool)

        self.fontId = QFontDatabase.addApplicationFont(":/image/icomoon.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(self.fontId).takeAt(0)
        self.iconFont = QFont(self.fontName)
        self.connect(self.A_B_power, SIGNAL("begin_test"), self.show_begin_test)
        self.connect(self.A_B_power, SIGNAL("get_power_true"), self.show_success_message)
        self.connect(self.A_B_power, SIGNAL("testing"), self.show_in_test)

        self.connect(self.B_powerb, SIGNAL("begin_test"), self.show_begin_test)
        self.connect(self.B_powerb, SIGNAL("get_power_true"), self.show_success_message)
        self.connect(self.B_powerb, SIGNAL("get_power_false"), self.show_false_message)
        self.connect(self.B_powerb, SIGNAL("testing"), self.show_in_test)

        self.connect(self.A_powera, SIGNAL("begin_test"), self.show_begin_test)
        self.connect(self.A_powera, SIGNAL("get_power_true"), self.show_success_message)
        self.connect(self.A_powera, SIGNAL("get_power_false"), self.show_false_message)
        self.connect(self.A_powera, SIGNAL("testing"), self.show_in_test)
        # self.connect(self.thread,SIGNAL("get_power_true"),self.show_success_message)
        # self.connect(self.Calculate_B,SIGNAL("get_power_false"),self.show_false_message)
        # self.SetIcon(self.ui.pushButton, QChar(0xf00d), 10)
        # self.SetIcon(self.ui.pushButton_2, QChar(0xf015), 12)
        # qss = QFile("black.css");
        # qss.open(QFile.ReadOnly);
        # q = QString(qss.readAll())
        # self.setStyleSheet(q);

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
    #         QApplication.postEvent(self, QEvent(174))
    #         event.accept()

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         self.move(event.globalPos() - self.dragPosition)
    #         event.accept()
        self.widget = self.ui.frame
        png = QtGui.QPixmap()
        png.load(os.getcwd()+"\\image\\caulate-b.jpg")
        palette1 = QtGui.QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(png))
        self.widget.setPalette(palette1)
        self.widget.setAutoFillBackground(True)


    def SetIcon(self, obj, text, size):
        self.iconFont.setPointSize(size)
        obj.setFont(self.iconFont)
        obj.setText(text)

    def btn_power_A(self):
        #diaoyong
        # A_powera = Worker_A()
        self.A_powera.run_A()

    def btn_power_B(self):
        #diaoyong worder_B
        # B_powerb = Worker_B()
        self.B_powerb.run_B()

    def btn_power_A_B(self):
        #diaoyong worker_A_B
        # A_B_power = Worker_A_B()
        # A_B_power.power_A_B()
        self.A_B_power.power_A_B()
    def btn_close(self):
        # self.done(1)
        self.close()

    def btn_change_to_xiansun(self):
        global i

        version = Version_ini()
        this_version = version.get_version()

        if this_version == 'WE2622':
            self.show_change_pathloss()
            old_path =  os.getcwd()
            print "kkkkk"
            os.chdir(old_path+'\\cablecal_tool\\release\\IQ_SETUP')
            os.system("Update_IQ_ATTEN.vbs")
            time.sleep(1)
            print "update IQ ATTEN ok"
            # os.system("createNewAtten.vbs")
            os.chdir(old_path)
            pathloss_change_txt_to_ini = XianSunTXT()
            pathloss_change_txt_to_ini.write_2g_xiansun_to_ini()
            pathloss_change_txt_to_ini.write_5g_xiansun_to_ini()
            pathloss_change_txt_to_ini.calcute_some_freq_xiansun_to_ini()
            i += 1
            if i%2 ==0:
                self.show_change_pathloss()
            else:
                self.show_change_pathloss_result()
        elif this_version == "I23B" or this_version == "G22B" or this_version == "WE2622_prep":
            self.show_change_pathloss()
            pathloss_change_txt_to_ini = XianSunTXT()
            pathloss_change_txt_to_ini.write_2g_xiansun_to_ini()
            pathloss_change_txt_to_ini.write_5g_xiansun_to_ini()
            pathloss_change_txt_to_ini.calcute_some_freq_xiansun_to_ini()
            i += 1
            if i%2 == 0:
                self.show_change_pathloss_result()
            else:
                self.show_change_pathloss()
        else:
            self.show_change_pathloss()
            pathloss_change_txt_to_ini = XianSunTXT()
            pathloss_change_txt_to_ini.write_2g_xiansun_to_ini()
            pathloss_change_txt_to_ini.write_5g_xiansun_to_ini()
            pathloss_change_txt_to_ini.calcute_some_freq_xiansun_to_ini()
            i += 1
            if i%2 == 0:
                self.show_change_pathloss_result()
            else:
                self.show_change_pathloss()



    def btn_open_tool(self):
        old_path =  os.getcwd()
        print old_path

        os.chdir(old_path+'\\cablecal_tool\\release')
        subprocess.Popen(["MeasCableLossTool.exe"])

        os.chdir(old_path)
        print "end"

    def show_success_message(self):
        self.ui.label.setText(u"执行完成！")
    def show_false_message(self):
        self.ui.label.setText(u"执行失败，请重试！")
    def show_begin_test(self):
        self.ui.label.setText(u"测试准备！")
    def show_in_test(self):
        self.ui.label.setText(u"计算power中，请稍候")
    def show_change_pathloss(self):
        self.ui.label.setText(u"乾坤大挪移 完成！")
    def show_change_pathloss_result(self):
        self.ui.label.setText(u"颠倒乾坤 完成！")