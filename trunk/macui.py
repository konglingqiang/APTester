from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MacPartEdit(QLineEdit):
    def __init__(self, parent = None):
        QLineEdit.__init__(self, parent)

        self.nextTab = None
        self.preTab = None
        self.setMaxLength(2)
        self.setFrame(False)
        self.setAlignment(Qt.AlignCenter)

        #validator = QIntValidator(0, 255, self)
        reg = QRegExp("[0-9a-fA-F]{2}")
        validator = QRegExpValidator(reg, self)
        self.setValidator(validator)

        self.connect(self, SIGNAL('textEdited(QString)'),\
                     self, SLOT('text_edited(QString)'))

    def set_nextTabEdit(self, nextTab):
        self.nextTab = nextTab
    
    def set_preTabEdit(self, preTab):
        self.preTab = preTab

    #def focusInEvent(self, event):
    #    self.selectAll()
    #    super(MacPartEdit, self).focusInEvent(event)

    def keyPressEvent(self, event):
        #if (event.key() == Qt.Key_Period):
        #    if self.nextTab:
        #        self.nextTab.setFocus()
        #        self.nextTab.selectAll()
        if (event.key() == Qt.Key_Right):
            if (self.cursorPosition() == self.text().length() and self.nextTab):
                self.nextTab.setFocus()
                self.nextTab.setCursorPosition(0)
        elif (event.key() == Qt.Key_Left):
            if (self.cursorPosition() == 0 and self.preTab):
                self.preTab.setFocus()
                self.preTab.setCursorPosition(self.preTab.text().length())
        elif (event.key() == Qt.Key_Backspace):
            if (self.cursorPosition() == 0 and self.hasSelectedText() == False and self.preTab):
                self.preTab.setFocus()
                self.preTab.setCursorPosition(self.preTab.text().length())
        elif (event.matches(QKeySequence.Paste)):
            self.mypaste()
        super(MacPartEdit, self).keyPressEvent(event)
    
    #def paste(self):
    #    print "hello paste"
    #    super(MacPartEdit, self).paste()
    
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        action = menu.actions()
        #paste
        action[5].triggered.disconnect(self.paste)
        action[5].triggered.connect(self.mypaste)
        menu.exec_(event.globalPos())
    
    def mypaste(self):
        clipboard_text = qApp.clipboard().text()
        current = self
        i = 0
        while (current and i < clipboard_text.length()):
            if (current.text().length() == 2):
                current =  current.nextTab
                if (current):
                    current.setFocus()
                    self.nextTab.setCursorPosition(0)
            else:
                current.insert(clipboard_text[i])
                i = i+1

    @pyqtSlot('QString')
    def text_edited(self, text):
        #validator = QIntValidator(0, 255, self)
        reg = QRegExp("[0-9a-fA-F]{2}")
        validator = QRegExpValidator(reg, self)
        macaddr = text
        pos = 0
        
        state = validator.validate(macaddr, pos)[0]
        if state == QValidator.Acceptable:
            #if macaddr.size() > 1:
            if macaddr.size() == 2:
                #ipnum = macaddr.toInt()[0]
                #if ipnum > 25:
                if self.nextTab:
                    self.nextTab.setFocus()
                    self.nextTab.setCursorPosition(0)
                    #self.nextTab.selectAll()

