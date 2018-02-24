# -*- coding: gbk -*-
__author__ = 'kaikai'

from A_power import *
from B_power import *

class Worker_A_B(QThread):

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
    def power_A_B(self):
        self.start()
    def run(self):
        self.emit(SIGNAL("begin_test"))
        power_A = Conf_A()
        power_B = Conf_B()
        power_A_B = Conf_A_B()
        # freq_all = ["2412","2437","2462"]
        chains = ["1","2"]
        myconfig_b = Conf_B()
        freq_2gs =myconfig_b.get_2g_items()
        for freq in freq_2gs:
        # for freq in freq_all:
            for chain in chains:

                powera_2g = string.atof(power_A.get_2g_power(freq[0], chain))
                powerb_2g = string.atof(power_B.get_2g_power(freq[0], chain))


                B_xiansun = str(powera_2g-powerb_2g)
                power_A_B.set_2g_power(freq[0], chain, B_xiansun)
        print "####################### 2g end #######################"

        freq_5gs =myconfig_b.get_5g_items()
        for freq in freq_5gs:
        # for freq in freq_all:
            for chain in chains:

                powera_5g = string.atof(power_A.get_5g_power(freq[0], chain))
                powerb_5g = string.atof(power_B.get_5g_power(freq[0], chain))


                B_xiansun = str(powera_5g-powerb_5g)
                power_A_B.set_5g_power(freq[0], chain, B_xiansun)
        print "####################### 5g end #######################"
        self.emit(SIGNAL("get_power_true"))
        #1.、从服务器地址中获得A站的配置文件并读取
        #2、读取B站的配置文件



class Conf_A_B():
    def __init__(self):
        # myconf = MyConf()
        # # b_xiansun = myconf.get_power_A_B_save_address()
        # self.filename = "xiansun.ini"
        # myconfig = MyConf()
        # power_A_address = myconfig.get_power_A_B_save_address()
        # self.filename = power_A_address+"\\"+"xiansun.ini"
        this_version = Version_ini()
        pathloss_file = this_version.get_pathloss_file()
        self.filename = os.getcwd()+"\\"+pathloss_file
    def set_2g_power(self, freq, chain, power):
        conf = Conf(self.filename)
        conf.setSection("2G")
        powers = conf.getValue("2G",freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index-1] = power
        power_str = ",".join(power_list)
        conf.setValue("2G", freq, power_str)
    def set_5g_power(self, freq, chain, power):
        conf = Conf(self.filename)
        conf.setSection("5G")
        powers = conf.getValue("5G",freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index-1] = power
        power_str = ",".join(power_list)
        conf.setValue("5G", freq, power_str)

    # def get_power(self, freq, chain):
    #     conf = Conf(self.filename)
    #     power_str = conf.getValue("power", freq)
    #     power_list = power_str.split(',')
    #     index = string.atoi(chain)
    #     return power_list[index-1]


    def get_2g_power(self, freq, chain):
        conf = Conf(self.filename)
        power_str = conf.getValue("2G", freq)
        power_list = power_str.split(',')
        index = string.atoi(chain)
        return power_list[index-1]