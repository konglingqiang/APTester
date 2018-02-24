# -*- coding: gbk -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import telnetlib
import os
import time
import string
from ctypes import *
from trunk.myconfig import *
from trunk.bdplug.dbop import *
from trunk.configlogic import *
from trunk.msglogic import *
from trunk.user.user import *
# from trunk.protest import *
import trunk.protest_standby
# import trunk.protest
import re
import os
import sys
# version = Version_ini()
#
# this_version = version.get_version()
# if this_version == "I23B" or this_version == "G22B":
#     from trunk.protest_I23B import *
# elif this_version == "WE2622" or this_version == "WE2622_prep":
#     from trunk.protest import *
# else:
#     from trunk.protest_I23B import *
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
from B_zhan_xian_sun.calculate_b_logic import *
# from trunk.B_zhan_xian_sun.A_power import *

from trunk.zhijuFrm import *
from trunk.zhijuLogic import *
# test_result = 0

class MyForm(QDialog):
    '''应用程序窗体'''
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)#
        # QWidget.setFocus()
        exit_str = self.show_login_dialog()
        self.location = self.geometry()#
        self.Max = False
        self.ui = Ui_frmMain()
        self.ui.setupUi(self)
        self.conf = TestConf()
        self.myconf = MyConf()
        user_type = self.myconf.get_user_type()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        self.connect(self.ui.btnMenu_Close,SIGNAL("clicked()"),qApp,SLOT('quit()'))
        self.connect(self.ui.btnMenu_Max,SIGNAL("clicked()"),self.on_btnMenu_Max_clicked)
        self.connect(self.ui.btnMenu_Min,SIGNAL("clicked()"),self.on_btnMenu_Min_clicked)
        #self.connect(self.ui.pushButton,SIGNAL("clicked()"),self.pushButton_clicked)
        #self.connect(self.ui.pushButton_2,SIGNAL("clicked()"),self.pushButton_2_clicked)
        #self.connect(self.ui.pushButton_3,SIGNAL("clicked()"),self.pushButton_3_clicked)
        self.fontId = QFontDatabase.addApplicationFont(":/image/icomoon.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(self.fontId).takeAt(0)
        self.iconFont = QFont(self.fontName)
        self.SetIcon(self.ui.btnMenu_Close, QChar(0xf00d), 10)
        self.SetIcon(self.ui.btnMenu_Max, QChar(0xf096), 10)
        self.SetIcon(self.ui.btnMenu_Min, QChar(0xf068), 10)
        self.SetIcon(self.ui.btnMenu, QChar(0xf0c9), 10)
        self.SetIcon(self.ui.btnSkin, QChar(0x42), 13)
        self.SetIcon(self.ui.lab_Ico, QChar(0xf015), 12)
        #self.SetIcon(self.ui.textEdit_2, QChar(0xe9e1), 12)
        self.qssfile = ""

        self.ui.lab_Title.installEventFilter(self)
        self.ui.lab_Ico.installEventFilter(self)

        # version = Version_ini()
        # this_version = version.get_version()
        # #初始化窗体的时候就创建一个线程，
        # if this_version == "WE2622" or this_version =="WE2622_prep":
        #     self.thread = Worker()#测试WB262工作线程
        # elif this_version == "I23B" or this_version == "G22B":
        #     self.thread = Worker_I23B()#测试I23B工作线程
        # else:
        #     self.thread = trunk.protest_standby.Worker_I23B()#测试I23B工作线程
        self.ui.pushButton_2.clicked.connect(self.doTest)
        #
        # self.connect(self.thread, SIGNAL("output"), self.makeText)
        # self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        # self.connect(self.thread, SIGNAL("terminated()"), self.updateUi_not_save_log)
        # # 触发保存日志。
        # # self.connect(self.thread, SIGNAL("save_log"), self.save_log_file_only())
        #
        # self.connect(self.thread, SIGNAL("table_color"), self.table_get_result)
        #
        # self.connect(self.thread, SIGNAL("error_ping"), self.show_error_lian_jie)
        # self.connect(self.thread, SIGNAL("error_change_mode"), self.show_error_change_mode)
        # self.connect(self.thread, SIGNAL("error_sn"), self.show_error_sn)
        # self.connect(self.thread, SIGNAL("error_telnet"), self.show_error_telnet)
        # self.connect(self.thread, SIGNAL("error_base_info"), self.show_error_base_info)
        # self.connect(self.thread, SIGNAL("error_ipuse"), self.show_error_ipuse)
        # self.connect(self.thread, SIGNAL("error_old_info"), self.show_error_old_info)
        # self.connect(self.thread, SIGNAL("error_change_mode"), self.show_error_change_mode)
        # self.connect(self.thread, SIGNAL("error_old_hours"), self.show_error_old_hours)
        # self.connect(self.thread, SIGNAL("set_focus"), self.set_focus_to_lineEdit)
        # self.connect(self.thread, SIGNAL("zhunbei_txt"), self.set_text_zhunbei)
        #
        # self.connect(self.thread, SIGNAL("exit"), self.exit)
        # self.connect(self.thread, SIGNAL("result_success"), self.change_result_btn_to_success)
        # self.connect(self.thread, SIGNAL("result_fail"), self.change_result_btn_to_fail)
        #
        # self.connect(self.thread, SIGNAL("testing1"), self.updateUi_testing1)
        # self.connect(self.thread, SIGNAL("testing2"), self.updateUi_testing2)
        # self.connect(self.thread, SIGNAL("testing3"), self.updateUi_testing3)
        # self.connect(self.thread, SIGNAL("jiaozhuning1"), self.updateUi_jiaozhuning1)
        # self.connect(self.thread, SIGNAL("jiaozhuning2"), self.updateUi_jiaozhuning2)
        # self.connect(self.thread, SIGNAL("jiaozhuning3"), self.updateUi_jiaozhuning3)




        self.configBox = MyConfigForm()
        self.connect(self.configBox, SIGNAL("set_begin_with"), self.set_begin_with)

        self.connect(self.configBox, SIGNAL("click_ok"), self.my_table_init)



        s = '''
        i = 20
        while(i>0):
            self.ui.tableWidget.insertRow(0)
            i = i-1
        '''
        #设置表格不可编辑
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        s='''
        #添加表格数据
        self.add_row(["IQ_DUT_CALIBRATION"])
        self.add_row(["IQ_MDK_TEST_BEGIN"])
        self.add_row(["IQ_VERIFY_TX_ALL","2412","11M","CHANI0"])
        self.add_row(["IQ_VERIFY_TX_ALL","2412","11M","CHANI1"])
        self.add_row(["IQ_VERIFY_TX_ALL","2412","11M","CHANI2"])
        self.add_row(["IQ_VERIFY_TX_ALL","2412","11M","CHANI3"])
        '''
        
        #self.table_add_header([u"项目", u"命令"])
        
        #item = self.ui.tableWidget.item(1,1)
        #成功绿
        #self.ui.tableWidget.itemAt(1,1).setStyleSheet("QTableView::item{background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #00FF00, stop:1 #00EE00);}\
        #                                   QTableView::item:selected{background:#00CD00;}\
        #                                   QTableView::item:hover{background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #00EE76, stop:1 #00CD66);}")
        #self.ui.tableWidget.item(2,2).setBackgroundColor(Qt.red)

        #失败红
        s = '''
        self.ui.tableWidget.setStyleSheet("QTableView::item{background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #EE3B3B, stop:1 #EE2C2C);}\
                                           QTableView::item:selected{background:#B22222;}\
                                           QTableView::item:hover{background:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #CD2626, stop:1 #CD0000);}")
        '''
        
        s = '''
        self.table_sucess(0)
        self.table_sucess(1)
        self.table_fail(2)
        self.table_sucess(3)
        self.table_sucess(4)
        self.table_fail(5)
        self.table_reset()
        '''

        # QWidget.setFocusPolicy()
        # self.ui.widget_main.setFocusPolicy(self.ui.lineEdit)
        self.ui.lcdNumber.display("00:00")
        self.ui.lineEdit.setFocus()
        self.ui.lineEdit.setMaxLength(13)
        #self.start_time = QDateTime.currentDateTime()
        self.start_time = QTime.fromString("00:00","mm:ss")
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.lcd_flash) 
        #self.timer.start(1000)
        
        
        font = self.ui.textEdit_2.currentFont()
        #self.iconFont.setPointSize(32)
        # self.ui.textEdit_2.setFontPointSize(64)
        #self.ui.textEdit_2.setAlignment(Qt.AlignJustify)
        #self.ui.textEdit_2.setTextColor(Qt.green)
        #self.ui.textEdit_2.setCurrentFont(self.iconFont)

        if(self.conf.get_begin_with_MACorSN()=='1'):
            print self.conf.get_begin_with_MACorSN()
            self.ui.label.setText(u"SN")
        else:
            self.ui.label.setText(u"MAC")

        self.ui.textEdit_2.setText(u"准备")



        #self.ui.textEdit_2.setTextColor(QColor.white)
        self.ui.textEdit_2.setAlignment(Qt.AlignCenter)
        #self.ui.textEdit_2.setStyleSheet("color:#FFF;border-style: none;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #00EE00, stop:1 #00CD00); ")
        self.ui.textEdit_2.setStyleSheet("color:#000;border-style: none;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #D4D4D4, stop:1 #D4D4D4);")
        #print self.ui.textEdit_2.currentFont().defaultFamily()
        
        
        #生成skin按钮菜单
        self.skin_menu = QMenu()
        self.skin_black_action = QAction(self.skin_menu)
        self.skin_ironblue_action = QAction(self.skin_menu)
        self.skin_silvery_action = QAction(self.skin_menu)
        self.skin_black_action.setCheckable(True)
        self.skin_ironblue_action.setCheckable(True)
        self.skin_silvery_action.setCheckable(True)
        self.skin_menu.addAction(self.skin_black_action)
        self.skin_menu.addAction(self.skin_ironblue_action)
        self.skin_menu.addAction(self.skin_silvery_action)
        self.skin_black_action.setText(u"   黑色  ")
        self.skin_ironblue_action.setText(u"   淡钢蓝  ")
        self.skin_silvery_action.setText(u"   银色  ")
        self.ui.btnSkin.setMenu(self.skin_menu)
        
        self.connect(self.skin_black_action, SIGNAL("triggered()"), self.set_style_black) 
        self.connect(self.skin_ironblue_action, SIGNAL("triggered()"), self.set_style_ironblue) 
        self.connect(self.skin_silvery_action, SIGNAL("triggered()"), self.set_style_silvery) 
        self.connect(self.skin_black_action, SIGNAL("hovered()"), self.set_style_black)
        self.connect(self.skin_ironblue_action, SIGNAL("hovered()"), self.set_style_ironblue)
        self.connect(self.skin_silvery_action, SIGNAL("hovered()"), self.set_style_silvery)
        
        self.menu_menu = QMenu()
        #生成菜单
        self.change_type_action = QAction(self.menu_menu)
        self.menu_menu.addAction(self.change_type_action)
        self.change_type_action.setText(u"  切换型号    ")
        if user_type == '2':

            self.do_config_action = QAction(self.menu_menu)
            self.reset_action = QAction(self.menu_menu)

            self.menu_menu.addAction(self.do_config_action)
            self.menu_menu.addAction(self.reset_action)

            self.do_config_action.setText(u"  设置    ")
            self.reset_action.setText(u"  清空输出    ")
            self.ui.btnMenu.setMenu(self.menu_menu)
            self.connect(self.reset_action, SIGNAL("triggered()"), self.reset_window)
            self.connect(self.do_config_action, SIGNAL("triggered()"), self.show_config_window)
        if user_type == '1':
            self.ui.textEdit.setVisible(False)
            self.ui.tableWidget.setVisible(False)
            self.ui.textEdit_2.setText(u"\n\n\n\n           准备")
        self.get_B_xiansun = QAction(self.menu_menu)
        self.get_B_xiansun.setText(u"  计算线损  ")
        self.menu_menu.addAction(self.get_B_xiansun)
        self.connect(self.get_B_xiansun, SIGNAL("triggered()"),self.show_xiansun_window)

        self.change_skin_action = QAction(self.menu_menu)
        self.menu_menu.addAction(self.change_skin_action)
        self.change_skin_action.setText(u"  皮肤    ")
        self.change_skin_action.setMenu(self.skin_menu)
        # s='''
        self.type_menu = QMenu()
        self.type_I23B_action = QAction(self.type_menu)
        self.type_I22B_action = QAction(self.type_menu)
        self.type_WE2622_action = QAction(self.type_menu)
        self.type_G22B_action = QAction(self.type_menu)
        self.type_G23B_action = QAction(self.type_menu)
        self.type_WE2622_prep_action = QAction(self.type_menu)

        # self.type_octeon_action = QAction(self.type_menu)
        self.type_I23B_action.setCheckable(True)
        self.type_I22B_action.setCheckable(True)
        self.type_WE2622_action.setCheckable(True)
        self.type_G22B_action.setCheckable(True)
        self.type_G23B_action.setCheckable(True)
        self.type_WE2622_prep_action.setCheckable(True)

        # self.type_octeon_action.setCheckable(True)
        # 添加点击
        self.type_menu.addAction(self.type_I23B_action)
        self.type_menu.addAction(self.type_I22B_action)
        self.type_menu.addAction(self.type_WE2622_action)
        self.type_menu.addAction(self.type_G22B_action)
        self.type_menu.addAction(self.type_G23B_action)
        #隐藏we2622_prep
        #self.type_menu.addAction(self.type_WE2622_prep_action)

        # self.type_menu.addAction(self.type_octeon_action)
        self.type_I23B_action.setText(u"  I23B型号  ")
        self.type_I22B_action.setText(u"  I22B型号  ")
        self.type_WE2622_action.setText(u"  WE2622型号  ")
        self.type_G22B_action.setText(u"  G22B型号  ")
        self.type_G23B_action.setText(u"  G23B型号  ")
        self.type_WE2622_prep_action.setText(u"  WE2622备用类型  ")

        # self.type_octeon_action.setText(u"  octeon系列  ")
        # '''
        self.change_type_action.setMenu(self.type_menu)

        # 绑定信号槽
        self.connect(self.type_I23B_action, SIGNAL("triggered()"), self.set_type_I23B)
        self.connect(self.type_I22B_action, SIGNAL("triggered()"), self.set_type_I22B)


        self.connect(self.type_WE2622_action, SIGNAL("triggered()"), self.set_type_WE2622)
        self.connect(self.type_G22B_action, SIGNAL("triggered()"), self.set_type_G22B)
        self.connect(self.type_G23B_action, SIGNAL("triggered()"), self.set_type_G23B)

        self.connect(self.type_WE2622_prep_action,SIGNAL("triggered()"),self.set_type_WE2622_prep)

        # self.connect(self.type_octeon_action, SIGNAL("triggered()"), self.set_type_octeon)
        # self.connect(self.type_I23B_action, SIGNAL("hovered()"), self.set_type_I23B)
        # self.connect(self.type_WE2622_action, SIGNAL("hovered()"), self.set_type_WE2622)
        # self.connect(self.type_octeon_action, SIGNAL("hovered()"), self.set_type_octeon)


        #定义右键菜单
        self.right_menu = QMenu()
        self.right_close_action = QAction(self.right_menu)
        self.right_max_action = QAction(self.right_menu)
        self.right_min_action = QAction(self.right_menu)
        #self.right_logo_action = QAction(self.right_menu)
        self.right_menu.addAction(self.right_min_action)
        self.right_menu.addAction(self.right_max_action)
        self.right_menu.addAction(self.right_close_action)
        #self.right_menu.addAction(self.right_logo_action)
        self.right_close_action.setText(u"  关闭    ")
        self.right_max_action.setText(u"  最大化    ")
        self.right_min_action.setText(u"  最小化    ")
        #self.right_logo_action.setFont(self.iconFont)
        #self.SetIcon(self.right_logo_action, "1", 10)
        #self.right_logo_action.setIconText(QChar(0xFFE5))
        #print self.right_logo_action.font().family()
        #self.right_logo_action.setIcon(QIcon(":/image/checkbox_checked.png"))
        #self.SetIcon(self.right_logo_action, QChar(0xf015), 10)
        self.right_close_action.setShortcuts(QKeySequence("Alt+F4"))
        
        self.connect(self.right_close_action, SIGNAL("triggered()"),self.close)
        self.connect(self.right_max_action, SIGNAL("triggered()"), self.on_btnMenu_Max_clicked) 
        self.connect(self.right_min_action, SIGNAL("triggered()"), self.on_btnMenu_Min_clicked) 
        
        #设置配置(放在界面定义后)
        self.set_skin()
        self.my_table_init(self.conf)

        # self.show_zhiju_view()
        #self.set_type()
        
        #self.emit(SIGNAL("table_color"), 0,"success")
        #self.emit(SIGNAL("table_color"), 1,"fail")
    def show_zhiju_view(self):
        zhiju = ZhijuDiaLog()
        zhiju.exec_()

    def close(self):
        sys.exit(0);

    def set_text_zhunbei(self):
        self.ui.textEdit_2.setText(u"\n\n\n\n           准备")

    def set_focus_to_lineEdit(self):
        self.ui.lineEdit.setFocus()
    def exit(self):
        self.thread.__del__()

    def btn_close(self):
        self.close()

    def change_result_btn_to_success(self):
        myconf = MyConf()
        testConf= TestConf()
        jiaozhun_flag = testConf.get_is_or_not_jiaozhun()
        sn_num = myconf.get_sn_num()
        jiaozhun_str = ""
        if jiaozhun_flag == "1":
            self.ui.textEdit_2.setText(u"\n\n"+sn_num+u"\n\n  初测        成功")

        else:
            self.ui.textEdit_2.setText(u"\n\n"+sn_num+u"\n\n  复测        成功")



        self.ui.textEdit_2.setAlignment(Qt.AlignCenter)
        self.ui.textEdit_2.setStyleSheet("color:#00FF00")
        # self.ui.textEdit_2.setStyleSheet("color:#FFF;border-style: none;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #98FB98, stop:1 #98FB98);")

    def change_result_btn_to_fail(self):
        # global test_result_fail
        global fail_mssage
        myconf = MyConf()
        testConf = TestConf()
        sn_num = myconf.get_sn_num()

        jiaozhun_str = ""

        jiaozhun_flag = testConf.get_is_or_not_jiaozhun()
        if jiaozhun_flag == "1":
            self.ui.textEdit_2.setText(u"\n"+sn_num+u"\n   初测         失败\n" +trunk.protest_standby.get_fail_massage())

        else:
            self.ui.textEdit_2.setText(u"\n"+sn_num+u"\n   复测         失败\n" +trunk.protest_standby.get_fail_massage())

        print str(trunk.protest_standby.get_test_result())+" #### test result####"
        self.ui.textEdit_2.setAlignment(Qt.AlignCenter)
        self.ui.textEdit_2.setStyleSheet("color:#FF0000")
        # self.ui.textEdit_2.setStyleSheet("color:#FFF;border-style: none;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #00EC00, stop:1 #00EC00);")



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()
 
    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.LeftButton and not self.Max):
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def set_begin_with(self):
        self.conf =  TestConf()
        if(self.conf.get_begin_with_MACorSN()=='1'):
            print (self.conf.get_something("global","begin_with_macorsn"))
            self.ui.label.setText(u"SN")
        else:
            self.ui.label.setText(u"MAC")

    def on_btnMenu_Max_clicked(self):
        w = QDesktopWidget()
        if(self.Max):
            self.setGeometry(self.location);
            self.SetIcon(self.ui.btnMenu_Max, QChar(0xf096), 10)
            self.ui.btnMenu_Max.setToolTip(u"最大化")
            self.right_max_action.setText(u"  最大化    ")
        else:
            self.location = self.geometry();
            self.setGeometry(w.availableGeometry())
            self.SetIcon(self.ui.btnMenu_Max, QChar(0xf079), 10)
            self.ui.btnMenu_Max.setToolTip(u"还原")
            self.right_max_action.setText(u"  还原    ")
        self.Max = not self.Max
    
    def on_btnMenu_Min_clicked(self):
        self.showMinimized()
    
    def SetIcon(self, obj, text, size):
        self.iconFont.setPointSize(size)
        obj.setFont(self.iconFont)
        obj.setText(text)
    
    def eventFilter(self, obj, event):
        if(obj == self.ui.lab_Title):
            if(event.type() == QEvent.MouseButtonDblClick):
                self.on_btnMenu_Max_clicked()
                return True
            elif(event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton):
                self.right_button_click()
                return True
        elif(obj == self.ui.lab_Ico):
            if(event.type() == QEvent.MouseButtonDblClick):
                self.accept()
                return True
            elif(event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton):
                self.right_button_click()
                return True
            elif(event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton):
                pos = self.ui.widget_main.geometry();
                self.right_menu.exec_(self.geometry().topLeft() + pos.topLeft())
                return True
        return QObject.eventFilter(self, obj, event)
    
    def makeText(self,mystr,color):
        self.ui.textEdit.moveCursor(11, 0)
        self.ui.textEdit.setTextColor(color)
        self.ui.textEdit.insertPlainText(mystr)

    def show_error_change_mode(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"AP执行命令时失败，请检查后重试", 2)
        return msg.exec_()

    def show_error_telnet(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"抱歉，向AP发送命令时失败！请重试！", 2)
        return msg.exec_()
    def show_error_sn(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"sn序列号不匹配，请检查重试！", 2)
        return msg.exec_()
    def show_error_base_info(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"当前AP基测信息未通过，请检查重试！", 2)
        return msg.exec_()
    def show_error_ipuse(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"当前电脑超出使用次数，请检查重试！", 2)
        return msg.exec_()
    def show_error_old_info(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"老化信息失败，请检查重试！", 2)
        return msg.exec_()
    def show_error_change_mode(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"登陆AP失败，请检查重试！", 2)
        return msg.exec_()
    def show_error_old_hours(self):
        msg = MyMSGForm()
        qss = QFile(self.qssfile);
        qss.open(QFile.ReadOnly);
        q = QString(qss.readAll())
        msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"老化时间不合格，请检查重试！", 2)
        return msg.exec_()

    #显示连接错误
    def show_error_lian_jie(self):
        msg = MyMSGForm()
        # qss = QFile(self.qssfile);
        # qss.open(QFile.ReadOnly);
        # q = QString(qss.readAll())
        # msg.setStyleSheet(q);
        #msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
        msg.SetMessage(u"连接地址ping失败，请检查连接", 2)
        return msg.exec_()

    def show_save_log_fail(self):
        msg = MyMSGForm()
        msg.SetMessage(u"保存日志log失败，请检查地址！", 2)
        return msg.exec_()

    def show_login_dialog(self):
        login = LoginDiaLog()
        return login.exec_()

    # def A_power_get(self):
    #     thread_A = Worker_A()
    #     conf = TestConf()
    #     thread_A.render(conf.get_default_ip())

    def create_test_thread(self,testconf,version="I23B"):
        '''创建测试线程'''
        # version = Version_ini()
        # this_version = version.get_version()
        # # 初始化窗体的时候就创建一个线程，
        # if this_version == "WE2622" or this_version == "WE2622_prep":
        #     self.thread = Worker()  # 测试WB262工作线程
        # elif this_version == "I23B" or this_version == "G22B":
        #     self.thread = Worker_I23B()  # 测试I23B工作线程
        # else:
        if version=="I22B":
            self.thread = trunk.protest_standby.Worker_I22B(testconf=testconf)  # 测试I23B工作线程
        elif version=="I23B":
            # self.thread = trunk.protest_I23B.Worker_I23B()  # 测试I23B工作线程
            self.thread = trunk.protest_standby.Worker_I23B(testconf=testconf)  # 测试I23B工作线程
        # self.ui.pushButton_2.clicked.connect(self.doTest)
        elif version=="WE2622":
            self.thread = trunk.protest_standby.Worker_WE2622(testconf=testconf)  # 测试WB262工作线程
        elif version == "WE2622_prep":
            self.thread = trunk.protest_standby.Worker_WE2622_prep(testconf=testconf)
        elif version == "G22B":
            self.thread = trunk.protest_standby.Worker_G22B(testconf=testconf)
        elif version == "G23B":
            self.thread = trunk.protest_standby.Worker_G23B(testconf=testconf)
        else:
            return "no match version"

        self.connect(self.thread, SIGNAL("output"), self.makeText)
        self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        self.connect(self.thread, SIGNAL("terminated()"), self.updateUi_not_save_log)
        # 触发保存日志。
        # self.connect(self.thread, SIGNAL("save_log"), self.save_log_file_only())

        self.connect(self.thread, SIGNAL("table_color"), self.table_get_result)

        self.connect(self.thread, SIGNAL("error_ping"), self.show_error_lian_jie)
        self.connect(self.thread, SIGNAL("error_change_mode"), self.show_error_change_mode)
        self.connect(self.thread, SIGNAL("error_sn"), self.show_error_sn)
        self.connect(self.thread, SIGNAL("error_telnet"), self.show_error_telnet)
        self.connect(self.thread, SIGNAL("error_base_info"), self.show_error_base_info)
        self.connect(self.thread, SIGNAL("error_ipuse"), self.show_error_ipuse)
        self.connect(self.thread, SIGNAL("error_old_info"), self.show_error_old_info)
        self.connect(self.thread, SIGNAL("error_change_mode"), self.show_error_change_mode)
        self.connect(self.thread, SIGNAL("error_old_hours"), self.show_error_old_hours)
        self.connect(self.thread, SIGNAL("set_focus"), self.set_focus_to_lineEdit)
        self.connect(self.thread, SIGNAL("zhunbei_txt"), self.set_text_zhunbei)

        self.connect(self.thread, SIGNAL("exit"), self.exit)
        self.connect(self.thread, SIGNAL("result_success"), self.change_result_btn_to_success)
        self.connect(self.thread, SIGNAL("result_fail"), self.change_result_btn_to_fail)

        self.connect(self.thread, SIGNAL("testing1"), self.updateUi_testing1)
        self.connect(self.thread, SIGNAL("testing2"), self.updateUi_testing2)
        self.connect(self.thread, SIGNAL("testing3"), self.updateUi_testing3)
        self.connect(self.thread, SIGNAL("jiaozhuning1"), self.updateUi_jiaozhuning1)
        self.connect(self.thread, SIGNAL("jiaozhuning2"), self.updateUi_jiaozhuning2)
        self.connect(self.thread, SIGNAL("jiaozhuning3"), self.updateUi_jiaozhuning3)

    def check_sn_or_mac(self,testconf):
        # testconf = TestConf()
        begin_with_mac_or_sn = testconf.get_begin_with_MACorSN()
        sn_num = self.get_and_set_sn()
        if begin_with_mac_or_sn == '1':
            if (sn_num):
                # msg = myHelper()
                msg = MyMSGForm()
                qss = QFile(self.qssfile);
                qss.open(QFile.ReadOnly);
                q = QString(qss.readAll())
                msg.setStyleSheet(q);
                # msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
                msg.SetMessage(u"设置sn地址错误，请检查sn地址是否正确！", 2)
                return msg.exec_()
        else:
            if (self.get_and_set_mac()):
                # msg = myHelper()
                msg = MyMSGForm()
                qss = QFile(self.qssfile);
                qss.open(QFile.ReadOnly);
                q = QString(qss.readAll())
                msg.setStyleSheet(q);
                # msg.ShowMessageBoxError(u"设置mac地址错误，请检查mac地址是否正确！")
                msg.SetMessage(u"设置mac地址错误，请检查mac地址是否正确！", 2)
                return msg.exec_()

    def start_test(self,testconf):
        self.ui.textEdit.setText("")
        self.ui.lcdNumber.display("00:00")
        # self.ui.lineEdit.setReadOnly(1)
        self.ui.pushButton_2.clicked.disconnect(self.doTest)
        # self.ui.pushButton_2.clicked.disconnect(self.config)
        self.ui.pushButton_2.setText(u"测试中...")
        x = time.localtime(time.time())
        t = time.strftime('%Y-%m-%d %H:%M:%S', x)
        self.thread.printstr(u"------ 开始测试 - %s -------\n" % t, QColor(255, 0, 0, 127))
        # self.thread.render(self.ui.lineEdit.text())

        # myconf = MyConf()
        # user_type = myconf.get_user_type()

        self.thread.render(testconf.get_default_ip())
        self.start_time = QTime.fromString("00:00", "mm:ss")
        self.timer.start(1000)
        # self.change_type_action.setEnabled(False)
        # if user_type == '2':
        #     self.reset_action.setEnabled(False)
        # self.table_init()
        self.my_table_init(testconf)
        self.ui.textEdit_2.setText(u"\n\n\n          测试中。。。")
        self.ui.textEdit_2.setAlignment(Qt.AlignCenter)
        self.ui.textEdit_2.setStyleSheet("color:#000;border-style: none;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #D4D4D4, stop:1 #D4D4D4);")

    def doTest(self):
        '''开始按钮操作'''
        print 'get version'
        version = Version_ini()
        print 'get test config'
        testconf = TestConf()
        print 'check sn or mac'
        # 检查sn或mac地址
        if self.check_sn_or_mac(testconf) !=None:
            return
        #根据选择的设备类型，产生一个测试线程
        print 'create test thread'
        if self.create_test_thread(testconf,version.get_version())!=None:
            QMessageBox(text=u"无法测试此版本！").exec_()
            return
        print 'start test'
        self.start_test(testconf)

    def is_or_not_begin_thread(self):
        #如果ping通了并且准备工作完成返回1否则返回0

        if self.ready_thread.ping_flag == 1:
            return 1
        else:
            return 0
    def updateUi_not_save_log(self):
        self.ui.pushButton_2.clicked.connect(self.doTest)
        #self.ui.pushButton_2.clicked.connect(self.config)
        self.ui.pushButton_2.setText(u"开始")
        x = time.localtime(time.time())
        t = time.strftime('%Y-%m-%d %H:%M:%S',x)
        self.thread.printstr(u"------ 测试结束 - %s -------\n" % t,QColor(255, 0, 0, 127))
        self.timer.stop()
        # self.change_type_action.setEnabled(True)
        myconf = MyConf()
        # user_type = myconf.get_user_type()
        # if user_type == '2':
        #     self.reset_action.setEnabled(True)
        # self.save_log_2_file()
    def updateUi_testing1(self):
        self.ui.textEdit_2.setText(u"\n\n\n 测试中。")
    def updateUi_testing2(self):
        self.ui.textEdit_2.setText(u"\n\n\n 测试中。 （＾_＾）")
    def updateUi_testing3(self):
        self.ui.textEdit_2.setText(u"\n\n\n 测试中。——")
    def updateUi_jiaozhuning1(self):
        self.ui.textEdit_2.setText(u"\n\n\n 校准中。（＾_＾）")
    def updateUi_jiaozhuning2(self):
        self.ui.textEdit_2.setText(u"\n\n\n 校准中。")
    def updateUi_jiaozhuning3(self):
        self.ui.textEdit_2.setText(u"\n\n\n 校准中。——")

    # def save_log_file_only(self):
    #     self.save_log_2_file()
    def updateUi(self): 
        #self.ui.lineEdit.setReadOnly(0)
        self.ui.pushButton_2.clicked.connect(self.doTest)
        #self.ui.pushButton_2.clicked.connect(self.config)
        self.ui.pushButton_2.setText(u"开始")
        x = time.localtime(time.time())
        t = time.strftime('%Y-%m-%d %H:%M:%S',x)
        self.thread.printstr(u"------ 测试结束 - %s -------\n" % t,QColor(255, 0, 0, 127))
        self.timer.stop()
        # self.change_type_action.setEnabled(True)
        myconf = MyConf()
        user_type = myconf.get_user_type()
        sn_num = myconf.get_sn_num()
        # if user_type == '2':
        #     self.reset_action.setEnabled(True)
        self.save_log_2_file()
        self.set_focus_to_lineEdit()
        # self.ui.textEdit.setText("")
        self.ui.lineEdit.setText("")

        # self.ui.textEdit_2.setText(u"准备")


        # if get_test_result() != 0:
        #     self.ui.textEdit_2.setText(u"\n"+sn_num+u"\n            失败" +get_fail_massage())
        #     self.ui.textEdit_2.setStyleSheet("color:#FF0000")
        #

        # else:
        #     self.ui.textEdit_2.setText(u"\n\n\n\n\n             成功")
        # self.ui.textEdit_2.setAlignment(Qt.AlignCenter)
        # self.ui.textEdit_2.setStyleSheet("color:#FFF;border-style: none;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #D4D4D4, stop:1 #D4D4D4);")
    def save_log_2_file(self):
        # 测试PC的MAC地址 _ 基板条码 _ 测试日期时间 _ 测试结果 _ 测试项目[初测/复测]
        global test_result_fail
        if(os.path.exists('mylog') == False):
            os.makedirs('mylog')
        t = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

        myconf = MyConf()
        testconf = TestConf()

        sn_str = myconf.get_sn_num()
        mac_str = self.get_this_mac_address()
        log_adress = myconf.get_log_address()

        station = testconf.get_is_or_not_jiaozhun()
        sta = "Test"#表示初测
        result_str = "Fail"#表示失败
        if station =='0':
            sta = 'Retest'
        print str(trunk.protest_standby.get_test_result())+" #### test result####"
        if trunk.protest_standby.get_test_result() == 0 :
            result_str = "Pass"
            trunk.protest_standby.set_fail_mssage('')
            trunk.protest_standby.set_jiaozhun_result(0)
        zhiju_str = myconf.get_zhiju_id()
        try:
            # file1 = open(log_adress+"\\"+mac_str+"-"+zhiju_str+"-"+sn_str+"-"+t+"-"+sta+"-"+result_str+".log", "w")
            file1 = open(
                log_adress + "\\" + mac_str + "-" + sn_str + "-" + t + "-" + sta + "-" + result_str + ".log",
                "w")

            file1.write(self.ui.textEdit.toPlainText())
        except:
            self.show_save_log_fail()
        finally:
            file1.close()
    def get_this_mac_address(self):
        import uuid
        node = uuid.getnode()
        mac = uuid.UUID(int = node).hex[-12:]
        return mac
    def lcd_flash(self):
        #current_time = QDateTime.currentDateTime()
        self.start_time = self.start_time.addSecs(1)
        self.ui.lcdNumber.display(self.start_time.toString("mm:ss"))
    
    #def table_item_sucess(self, line):
    def add_row(self, item_list):
        length = len(item_list)
        total_row = self.ui.tableWidget.rowCount()
        total_column = self.ui.tableWidget.columnCount()
        self.ui.tableWidget.insertRow(total_row)
        for j in range(total_column):
            if(j < length):
                newItem = QTableWidgetItem(item_list[j])
                self.ui.tableWidget.setItem(total_row, j, newItem)
            else:
                newItem = QTableWidgetItem("")
                self.ui.tableWidget.setItem(total_row, j, newItem)
            
    def row_set_color(self, n, color):
        total_column = self.ui.tableWidget.columnCount()
        #print "column = " + str(total_column)
        for j in range(total_column):
            #print n,j
            self.ui.tableWidget.item(n, j).setBackgroundColor(color)

        self.ui.tableWidget.scrollToItem(self.ui.tableWidget.item(n, 0))


    
    def table_sucess(self, n):
        #light_green = QColor(Qt.green).lighter(factor = 128)
        light_green = QColor(Qt.green).lighter(factor = 150)
        self.row_set_color(n, light_green)
    
    def table_fail(self, n):
        self.row_set_color(n, Qt.red)
    
    def table_reset(self):
        total_row = self.ui.tableWidget.rowCount()
        for n in range(total_row):
            self.row_set_color(n, Qt.white)
    
    def set_style(self, qssfile):
        qss = QFile(qssfile); 
        qss.open(QFile.ReadOnly); 
        q = QString(qss.readAll())
        self.setStyleSheet(q); 
        self.skin_menu.setStyleSheet(q); 
        self.menu_menu.setStyleSheet(q); 
        #self.type_menu.setStyleSheet(q); 
        self.right_menu.setStyleSheet(q); 
    
    def set_style_black(self):
        myconf = MyConf()
        myconf.set_skin_black()
        self.set_style("black.css")
        self.qssfile = "black.css"
        self.skin_uncheck_all()
        self.skin_black_action.setChecked(True)
    
    def set_style_ironblue(self):
        myconf = MyConf()
        myconf.set_skin_ironblue()
        self.set_style("ironblue.css")
        self.qssfile = "ironblue.css"
        self.skin_uncheck_all()
        self.skin_ironblue_action.setChecked(True)
        
    def set_style_silvery(self):
        myconf = MyConf()
        myconf.set_skin_silvery()
        self.set_style("silvery.css")
        self.qssfile = "silvery.css"
        self.skin_uncheck_all()
        self.skin_silvery_action.setChecked(True)
    
    def set_skin(self):
        myconf = MyConf()
        skin = myconf.get_skin()
        
        if(skin == "black"):
            #self.set_style("black.css")
            self.set_style_black()
        elif(skin == 'ironblue'):
            #self.set_style("ironblue.css")
            self.set_style_ironblue()
        elif(skin == 'silvery'):
            #self.set_style("silvery.css")
            self.set_style_silvery()
    
    def skin_uncheck_all(self):
        self.skin_black_action.setChecked(False)
        self.skin_ironblue_action.setChecked(False)
        self.skin_silvery_action.setChecked(False)


    def set_type_WE2622_prep(self):
        version = Version_ini()
        version.set_version("WE2622_prep")
        self.type_uncheck_all()
        self.type_WE2622_prep_action.setChecked(True)
        # self.type_G22B_action.setChecked(False)
        # self.type_G23B_action.setChecked(False)
        # self.type_I23B_action.setChecked(False)
        # self.type_WE2622_action.setChecked(False)
        # self.type_I22B_action.setChecked(False)
        # 刷新窗口。
        testconf = TestConf()
        self.my_table_init(testconf)
        # 更新显示版本
        self.info_window_flush()

    def set_type_G23B(self):
        version = Version_ini()
        version.set_version("G23B")
        self.type_uncheck_all()
        self.type_G23B_action.setChecked(True)
        # self.type_I23B_action.setChecked(False)
        # self.type_WE2622_action.setChecked(False)
        # self.type_WE2622_prep_action.setChecked(False)
        # self.type_G22B_action.setChecked(False)
        # self.type_I22B_action.setChecked(False)
        # 刷新窗口。
        testconf = TestConf()
        self.my_table_init(testconf)
        # 更新显示版本
        self.info_window_flush()

    def set_type_G22B(self):
        version = Version_ini()
        version.set_version("G22B")
        self.type_uncheck_all()
        self.type_G22B_action.setChecked(True)
        # self.type_G23B_action.setChecked(False)
        # self.type_I23B_action.setChecked(False)
        # self.type_WE2622_action.setChecked(False)
        # self.type_WE2622_prep_action.setChecked(False)
        # self.type_I22B_action.setChecked(False)
        # 刷新窗口。
        testconf = TestConf()
        self.my_table_init(testconf)
        # 更新显示版本
        self.info_window_flush()

    def set_type_I22B(self):
        version = Version_ini()
        # 修改配置中version。ini版本为I23B
        version.set_version("I22B")
        self.type_uncheck_all()
        self.type_I22B_action.setChecked(True)
        # self.type_I23B_action.setChecked(False)
        # self.type_WE2622_action.setChecked(False)
        # self.type_G22B_action.setChecked(False)
        # self.type_G23B_action.setChecked(False)
        # self.type_WE2622_prep_action.setChecked(False)
        # 刷新窗口。
        testconf=TestConf()
        self.my_table_init(testconf)
        # 更新显示版本
        self.info_window_flush()

    def set_type_I23B(self):
        version = Version_ini()
        # 修改配置中version。ini版本为I23B
        version.set_version("I23B")
        self.type_uncheck_all()
        self.type_I23B_action.setChecked(True)
        # self.type_WE2622_action.setChecked(False)
        # self.type_G22B_action.setChecked(False)
        # self.type_WE2622_prep_action.setChecked(False)
        # self.type_I22B_action.setChecked(False)
        # self.type_G23B_action.setChecked(False)
        # 刷新窗口。
        testconf = TestConf()
        self.my_table_init(testconf)
        # 更新显示版本
        self.info_window_flush()


    def set_type_WE2622(self):
        version = Version_ini()
        # 修改配置中version。ini版本为I23B
        version.set_version("WE2622")
        self.type_uncheck_all()
        self.type_WE2622_action.setChecked(True)
        # self.type_I23B_action.setChecked(False)
        # self.type_G22B_action.setChecked(False)
        # self.type_WE2622_prep_action.setChecked(False)
        # self.type_I22B_action.setChecked(False)
        # self.type_G23B_action.setChecked(False)
        # 刷新窗口。
        testconf = TestConf()
        self.my_table_init(testconf)
        self.info_window_flush()
        
    # def set_type_octeon(self):
    #     myconf = MyConf()
    #     myconf.set_type_octeon()
    #     self.type_uncheck_all()
    #     self.type_octeon_action.setChecked(True)
    #     #self.table_add_header([u"项目", u"命令"])
    #     self.octeon_table_init()
    #     self.info_window_flush()
    
    # def set_type(self):
    #     myconf = MyConf()
    #     mytype = myconf.get_type()
    #
    #     if(mytype == "mt7620a"):
    #         self.set_type_I23B()
    #     elif(mytype == 'ar934x'):
    #         self.set_type_WE2622()
    #     # elif(mytype == 'octeon'):
    #     #     self.set_type_octeon()

    # 设置当前都为为选中状态。
    def type_uncheck_all(self):
        pass
        self.type_I23B_action.setChecked(False)
        self.type_WE2622_action.setChecked(False)
        self.type_G22B_action.setChecked(False)
        self.type_G23B_action.setChecked(False)
        self.type_WE2622_prep_action.setChecked(False)
        self.type_I22B_action.setChecked(False)
        # self.type_octeon_action.setChecked(False)

    def right_button_click(self):
        cur = self.cursor()
        self.right_menu.exec_(cur.pos())
    
    #添加表头
    def table_add_header(self, item_list):
        length = len(item_list)
        #print length
        #total_row = self.ui.tableWidget.rowCount()
        #total_column = self.ui.tableWidget.columnCount()
        #self.ui.tableWidget.insertRow(total_row)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(length)
        for j in range(length):
            item = QTableWidgetItem()
            self.ui.tableWidget.setHorizontalHeaderItem(j, item)
            self.ui.tableWidget.horizontalHeaderItem(j).setText(item_list[j])
            #if(j < length):
            #    newItem = QTableWidgetItem(item_list[j])
            #    self.ui.tableWidget.setItem(total_row, j, newItem)
            #else:
            #    newItem = QTableWidgetItem("")
            #    self.ui.tableWidget.setItem(total_row, j, newItem)
    
    def info_window_flush(self):
        # myconf = MyConf()
        # mytype = myconf.get_type()
        version = Version_ini()
        this_version = version.get_version()
        this_type = u"博达通信--"+this_version
        self.ui.lab_Title.setText(this_type)

        # 设置皮肤
        self.set_skin()
        
    # def table_init(self):
    #     # myconf = MyConf()
    #     # version = Version_ini()
    #     # mytype = version.get_version()
    #     self.my_table_init()
    #     # if(mytype == "mt7620a"):
    #     #     self.my_table_init()
    #     # elif(mytype == 'ar934x'):
    #     #     self.my_table_init()
    #     # elif(mytype == 'octeon'):
    #     #     self.octeon_table_init()
    
    # def add_table_row(self, name, freq_all, rate_all, chain_all):
    #     for freq in freq_all:
    #         for rate in rate_all:
    #             for chain in chain_all:
    #                 self.add_row([name,freq,rate,chain])
    #
    def add_2G_table(self):

        self.add_row([u"2G校准"])
        self.add_row([u"2G频偏校准"])

        testconfigxml = TestConfigxml()
        root = testconfigxml.read_xml()
        test = testconfigxml.get_all_test(root)
        for g2_or_g5 in test:
            if(g2_or_g5.get('name')=='2G'):
                all_test_items = testconfigxml.get_test_items(g2_or_g5)
                for test_item in all_test_items:
                    if test_item.get('name') == "ht20":
                        all_freqs = testconfigxml.get_all_freq(test_item)
                        for freqs in all_freqs:
                            val = freqs.find('val').text
                            rates = freqs.find('rate').text.split(",")
                            chains = freqs.find('chain').text.split(",")

                            for rate in rates:
                                for chain in chains:
                                    self.add_row(["2G tx ht20",val, rate, chain])
                    elif test_item.get('name') == "ht40":
                        all_freqs = testconfigxml.get_all_freq(test_item)
                        for freqs in all_freqs:
                            val = freqs.find('val').text
                            rates = freqs.find('rate').text.split(",")
                            chains = freqs.find('chain').text.split(",")

                            for rate in rates:
                                for chain in chains:
                                    self.add_row(["2G tx ht40",val, rate, chain])
                    else:
                        all_freqs = testconfigxml.get_all_freq(test_item)
                        for freqs in all_freqs:
                            val = freqs.find('val').text
                            rates = freqs.find('rate').text.split(",")
                            chains = freqs.find('chain').text.split(",")

                            for rate in rates:
                                for chain in chains:
                                    self.add_row(["2G rx",val, rate, chain])






        # testconf = TestConf()
        # self.add_row([u"2G校准"])
        # self.add_row([u"2G频偏校准"])
        # #print "tx_power_ht20_freq",testconf.get_num_of_something("2G","tx_power_ht20_freq")
        # tx_ht20_freq = testconf.get_something("2G","tx_ht20_freq").split(",")
        # tx_ht20_rate = testconf.get_something("2G","tx_ht20_rate").split(",")
        # tx_ht20_chain = testconf.get_something("2G","tx_ht20_chain").split(",")
        # self.add_table_row("2G tx ht20", tx_ht20_freq, tx_ht20_rate, tx_ht20_chain)
        # tx_ht40_freq = testconf.get_something("2G","tx_ht40_freq").split(",")
        # tx_ht40_rate = testconf.get_something("2G","tx_ht40_rate").split(",")
        # tx_ht40_chain = testconf.get_something("2G","tx_ht40_chain").split(",")
        # self.add_table_row("2G tx ht40", tx_ht40_freq, tx_ht40_rate, tx_ht40_chain)
        # s = '''
        # tx_evm_ht20_freq = testconf.get_something("2G","tx_evm_ht20_freq").split(",")
        # tx_evm_ht20_rate = testconf.get_something("2G","tx_evm_ht20_rate").split(",")
        # tx_evm_ht20_chain = testconf.get_something("2G","tx_evm_ht20_chain").split(",")
        # self.add_table_row("2G tx evm ht20", tx_evm_ht20_freq, tx_evm_ht20_rate, tx_evm_ht20_chain)
        # tx_evm_ht40_freq = testconf.get_something("2G","tx_evm_ht40_freq").split(",")
        # tx_evm_ht40_rate = testconf.get_something("2G","tx_evm_ht40_rate").split(",")
        # tx_evm_ht40_chain = testconf.get_something("2G","tx_evm_ht40_chain").split(",")
        # self.add_table_row("2G tx evm ht40", tx_evm_ht40_freq, tx_evm_ht40_rate, tx_evm_ht40_chain)
        # tx_evm_ppm_freq = testconf.get_something("2G","tx_evm_ppm_freq").split(",")
        # tx_evm_ppm_rate = testconf.get_something("2G","tx_evm_ppm_rate").split(",")
        # tx_evm_ppm_chain = testconf.get_something("2G","tx_evm_ppm_chain").split(",")
        # self.add_table_row("2G tx evm.ppm", tx_evm_ppm_freq, tx_evm_ppm_rate, tx_evm_ppm_chain)
        # tx_mask_freq = testconf.get_something("2G","tx_mask_freq").split(",")
        # tx_mask_rate = testconf.get_something("2G","tx_mask_rate").split(",")
        # tx_mask_chain = testconf.get_something("2G","tx_mask_chain").split(",")
        # self.add_table_row(u"2G频谱模板", tx_mask_freq, tx_mask_rate, tx_mask_chain)
        # '''
        # rx_freq = testconf.get_something("2G","rx_freq").split(",")
        # rx_rate = testconf.get_something("2G","rx_rate").split(",")
        # rx_chain = testconf.get_something("2G","rx_chain").split(",")
        # self.add_table_row("2G rx", rx_freq, rx_rate, rx_chain)
        #

    def add_5G_table(self):
        self.add_row([u"5G校准"])
        self.add_row([u"5G频偏校准"])

        testconfigxml = TestConfigxml()
        root = testconfigxml.read_xml()
        test = testconfigxml.get_all_test(root)
        for g2_or_g5 in test:
            if(g2_or_g5.get('name')=='5G'):
                all_test_items = testconfigxml.get_test_items(g2_or_g5)
                for test_item in all_test_items:
                    if test_item.get('name') == "ht20":
                        all_freqs = testconfigxml.get_all_freq(test_item)
                        for freqs in all_freqs:
                            val = freqs.find('val').text
                            rates = freqs.find('rate').text.split(",")
                            chains = freqs.find('chain').text.split(",")

                            for rate in rates:
                                for chain in chains:
                                    self.add_row(["5G tx ht20",val, rate, chain])
                    elif test_item.get('name') == "ht40":
                        all_freqs = testconfigxml.get_all_freq(test_item)
                        for freqs in all_freqs:
                            val = freqs.find('val').text
                            rates = freqs.find('rate').text.split(",")
                            chains = freqs.find('chain').text.split(",")

                            for rate in rates:
                                for chain in chains:
                                    self.add_row(["5G tx ht40",val, rate, chain])
                    else:
                        all_freqs = testconfigxml.get_all_freq(test_item)
                        for freqs in all_freqs:
                            val = freqs.find('val').text
                            rates = freqs.find('rate').text.split(",")
                            chains = freqs.find('chain').text.split(",")

                            for rate in rates:
                                for chain in chains:
                                    self.add_row(["5G rx",val, rate, chain])



        # testconf = TestConf()
        # self.add_row([u"5G校准"])
        # self.add_row([u"5G频偏校准"])
        # tx_ht20_freq = testconf.get_something("5G","tx_ht20_freq").split(",")
        # tx_ht20_rate = testconf.get_something("5G","tx_ht20_rate").split(",")
        # tx_ht20_chain = testconf.get_something("5G","tx_ht20_chain").split(",")
        # self.add_table_row("5G tx ht20", tx_ht20_freq, tx_ht20_rate, tx_ht20_chain)
        # tx_ht40_freq = testconf.get_something("5G","tx_ht40_freq").split(",")
        # tx_ht40_rate = testconf.get_something("5G","tx_ht40_rate").split(",")
        # tx_ht40_chain = testconf.get_something("5G","tx_ht40_chain").split(",")
        # self.add_table_row("5G tx ht40", tx_ht40_freq, tx_ht40_rate, tx_ht40_chain)
        # s = '''
        # tx_evm_ht20_freq = testconf.get_something("5G","tx_evm_ht20_freq").split(",")
        # tx_evm_ht20_rate = testconf.get_something("5G","tx_evm_ht20_rate").split(",")
        # tx_evm_ht20_chain = testconf.get_something("5G","tx_evm_ht20_chain").split(",")
        # self.add_table_row("5G tx evm ht20", tx_evm_ht20_freq, tx_evm_ht20_rate, tx_evm_ht20_chain)
        # tx_evm_ht40_freq = testconf.get_something("5G","tx_evm_ht40_freq").split(",")
        # tx_evm_ht40_rate = testconf.get_something("5G","tx_evm_ht40_rate").split(",")
        # tx_evm_ht40_chain = testconf.get_something("5G","tx_evm_ht40_chain").split(",")
        # self.add_table_row("5G tx evm ht40", tx_evm_ht40_freq, tx_evm_ht40_rate, tx_evm_ht40_chain)
        # tx_evm_ppm_freq = testconf.get_something("5G","tx_evm_ppm_freq").split(",")
        # tx_evm_ppm_rate = testconf.get_something("5G","tx_evm_ppm_rate").split(",")
        # tx_evm_ppm_chain = testconf.get_something("5G","tx_evm_ppm_chain").split(",")
        # self.add_table_row("5G tx evm.ppm", tx_evm_ppm_freq, tx_evm_ppm_rate, tx_evm_ppm_chain)
        # tx_mask_freq = testconf.get_something("5G","tx_mask_freq").split(",")
        # tx_mask_rate = testconf.get_something("5G","tx_mask_rate").split(",")
        # tx_mask_chain = testconf.get_something("5G","tx_mask_chain").split(",")
        # self.add_table_row(u"5G频谱模板", tx_mask_freq, tx_mask_rate, tx_mask_chain)
        # '''
        # rx_freq = testconf.get_something("5G","rx_freq").split(",")
        # rx_rate = testconf.get_something("5G","rx_rate").split(",")
        # rx_chain = testconf.get_something("5G","rx_chain").split(",")
        # self.add_table_row("5G rx", rx_freq, rx_rate, rx_chain)
    
    def my_table_init(self,testconf):
        # testconf = TestConf()
        self.table_add_header([u"测试项目", u"信道", u"速率", u"天线"])
        how_to_test = testconf.get_something("global","how_to_test")
        if(how_to_test == "0"):
            self.add_2G_table()
        elif(how_to_test == "1"):
            self.add_5G_table()
        else:
            self.add_2G_table()
            self.add_5G_table()
    
    # def mtk_table_init(self):
    #     testconf = TestConf()
    #     self.table_add_header([u"测试项目", u"信道", u"速率", u"天线"])
    #     how_to_test = testconf.get_something("global","how_to_test")
    #     if(how_to_test == "0"):
    #         self.add_2G_table()
    #     elif(how_to_test == "1"):
    #         self.add_5G_table()
    #     else:
    #         self.add_2G_table()
    #         self.add_5G_table()
            
    s = '''
    def mtk_table_init(self):
        self.table_add_header([u"项目", u"命令"])
        self.add_row([u"测试软件版本：","protest --software"])
        self.add_row([u"测试硬件版本：","protest --hardware"])
        self.add_row([u"禁用按键正常功能：","protest --button -ban"])
        self.add_row([u"恢复按键正常功能：","protest --button -resume"])
        self.add_row([u"USB测试：","protest --usb"])
        self.add_row([u"LAN/WAN口测试：","protest --lanwantest"])
        self.add_row([u"检查是否处于恢复出厂默认配置状态：","protest --restore -status"])
        self.add_row([u"无线速率读取：","wifi_get rate"])
        self.add_row([u"无线速率设置：","wifi_set set %s"])
        self.add_row([u"无线信道读取：","wifi_get channel"])
        self.add_row([u"无线信道设置：","wifi_set channel %s"])
        self.add_row([u"无线国家代码读取：","wifi_get country"])
        self.add_row([u"无线国家代码设置：","wifi_set country %s"])
        self.add_row([u"写入MAC：","protest --mac -w %s"])
        self.add_row([u"检查MAC：","protest --mac -r"])
        
        self.add_row([u"查看产品无线SSID(2.4G)：","protest --ssid -r"])
        #self.add_row([u"查看产品无线SSID(5G)：","protest5g --ssid -r"])
        self.add_row([u"写入产品无线SSID(2.4G)：","protest --ssid -w %s"])
        #self.add_row([u"写入产品无线SSID(5G)：","protest5g --ssid -w %s"])
        self.add_row([u"TF卡支持测试：","protest --tf"])
        self.add_row([u"检查端口MAC：","ifconfig | grep HWaddr"])
        self.add_row([u"设置wan口地址：","protest --wanip -add %s 255.255.255.0"])
        self.add_row([u"恢复wan口配置：","protest --wanip -del"])
        #self.add_row([""])
    '''
    
    def ar934x_table_init(self):
        self.table_add_header([u"项目", u"命令"])
    
    def octeon_table_init(self):
        self.table_add_header([u"项目", u"命令"])

    def re_write_snormac(self,snormac):
        self.ui.label.setText(snormac)



    def table_get_result(self, line, result):
        #print "table_get_result", line, result
        if(result == "success"):
            self.table_sucess(line)
        else:
            self.table_fail(line)
    
    def reset_window(self):
        self.ui.textEdit.setText("")
        self.ui.lcdNumber.display("00:00")
        #self.set_type()

    def show_xiansun_window(self):
        calculate_B = Calculate_B()
        calculate_B.exec_()

    def show_config_window(self):
        testconfig = TestConf()
        qss = QFile(self.qssfile)
        qss.open(QFile.ReadOnly)
        q = QString(qss.readAll())
        s = '''
        configBox = MyConfigForm()
        configBox.setStyleSheet(q);
        configBox.exec_()
        '''
        self.configBox.setStyleSheet(q); 
        self.configBox.exec_()

    #将sn写入到txt文件中
    # def change_test_file_sn(self,filename,sn):
    #     file_object = open(filename)
    #     try:
    #         all_the_text = file_object.read()
    #     finally:
    #         file_object.close()
    #     #print re.findall(r"set mac=.*\n", all_the_text)
    #     result, number = re.subn(r"set sn=.*\n", "set sn="+sn+";\n", all_the_text)
    #     file_object = open(filename,"w")
    #     file_object.write(result)
    #     file_object.close()

    def change_test_file_mac(self, filename, mac):
        file_object = open(filename)
        try:
            all_the_text = file_object.read()
        finally:
            file_object.close()
        #print re.findall(r"set mac=.*\n", all_the_text)
        result, number = re.subn(r"set mac=.*\n", "set mac="+mac+";\n", all_the_text)
        file_object = open(filename,"w")
        file_object.write(result)
        file_object.close()
    
    def unpackMAC(self, mac):
        blocks=[mac[x:x+2] for x in xrange(0, len(mac), 2)]
        return ':'.join(blocks)
    
    def calc_mac_add_8(self, mac):
        macstr = mac.replace("-","").replace(":","")
        mac_int = int(macstr,16)
        mac_int = mac_int+8
        mac_hex = "%x" %mac_int
        return self.unpackMAC(mac_hex.replace("0x","").replace("L",""))

    def sn_is_right_format(self,sn):
        pattern = re.compile(r'^.{13}$')
        if(pattern.match(sn)):
            return 1
        else:
            return 0

    def mac_is_right_format(self, mac):
        pattern = re.compile(r'^([0-9a-fA-F]{2})(([/\s:-][0-9a-fA-F]{2}){5})$')
        if(pattern.match(mac)):
            return 1
        else:
            return 0

    def set_sn(self,this_sn):
            global sn
            sn = this_sn
    def get_sn(self):
            global sn
            return sn


    def get_and_set_sn(self):
        global sn
        sn = str(self.ui.lineEdit.text())
        # self.set_sn(sn)
        self.myconf.set_sn_num(sn)
        if(sn == ""):
            return -1
        if(not self.sn_is_right_format(sn)):
            return -1
        # sn = sn.lower().replace()#需要查看序列码是什么形式，判断需不需要替代
        # testconf = TestConf()
        # begin_with_mac_or_sn = testconf.get_begin_with_MACorSN()
        # # try:
        #     if(begin_with_mac_or_sn == "0"):
        #         self.change_test_file_sn("test_cmd_2g.txt",sn)
        #     elif(begin_with_mac_or_sn == "1"):
        #         self.change_test_file_sn("test_cmd_5g.txt",sn)
        #     else:
        #         self.change_test_file_sn("test_cmd_2g.txt",sn)
        #         mac2 = self.calc_mac_add_8(sn)
        #         self.change_test_file_sn("test_cmd_5g.txt",sn)
        # except:
        #     return -1
        return 0

    def get_and_set_mac(self):
        mac = str(self.ui.lineEdit.text())
        if(mac == ""):
            return -1
        if(not self.mac_is_right_format(mac)):
            return -1
        mac = mac.lower().replace("-",":")
        testconf = TestConf()
        how_to_test = testconf.get_howtotest()
        try:
            if(how_to_test == "0"):
                self.change_test_file_mac("test_cmd_2g.txt",mac)
            elif(how_to_test == "1"):
                self.change_test_file_mac("test_cmd_5g.txt",mac)
            else:
                self.change_test_file_mac("test_cmd_2g.txt",mac)
                mac2 = self.calc_mac_add_8(mac)
                self.change_test_file_mac("test_cmd_5g.txt",mac2)
        except:
            return -1
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())