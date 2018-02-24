# -*- coding: gbk -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from msgbox import Ui_frmMessageBox
import dev_rc

class MyMSGForm(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.location = self.geometry()
        self.Max = False;
        self.ui=Ui_frmMessageBox()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connect(self.ui.btnMenu_Close,SIGNAL("clicked()"),SLOT("close()"))
        self.connect(self.ui.btnCancel,SIGNAL("clicked()"),SLOT("close()"))
        self.connect(self.ui.btnOk,SIGNAL("clicked()"),self.btnOk_clicked)
        self.fontId = QFontDatabase.addApplicationFont(":/image/icomoon.ttf")
        self.fontName = QFontDatabase.applicationFontFamilies(self.fontId).takeAt(0)
        self.iconFont = QFont(self.fontName)
        self.SetIcon(self.ui.btnMenu_Close, QChar(0xf00d), 10)
        self.SetIcon(self.ui.lab_Ico, QChar(0xf015), 12)
        qss = QFile("black.css"); 
        qss.open(QFile.ReadOnly); 
        q = QString(qss.readAll())
        self.setStyleSheet(q); 

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()
 
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def SetIcon(self, obj, text, size):
        self.iconFont.setPointSize(size)
        obj.setFont(self.iconFont)
        obj.setText(text)
    
    def SetMessage(self, msg, mytype):
        if(mytype == 0):
            self.ui.labIcoMain.setStyleSheet("border-image: url(:/image/info.png);")
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
        self.done(1)
        self.close()