class MacEdit(QLineEdit):
    def __init__(self, parent = None):
        QLineEdit.__init__(self, parent)

        self.mac_part1 = MacPartEdit()
        self.mac_part2 = MacPartEdit()
        self.mac_part3 = MacPartEdit()
        self.mac_part4 = MacPartEdit()
        self.mac_part5 = MacPartEdit()
        self.mac_part6 = MacPartEdit()
        self.mac_part1.setAlignment(Qt.AlignCenter)
        self.mac_part2.setAlignment(Qt.AlignCenter)
        self.mac_part3.setAlignment(Qt.AlignCenter)
        self.mac_part4.setAlignment(Qt.AlignCenter)
        self.mac_part5.setAlignment(Qt.AlignCenter)
        self.mac_part6.setAlignment(Qt.AlignCenter)

        self.labeldot1 = QLabel('-')
        self.labeldot2 = QLabel('-')
        self.labeldot3 = QLabel('-')
        self.labeldot4 = QLabel('-')
        self.labeldot5 = QLabel('-')
        self.labeldot1.setAlignment(Qt.AlignCenter)
        self.labeldot2.setAlignment(Qt.AlignCenter)
        self.labeldot3.setAlignment(Qt.AlignCenter)
        self.labeldot4.setAlignment(Qt.AlignCenter)
        self.labeldot5.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()        
        layout.addWidget(self.mac_part1)
        layout.addWidget(self.labeldot1)
        layout.addWidget(self.mac_part2)
        layout.addWidget(self.labeldot2)
        layout.addWidget(self.mac_part3)
        layout.addWidget(self.labeldot3)
        layout.addWidget(self.mac_part4)
        layout.addWidget(self.labeldot4)
        layout.addWidget(self.mac_part5)
        layout.addWidget(self.labeldot5)
        layout.addWidget(self.mac_part6)
        layout.setSpacing(0)
        layout.setContentsMargins(QMargins(2, 2, 2, 2))
        
        self.setLayout(layout)

        QWidget.setTabOrder(self.mac_part1, self.mac_part2)
        QWidget.setTabOrder(self.mac_part2, self.mac_part3)
        QWidget.setTabOrder(self.mac_part3, self.mac_part4)
        QWidget.setTabOrder(self.mac_part4, self.mac_part5)
        QWidget.setTabOrder(self.mac_part5, self.mac_part6)
        self.mac_part1.set_nextTabEdit(self.mac_part2)
        self.mac_part2.set_nextTabEdit(self.mac_part3)
        self.mac_part3.set_nextTabEdit(self.mac_part4)
        self.mac_part4.set_nextTabEdit(self.mac_part5)
        self.mac_part5.set_nextTabEdit(self.mac_part6)
        
        self.mac_part2.set_preTabEdit(self.mac_part1)
        self.mac_part3.set_preTabEdit(self.mac_part2)
        self.mac_part4.set_preTabEdit(self.mac_part3)
        self.mac_part5.set_preTabEdit(self.mac_part4)
        self.mac_part6.set_preTabEdit(self.mac_part5)

        self.connect(self.mac_part1, SIGNAL('textChanged(QString)'),\
                     self, SLOT('textChangedSlot(QString)'))
        self.connect(self.mac_part2, SIGNAL('textChanged(QString)'),\
                     self, SLOT('textChangedSlot(QString)'))
        self.connect(self.mac_part3, SIGNAL('textChanged(QString)'),\
                     self, SLOT('textChangedSlot(QString)'))
        self.connect(self.mac_part4, SIGNAL('textChanged(QString)'),\
                     self, SLOT('textChangedSlot(QString)'))
        self.connect(self.mac_part5, SIGNAL('textChanged(QString)'),\
                     self, SLOT('textChangedSlot(QString)'))
        self.connect(self.mac_part6, SIGNAL('textChanged(QString)'),\
                     self, SLOT('textChangedSlot(QString)'))

        self.connect(self.mac_part1, SIGNAL('textEdited(QString)'),\
                     self, SLOT('textEditedSlot(QString)'))
        self.connect(self.mac_part2, SIGNAL('textEdited(QString)'),\
                     self, SLOT('textEditedSlot(QString)'))
        self.connect(self.mac_part3, SIGNAL('textEdited(QString)'),\
                     self, SLOT('textEditedSlot(QString)'))
        self.connect(self.mac_part4, SIGNAL('textEdited(QString)'),\
                     self, SLOT('textEditedSlot(QString)'))
        self.connect(self.mac_part5, SIGNAL('textEdited(QString)'),\
                     self, SLOT('textEditedSlot(QString)'))
        self.connect(self.mac_part6, SIGNAL('textEdited(QString)'),\
                     self, SLOT('textEditedSlot(QString)'))

    @pyqtSlot('QString')
    def textChangedSlot(self, text):
        macpart1 = self.mac_part1.text()
        macpart2 = self.mac_part2.text()
        macpart3 = self.mac_part3.text()
        macpart4 = self.mac_part4.text()
        macpart5 = self.mac_part5.text()
        macpart6 = self.mac_part6.text()

        macaddr = QString('%1:%2:%3:%4:%5:%6')\
                 .arg(macpart1)\
                 .arg(macpart2)\
                 .arg(macpart3)\
                 .arg(macpart4)\
                 .arg(macpart5)\
                 .arg(macpart6)
        self.emit(SIGNAL('textChanged'), macaddr)

    @pyqtSlot('QString')
    def textEditedSlot(self, text):
        macpart1 = self.mac_part1.text()
        macpart2 = self.mac_part2.text()
        macpart3 = self.mac_part3.text()
        macpart4 = self.mac_part4.text()
        macpart5 = self.mac_part5.text()
        macpart6 = self.mac_part6.text()

        macaddr = QString('%1:%2:%3:%4:%5:%6')\
                 .arg(macpart1)\
                 .arg(macpart2)\
                 .arg(macpart3)\
                 .arg(macpart4)\
                 .arg(macpart5)\
                 .arg(macpart6)
        self.emit(SIGNAL('textEdited'), macaddr)

    def setText(self, text):
        regexp = QRegExp('^([0-9a-fA-F]{2})(([/\s:-][0-9a-fA-F]{2}){5})$')
        validator = QRegExpValidator(regexp ,self)
        nPos = 0
        state = validator.validate(text, nPos)[0]

        macpart1 = QString()
        macpart2 = QString()
        macpart3 = QString()
        macpart4 = QString()
        macpart5 = QString()
        macpart6 = QString()

        if state == QValidator.Acceptable:  # valid
            macpartlist = text.split('-')

            strcount = len(macpartlist)
            index = 0
            if index < strcount:
                macpart1 = macpartlist[index]
            index += 1
            if index < strcount:
                macpart2 = macpartlist[index]
                index += 1
            if index < strcount:
                macpart3 = macpartlist[index]
                index += 1
            if index < strcount:
                macpart4 = macpartlist[index]
                index += 1
            if index < strcount:
                macpart5 = macpartlist[index]
                index += 1
            if index < strcount:
                macpart6 = macpartlist[index]

        self.mac_part1.setText(macpart1)
        self.mac_part2.setText(macpart2)
        self.mac_part3.setText(macpart3)
        self.mac_part4.setText(macpart4)
        self.mac_part5.setText(macpart5)
        self.mac_part6.setText(macpart6)

    def text(self):
        macpart1 = self.mac_part1.text()
        macpart2 = self.mac_part2.text()
        macpart3 = self.mac_part3.text()
        macpart4 = self.mac_part4.text()
        macpart5 = self.mac_part5.text()
        macpart6 = self.mac_part6.text()

        return QString('%1:%2:%3:%4:%5:%6')\
                 .arg(macpart1)\
                 .arg(macpart2)\
                 .arg(macpart3)\
                 .arg(macpart4)\
                 .arg(macpart5)\
                 .arg(macpart6)

    def setStyleSheet(self, styleSheet):
        self.mac_part1.setStyleSheet(styleSheet)
        self.mac_part2.setStyleSheet(styleSheet)
        self.mac_part3.setStyleSheet(styleSheet)
        self.mac_part4.setStyleSheet(styleSheet)
        self.mac_part5.setStyleSheet(styleSheet)
        self.mac_part6.setStyleSheet(styleSheet)