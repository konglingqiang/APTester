# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\ui\loginDialog.ui'
#
# Created: Fri Dec 02 14:18:48 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_loginDialog(object):
    def setupUi(self, configBox):
        configBox.setObjectName(_fromUtf8("configBox"))
        configBox.resize(389, 278)
        self.verticalLayout = QtGui.QVBoxLayout(configBox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_main = QtGui.QWidget(configBox)
        self.widget_main.setStyleSheet(_fromUtf8("font: 11pt \"微软雅黑\";"))
        self.widget_main.setObjectName(_fromUtf8("widget_main"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_main)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.widget_main)
        self.groupBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(140, 190, 75, 23))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 190, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(100, 80, 51, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(100, 120, 51, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_2.setStyleSheet("line-edit-password-character: 42");
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(160, 80, 161, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 120, 161, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout.addWidget(self.widget_main)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(110, 160, 251, 21))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.retranslateUi(configBox)
        QtCore.QMetaObject.connectSlotsByName(configBox)

    def retranslateUi(self, configBox):
        configBox.setWindowTitle(_translate("configBox", "提示", None))
        self.pushButton.setText(_translate("configBox", "登录", None))
        self.pushButton_2.setText(_translate("configBox", "取消", None))
        self.label.setText(_translate("configBox", "账号：", None))
        self.label_2.setText(_translate("configBox", "密码：", None))
        # self.label_3.setText(_translate("configBox", "密码：", None))

