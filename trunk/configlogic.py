# -*- coding: gbk -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from configui import Ui_configBox
import dev_rc
from myconfig import *
from PyQt4 import QtCore, QtGui
from myui import *
from logic import *

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MyConfigForm(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.location = self.geometry()
        self.Max = False;

        self.ui=Ui_configBox()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect(self.ui.btnMenu_Close,SIGNAL("clicked()"),SLOT("close()"))
        self.connect(self.ui.btnCancel,SIGNAL("clicked()"),SLOT("close()"))
        self.connect(self.ui.btnOk,SIGNAL("clicked()"),self.btnOk_clicked)

        #配置工作页面的btnok按钮事件
        self.connect(self.ui.btnOk_2,SIGNAL("clicked()"),self.btnOk_clicked)
        self.connect(self.ui.btnCancel_2,SIGNAL("clicked()"),SLOT("close()"))

        # 测试环境配置页面btn按钮事件
        self.connect(self.ui.btnOk_3,SIGNAL("clicked()"),self.btnOk_clicked)
        self.connect(self.ui.btnCancel_3,SIGNAL("clicked()"),SLOT("close()"))


        self.fontId = QFontDatabase.addApplicationFont(":/image/icomoon.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(self.fontId).takeAt(0)
        self.iconFont = QFont(self.fontName)
        self.SetIcon(self.ui.btnMenu_Close, QChar(0xf00d), 10)
        #self.SetIcon(self.ui.lab_Ico, QChar(0xf015), 12)
        qss = QFile("black.css"); 
        qss.open(QFile.ReadOnly); 
        q = QString(qss.readAll())
        self.setStyleSheet(q);
        # self.xiansuntxt = XianSunTXT()
        # self.xiansuntxt.read_2g_xian_sun_txt()
        # self.xiansuntxt.read_5g_xian_sun_txt()
        # self.xiansuntxt.write_2g_xiansun_to_ini()
        # self.xiansuntxt.write_5g_xiansun_to_ini()
        # self.xiansuntxt.write_5g_xiansun_to_xml()

        self.show_current_config()




    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()
 
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
           # self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def SetIcon(self, obj, text, size):
        self.iconFont.setPointSize(size)
        obj.setFont(self.iconFont)
        obj.setText(text)
    
    def SetMessage(self, msg, mytype):
        if(mytype == 0):
            self.ui.labIcoMain.setStyleSheet("border-image: url(:/image/myconfig.png);")
            self.ui.btnCancel.setVisible(False)
            self.ui.lab_Title.setText(u"提示")
        elif(mytype == 1):
            self.ui.labIcoMain.setStyleSheet("border-image: url(:/image/question.png);")
            self.ui.lab_Title.setText(u"询问")
        elif(mytype == 2):
            self.ui.labIcoMain.setStyleSheet("border-image: url(:/image/error.png);")
            self.ui.btnCancel.setVisible(False)
            self.ui.lab_Title.setText(u"错误")
        self.ui.labInfo.setText(msg)
        
    def btnOk_clicked(self):
        self.set_current_config()
        self.emit(SIGNAL("click_ok"))
        self.done(1)
        self.close()

    #默认显示配置
    def show_current_config(self):
        self.show_how_to_test()
        # self.show_write_art()
#       self.show_2G_freq_for_lost()
#         self.show_5G_freq_for_lost()
#         self.show_2G_lost_for_freq()
#         self.show_5G_lost_for_freq()
#         self.show_2G_pcdac()
#         self.show_5G_pcdac()
#         self.show_2G_ppm_limit()
#         self.show_5G_ppm_limit()
#         self.show_2G_power_limit_ht20()
#         self.show_5G_power_limit_ht20()
#         self.show_2G_power_limit_ht40()
#         self.show_5G_power_limit_ht40()
#         self.show_2G_freq_rate_chain()
#         self.show_5G_freq_rate_chain()
#         self.show_2G_other_config()
#         self.show_5G_other_config()
        self.show_how_to_SNorMAC()
        self.show_defaultIp()
        self.show_username()
        self.show_password()
        self.show_massage_for_all_table()
        self.show_is_or_not_jiaozhun()
        self.show_2g_defaut_port()
        self.show_5g_defaut_port()
        self.show_old_hour()
        self.show_max_ip_use()
        self.show_log_address()
        self.show_power_A_B_save_address()

    def show_how_to_test(self):
        testconfig = TestConf()
        how_to_test = testconfig.get_howtotest()
        if(how_to_test == "2"):
            self.ui.radioButton_3.setChecked(True)
        elif(how_to_test == "1"):
            self.ui.radioButton_2.setChecked(True)
        else:
            self.ui.radioButton.setChecked(True)

    #显示默认是否校准
    def show_is_or_not_jiaozhun(self):
        testconfig = TestConf()
        if(testconfig.get_is_or_not_jiaozhun()=="1"):
            self.ui.radioButton_8.setChecked(True)
        else:
            self.ui.radioButton_9.setChecked(True)

    #显示默认SN或者MAC
    def show_how_to_SNorMAC(self):
        testconfig = TestConf()

        if(testconfig.get_begin_with_MACorSN()== '1'):
            self.ui.radioButton_7.setChecked(True)
        else:
            self.ui.radioButton_6.setChecked(True)



    def show_write_art(self):
        testconfig = TestConf()
        how_to_test = testconfig.get_write_art()
        if(how_to_test == "1"):
            self.ui.radioButton_4.setChecked(True)
        else:
            self.ui.radioButton_5.setChecked(True)
    
    # def show_2G_freq_for_lost(self):
    #     testconfig = TestConf()
    #     freq_for_lost = testconfig.get_2G_freq_for_lost()
    #     self.ui.lineEdit_12.setText(freq_for_lost)


    # def show_5G_freq_for_lost(self):
    #     testconfig = TestConf()
    #     freq_for_lost = testconfig.get_5G_freq_for_lost()
    #     self.ui.lineEdit_7.setText(freq_for_lost)


    def show_2g_defaut_port(self):
        testconfig = TestConf()
        self.ui.lineEdit.setText(testconfig.get_2g_default_port())
    def show_5g_defaut_port(self):
        testconfig =TestConf()
        self.ui.lineEdit_3.setText(testconfig.get_5g_default_port())

    def show_username(self):
        testconfig = TestConf()
        self.ui.lineEdit_26.setText(testconfig.get_username())

    def show_password(self):
        testconfig = TestConf()
        self.ui.lineEdit_27.setText(testconfig.get_password())

    #显示默认ip
    def show_defaultIp(self):
        testconfig = TestConf()
        self.ui.lineEdit_25.setText(testconfig.get_default_ip())

    def show_2G_lost_for_freq(self):
        testconfig = TestConf()
        lost_for_freq = testconfig.get_2G_lost_for_freq()
        self.ui.lineEdit_13.setText(lost_for_freq)
    
    def show_5G_lost_for_freq(self):
        testconfig = TestConf()
        lost_for_freq = testconfig.get_5G_lost_for_freq()
        self.ui.lineEdit_8.setText(lost_for_freq)
    
    def show_2G_pcdac(self):
        testconfig = TestConf()
        pcdac = testconfig.get_2G_pcdac()
        self.ui.lineEdit_11.setText(pcdac)
    
    def show_5G_pcdac(self):
        testconfig = TestConf()
        pcdac = testconfig.get_5G_pcdac()
        self.ui.lineEdit_6.setText(pcdac)
        
    def show_2G_ppm_limit(self):
        testconfig = TestConf()
        ppm_limit = testconfig.get_2G_ppm_limit()
        self.ui.lineEdit_14.setText(ppm_limit)
    
    def show_5G_ppm_limit(self):
        testconfig = TestConf()
        ppm_limit = testconfig.get_5G_ppm_limit()
        self.ui.lineEdit_9.setText(ppm_limit)
    
    def show_2G_power_limit_ht20(self):
        testconfig = TestConf()
        power_limit_ht20 = testconfig.get_2G_power_limit_ht20()
        self.ui.lineEdit_15.setText(power_limit_ht20)
    
    def show_5G_power_limit_ht20(self):
        testconfig = TestConf()
        power_limit_ht20 = testconfig.get_5G_power_limit_ht20()
        self.ui.lineEdit_10.setText(power_limit_ht20)
    
    def show_2G_power_limit_ht40(self):
        testconfig = TestConf()
        power_limit_ht40 = testconfig.get_2G_power_limit_ht40()
        self.ui.lineEdit.setText(power_limit_ht40)
    
    def show_5G_power_limit_ht40(self):
        testconfig = TestConf()
        power_limit_ht40 = testconfig.get_5G_power_limit_ht40()
        self.ui.lineEdit_2.setText(power_limit_ht40)
    
    def show_2G_freq_rate_chain(self):
        testconfig = TestConf()
        self.ui.lineEdit_3.setText(testconfig.get_something("2G","tx_ht20_freq"))
        self.ui.lineEdit_18.setText(testconfig.get_something("2G","tx_ht20_rate"))
        self.ui.lineEdit_20.setText(testconfig.get_something("2G","tx_ht20_chain"))
        self.ui.lineEdit_4.setText(testconfig.get_something("2G","tx_ht40_freq"))
        self.ui.lineEdit_21.setText(testconfig.get_something("2G","tx_ht40_rate"))
        self.ui.lineEdit_22.setText(testconfig.get_something("2G","tx_ht40_chain"))
        s = '''
        self.ui.lineEdit_3.setText(testconfig.get_something("2G","tx_power_ht20_freq"))
        self.ui.lineEdit_18.setText(testconfig.get_something("2G","tx_power_ht20_rate"))
        self.ui.lineEdit_20.setText(testconfig.get_something("2G","tx_power_ht20_chain"))
        self.ui.lineEdit_4.setText(testconfig.get_something("2G","tx_power_ht40_freq"))
        self.ui.lineEdit_21.setText(testconfig.get_something("2G","tx_power_ht40_rate"))
        self.ui.lineEdit_22.setText(testconfig.get_something("2G","tx_power_ht40_chain"))
        self.ui.lineEdit_25.setText(testconfig.get_something("2G","tx_evm_ht20_freq"))
        self.ui.lineEdit_26.setText(testconfig.get_something("2G","tx_evm_ht20_rate"))
        self.ui.lineEdit_27.setText(testconfig.get_something("2G","tx_evm_ht20_chain"))
        self.ui.lineEdit_31.setText(testconfig.get_something("2G","tx_evm_ht40_freq"))
        self.ui.lineEdit_32.setText(testconfig.get_something("2G","tx_evm_ht40_rate"))
        self.ui.lineEdit_33.setText(testconfig.get_something("2G","tx_evm_ht40_chain"))
        self.ui.lineEdit_37.setText(testconfig.get_something("2G","tx_evm_ppm_freq"))
        self.ui.lineEdit_38.setText(testconfig.get_something("2G","tx_evm_ppm_rate"))
        self.ui.lineEdit_39.setText(testconfig.get_something("2G","tx_evm_ppm_chain"))
        self.ui.lineEdit_43.setText(testconfig.get_something("2G","tx_mask_freq"))
        self.ui.lineEdit_44.setText(testconfig.get_something("2G","tx_mask_rate"))
        self.ui.lineEdit_45.setText(testconfig.get_something("2G","tx_mask_chain"))
        '''
        self.ui.lineEdit_49.setText(testconfig.get_something("2G","rx_freq"))
        self.ui.lineEdit_50.setText(testconfig.get_something("2G","rx_rate"))
        self.ui.lineEdit_51.setText(testconfig.get_something("2G","rx_chain"))
    
    def show_5G_freq_rate_chain(self):
        testconfig = TestConf()
        self.ui.lineEdit_5.setText(testconfig.get_something("5G","tx_ht20_freq"))
        self.ui.lineEdit_17.setText(testconfig.get_something("5G","tx_ht20_rate"))
        self.ui.lineEdit_19.setText(testconfig.get_something("5G","tx_ht20_chain"))
        self.ui.lineEdit_16.setText(testconfig.get_something("5G","tx_ht40_freq"))
        self.ui.lineEdit_23.setText(testconfig.get_something("5G","tx_ht40_rate"))
        self.ui.lineEdit_24.setText(testconfig.get_something("5G","tx_ht40_chain"))
        s = '''
        self.ui.lineEdit_5.setText(testconfig.get_something("5G","tx_power_ht20_freq"))
        self.ui.lineEdit_17.setText(testconfig.get_something("5G","tx_power_ht20_rate"))
        self.ui.lineEdit_19.setText(testconfig.get_something("5G","tx_power_ht20_chain"))
        self.ui.lineEdit_16.setText(testconfig.get_something("5G","tx_power_ht40_freq"))
        self.ui.lineEdit_23.setText(testconfig.get_something("5G","tx_power_ht40_rate"))
        self.ui.lineEdit_24.setText(testconfig.get_something("5G","tx_power_ht40_chain"))
        self.ui.lineEdit_28.setText(testconfig.get_something("5G","tx_evm_ht20_freq"))
        self.ui.lineEdit_29.setText(testconfig.get_something("5G","tx_evm_ht20_rate"))
        self.ui.lineEdit_30.setText(testconfig.get_something("5G","tx_evm_ht20_chain"))
        self.ui.lineEdit_34.setText(testconfig.get_something("5G","tx_evm_ht40_freq"))
        self.ui.lineEdit_35.setText(testconfig.get_something("5G","tx_evm_ht40_rate"))
        self.ui.lineEdit_36.setText(testconfig.get_something("5G","tx_evm_ht40_chain"))
        self.ui.lineEdit_40.setText(testconfig.get_something("5G","tx_evm_ppm_freq"))
        self.ui.lineEdit_41.setText(testconfig.get_something("5G","tx_evm_ppm_rate"))
        self.ui.lineEdit_42.setText(testconfig.get_something("5G","tx_evm_ppm_chain"))
        self.ui.lineEdit_46.setText(testconfig.get_something("5G","tx_mask_freq"))
        self.ui.lineEdit_47.setText(testconfig.get_something("5G","tx_mask_rate"))
        self.ui.lineEdit_48.setText(testconfig.get_something("5G","tx_mask_chain"))
        '''
        self.ui.lineEdit_52.setText(testconfig.get_something("5G","rx_freq"))
        self.ui.lineEdit_53.setText(testconfig.get_something("5G","rx_rate"))
        self.ui.lineEdit_54.setText(testconfig.get_something("5G","rx_chain"))


    def show_2G_other_config(self):
        testconfig = TestConf()
        self.ui.lineEdit_55.setText(testconfig.get_something("2G","rate_for_powerlevel"))
        self.ui.lineEdit_56.setText(testconfig.get_something("2G","powerlevel_for_rate"))
    
    def show_5G_other_config(self):
        testconfig = TestConf()
        self.ui.lineEdit_57.setText(testconfig.get_something("5G","rate_for_powerlevel"))
        self.ui.lineEdit_58.setText(testconfig.get_something("5G","powerlevel_for_rate"))

    def set_begin_with_SNorMAC(self):
        testconfig = TestConf()

        if(self.ui.radioButton_7.isChecked()):
            testconfig.set_begin_SN()
            # self.frm_ui.label.setText(u"SN:")
            self.emit(SIGNAL("set_begin_with"))
        else:
            testconfig.set_beging_MAC()
            # self.frm_ui.label.setText(u"MAC")
            self.emit(SIGNAL("set_begin_with"))

    def show_old_hour(self):
        myconf = MyConf()
        self.ui.lineEdit_4.setText(myconf.get_old_hour())
    def show_max_ip_use(self):
        myconf = MyConf()
        self.ui.lineEdit_5.setText(myconf.get_max_ip_use())
    def show_log_address(self):
        myconf = MyConf()
        self.ui.lineEdit_7.setText(myconf.get_log_address())
    def show_power_A_B_save_address(self):
        myconf = MyConf()
        self.ui.lineEdit_8.setText(myconf.get_power_A_B_save_address())

    def set_old_hour(self):
        myconf = MyConf()
        old_hour = self.ui.lineEdit_4.text()
        myconf.set_old_hour(old_hour)
    def set_max_ip_use(self):
        myconf = MyConf()
        max_ip_use = self.ui.lineEdit_5.text()
        myconf.set_max_ip_use(max_ip_use)
    def set_log_address(self):
        myconf = MyConf()
        log_address = self.ui.lineEdit_7.text()
        myconf.set_log_address(log_address)
    def set_power_A_B_save_address(self):
        myconf = MyConf()
        power_A_B_save_address = self.ui.lineEdit_8.text()
        myconf.set_power_A_B_save_address(power_A_B_save_address)




    def set_2g_default_port(self):
        testconfig = TestConf()
        port_2g = self.ui.lineEdit.text()
        testconfig.set_2g_default_port(port_2g)

    def set_5g_default_port(self):
        testconfig = TestConf()
        port_5g = self.ui.lineEdit_3.text()
        testconfig.set_5g_default_port(port_5g)

    def set_is_or_not_jiaozhun(self):
        testconfig = TestConf()
        if(self.ui.radioButton_8.isChecked()):
            testconfig.set_is_or_not_jiaozhun(1)
        elif self.ui.radioButton_9.isChecked():
            testconfig.set_is_or_not_jiaozhun(0)


    def set_username(self):
        testconfig = TestConf()
        username = self.ui.lineEdit_26.text()

        testconfig.set_username(username)

    def set_password(self):
        testconfig = TestConf()
        password = self.ui.lineEdit_27.text()

        testconfig.set_password(password)
    def set_how_to_test(self):
        testconfig = TestConf()
        if(self.ui.radioButton_3.isChecked()):
            testconfig.set_howtotest_both()
        elif(self.ui.radioButton_2.isChecked()):
            testconfig.set_howtotest_5G()
        else:
            testconfig.set_howtotest_2G()
    
    # def set_write_art(self):
    #     testconfig = TestConf()
    #     if(self.ui.radioButton_4.isChecked()):
    #         testconfig.set_write_art_only_when_sucess()
    #
    #     else:
    #         testconfig.set_write_art_no_matter_what()

    def set_default_ip(self):
        testconfig = TestConf()
        default_ip = self.ui.lineEdit_25.text()
        testconfig.set_default_ip(default_ip)
    # def set_2G_freq_for_lost(self):
    #     testconfig = TestConf()
    #     freq_for_lost = self.ui.lineEdit_12.text()
    #     testconfig.set_2G_freq_for_lost(freq_for_lost)
    #
    def set_5G_freq_for_lost(self):
        testconfig = TestConf()
        freq_for_lost = self.ui.lineEdit_7.text()
        testconfig.set_5G_freq_for_lost(freq_for_lost)
    
    def set_2G_lost_for_freq(self):
        testconfig = TestConf()
        lost_for_freq = self.ui.lineEdit_13.text()
        testconfig.set_2G_lost_for_freq(lost_for_freq)
    
    def set_5G_lost_for_freq(self):
        testconfig = TestConf()
        lost_for_freq = self.ui.lineEdit_8.text()
        testconfig.set_5G_lost_for_freq(lost_for_freq)
    
    def set_2G_pcdac(self,tree):
        testconfigxml = TestConfigxml()
        pcdac = self.ui.lineEdit_15.text()
        testconfigxml.set_2g_pcdac(pcdac,tree)

    def set_5G_pcdac(self,tree):
        testconfigxml = TestConfigxml()
        pcdac = self.ui.lineEdit_6.text()
        testconfigxml.set_5g_pcdac(pcdac,tree)
    
    def set_2G_ppm_limit(self,tree):
        testconfigxml = TestConfigxml()
        ppm_limit = self.ui.lineEdit_11.text()
        testconfigxml.set_2g_ppm_limit(ppm_limit,tree)
    
    def set_5G_ppm_limit(self,tree):
        testconfigxml = TestConfigxml()
        ppm_limit = self.ui.lineEdit_9.text()
        testconfigxml.set_5g_ppm_limit(ppm_limit,tree)
    
    def set_2G_power_limit_ht20(self,tree):
        testconfigxml = TestConfigxml()
        power_limit_ht20 = self.ui.lineEdit_28.text()
        testconfigxml.set_2g_power_limit_ht20(power_limit_ht20,tree)

    def set_5G_power_limit_ht20(self,tree):
        testconfigxml = TestConfigxml()
        power_limit_ht20 = self.ui.lineEdit_10.text()
        testconfigxml.set_5g_power_limit_ht20(power_limit_ht20,tree)
    
    def set_2G_power_limit_ht40(self,tree):
        testconfigxml = TestConfigxml()
        power_limit_ht40 = self.ui.lineEdit_14.text()
        testconfigxml.set_2g_power_limit_ht40(power_limit_ht40,tree)

    def set_5G_power_limit_ht40(self,tree):
        testconfigxml = TestConfigxml()
        power_limit_ht40 = self.ui.lineEdit_2.text()
        testconfigxml.set_5g_power_limit_ht40(power_limit_ht40,tree)
    
    def set_2G_freq_rate_chain(self):
        testconfig = TestConf()
        testconfig.set_something("2G","tx_ht20_freq",self.ui.lineEdit_3.text())
        testconfig.set_something("2G","tx_ht20_rate",self.ui.lineEdit_18.text())
        testconfig.set_something("2G","tx_ht20_chain",self.ui.lineEdit_20.text())
        testconfig.set_something("2G","tx_ht40_freq",self.ui.lineEdit_4.text())
        testconfig.set_something("2G","tx_ht40_rate",self.ui.lineEdit_21.text())
        testconfig.set_something("2G","tx_ht40_chain",self.ui.lineEdit_22.text())
        s = '''
        testconfig.set_something("2G","tx_power_ht20_freq",self.ui.lineEdit_3.text())
        testconfig.set_something("2G","tx_power_ht20_rate",self.ui.lineEdit_18.text())
        testconfig.set_something("2G","tx_power_ht20_chain",self.ui.lineEdit_20.text())
        testconfig.set_something("2G","tx_power_ht40_freq",self.ui.lineEdit_4.text())
        testconfig.set_something("2G","tx_power_ht40_rate",self.ui.lineEdit_21.text())
        testconfig.set_something("2G","tx_power_ht40_chain",self.ui.lineEdit_22.text())
        testconfig.set_something("2G","tx_evm_ht20_freq",self.ui.lineEdit_25.text())
        testconfig.set_something("2G","tx_evm_ht20_rate",self.ui.lineEdit_26.text())
        testconfig.set_something("2G","tx_evm_ht20_chain",self.ui.lineEdit_27.text())
        testconfig.set_something("2G","tx_evm_ht40_freq",self.ui.lineEdit_31.text())
        testconfig.set_something("2G","tx_evm_ht40_rate",self.ui.lineEdit_32.text())
        testconfig.set_something("2G","tx_evm_ht40_chain",self.ui.lineEdit_33.text())
        testconfig.set_something("2G","tx_evm_ppm_freq",self.ui.lineEdit_37.text())
        testconfig.set_something("2G","tx_evm_ppm_rate",self.ui.lineEdit_38.text())
        testconfig.set_something("2G","tx_evm_ppm_chain",self.ui.lineEdit_39.text())
        testconfig.set_something("2G","tx_mask_freq",self.ui.lineEdit_43.text())
        testconfig.set_something("2G","tx_mask_rate",self.ui.lineEdit_44.text())
        testconfig.set_something("2G","tx_mask_chain",self.ui.lineEdit_45.text())
        '''
        testconfig.set_something("2G","rx_freq",self.ui.lineEdit_49.text())
        testconfig.set_something("2G","rx_rate",self.ui.lineEdit_50.text())
        testconfig.set_something("2G","rx_chain",self.ui.lineEdit_51.text())

    def save_freq_rate_chain(self):
        testconfxml = TestConfigxml()
        table_2g_freq_for_ht20 = self.ui.tableWidget_6
        for i in range(table_2g_freq_for_ht20.rowCount()):
            print i
            print table_2g_freq_for_ht20.item(i,0)
            if table_2g_freq_for_ht20.item(i,0) is None:
                continue
            freq = table_2g_freq_for_ht20.item(i,0).text()
            rates = table_2g_freq_for_ht20.item(i,1).text()
            chains = table_2g_freq_for_ht20.item(i,2).text()
            #1获得当前行的元素的值
            #2将获得到的值保存到xml文件中
            testconfxml.save_tabel_freq_rate_chain(freq,rates,chains,'2G','ht20')

        table_2g_freq_for_ht40 = self.ui.tableWidget_7
        for i in range(table_2g_freq_for_ht40.rowCount()):
            if table_2g_freq_for_ht40.item(i,0) is None:
                break
            freq = table_2g_freq_for_ht40.item(i,0).text()
            rates = table_2g_freq_for_ht40.item(i,1).text()
            chains = table_2g_freq_for_ht40.item(i,2).text()

            testconfxml.save_tabel_freq_rate_chain(freq,rates,chains,'2G','ht40')


        table_2g_freq_for_rx = self.ui.tableWidget_8
        for i in range(table_2g_freq_for_rx.rowCount()):
            if table_2g_freq_for_rx.item(i,0) is None:
                break
            freq = table_2g_freq_for_rx.item(i,0).text()
            rates = table_2g_freq_for_rx.item(i,1).text()
            chains = table_2g_freq_for_rx.item(i,2).text()

            testconfxml.save_tabel_freq_rate_chain(freq,rates,chains,'2G','rx')

        table_5g_freq_for_ht20 = self.ui.tableWidget
        for i in range(table_5g_freq_for_ht20.rowCount()):
            if table_5g_freq_for_ht20.item(i,0) is None:
                break
            freq = table_5g_freq_for_ht20.item(i,0).text()
            rates = table_5g_freq_for_ht20.item(i,1).text()
            chains = table_5g_freq_for_ht20.item(i,2).text()

            testconfxml.save_tabel_freq_rate_chain(freq,rates,chains,'5G','ht20')

        table_5g_freq_for_ht40 = self.ui.tableWidget_4
        for i in range(table_5g_freq_for_ht40.rowCount()):
            if table_5g_freq_for_ht40.item(i,0) is None:
                break
            freq = table_5g_freq_for_ht40.item(i,0).text()
            rates = table_5g_freq_for_ht40.item(i,1).text()
            chains = table_5g_freq_for_ht40.item(i,2).text()

            testconfxml.save_tabel_freq_rate_chain(freq,rates,chains,'5G','ht40')

        table_5g_freq_for_rx = self.ui.tableWidget_5
        for i in range(table_5g_freq_for_rx.rowCount()):
            if table_5g_freq_for_rx.item(i,0) is None:
                continue
            freq = table_5g_freq_for_rx.item(i,0).text()
            rates = table_5g_freq_for_rx.item(i,1).text()
            chains = table_5g_freq_for_rx.item(i,2).text()

            testconfxml.save_tabel_freq_rate_chain(freq,rates,chains,'5G','rx')





    def set_5G_freq_rate_chain(self):
        testconfig = TestConf()
        testconfig.set_something("5G","tx_ht20_freq",self.ui.lineEdit_5.text())
        testconfig.set_something("5G","tx_ht20_rate",self.ui.lineEdit_17.text())
        testconfig.set_something("5G","tx_ht20_chain",self.ui.lineEdit_19.text())
        testconfig.set_something("5G","tx_ht40_freq",self.ui.lineEdit_16.text())
        testconfig.set_something("5G","tx_ht40_rate",self.ui.lineEdit_23.text())
        testconfig.set_something("5G","tx_ht40_chain",self.ui.lineEdit_24.text())
        s = '''
        testconfig.set_something("5G","tx_power_ht20_freq",self.ui.lineEdit_5.text())
        testconfig.set_something("5G","tx_power_ht20_rate",self.ui.lineEdit_17.text())
        testconfig.set_something("5G","tx_power_ht20_chain",self.ui.lineEdit_19.text())
        testconfig.set_something("5G","tx_power_ht40_freq",self.ui.lineEdit_16.text())
        testconfig.set_something("5G","tx_power_ht40_rate",self.ui.lineEdit_23.text())
        testconfig.set_something("5G","tx_power_ht40_chain",self.ui.lineEdit_24.text())
        testconfig.set_something("5G","tx_evm_ht20_freq",self.ui.lineEdit_28.text())
        testconfig.set_something("5G","tx_evm_ht20_rate",self.ui.lineEdit_29.text())
        testconfig.set_something("5G","tx_evm_ht20_chain",self.ui.lineEdit_30.text())
        testconfig.set_something("5G","tx_evm_ht40_freq",self.ui.lineEdit_34.text())
        testconfig.set_something("5G","tx_evm_ht40_rate",self.ui.lineEdit_35.text())
        testconfig.set_something("5G","tx_evm_ht40_chain",self.ui.lineEdit_36.text())
        testconfig.set_something("5G","tx_evm_ppm_freq",self.ui.lineEdit_40.text())
        testconfig.set_something("5G","tx_evm_ppm_rate",self.ui.lineEdit_41.text())
        testconfig.set_something("5G","tx_evm_ppm_chain",self.ui.lineEdit_42.text())
        testconfig.set_something("5G","tx_mask_freq",self.ui.lineEdit_46.text())
        testconfig.set_something("5G","tx_mask_rate",self.ui.lineEdit_47.text())
        testconfig.set_something("5G","tx_mask_chain",self.ui.lineEdit_48.text())
        '''
        testconfig.set_something("5G","rx_freq",self.ui.lineEdit_52.text())
        testconfig.set_something("5G","rx_rate",self.ui.lineEdit_53.text())
        testconfig.set_something("5G","rx_chain",self.ui.lineEdit_54.text())
        
    def set_2G_other_config(self):
        testconfig = TestConf()
        testconfig.set_something("2G","rate_for_powerlevel",self.ui.lineEdit_55.text())
        testconfig.set_something("2G","powerlevel_for_rate",self.ui.lineEdit_56.text())
    
    def set_5G_other_config(self):
        testconfig = TestConf()
        testconfig.set_something("5G","rate_for_powerlevel",self.ui.lineEdit_57.text())
        testconfig.set_something("5G","powerlevel_for_rate",self.ui.lineEdit_58.text())
        
    def set_current_config(self):
        configxml = TestConfigxml()
        tree = configxml.read_xml()
        #初始化设置
        self.set_how_to_test()
        # self.set_write_art()
        # self.set_2G_freq_for_lost()
        # self.set_5G_freq_for_lost()
        # self.set_2G_lost_for_freq()
        # self.set_5G_lost_for_freq()
        self.set_2G_pcdac(tree)
        self.set_5G_pcdac(tree)
        self.set_2G_ppm_limit(tree)
        self.set_5G_ppm_limit(tree)
        self.set_2G_power_limit_ht20(tree)
        self.set_5G_power_limit_ht20(tree)
        self.set_2G_power_limit_ht40(tree)
        self.set_5G_power_limit_ht40(tree)

        configxml.write_xml(tree)
        # self.set_2G_freq_rate_chain()
        # self.set_5G_freq_rate_chain()
        # self.set_2G_other_config()
        # self.set_5G_other_config()
        self.set_begin_with_SNorMAC()
        self.set_default_ip()
        self.set_username()
        self.set_password()
        self.set_2g_default_port()
        self.set_5g_default_port()
        self.set_is_or_not_jiaozhun()
        self.save_freq_rate_chain()
        self.set_old_hour()
        self.set_max_ip_use()
        self.set_log_address()
        self.set_power_A_B_save_address()

    #显示频率——线损表格
    def show_freq_for_lost_message(self, g2_or_g5, table):
        # testconfigxml = TestConfigxml()
        # freq_for_lost = testconfigxml.get_freq_for_lost(g2_or_g5)
        #
        # all_freqs_in_freq_for_lost_ = testconfigxml.get_all_freq(freq_for_lost)
        # freq_y = 0
        # # rows = len(all_freqs_in_freq_for_lost_)
        # # table.insertRow(rows)
        # for freq in all_freqs_in_freq_for_lost_:
        #     #一个循环在频率——线损表格中添加一行
        #     val = freq.find('val').text
        #     lost = freq.find('lost').text
        #     new_item_val = QTableWidgetItem(val)
        #     new_item_lost = QTableWidgetItem(lost)
        #     table.setItem(freq_y, 0, new_item_val)
        #     table.setItem(freq_y, 1, new_item_lost)
        #     freq_y = freq_y+1
        xiansunini = Xian_Sun_ini()
        items = xiansunini.get_2g_or_5g_items(g2_or_g5)
        freq_y = 0
        for item in items:
            new_item_val = QTableWidgetItem(item[0])
            new_item_lost = QTableWidgetItem(xiansunini.get_value_for_freq(g2_or_g5,item[0]))
            table.setItem(freq_y, 0, new_item_val)
            table.setItem(freq_y, 1, new_item_lost)
            freq_y = freq_y+1

    #显示ht20表格
    def show_ht20_table_massage(self, g2_or_g5, table):
        testconfigxml = TestConfigxml()
        all_test_items = testconfigxml.get_test_items(g2_or_g5)

        for items in all_test_items:
            if items.get('name') == "ht20":
                all_freqs_in_test_items = testconfigxml.get_all_freq(items)
                freq_y = 0

                for items_freq in all_freqs_in_test_items:
                    val = items_freq.find('val').text
                    rate = items_freq.find('rate').text
                    chain = items_freq.find('chain').text
                    table.setItem(freq_y, 0, QTableWidgetItem(val))
                    table.setItem(freq_y, 1, QTableWidgetItem(rate))
                    table.setItem(freq_y, 2, QTableWidgetItem(chain))
                    freq_y = freq_y+1

    #显示ht40表格
    def show_ht40_table_massage(self, g2_or_g5, table):
        testconfigxml = TestConfigxml()
        all_test_items = testconfigxml.get_test_items(g2_or_g5)

        for items in all_test_items:
            if items.get('name') == "ht40":
                all_freqs_in_test_items = testconfigxml.get_all_freq(items)
                freq_y = 0

                for items_freq in all_freqs_in_test_items:
                    val = items_freq.find('val').text
                    rate = items_freq.find('rate').text
                    chain = items_freq.find('chain').text
                    table.setItem(freq_y, 0, QTableWidgetItem(val))
                    table.setItem(freq_y, 1, QTableWidgetItem(rate))
                    table.setItem(freq_y, 2, QTableWidgetItem(chain))
                    freq_y = freq_y+1
    #显示rx表格
    def show_rx_table_massage(self, g2_or_g5, table):
        testconfigxml = TestConfigxml()
        all_test_items = testconfigxml.get_test_items(g2_or_g5)

        for items in all_test_items:
            if items.get('name') == "rx":
                all_freqs_in_test_items = testconfigxml.get_all_freq(items)

                freq_y = 0
                for items_freq in all_freqs_in_test_items:
                    val = items_freq.find('val').text
                    rate = items_freq.find('rate').text
                    chain = items_freq.find('chain').text
                    table.setItem(freq_y, 0, QTableWidgetItem(val))
                    table.setItem(freq_y, 1, QTableWidgetItem(rate))
                    table.setItem(freq_y, 2, QTableWidgetItem(chain))
                    freq_y = freq_y+1
    #显示——速率——功率
    def show_power_rate(self, g2_or_g5,table):
        testconfigxml = TestConfigxml()
        power_rate = testconfigxml.get_power_rate(g2_or_g5)

        all_freqs_in_power_rate_ = testconfigxml.get_all_pr_items(power_rate)
        freq_y = 0
        for freq in all_freqs_in_power_rate_:
            #一个循环在频率——线损表格中添加一行
            level = freq.find('level').text
            rate = freq.find('rate').text
            table.setItem(freq_y, 0, QTableWidgetItem(level))
            table.setItem(freq_y, 1, QTableWidgetItem(rate))
            freq_y = freq_y+1



    def show_other_info(self, info, lineEdit):
        lineEdit.setText(info)

    #向表格窗体中添加数据。5个表格。一起添加
    def show_massage_for_all_table(self):
        testconfigxml = TestConfigxml()
        root = testconfigxml.read_xml()
        test = testconfigxml.get_all_test(root)
        for g2_or_g5 in test:
            if(g2_or_g5.get('name')=='2G'):
                tablewidget_6 = self.ui.tableWidget_6
                tablewidget_7 = self.ui.tableWidget_7
                tablewidget_8 = self.ui.tableWidget_8
                tablewidget_9 = self.ui.tableWidget_9
                tablewidget_10 = self.ui.tableWidget_10

                lineEdit_pcdac = self.ui.lineEdit_15
                lineEdit_ppm_limit = self.ui.lineEdit_11
                lineEdit_ht20_power_limit = self.ui.lineEdit_28
                lineEdit_ht40_power_limit = self.ui.lineEdit_14

                pcdac = g2_or_g5.get('pcdac')
                ppm_limit = g2_or_g5.get('ppm_limit')
                ht20_power_limit = g2_or_g5.get('power_limit_ht20')
                ht40_power_limit = g2_or_g5.get('power_limit_ht40')

                self.show_other_info(pcdac,lineEdit_pcdac)
                self.show_other_info(ppm_limit,lineEdit_ppm_limit)
                self.show_other_info(ht20_power_limit,lineEdit_ht20_power_limit)
                self.show_other_info(ht40_power_limit,lineEdit_ht40_power_limit)

                self.show_freq_for_lost_message(g2_or_g5.get('name'), tablewidget_9)
                self.show_ht20_table_massage(g2_or_g5, tablewidget_6)
                self.show_ht40_table_massage(g2_or_g5, tablewidget_7)
                self.show_rx_table_massage(g2_or_g5, tablewidget_8)
                self.show_power_rate(g2_or_g5,tablewidget_10)
            else:

                tablewidget_1 = self.ui.tableWidget
                tablewidget_2 = self.ui.tableWidget_2
                tablewidget_3 = self.ui.tableWidget_3
                tablewidget_4 = self.ui.tableWidget_4
                tablewidget_5 = self.ui.tableWidget_5


                lineEdit_pcdac = self.ui.lineEdit_6
                lineEdit_ppm_limit = self.ui.lineEdit_9
                lineEdit_ht20_power_limit = self.ui.lineEdit_10
                lineEdit_ht40_power_limit = self.ui.lineEdit_2

                pcdac = g2_or_g5.get('pcdac')
                ppm_limit = g2_or_g5.get('ppm_limit')
                ht20_power_limit = g2_or_g5.get('power_limit_ht20')
                ht40_power_limit = g2_or_g5.get('power_limit_ht40')

                self.show_other_info(pcdac,lineEdit_pcdac)
                self.show_other_info(ppm_limit,lineEdit_ppm_limit)
                self.show_other_info(ht20_power_limit,lineEdit_ht20_power_limit)
                self.show_other_info(ht40_power_limit,lineEdit_ht40_power_limit)

                self.show_freq_for_lost_message(g2_or_g5.get('name'), tablewidget_2)
                self.show_ht20_table_massage(g2_or_g5, tablewidget_1)
                self.show_ht40_table_massage(g2_or_g5, tablewidget_4)
                self.show_rx_table_massage(g2_or_g5, tablewidget_5)
                self.show_power_rate(g2_or_g5, tablewidget_3)





