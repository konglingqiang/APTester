__author__ = 'kaikai'

import subprocess
from PyQt4.QtCore import *
from PyQt4.QtGui import QColor


class run_thread(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
    def run_art2(self):
        self.start()
    def run(self):
        global test_result
        popen = subprocess.Popen(['ping'], stdout=subprocess.PIPE)
        while True:
            buff = popen.stdout.readline()
            print buff
            if " fail " in buff:
                self.printstr(buff+'\n',QColor(255, 0, 0, 220))
            else:
                self.printstr(buff+'\n',QColor(0, 0, 0, 220))

            if "        Total" in buff:
                buff_list = buff.split(':')
                fail_num = buff_list[1].replace(' ','')
                if fail_num is not '0':
                    test_result = 1


            print popen.poll()
            if buff == '' and popen.poll() is not None:
                if test_result is not 0:
                    self.emit(SIGNAL("fail"))
                else:
                    self.emit(SIGNAL("success"))
                break