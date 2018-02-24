#coding:utf-8
import ConfigParser
import os
import string
import sys


# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
# print rootPath +'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
class Conf():
    def __init__(self,name):
        self.name = name
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(name)
             
    def getSections(self):
        return self.cp.sections()
     
    def getOptions(self, section):
        if self.cp.has_section(section):
            return self.cp.options(section)
     
    def getItems(self, section):
        if self.cp.has_section(section):
            return self.cp.items(section)
         
    def getValue(self, section, option):
        if self.cp.has_option(section, option):
            return self.cp.get(section, option)
     
    def setSection(self, section):
        if not self.cp.has_section(section):
            self.cp.add_section(section)
            self.cp.write(open(self.name,'w'))
     
    def setValue(self, section, option, value):
        if not self.cp.has_option(section, option):
            self.cp.set(section, option, value)
            self.cp.write(open(self.name,'w'))
        else:
            self.updateValue(section, option, value)
     
    def delSection(self, section):
        if self.cp.has_section(section):
            self.cp.remove_section(section)
            self.cp.write(open(self.name,'w'))
     
    def delOption(self, section, option):
        if self.cp.has_option(section, option):
            self.cp.remove_option(section, option)
            self.cp.write(open(self.name,'w'))
             
    def updateValue(self, section, option, value):
        if self.cp.has_option(section, option):
            self.cp.set(section, option, value)
            self.cp.write(open(self.name,'w'))


class MyConf():
    def __init__(self):
        this_version = Version_ini()
        config_file = this_version.get_config_file()
        self.filename = os.getcwd()+"\\"+config_file
        if (not os.path.exists(self.filename)):
            self.set_default_config()
    def set_skin_black(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "skin", "black")
    def set_skin_ironblue(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "skin", "ironblue")
    def set_skin_silvery(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "skin", "silvery")

    def set_old_hour(self, old_hour):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "old_hour", old_hour)
    def set_max_ip_use(self, max_ip_use):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "max_ip_use", max_ip_use)
    def set_log_address(self, log_address):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "log_address", log_address)
    def set_power_A_B_save_address(self, power_A_B_save_address):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "power_A_B_save_address", power_A_B_save_address)
    def set_username(self, username):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","username",username)
    def get_username(self):
        conf = Conf(self.filename)
        return conf.getValue("global","username")

    def set_IQ_connect(self,IQ_connect):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","IQ_connect",IQ_connect)

    def get_IQ_connect(self):
        conf = Conf(self.filename)
        return conf.getValue("global","IQ_connect")

    def set_ap_model(self,ap_model):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","ap_model",ap_model)
    def get_ap_model(self):
        conf = Conf(self.filename)
        return conf.getValue("global","ap_model")

    def get_old_hour(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "old_hour")
    def get_max_ip_use(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "max_ip_use")
    def get_log_address(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "log_address")
    def get_power_A_B_save_address(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "power_A_B_save_address")
    def get_fail_stop(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "fail_stop")
    def set_fail_stop(self,fail_stop_flag):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","fail_stop",fail_stop_flag)
    def set_user_type(self, type):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","user_type", type)
    def get_user_type(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "user_type")
    def set_sn_num(self,sn_num):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","sn_num",sn_num)
    def get_sn_num(self):
        conf = Conf(self.filename)
        return conf.getValue("global","sn_num")
    def get_skin(self):
        conf = Conf(self.filename)
        return conf.getValue("global","skin")
    def set_type_mt7620a(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "type", "mt7620a")
    def set_type_ar934x(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "type", "ar934x")
    def set_type_octeon(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "type", "octeon")
    def get_type(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "type")
    def set_default_config(self):
        self.set_skin_black()
        self.set_type_mt7620a()

    def set_pmgr_link(self,pmgr_link):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "pmgr_link", pmgr_link)
    def get_pmgr_link(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "pmgr_link")

    def set_aysnc_id(self,aysnc_id):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","aysnc_id",aysnc_id)
    def get_aysnc_id(self):
        conf = Conf(self.filename)
        return conf.getValue("global","aysnc_id")

#     治具id
    def set_zhiju_id(self,zhiju_id):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","zhiju_id",zhiju_id)
    def get_zhiju_id(self):
        conf = Conf(self.filename)
        return conf.getValue("global","zhiju_id")


class TestConf():
    def __init__(self):
        this_version = Version_ini()
        testconfig_file = this_version.get_testConfig_file()
        self.filename =os.getcwd()+ "\\" + testconfig_file
        if (not os.path.exists(self.filename)):
            self.set_default_config()
    def get_num_of_something(self, section, item):
        conf = Conf(self.filename)
        return conf.getValue(section,item).count(",")+1
    def set_something(self, section, item, value):
        conf = Conf(self.filename)
        conf.setSection(section)
        conf.setValue(section, item, value)
    def get_something(self, section, item):
        conf = Conf(self.filename)
        return conf.getValue(section,item)
    def set_write_art_only_when_sucess(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "write_art", "1")
    def set_write_art_no_matter_what(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "write_art", "2")
    def get_write_art(self):
        conf = Conf(self.filename)
        return conf.getValue("global","write_art")
    def set_howtotest_2G(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "how_to_test", "0")

    def set_beging_MAC(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "begin_with_MACorSN", 0)
    #设置用户名
    def set_username(self, username):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "username", username)

    def set_password(self, password):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "password", password)

    def set_use_art2(self,use_art2):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "use_art2", use_art2)
    def get_use_art2(self):
        conf = Conf(self.filename)
        return conf.getValue("global","use_art2")

    def set_2g_default_port(self, port_2g):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "port_2g", port_2g)

    def set_5g_default_port(self, port_5g):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "port_5g", port_5g)
    def set_fail_retest_num(self,num):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "fail_retest_num",num)
    def get_fail_retest_num(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "fail_retest_num")
    def set_B_station_loop_capture(self,loop_capture):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "B_station_loop_capture", loop_capture)
    def get_B_station_loop_capture(self):
        conf = Conf(self.filename)
        return conf.getValue("global","B_station_loop_capture")
    def set_is_or_not_jiaozhun(self, jiaozhun_flag):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "is_or_not_jiaozhun", jiaozhun_flag)

    def set_begin_SN(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "begin_with_MACorSN", 1)
    def set_default_ip(self, default_ip):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "default_ip", default_ip)

    def set_howtotest_5G(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "how_to_test", "1")
    def set_howtotest_both(self):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "how_to_test", "2")
    def get_howtotest(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "how_to_test")
    def get_begin_with_MACorSN(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "begin_with_macorsn")

    def get_2g_default_port(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "port_2g")

    def get_5g_default_port(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "port_5g")


    def get_is_or_not_jiaozhun(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "is_or_not_jiaozhun")

    def get_username(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "username")

    def get_password(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "password")

    def get_default_ip(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "default_Ip")

    def set_loop_capture(self,loop_capture_num):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","loop_capture",loop_capture_num)
    def get_loop_capture(self):
        conf = Conf(self.filename)
        return conf.getValue("global","loop_capture")


    def set_ART_pathloss(self,art_pathloss):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","art_pathloss",art_pathloss)
    def get_art_pathloss(self):
        conf = Conf(self.filename)
        return conf.getValue("global","art_pathloss")


    def set_loop_jiaozhun_sleep(self,jiaozhun_sleep):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","loop_jiaozhun_sleep",jiaozhun_sleep)
    def get_loop_jiaozhun_sleep(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "loop_jiaozhun_sleep")
    def set_jiaozhun_power_add(self,jiaozhun_power_add):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","jiaozhun_power_add",jiaozhun_power_add)
    def get_jiaozhun_power_add(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "jiaozhun_power_add")

    def set_jiaozhun_power_add_5G(self,jiaozhun_power_add_5G):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","jiaozhun_power_add_5G",jiaozhun_power_add_5G)
    def get_jiaozhun_power_add_5G(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "jiaozhun_power_add_5G")

    def set_run_2g_tx(self,run_2g_tx):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","run_2g_tx",run_2g_tx)
    def get_run_2g_tx(self):
        conf = Conf(self.filename)
        return conf.getValue("global","run_2g_tx")

    def set_run_2g_rx(self,run_2g_rx):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","run_2g_tx",run_2g_rx)
    def get_run_2g_rx(self):
        conf = Conf(self.filename)
        return conf.getValue("global","run_2g_rx")
    def set_run_5g_tx(self,run_5g_tx):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","run_5g_tx",run_5g_tx)
    def get_run_5g_tx(self):
        conf = Conf(self.filename)
        return conf.getValue("global","run_5g_tx")

    def set_run_5g_rx(self,run_5g_rx):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","run_5g_rx",run_5g_rx)
    def get_run_5g_rx(self):
        conf = Conf(self.filename)
        return conf.getValue("global","run_5g_rx")



    def set_jiaozhun_warmup(self,warmup):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "jiaozhun_warmup",warmup)
    def get_jiaozhun_warmup(self):
        conf = Conf(self.filename)
        return conf.getValue("global","jiaozhun_warmup")
    def get_jiaozhun_warmup_5G(self):
        conf = Conf(self.filename)
        return conf.getValue("global","jiaozhun_warmup_5g")
    def set_jiaozhun_warmup_5G(self,jiaozhun_warmup_5g):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global", "jiaozhun_warmup_5g",jiaozhun_warmup_5g)
    def set_loop_tx_sleep(self, sleep_time):
        conf = Conf(self.filename)
        conf.setSection("global")
        conf.setValue("global","loop_tx_sleep" ,sleep_time)
    def get_loop_tx_sleep(self):
        conf = Conf(self.filename)
        return conf.getValue("global", "loop_tx_sleep")

    def set_2G_freq_for_lost(self, freq_for_lost):
        conf = Conf(self.filename)
        conf.setSection("2G")
        conf.setValue("2G", "freq_for_lost", freq_for_lost)
    def get_2G_freq_for_lost(self):
        conf = Conf(self.filename)
        return conf.getValue("2G","freq_for_lost")
        
    def set_5G_freq_for_lost(self, freq_for_lost):
        conf = Conf(self.filename)
        conf.setSection("5G")
        conf.setValue("5G", "freq_for_lost", freq_for_lost)
    def get_5G_freq_for_lost(self):
        conf = Conf(self.filename)
        return conf.getValue("5G","freq_for_lost")
        
    def set_2G_lost_for_freq(self, lost_for_freq):
        conf = Conf(self.filename)
        conf.setSection("2G")
        conf.setValue("2G", "lost_for_freq", lost_for_freq)
    def get_2G_lost_for_freq(self):
        conf = Conf(self.filename)
        return conf.getValue("2G","lost_for_freq")
        
    def set_5G_lost_for_freq(self, lost_for_freq):
        conf = Conf(self.filename)
        conf.setSection("5G")
        conf.setValue("5G", "lost_for_freq", lost_for_freq)
    def get_5G_lost_for_freq(self):
        conf = Conf(self.filename)
        return conf.getValue("5G","lost_for_freq")
        
    def set_2G_pcdac(self, pcdac):
        conf = Conf(self.filename)
        conf.setSection("2G")
        conf.setValue("2G", "pcdac", pcdac)
    def get_2G_pcdac(self):
        conf = Conf(self.filename)
        return conf.getValue("2G","pcdac")
    
    def set_5G_pcdac(self, pcdac):
        conf = Conf(self.filename)
        conf.setSection("5G")
        conf.setValue("5G", "pcdac", pcdac)
    def get_5G_pcdac(self):
        conf = Conf(self.filename)
        return conf.getValue("5G","pcdac")
    
    def set_2G_ppm_limit(self, ppm_limit):
        conf = Conf(self.filename)
        conf.setSection("2G")
        conf.setValue("2G", "ppm_limit", ppm_limit)
    def get_2G_ppm_limit(self):
        conf = Conf(self.filename)
        return conf.getValue("2G","ppm_limit")
    
    def set_5G_ppm_limit(self, ppm_limit):
        conf = Conf(self.filename)
        conf.setSection("5G")
        conf.setValue("5G", "ppm_limit", ppm_limit)
    def get_5G_ppm_limit(self):
        conf = Conf(self.filename)
        return conf.getValue("5G","ppm_limit")
    
    def set_2G_power_limit_ht20(self, power_limit_ht20):
        conf = Conf(self.filename)
        conf.setSection("2G")
        conf.setValue("2G", "power_limit_ht20", power_limit_ht20)
    def get_2G_power_limit_ht20(self):
        conf = Conf(self.filename)
        return conf.getValue("2G","power_limit_ht20")
    
    def set_5G_power_limit_ht20(self, power_limit_ht20):
        conf = Conf(self.filename)
        conf.setSection("5G")
        conf.setValue("5G", "power_limit_ht20", power_limit_ht20)
    def get_5G_power_limit_ht20(self):
        conf = Conf(self.filename)
        return conf.getValue("5G","power_limit_ht20")
    
    def set_2G_power_limit_ht40(self, power_limit_ht40):
        conf = Conf(self.filename)
        conf.setSection("2G")
        conf.setValue("2G", "power_limit_ht40", power_limit_ht40)
    def get_2G_power_limit_ht40(self):
        conf = Conf(self.filename)
        return conf.getValue("2G","power_limit_ht40")
    
    def set_5G_power_limit_ht40(self, power_limit_ht40):
        conf = Conf(self.filename)
        conf.setSection("5G")
        conf.setValue("5G", "power_limit_ht40", power_limit_ht40)
    def get_5G_power_limit_ht40(self):
        conf = Conf(self.filename)
        return conf.getValue("5G","power_limit_ht40")
        
    def set_default_config(self):
        self.set_howtotest_both()
        # self.set_2G_freq_for_lost("2412,2437,2452,2462")
        # self.set_5G_freq_for_lost("5180,5240,5260,5320,5500,5700,5745,5805")
        # self.set_2G_lost_for_freq("19.2,19.2,19.2,19.2")
        # self.set_5G_lost_for_freq("21.5,21.5,21.5,21.5,21,21,21,21.8")
        # self.set_2G_pcdac("40")
        # self.set_5G_pcdac("40")
        # self.set_2G_ppm_limit("20")
        # self.set_5G_ppm_limit("20")
        # self.set_2G_power_limit_ht20("2.5")
        # self.set_5G_power_limit_ht20("2.5")
        # self.set_2G_power_limit_ht40("2")
        # self.set_5G_power_limit_ht40("2")
        # self.set_something("2G", "tx_ht20_freq", "2412,2437,2462")
        # self.set_something("2G", "tx_ht20_rate", "11s,6,54,t0,t7")
        # self.set_something("2G", "tx_ht20_chain", "1,2")
        # self.set_something("2G", "tx_ht40_freq", "2412,2437,2462")
        # self.set_something("2G", "tx_ht40_rate", "f0,f7")
        # self.set_something("2G", "tx_ht40_chain", "1,2")
        s = '''
        self.set_something("2G", "tx_power_ht20_freq", "2412,2437,2462")
        self.set_something("2G", "tx_power_ht20_rate", "11s,6,t0,t7")
        self.set_something("2G", "tx_power_ht20_chain", "1,2")
        self.set_something("2G", "tx_power_ht40_freq", "2412,2437,2462")
        self.set_something("2G", "tx_power_ht40_rate", "f0,f7")
        self.set_something("2G", "tx_power_ht40_chain", "1,2")
        self.set_something("2G", "tx_evm_ht20_freq", "2412,2437,2462")
        self.set_something("2G", "tx_evm_ht20_rate", "54,t7")
        self.set_something("2G", "tx_evm_ht20_chain", "1,2")
        self.set_something("2G", "tx_evm_ht40_freq", "2412,2437,2452")
        self.set_something("2G", "tx_evm_ht40_rate", "f7")
        self.set_something("2G", "tx_evm_ht40_chain", "1,2")
        self.set_something("2G", "tx_evm_ppm_freq", "2437")
        self.set_something("2G", "tx_evm_ppm_rate", "54")
        self.set_something("2G", "tx_evm_ppm_chain", "1")
        self.set_something("2G", "tx_mask_freq", "2437,2462")
        self.set_something("2G", "tx_mask_rate", "1l,6,t0,f0")
        self.set_something("2G", "tx_mask_chain", "1,2")
        '''
        # self.set_something("2G", "rx_freq", "2412,2437,2462")
        # self.set_something("2G", "rx_rate", "5l,54,t7")
        # self.set_something("2G", "rx_chain", "1,2")
        # self.set_something("2G", "rate_for_powerlevel", "5l,11l,6,54,t7,t8,t15,t16,t23,f7,f8,f15,f16,f23,vt0,vt8,vt10,vt18,vt20,vt29,vf0,vf9,vf10,vf19,vf20,vf29,ve0,ve9,ve10,ve19,ve20,ve29,vt7,vf7,ve7")
        # self.set_something("2G", "powerlevel_for_rate", "-90,-90,-82,-65,-65,-82,-64,-82,-64,-64,-79,-61,-79,-61,-82,-59,-82,-59,-82,-59,-79,-54,-79,-54,-79,-54,-76,-51,-76,-51,-76,-51,-65,-62,-59")
        #
        # self.set_something("5G", "tx_ht20_freq", "5180,5500,5805")
        # self.set_something("5G", "tx_ht20_rate", "6,t0,t7")
        # self.set_something("5G", "tx_ht20_chain", "1,2")
        # self.set_something("5G", "tx_ht40_freq", "5180,5500,5805")
        # self.set_something("5G", "tx_ht40_rate", "f0,f7")
        # self.set_something("5G", "tx_ht40_chain", "1,2")
        s = '''
        self.set_something("5G", "tx_power_ht20_freq", "5180,5500,5805")
        self.set_something("5G", "tx_power_ht20_rate", "6,t0,t7")
        self.set_something("5G", "tx_power_ht20_chain", "1,2")
        self.set_something("5G", "tx_power_ht40_freq", "5180,5500,5805")
        self.set_something("5G", "tx_power_ht40_rate", "f0,f7")
        self.set_something("5G", "tx_power_ht40_chain", "1,2")
        self.set_something("5G", "tx_evm_ht20_freq", "5180,5500,5805")
        self.set_something("5G", "tx_evm_ht20_rate", "54,t7")
        self.set_something("5G", "tx_evm_ht20_chain", "1,2")
        self.set_something("5G", "tx_evm_ht40_freq", "5180,5500,5805")
        self.set_something("5G", "tx_evm_ht40_rate", "f7")
        self.set_something("5G", "tx_evm_ht40_chain", "1,2")
        self.set_something("5G", "tx_evm_ppm_freq", "5500")
        self.set_something("5G", "tx_evm_ppm_rate", "54")
        self.set_something("5G", "tx_evm_ppm_chain", "1")
        self.set_something("5G", "tx_mask_freq", "5500")
        self.set_something("5G", "tx_mask_rate", "6,t0,f0")
        self.set_something("5G", "tx_mask_chain", "1,2")
        '''
        self.set_something("5G", "rx_freq", "5180,5500,5805")
        self.set_something("5G", "rx_rate", "6,54")
        self.set_something("5G", "rx_chain", "1,2")
        self.set_something("5G", "rate_for_powerlevel", "5l,11l,6,54,t7,t8,t15,t16,t23,f7,f8,f15,f16,f23,vt0,vt8,vt10,vt18,vt20,vt29,vf0,vf9,vf10,vf19,vf20,vf29,ve0,ve9,ve10,ve19,ve20,ve29,vt7,vf7,ve7")
        self.set_something("5G", "powerlevel_for_rate", "-90,-90,-82,-65,-65,-82,-64,-82,-64,-64,-79,-61,-79,-61,-82,-59,-82,-59,-82,-59,-79,-54,-79,-54,-79,-54,-76,-51,-76,-51,-76,-51,-65,-62,-59")
        self.set_write_art_only_when_sucess()

try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET
import sys

class TestConfigxml():

    def  __init__(self):
        this_version = Version_ini()
        test_item_xml = this_version.get_test_item_xml()
        self.filename = os.getcwd()+"\\" + test_item_xml

    def read_xml(self):
        '''''读取并解析xml文件
           in_path: xml路径
           return: ElementTree'''
        tree = ET.parse(self.filename)

        return tree
    def write_xml(self, tree):
        tree.write(self.filename)

    #获得所有test
    def get_all_test(self, tree):
        test_config = tree.getroot()
        test = test_config.findall('test')

        return  test

    #获得freq_for_lost
    def get_freq_for_lost(self, test):
        freq_for_lost = test.find('freq_for_lost')
        return freq_for_lost

    #获得test_items
    def get_test_items(self, test):
        test_items = test.findall('test_items')
        return test_items
    #获得power_rate
    def get_power_rate(self, test):
        power_rate = test.find('power_rate')
        return power_rate
    #获得freq
    def get_all_freq(self, f_or_t_or_p):
        freq = f_or_t_or_p.findall('freq')
        return freq

    def get_all_pr_items(self,f_or_t_or_p):
        pr_items = f_or_t_or_p.findall('pr_items')
        return pr_items

    # 修改2g或5g的pcdac值
    # def set_padac(self,g2_or_g5,padac):
    #     tree = self.read_xml()
    #     tests = self.get_all_test(tree)
    #     for test in tests:
    #         if test.get('name') == g2_or_g5:
    #             test.get("pcdac")
    # def set_ppm_limit(self,g2_or_g5,ppm_limit):
    #
    # def set_ht20_power_limit(self,g2_or_g5,power_limit):
    #
    # def set_ht40_power_limit(self,g2_or_g5,power_limit):

    def get_2g_pcdac(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                return test.get("pcdac")

    def set_2g_pcdac(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                # print test.get("pcdac")
                test.set("pcdac",unicode(value, 'utf-8', 'ignore'))
        # print str(tree)
        # self.write_xml(tree)

    def get_2g_ppm_limit(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                return test.get("ppm_limit")

    def set_2g_ppm_limit(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                # return test.get("ppm_limit")
                test.set("ppm_limit",unicode(value, 'utf-8', 'ignore'))
        # self.write_xml(tree)
    def get_2g_power_limit_ht20(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                return test.get("power_limit_ht20")

    def set_2g_power_limit_ht20(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                # return test.get("power_limit_ht20")
                test.set("power_limit_ht20",unicode(value, 'utf-8', 'ignore'))
        # self.write_xml(tree)
    def get_2g_power_limit_ht40(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                return test.get("power_limit_ht40")

    def set_2g_power_limit_ht40(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                # return test.get("power_limit_ht40")
                test.set("power_limit_ht40",unicode(value, 'utf-8', 'ignore'))
        # self.write_xml(tree)
    def get_5g_pcdac(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                return test.get("pcdac")
    def set_5g_pcdac(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                # return test.get("pcdac")
                test.set("pcdac",unicode(value, 'utf-8', 'ignore'))
        # self.write_xml(tree)
    def get_5g_ppm_limit(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                return test.get("ppm_limit")

    def set_5g_ppm_limit(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                # return test.get("ppm_limit")
                test.set("ppm_limit",unicode(value, 'utf-8', 'ignore'))
        # self.write_xml(tree)
    def get_5g_power_limit_ht20(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                return test.get("power_limit_ht20")

    def set_5g_power_limit_ht20(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                # return test.get("power_limit_ht20")
                test.set("power_limit_ht20",unicode(value, 'utf-8', 'ignore'))

        # self.write_xml(tree)
    def get_5g_power_limit_ht40(self):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                return test.get("power_limit_ht40")

    def set_5g_power_limit_ht40(self,value,tree):
        # tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                # return test.get("power_limit_ht40")
                test.set("power_limit_ht40",unicode(value, 'utf-8', 'ignore'))
        # self.write_xml(tree)
    def get_2g_tx_ht20_freq(self):
        val_list = {}
        val_list_list=[]
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == "ht20":
                        freqs = self.get_all_freq(test_item)

                        for freq in freqs:
                            val = freq.find('val').text
                            print val+"########################################################"
                            # val_list[freq] = val
                            val_list_list.append({freq:val})

        return val_list_list

    def get_2g_tx_ht40_freq(self):
        val_list = {}
        val_list_list=[]
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == "ht40":
                        freqs = self.get_all_freq(test_item)

                        for freq in freqs:
                            val = freq.find('val').text
                            print val+"############################################"

                            # val_list[freq] = val

                            val_list_list.append({freq:val})

        return val_list_list

    def get_2g_tx_rx_freq(self):
        val_list = {}
        val_list_list=[]
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == "rx":
                        freqs = self.get_all_freq(test_item)

                        for freq in freqs:
                            val = freq.find('val').text
                            print val+"###################################"
                            # val_list[freq] = val
                            val_list_list.append({freq:val})
        return  val_list_list
    def get_5g_tx_ht20_freq(self):
        val_list = {}
        val_list_list=[]
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == "ht20":
                        freqs = self.get_all_freq(test_item)

                        for freq in freqs:
                            val = freq.find('val').text
                            # val_list[freq] = val
                            val_list_list.append({freq:val})
        return  val_list_list

    def get_5g_tx_ht40_freq(self):
        val_list = {}
        val_list_list=[]
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == "ht40":
                        freqs = self.get_all_freq(test_item)

                        for freq in freqs:
                            val = freq.find('val').text
                            # val_list[freq] = val
                            val_list_list.append({freq:val})
        return  val_list_list

    def get_5g_tx_rx_freq(self):
        val_list = {}
        val_list_list=[]
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "5G":
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == "rx":
                        freqs = self.get_all_freq(test_item)

                        for freq in freqs:
                            val = freq.find('val').text
                            # val_list[freq] = val
                            val_list_list.append({freq:val})
        return val_list_list


    #根据freq获得rate
    def get_rate_this(self,freq):
        rate_list = freq.find('rate').text.split(',')
        return rate_list
    def get_chain_this(self, freq):
        chain_list = freq.find('chain').text.split(',')
        return chain_list

    #获得2g ht20测试项的个数
    def get_num_of_2g_tx_ht20_freq(self):
        num = 0
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name') == "2G":
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == "ht20":
                        freqs = self.get_all_freq(test_item)
                        len_freq = len(freqs)
                        for freq in freqs:
                            rate = freq.find('rate').text.split(',')
                            len_rate = len(rate)
                            chain = freq.find('chain').text.split(',')
                            len_chain = len(chain)
                            num += len_rate * len_chain

        return num
    # 获得2g ht40测试项的个数
    def get_num_of_2g_tx_ht40_freq(self):
            num = 0
            tree = self.read_xml()
            tests = self.get_all_test(tree)
            for test in tests:
                if test.get('name') == "2G":
                    test_items = self.get_test_items(test)
                    for test_item in test_items:
                        if test_item.get('name') == "ht40":
                            freqs = self.get_all_freq(test_item)
                            len_freq = len(freqs)
                            for freq in freqs:
                                rate = freq.find('rate').text.split(',')
                                len_rate = len(rate)
                                chain = freq.find('chain').text.split(',')
                                len_chain = len(chain)
                                num += len_rate * len_chain

            return num

    def get_num_of_2g_rx_freq(self):
            num = 0
            tree = self.read_xml()
            tests = self.get_all_test(tree)
            for test in tests:
                if test.get('name') == "2G":
                    test_items = self.get_test_items(test)
                    for test_item in test_items:
                        if test_item.get('name') == "rx":
                            freqs = self.get_all_freq(test_item)
                            len_freq = len(freqs)
                            for freq in freqs:
                                rate = freq.find('rate').text.split(',')
                                len_rate = len(rate)
                                chain = freq.find('chain').text.split(',')
                                len_chain = len(chain)
                                num += len_rate * len_chain

            return num

    def get_num_of_5g_tx_ht20_freq(self):
            num = 0
            tree = self.read_xml()
            tests = self.get_all_test(tree)
            for test in tests:
                if test.get('name') == "5G":
                    test_items = self.get_test_items(test)
                    for test_item in test_items:
                        if test_item.get('name') == "ht20":
                            freqs = self.get_all_freq(test_item)
                            len_freq = len(freqs)
                            for freq in freqs:
                                rate = freq.find('rate').text.split(',')
                                len_rate = len(rate)
                                chain = freq.find('chain').text.split(',')
                                len_chain = len(chain)
                                num += len_rate * len_chain

            return num

    def get_num_of_5g_tx_ht40_freq(self):
            num = 0
            tree = self.read_xml()
            tests = self.get_all_test(tree)
            for test in tests:
                if test.get('name') == "5G":
                    test_items = self.get_test_items(test)
                    for test_item in test_items:
                        if test_item.get('name') == "ht40":
                            freqs = self.get_all_freq(test_item)
                            len_freq = len(freqs)
                            for freq in freqs:
                                rate = freq.find('rate').text.split(',')
                                len_rate = len(rate)
                                chain = freq.find('chain').text.split(',')
                                len_chain = len(chain)
                                num += len_rate * len_chain

            return num

    def get_num_of_5g_rx_freq(self):
            num = 0
            tree = self.read_xml()
            tests = self.get_all_test(tree)
            for test in tests:
                if test.get('name') == "5G":
                    test_items = self.get_test_items(test)
                    for test_item in test_items:
                        if test_item.get('name') == "rx":
                            freqs = self.get_all_freq(test_item)
                            len_freq = len(freqs)
                            for freq in freqs:
                                rate = freq.find('rate').text.split(',')
                                len_rate = len(rate)
                                chain = freq.find('chain').text.split(',')
                                len_chain = len(chain)
                                num += len_rate * len_chain

            return num
    #将页面表格中的数据保存到xml文档中
    def save_tabel_freq_rate_chain(self,this_freq,this_rate,this_chain,g2_or_g5,ht20_or_ht40_or_tx):
        tree = self.read_xml()
        tests = self.get_all_test(tree)
        for test in tests:
            if test.get('name')==g2_or_g5:
                test_items = self.get_test_items(test)
                for test_item in test_items:
                    if test_item.get('name') == ht20_or_ht40_or_tx:
                        freqs = self.get_all_freq(test_item)
                        freqs_text=[]
                        for i in freqs:
                            j = i.text
                            freqs_text.append(j)
                        if this_freq in freqs_text:
                            for freq in freqs:
                                val = freq.find('val').text
                                if val == this_freq:
                                    freq.find('rate').text = this_rate
                                    freq.find('chain').text = this_chain
                        else:
                            new_freq = ET.Element('freq')
                            test_item.append(new_freq)
                            new_freq_val = ET.Element('val')
                            new_freq_rate = ET.Element('rate')
                            new_freq_chain = ET.Element('chain')

                            new_freq_val.text = this_freq
                            new_freq_rate.text = this_rate
                            new_freq_chain.text = this_chain

                            new_freq.append(new_freq_val)
                            new_freq.append(new_freq_rate)
                            new_freq.append(new_freq_chain)


        # self.write_xml(tree)

class XianSunTXT_1():
    def __init__(self):
        self.xiansun_ini = Xian_Sun_ini_1()
        # print os.getcwd()
        self.filename = os.getcwd()+"\\cablecal_tool\\release\\IQ_SETUP\\IQ_ATTEN2.txt"
        self.list_2g_has_pathloss = []
        self.list_5g_has_pathloss = []
        self.all_2g_freq_pathloss_list = self.xiansun_ini.get_2g_or_5g_items("2G")
        self.all_5g_freq_pathloss_list = self.xiansun_ini.get_2g_or_5g_items("5G")
    def read_2g_xian_sun_txt(self):
        f = open(self.filename)
        line = f.readline()
        list_2g_pinlv_xiansun = []
        chain_2g_list = []

        while line:
            # print line
            if "IQ_FIXED_ATTEN_2_4_CHAIN0" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN1" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN2" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN3" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN4" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_FIXED_ATTEN_2_4_CHAIN5" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue


            # line = f.readline()
            if "IQ_ATTEN_2_4_BEGIN" in line:
                def do():

                    this_pinlv_xiansun =line[:-1].split("  ")
                    # print this_pinlv_xiansun
                    for i in range(len(this_pinlv_xiansun)-1):
                        print i
                        this_pinlv_xiansun[i+1] = float(this_pinlv_xiansun[i+1])+chain_2g_list[i]

                    list_2g_pinlv_xiansun.append(this_pinlv_xiansun)

                while "IQ_ATTEN_2_4_END" not in line:
                    line = f.readline()
                    do()
            else:
                line = f.readline()


        f.close()
        return list_2g_pinlv_xiansun

    #读取txt文件中线损
    def read_5g_xian_sun_txt(self):
        f = open(self.filename)
        line = f.readline()
        list_5g_pinlv_xiansun = []
        chain_5g_list = []
        while line:
            # print line



            # print line
            if "IQ_FIXED_ATTEN_5_CHAIN0 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN1 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN2 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN3 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN4 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_FIXED_ATTEN_5_CHAIN5" in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_ATTEN_5_BEGIN" in line:
                def do():

                    this_pinlv_xiansun = line[:-1].split("  ")

                    # print this_pinlv_xiansun
                    for i in range(len(this_pinlv_xiansun)-1):
                        this_pinlv_xiansun[i+1] = float(this_pinlv_xiansun[i+1])+chain_5g_list[i]

                    list_5g_pinlv_xiansun.append(this_pinlv_xiansun)

                    # list_5g_pinlv_xiansun.append(this_pinlv_xiansun)
                while "IQ_ATTEN_5_END" not in line:
                    line = f.readline()
                    do()
            else:
                line = f.readline()

        f.close()
        return  list_5g_pinlv_xiansun

    def write_2g_xiansun_to_ini(self):
        xiansun_2g_list = self.read_2g_xian_sun_txt()
        print xiansun_2g_list
        for xiansun_2g in xiansun_2g_list:
            for i in range(len(xiansun_2g)-1):
                self.xiansun_ini.set_xiansun_ini(xiansun_2g[0],str(i+1),xiansun_2g[i+1],'2G')
            self.list_2g_has_pathloss.append(xiansun_2g[0])
    def write_5g_xiansun_to_ini(self):
        xiansun_5g_list = self.read_5g_xian_sun_txt()
        print "xiansun_5g_list:"+str(xiansun_5g_list)
        for xiansun_5g in xiansun_5g_list:
            for i in range(len(xiansun_5g)-1):
                self.xiansun_ini.set_xiansun_ini(xiansun_5g[0],str(i+1),xiansun_5g[i+1],'5G')
            self.list_5g_has_pathloss.append(xiansun_5g[0])
    def calcute_some_freq_xiansun_to_ini(self):
        self.list_5g_has_pathloss = self.list_5g_has_pathloss[:-1]
        self.list_2g_has_pathloss = self.list_2g_has_pathloss[:-1]
        print self.list_5g_has_pathloss
        print self.list_2g_has_pathloss
        for g2_pathloss in self.all_2g_freq_pathloss_list:
            print "all_2g_freq_pathloss_list...."+str(self.all_2g_freq_pathloss_list)
            print "g2_pathloss:  "+ g2_pathloss[0]

            print "list_2g_has_pathloss:   "+str(self.list_2g_has_pathloss)
            if g2_pathloss[0] in self.list_2g_has_pathloss:
                continue
            else:
                this_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",g2_pathloss[0]).split(',')

                # next_index = 0
                # next_freq = ''
                for freq in self.list_2g_has_pathloss:
                    if string.atof(freq)> string.atof(g2_pathloss[0]):
                        next_index = self.list_2g_has_pathloss.index(freq)
                        next_freq = string.atof(freq)
                        break
                print str(int(next_freq))
                next_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",str(int(next_freq))).split(',')

                pre_index = next_index-1
                pre_freq = string.atof(self.list_2g_has_pathloss[pre_index])
                pre_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",str(int(pre_freq))).split(',')

                for i in range(len(pre_freq_pathloss)):
                    print "pre_freq_pathloss   "+pre_freq_pathloss[i]
                    print "next_freq_pathloss   "+next_freq_pathloss[i]
                    # 计算
                    this_freq_pathloss[i] = ((string.atof(pre_freq_pathloss[i]) - string.atof(next_freq_pathloss[i]))/(pre_freq-next_freq))*(string.atof(g2_pathloss[0])-next_freq)+string.atof(next_freq_pathloss[i])

                    self.xiansun_ini.set_xiansun_ini_for_calculate(g2_pathloss[0],str(i),str(round(this_freq_pathloss[i],2)),'2G')
                    print g2_pathloss[0] +  "_____"+str(i) + "__"+str(this_freq_pathloss[i])
    #             获得当前频率的上一个频率的线损，
    #             获得当前频率的下一个频率的线损。
    #             根据公式计算出当前频率的线损。
        for g5_pathloss in self.all_5g_freq_pathloss_list:
            print "all_5g_freq_pathloss_list...."+str(self.all_5g_freq_pathloss_list)
            print "g5_pathloss:  "+ g5_pathloss[0]

            print "list_5g_has_pathloss:   "+str(self.list_5g_has_pathloss)
            if g5_pathloss[0] in self.list_5g_has_pathloss:
                continue
            else:
                this_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",g5_pathloss[0]).split(',')

                # next_index = 0
                # next_freq = ''
                for freq in self.list_5g_has_pathloss:
                    if string.atof(freq)> string.atof(g5_pathloss[0]):
                        next_index = self.list_5g_has_pathloss.index(freq)
                        next_freq = string.atof(freq)
                        break
                print str(int(next_freq))
                next_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",str(int(next_freq))).split(',')

                pre_index = next_index-1
                pre_freq = string.atof(self.list_5g_has_pathloss[pre_index])
                pre_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",str(int(pre_freq))).split(',')

                for i in range(len(pre_freq_pathloss)):
                    print "pre_freq_pathloss   "+pre_freq_pathloss[i]
                    print "next_freq_pathloss   "+next_freq_pathloss[i]
                    # 计算
                    this_freq_pathloss[i] = ((string.atof(pre_freq_pathloss[i]) - string.atof(next_freq_pathloss[i]))/(pre_freq-next_freq))*(string.atof(g5_pathloss[0])-next_freq)+string.atof(next_freq_pathloss[i])

                    self.xiansun_ini.set_xiansun_ini_for_calculate(g5_pathloss[0],str(i),str(round(this_freq_pathloss[i],2)),'5G')
                    print g5_pathloss[0] +  "_____"+str(i) + "__"+str(this_freq_pathloss[i])
    # def write_2g_xiansun_to_xml(self):
    #     #将或得到的线损写入到xml文件中
    #     xiansun_2g_list = self.read_2g_xian_sun_txt()
    #     # doc = parse('testConfig.xml')
    #     testconfigxml = TestConfigxml()
    #
    #     root = testconfigxml.read_xml()
    #     testconfigxml.write_xml(root)
    #     tests = testconfigxml.get_all_test(root)
    #     for test in tests:
    #         if test.get('name')=="2G" :
    #             freq_for_lost = testconfigxml.get_freq_for_lost(test)
    #             freqs = testconfigxml.get_all_freq(freq_for_lost)
    #             for freq in freqs:
    #
    #                 val = freq.find('val').text
    #                 for xiansun_2g in xiansun_2g_list:
    #                     print xiansun_2g[0]
    #                     print val
    #                     if val == xiansun_2g[0]:
    #                         del xiansun_2g[0]
    #                         print freq.find('lost').text
    #                         # freq.find('lost').text = ",".join(str(i) for i in xiansun_2g)
    #                         freq.find('lost').text = ",".join(xiansun_2g)
    #
    #                         print freq.find('lost').text
    #     # testconfigxml.write_xml(root)
    # def write_5g_xiansun_to_xml(self):
    #     xiansun_5g_list = self.read_5g_xian_sun_txt()
    #     testconfigxml = TestConfigxml()
    #     root = testconfigxml.read_xml()
    #     tests = testconfigxml.get_all_test(root)
    #     for test in tests:
    #         if test.get('name')=="5G" :
    #             freq_for_lost = testconfigxml.get_freq_for_lost(test)
    #             freqs = testconfigxml.get_all_freq(freq_for_lost)
    #             for freq in freqs:
    #
    #                 val = freq.find('val').text
    #                 for xiansun_5g in xiansun_5g_list:
    #                     print xiansun_5g[0]
    #                     if val == xiansun_5g[0]:
    #                         del xiansun_5g[0]
    #                         print freq.find('lost').text
    #                         # freq.find('lost').text = ",".join(str(i) for i in xiansun_5g)
    #                         freq.find('lost').text = ",".join(xiansun_5g)
    #
        # testconfigxml.write_xml(root)
class XianSunTXT_2():
    def __init__(self):
        self.xiansun_ini = Xian_Sun_ini_2()
        # print os.getcwd()
        self.filename = os.getcwd()+"\\cablecal_tool\\release\\IQ_SETUP\\IQ_ATTEN3.txt"
        self.list_2g_has_pathloss = []
        self.list_5g_has_pathloss = []
        self.all_2g_freq_pathloss_list = self.xiansun_ini.get_2g_or_5g_items("2G")
        self.all_5g_freq_pathloss_list = self.xiansun_ini.get_2g_or_5g_items("5G")
    def read_2g_xian_sun_txt(self):
        f = open(self.filename)
        line = f.readline()
        list_2g_pinlv_xiansun = []
        chain_2g_list = []

        while line:
            # print line
            if "IQ_FIXED_ATTEN_2_4_CHAIN0" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN1" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN2" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN3" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN4" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_FIXED_ATTEN_2_4_CHAIN5" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue


            # line = f.readline()
            if "IQ_ATTEN_2_4_BEGIN" in line:
                def do():

                    this_pinlv_xiansun =line[:-1].split("  ")
                    # print this_pinlv_xiansun
                    for i in range(len(this_pinlv_xiansun)-1):
                        print i
                        this_pinlv_xiansun[i+1] = float(this_pinlv_xiansun[i+1])+chain_2g_list[i]

                    list_2g_pinlv_xiansun.append(this_pinlv_xiansun)

                while "IQ_ATTEN_2_4_END" not in line:
                    line = f.readline()
                    do()
            else:
                line = f.readline()


        f.close()
        return list_2g_pinlv_xiansun

    #读取txt文件中线损
    def read_5g_xian_sun_txt(self):
        f = open(self.filename)
        line = f.readline()
        list_5g_pinlv_xiansun = []
        chain_5g_list = []
        while line:
            # print line



            # print line
            if "IQ_FIXED_ATTEN_5_CHAIN0 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN1 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN2 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN3 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN4 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_FIXED_ATTEN_5_CHAIN5" in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_ATTEN_5_BEGIN" in line:
                def do():

                    this_pinlv_xiansun = line[:-1].split("  ")

                    # print this_pinlv_xiansun
                    for i in range(len(this_pinlv_xiansun)-1):
                        this_pinlv_xiansun[i+1] = float(this_pinlv_xiansun[i+1])+chain_5g_list[i]

                    list_5g_pinlv_xiansun.append(this_pinlv_xiansun)

                    # list_5g_pinlv_xiansun.append(this_pinlv_xiansun)
                while "IQ_ATTEN_5_END" not in line:
                    line = f.readline()
                    do()
            else:
                line = f.readline()

        f.close()
        return  list_5g_pinlv_xiansun

    def write_2g_xiansun_to_ini(self):
        xiansun_2g_list = self.read_2g_xian_sun_txt()
        print xiansun_2g_list
        for xiansun_2g in xiansun_2g_list:
            for i in range(len(xiansun_2g)-1):
                self.xiansun_ini.set_xiansun_ini(xiansun_2g[0],str(i+1),xiansun_2g[i+1],'2G')
            self.list_2g_has_pathloss.append(xiansun_2g[0])
    def write_5g_xiansun_to_ini(self):
        xiansun_5g_list = self.read_5g_xian_sun_txt()
        print "xiansun_5g_list:"+str(xiansun_5g_list)
        for xiansun_5g in xiansun_5g_list:
            for i in range(len(xiansun_5g)-1):
                self.xiansun_ini.set_xiansun_ini(xiansun_5g[0],str(i+1),xiansun_5g[i+1],'5G')
            self.list_5g_has_pathloss.append(xiansun_5g[0])
    def calcute_some_freq_xiansun_to_ini(self):
        self.list_5g_has_pathloss = self.list_5g_has_pathloss[:-1]
        self.list_2g_has_pathloss = self.list_2g_has_pathloss[:-1]
        print self.list_5g_has_pathloss
        print self.list_2g_has_pathloss
        for g2_pathloss in self.all_2g_freq_pathloss_list:
            print "all_2g_freq_pathloss_list...."+str(self.all_2g_freq_pathloss_list)
            print "g2_pathloss:  "+ g2_pathloss[0]

            print "list_2g_has_pathloss:   "+str(self.list_2g_has_pathloss)
            if g2_pathloss[0] in self.list_2g_has_pathloss:
                continue
            else:
                this_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",g2_pathloss[0]).split(',')

                # next_index = 0
                # next_freq = ''
                for freq in self.list_2g_has_pathloss:
                    if string.atof(freq)> string.atof(g2_pathloss[0]):
                        next_index = self.list_2g_has_pathloss.index(freq)
                        next_freq = string.atof(freq)
                        break
                print str(int(next_freq))
                next_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",str(int(next_freq))).split(',')

                pre_index = next_index-1
                pre_freq = string.atof(self.list_2g_has_pathloss[pre_index])
                pre_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",str(int(pre_freq))).split(',')

                for i in range(len(pre_freq_pathloss)):
                    print "pre_freq_pathloss   "+pre_freq_pathloss[i]
                    print "next_freq_pathloss   "+next_freq_pathloss[i]
                    # 计算
                    this_freq_pathloss[i] = ((string.atof(pre_freq_pathloss[i]) - string.atof(next_freq_pathloss[i]))/(pre_freq-next_freq))*(string.atof(g2_pathloss[0])-next_freq)+string.atof(next_freq_pathloss[i])

                    self.xiansun_ini.set_xiansun_ini_for_calculate(g2_pathloss[0],str(i),str(round(this_freq_pathloss[i],2)),'2G')
                    print g2_pathloss[0] +  "_____"+str(i) + "__"+str(this_freq_pathloss[i])
    #             获得当前频率的上一个频率的线损，
    #             获得当前频率的下一个频率的线损。
    #             根据公式计算出当前频率的线损。
        for g5_pathloss in self.all_5g_freq_pathloss_list:
            print "all_5g_freq_pathloss_list...."+str(self.all_5g_freq_pathloss_list)
            print "g5_pathloss:  "+ g5_pathloss[0]

            print "list_5g_has_pathloss:   "+str(self.list_5g_has_pathloss)
            if g5_pathloss[0] in self.list_5g_has_pathloss:
                continue
            else:
                this_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",g5_pathloss[0]).split(',')

                # next_index = 0
                # next_freq = ''
                for freq in self.list_5g_has_pathloss:
                    if string.atof(freq)> string.atof(g5_pathloss[0]):
                        next_index = self.list_5g_has_pathloss.index(freq)
                        next_freq = string.atof(freq)
                        break
                print str(int(next_freq))
                next_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",str(int(next_freq))).split(',')

                pre_index = next_index-1
                pre_freq = string.atof(self.list_5g_has_pathloss[pre_index])
                pre_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",str(int(pre_freq))).split(',')

                for i in range(len(pre_freq_pathloss)):
                    print "pre_freq_pathloss   "+pre_freq_pathloss[i]
                    print "next_freq_pathloss   "+next_freq_pathloss[i]
                    # 计算
                    this_freq_pathloss[i] = ((string.atof(pre_freq_pathloss[i]) - string.atof(next_freq_pathloss[i]))/(pre_freq-next_freq))*(string.atof(g5_pathloss[0])-next_freq)+string.atof(next_freq_pathloss[i])

                    self.xiansun_ini.set_xiansun_ini_for_calculate(g5_pathloss[0],str(i),str(round(this_freq_pathloss[i],2)),'5G')
                    print g5_pathloss[0] +  "_____"+str(i) + "__"+str(this_freq_pathloss[i])
    # def write_2g_xiansun_to_xml(self):
    #     #将或得到的线损写入到xml文件中
    #     xiansun_2g_list = self.read_2g_xian_sun_txt()
    #     # doc = parse('testConfig.xml')
    #     testconfigxml = TestConfigxml()
    #
    #     root = testconfigxml.read_xml()
    #     testconfigxml.write_xml(root)
    #     tests = testconfigxml.get_all_test(root)
    #     for test in tests:
    #         if test.get('name')=="2G" :
    #             freq_for_lost = testconfigxml.get_freq_for_lost(test)
    #             freqs = testconfigxml.get_all_freq(freq_for_lost)
    #             for freq in freqs:
    #
    #                 val = freq.find('val').text
    #                 for xiansun_2g in xiansun_2g_list:
    #                     print xiansun_2g[0]
    #                     print val
    #                     if val == xiansun_2g[0]:
    #                         del xiansun_2g[0]
    #                         print freq.find('lost').text
    #                         # freq.find('lost').text = ",".join(str(i) for i in xiansun_2g)
    #                         freq.find('lost').text = ",".join(xiansun_2g)
    #
    #                         print freq.find('lost').text
    #     # testconfigxml.write_xml(root)
    # def write_5g_xiansun_to_xml(self):
    #     xiansun_5g_list = self.read_5g_xian_sun_txt()
    #     testconfigxml = TestConfigxml()
    #     root = testconfigxml.read_xml()
    #     tests = testconfigxml.get_all_test(root)
    #     for test in tests:
    #         if test.get('name')=="5G" :
    #             freq_for_lost = testconfigxml.get_freq_for_lost(test)
    #             freqs = testconfigxml.get_all_freq(freq_for_lost)
    #             for freq in freqs:
    #
    #                 val = freq.find('val').text
    #                 for xiansun_5g in xiansun_5g_list:
    #                     print xiansun_5g[0]
    #                     if val == xiansun_5g[0]:
    #                         del xiansun_5g[0]
    #                         print freq.find('lost').text
    #                         # freq.find('lost').text = ",".join(str(i) for i in xiansun_5g)
    #                         freq.find('lost').text = ",".join(xiansun_5g)
    #
        # testconfigxml.write_xml(root)

class XianSunTXT():
    def __init__(self):
        self.xiansun_ini = Xian_Sun_ini()
        # print os.getcwd()
        self.filename = os.getcwd()+"\\cablecal_tool\\release\\IQ_SETUP\\IQ_ATTEN.txt"
        self.list_2g_has_pathloss = []
        self.list_5g_has_pathloss = []
        self.all_2g_freq_pathloss_list = self.xiansun_ini.get_2g_or_5g_items("2G")
        self.all_5g_freq_pathloss_list = self.xiansun_ini.get_2g_or_5g_items("5G")
    def read_2g_xian_sun_txt(self):
        f = open(self.filename)
        line = f.readline()
        list_2g_pinlv_xiansun = []
        chain_2g_list = []

        while line:
            # print line
            if "IQ_FIXED_ATTEN_2_4_CHAIN0" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN1" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN2" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN3" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_2_4_CHAIN4" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_FIXED_ATTEN_2_4_CHAIN5" in line:
                chain_2g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue


            # line = f.readline()
            if "IQ_ATTEN_2_4_BEGIN" in line:
                def do():

                    this_pinlv_xiansun =line[:-1].split("  ")
                    # print this_pinlv_xiansun
                    for i in range(len(this_pinlv_xiansun)-1):
                        print i
                        this_pinlv_xiansun[i+1] = float(this_pinlv_xiansun[i+1])+chain_2g_list[i]

                    list_2g_pinlv_xiansun.append(this_pinlv_xiansun)

                while "IQ_ATTEN_2_4_END" not in line:
                    line = f.readline()
                    do()
            else:
                line = f.readline()


        f.close()
        return list_2g_pinlv_xiansun

    #读取txt文件中线损
    def read_5g_xian_sun_txt(self):
        f = open(self.filename)
        line = f.readline()
        list_5g_pinlv_xiansun = []
        chain_5g_list = []
        while line:
            # print line



            # print line
            if "IQ_FIXED_ATTEN_5_CHAIN0 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN1 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN2 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN3 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue
            if "IQ_FIXED_ATTEN_5_CHAIN4 " in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_FIXED_ATTEN_5_CHAIN5" in line:
                chain_5g_list.append(float(line.split("=")[1].strip()))
                line = f.readline()
                continue

            if "IQ_ATTEN_5_BEGIN" in line:
                def do():

                    this_pinlv_xiansun = line[:-1].split("  ")

                    # print this_pinlv_xiansun
                    for i in range(len(this_pinlv_xiansun)-1):
                        this_pinlv_xiansun[i+1] = float(this_pinlv_xiansun[i+1])+chain_5g_list[i]

                    list_5g_pinlv_xiansun.append(this_pinlv_xiansun)

                    # list_5g_pinlv_xiansun.append(this_pinlv_xiansun)
                while "IQ_ATTEN_5_END" not in line:
                    line = f.readline()
                    do()
            else:
                line = f.readline()

        f.close()
        return  list_5g_pinlv_xiansun

    def write_2g_xiansun_to_ini(self):
        xian_sun_ini = Xian_Sun_ini()
        xiansun_2g_list = self.read_2g_xian_sun_txt()
        print xiansun_2g_list
        for xiansun_2g in xiansun_2g_list:
            for i in range(len(xiansun_2g)-1):
                xian_sun_ini.set_xiansun_ini(xiansun_2g[0],str(i+1),xiansun_2g[i+1],'2G')
            self.list_2g_has_pathloss.append(xiansun_2g[0])
    def write_5g_xiansun_to_ini(self):
        xian_sun_ini = Xian_Sun_ini()
        xiansun_5g_list = self.read_5g_xian_sun_txt()
        print "xiansun_5g_list:"+str(xiansun_5g_list)
        for xiansun_5g in xiansun_5g_list:
            for i in range(len(xiansun_5g)-1):
                xian_sun_ini.set_xiansun_ini(xiansun_5g[0],str(i+1),xiansun_5g[i+1],'5G')
            self.list_5g_has_pathloss.append(xiansun_5g[0])
    def calcute_some_freq_xiansun_to_ini(self):
        self.list_5g_has_pathloss = self.list_5g_has_pathloss[:-1]
        self.list_2g_has_pathloss = self.list_2g_has_pathloss[:-1]
        print self.list_5g_has_pathloss
        print self.list_2g_has_pathloss
        for g2_pathloss in self.all_2g_freq_pathloss_list:
            print "all_2g_freq_pathloss_list...."+str(self.all_2g_freq_pathloss_list)
            print "g2_pathloss:  "+ g2_pathloss[0]

            print "list_2g_has_pathloss:   "+str(self.list_2g_has_pathloss)
            if g2_pathloss[0] in self.list_2g_has_pathloss:
                continue
            else:
                this_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",g2_pathloss[0]).split(',')

                # next_index = 0
                # next_freq = ''
                for freq in self.list_2g_has_pathloss:
                    if string.atof(freq)> string.atof(g2_pathloss[0]):
                        next_index = self.list_2g_has_pathloss.index(freq)
                        next_freq = string.atof(freq)
                        break
                print str(int(next_freq))
                next_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",str(int(next_freq))).split(',')

                pre_index = next_index-1
                pre_freq = string.atof(self.list_2g_has_pathloss[pre_index])
                pre_freq_pathloss = self.xiansun_ini.get_value_for_freq("2G",str(int(pre_freq))).split(',')

                for i in range(len(pre_freq_pathloss)):
                    print "pre_freq_pathloss   "+pre_freq_pathloss[i]
                    print "next_freq_pathloss   "+next_freq_pathloss[i]
                    # 计算
                    this_freq_pathloss[i] = ((string.atof(pre_freq_pathloss[i]) - string.atof(next_freq_pathloss[i]))/(pre_freq-next_freq))*(string.atof(g2_pathloss[0])-next_freq)+string.atof(next_freq_pathloss[i])

                    self.xiansun_ini.set_xiansun_ini_for_calculate(g2_pathloss[0],str(i),str(round(this_freq_pathloss[i],2)),'2G')
                    print g2_pathloss[0] +  "_____"+str(i) + "__"+str(this_freq_pathloss[i])
    #             获得当前频率的上一个频率的线损，
    #             获得当前频率的下一个频率的线损。
    #             根据公式计算出当前频率的线损。
        for g5_pathloss in self.all_5g_freq_pathloss_list:
            print "all_5g_freq_pathloss_list...."+str(self.all_5g_freq_pathloss_list)
            print "g5_pathloss:  "+ g5_pathloss[0]

            print "list_5g_has_pathloss:   "+str(self.list_5g_has_pathloss)
            if g5_pathloss[0] in self.list_5g_has_pathloss:
                continue
            else:
                this_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",g5_pathloss[0]).split(',')

                # next_index = 0
                # next_freq = ''
                for freq in self.list_5g_has_pathloss:
                    if string.atof(freq)> string.atof(g5_pathloss[0]):
                        next_index = self.list_5g_has_pathloss.index(freq)
                        next_freq = string.atof(freq)
                        break
                print str(int(next_freq))
                next_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",str(int(next_freq))).split(',')

                pre_index = next_index-1
                pre_freq = string.atof(self.list_5g_has_pathloss[pre_index])
                pre_freq_pathloss = self.xiansun_ini.get_value_for_freq("5G",str(int(pre_freq))).split(',')

                for i in range(len(pre_freq_pathloss)):
                    print "pre_freq_pathloss   "+pre_freq_pathloss[i]
                    print "next_freq_pathloss   "+next_freq_pathloss[i]
                    # 计算
                    this_freq_pathloss[i] = ((string.atof(pre_freq_pathloss[i]) - string.atof(next_freq_pathloss[i]))/(pre_freq-next_freq))*(string.atof(g5_pathloss[0])-next_freq)+string.atof(next_freq_pathloss[i])

                    self.xiansun_ini.set_xiansun_ini_for_calculate(g5_pathloss[0],str(i),str(round(this_freq_pathloss[i],2)),'5G')
                    print g5_pathloss[0] +  "_____"+str(i) + "__"+str(this_freq_pathloss[i])
    # def write_2g_xiansun_to_xml(self):
    #     #将或得到的线损写入到xml文件中
    #     xiansun_2g_list = self.read_2g_xian_sun_txt()
    #     # doc = parse('testConfig.xml')
    #     testconfigxml = TestConfigxml()
    #
    #     root = testconfigxml.read_xml()
    #     testconfigxml.write_xml(root)
    #     tests = testconfigxml.get_all_test(root)
    #     for test in tests:
    #         if test.get('name')=="2G" :
    #             freq_for_lost = testconfigxml.get_freq_for_lost(test)
    #             freqs = testconfigxml.get_all_freq(freq_for_lost)
    #             for freq in freqs:
    #
    #                 val = freq.find('val').text
    #                 for xiansun_2g in xiansun_2g_list:
    #                     print xiansun_2g[0]
    #                     print val
    #                     if val == xiansun_2g[0]:
    #                         del xiansun_2g[0]
    #                         print freq.find('lost').text
    #                         # freq.find('lost').text = ",".join(str(i) for i in xiansun_2g)
    #                         freq.find('lost').text = ",".join(xiansun_2g)
    #
    #                         print freq.find('lost').text
    #     # testconfigxml.write_xml(root)
    # def write_5g_xiansun_to_xml(self):
    #     xiansun_5g_list = self.read_5g_xian_sun_txt()
    #     testconfigxml = TestConfigxml()
    #     root = testconfigxml.read_xml()
    #     tests = testconfigxml.get_all_test(root)
    #     for test in tests:
    #         if test.get('name')=="5G" :
    #             freq_for_lost = testconfigxml.get_freq_for_lost(test)
    #             freqs = testconfigxml.get_all_freq(freq_for_lost)
    #             for freq in freqs:
    #
    #                 val = freq.find('val').text
    #                 for xiansun_5g in xiansun_5g_list:
    #                     print xiansun_5g[0]
    #                     if val == xiansun_5g[0]:
    #                         del xiansun_5g[0]
    #                         print freq.find('lost').text
    #                         # freq.find('lost').text = ",".join(str(i) for i in xiansun_5g)
    #                         freq.find('lost').text = ",".join(xiansun_5g)
    #
        # testconfigxml.write_xml(root)


class Xian_Sun_ini_1():
    def __init__(self):
        this_version = Version_ini()
        pathloss_file = this_version.get_pathloss_file()
        self.filename = os.getcwd()+"\\cablecal_tool\\release\\IQ_SETUP\\xiansun_1.ini"

    def set_xiansun_ini(self, freq, chain, power,g2_or_g5):
        conf = Conf(self.filename)
        conf.setSection(g2_or_g5)
        powers = conf.getValue(g2_or_g5,freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index-1] = str(power)
        power_str = ",".join(power_list)
        conf.setValue(g2_or_g5, freq, power_str)

    def set_xiansun_ini_for_calculate(self, freq, chain, power,g2_or_g5):
        conf = Conf(self.filename)
        conf.setSection(g2_or_g5)
        powers = conf.getValue(g2_or_g5,freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index] = power
        power_str = ",".join(power_list)

        conf.setValue(g2_or_g5, freq, power_str)


    def get_xiansun_ini(self, freq, chain, g2_or_g5):
        conf = Conf(self.filename)
        power_str = conf.getValue(g2_or_g5, freq)
        power_list = power_str.split(',')
        index = string.atoi(chain)
        return string.atof(power_list[index-1])
    def get_2g_or_5g_items(self,g2_or_g5):
        conf = Conf(self.filename)
        items = conf.getItems(g2_or_g5)
        return items
    def get_value_for_freq(self, g2_or_g5, freq):
        conf = Conf(self.filename)
        return conf.getValue(g2_or_g5,freq)

class Xian_Sun_ini_2():
    def __init__(self):
        self.filename = os.getcwd()+"\\cablecal_tool\\release\\IQ_SETUP\\xiansun_2.ini"

    def set_xiansun_ini(self, freq, chain, power,g2_or_g5):
        conf = Conf(self.filename)
        conf.setSection(g2_or_g5)
        powers = conf.getValue(g2_or_g5,freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index-1] = str(power)
        power_str = ",".join(power_list)
        conf.setValue(g2_or_g5, freq, power_str)

    def set_xiansun_ini_for_calculate(self, freq, chain, power,g2_or_g5):
        conf = Conf(self.filename)
        conf.setSection(g2_or_g5)
        powers = conf.getValue(g2_or_g5,freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index] = power
        power_str = ",".join(power_list)

        conf.setValue(g2_or_g5, freq, power_str)


    def get_xiansun_ini(self, freq, chain, g2_or_g5):
        conf = Conf(self.filename)
        power_str = conf.getValue(g2_or_g5, freq)
        power_list = power_str.split(',')
        index = string.atoi(chain)
        return string.atof(power_list[index-1])
    def get_2g_or_5g_items(self,g2_or_g5):
        conf = Conf(self.filename)
        items = conf.getItems(g2_or_g5)
        return items
    def get_value_for_freq(self, g2_or_g5, freq):
        conf = Conf(self.filename)
        return conf.getValue(g2_or_g5,freq)

class Xian_Sun_ini():
    def __init__(self):
        this_version = Version_ini()
        pathloss_file = this_version.get_pathloss_file()
        self.filename = os.getcwd()+"\\" + pathloss_file

    def set_xiansun_ini(self, freq, chain, power,g2_or_g5):
        conf = Conf(self.filename)
        conf.setSection(g2_or_g5)
        powers = conf.getValue(g2_or_g5,freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index-1] = str(power)
        power_str = ",".join(power_list)
        conf.setValue(g2_or_g5, freq, power_str)

    def set_xiansun_ini_for_calculate(self, freq, chain, power,g2_or_g5):
        conf = Conf(self.filename)
        conf.setSection(g2_or_g5)
        powers = conf.getValue(g2_or_g5,freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index] = power
        power_str = ",".join(power_list)

        conf.setValue(g2_or_g5, freq, power_str)


    def get_xiansun_ini(self, freq, chain, g2_or_g5):
        conf = Conf(self.filename)
        power_str = conf.getValue(g2_or_g5, freq)
        power_list = power_str.split(',')
        index = string.atoi(chain)
        return string.atof(power_list[index-1])
    def get_2g_or_5g_items(self,g2_or_g5):
        conf = Conf(self.filename)
        items = conf.getItems(g2_or_g5)
        return items
    def get_value_for_freq(self, g2_or_g5, freq):
        conf = Conf(self.filename)
        return conf.getValue(g2_or_g5,freq)

    def get_pathloss_from_two_file(self):
        xian_Sun_ini_1 = Xian_Sun_ini_1()
        xian_Sun_ini_2 = Xian_Sun_ini_2()

        conf = Conf(self.filename)

        pathloss_2G_list = xian_Sun_ini_1.get_2g_or_5g_items("2G")
        pathloss_5G_list = xian_Sun_ini_2.get_2g_or_5g_items("5G")

        this_pathloss_2G_list = self.get_2g_or_5g_items("2G")
        this_pathloss_5G_list = self.get_2g_or_5g_items("5G")

        for pathloss_2G in pathloss_2G_list:
            for this_pathloss_2G in pathloss_2G_list:
                if pathloss_2G[0] == this_pathloss_2G[0]:
                    conf.setValue("2G",this_pathloss_2G[0],pathloss_2G[1])

        for pathloss_5G in pathloss_5G_list:
            for this_pathloss_5G in this_pathloss_5G_list:
                if pathloss_5G[0] == this_pathloss_5G[0]:
                    conf.setValue("5G",this_pathloss_5G[0],pathloss_5G[1])



class ART_xiansun():
    def __init__(self):
        print os.getcwd()
        self.filename = os.getcwd()+"\\ART2\\art2_ver_4_9_844_release\\bin\\station_files\\pathloss.art"
    def change_ART_xiansun(self):

        testconf = TestConf()
        xiansun_ini = Xian_Sun_ini()
        art_pathlosses = testconf.get_art_pathloss()
        # open file
        art_pathloss_list = art_pathlosses.split(",")
        fout = open(self.filename, "w")

        chains = ['1','2','4']
        xiansun_str_list = {}
        for chian in chains:
            xiansun_str_list[chian] = ''
            for art_pathloss in art_pathloss_list:
                freq = string.atof(art_pathloss)
                if freq>5000:
                    xiansun_this_freq = xiansun_ini.get_xiansun_ini(art_pathloss,chian,"5G")
                    xiansun_str_list[chian] += str(xiansun_this_freq)+','
                else:
                    xiansun_this_freq = xiansun_ini.get_xiansun_ini(art_pathloss,chian,"2G")
                    xiansun_str_list[chian] += str(xiansun_this_freq)+','
            fout.write("path device=vsa;f=" +art_pathlosses+";"+"chain="+ chian+';'+'loss=' + xiansun_str_list[chian][:-1]+';\n')
            fout.write("path device=vsg;f=" +art_pathlosses+";"+"chain="+ chian+';'+'loss=' + xiansun_str_list[chian][:-1]+';\n')



        # fin = open(self.filename, "r")


        # fout.truncate()
        #
        # header line
        # header = fin.readline()
        # fout.write(header)
        # # data lines
        # for line in fin:
        #     dat_in = line.split()
        #     dat_in[3] = "5.2" # modify data
        #     dat_out = " ".join(dat_in)
        #     fout.write(dat_out+"\n")
        # # close file
        # fin.close()
        fout.close()


class Version_ini():
    def __init__(self):
        self.filename = os.getcwd()+"\\version.ini"
        self.version_type = self.get_version()
    def set_version(self, version):
        conf = Conf(self.filename)
        conf.setSection("version")
        conf.setValue("version", "version", version)
    def get_version(self):
        conf = Conf(self.filename)
        return conf.getValue("version","version")



    def get_work_thread_name(self):
        conf = Conf(self.filename)
        return conf.getValue(self.version_type,"work_thread_name")
    def set_work_thread_name(self,work_thread_name):
        conf = Conf(self.filename)
        conf.setSection(self.version_type)
        conf.setValue(self.version_type,"work_thread_name",work_thread_name)

    def get_test_item_xml(self):
        conf = Conf(self.filename)
        return conf.getValue(self.version_type,"test_item_xml")
    def set_test_item_xml(self,test_item_xml):
        conf = Conf(self.filename)
        conf.setSection(self.version_type)
        conf.setValue(self.version_type,"test_item_xml",test_item_xml)


    def get_pathloss_file(self):
        conf = Conf(self.filename)
        return conf.getValue(self.version_type, "pathloss_file")
    def set_pathloss_file(self,pathloss_file):
        conf = Conf(self.filename)
        conf.setSection(self.version_type)
        conf.setValue(self.version_type,"pathloss_file",pathloss_file)

    def get_config_file(self):
        conf = Conf(self.filename)
        return conf.getValue(self.version_type,"config_file")
    def set_config_file(self,config_file):
        conf = Conf(self.filename)
        conf.setSection(self.version_type)
        conf.setValue(self.version_type,"config_file",config_file)


    def get_testConfig_file(self):
        conf = Conf(self.filename)
        return conf.getValue(self.version_type,"testConfig_file")
    def set_testConfig_file(self,testConfig_file):
        conf = Conf(self.filename)
        conf.setSection(self.version_type)
        conf.setValue(self.version_type,"testConfig_file",testConfig_file)


    def get_art_refDesighs_catalog(self):
        conf = Conf(self.filename)
        return conf.getValue(self.version_type,"art_refDesighs_catalog")
    def set_art_refDesighs_catalog(self,art_refDesighs_catalog):
        conf = Conf(self.filename)
        conf.setSection(self.version_type)
        conf.setValue(self.version_type,"art_refDesighs_catalog",art_refDesighs_catalog)
    #
    # 根据不同的板子使用不同路径下的art2配置文件
    def change_ART2_config_folder(self):
        this_version_catalog_list = self.get_art_refDesighs_catalog().split(',')
        ref_decices_file = os.getcwd() + '\\ART2\\art2_ver_4_9_844_release\\bin\\station_files\\ref_devices.art'

        f = open(ref_decices_file, "w")

        f.write("assign number.radios="+ this_version_catalog_list[0]+";\n")
        f.write("assign referenceID[1]="+this_version_catalog_list[1]+';\n')
        f.write("assign referenceID[2]="+this_version_catalog_list[2]+';\n')

        f.close()

class ART_jiaozhun():
    def __init__(self):
        version = Version_ini()
        art2_refDesighs_catalog = version.get_art_refDesighs_catalog().split(',')
        self.filename_2g = os.getcwd()+"\\ART2\\art2_ver_4_9_844_release\\command\\refDesigns\\" + art2_refDesighs_catalog[1]+"\\setup_overwrite.art"
        self.filename_5g = os.getcwd()+"\\ART2\\art2_ver_4_9_844_release\\command\\refDesigns\\" + art2_refDesighs_catalog[2]+"\\setup_overwrite.art"


    # 修改配置文件 只测试2g
    # 将2gdisabled 设为0,5g disabled设为1
    def only_2g_jiaozhun(self):

        f2 = open(self.filename_2g,"r+")

        line_list = f2.readlines()

        for line in line_list:
            if "assign 2G.Disable" in line:
                index2 = line_list.index(line)
                line_list[index2] = "assign 2G.Disable = 0\n"
            if "assign 5G.Disable" in line:
                index5 = line_list.index(line)
                line_list[index5] = "assign 5G.Disable = 1\n"


        f2w = open(self.filename_2g,"w+")
        f2w.writelines(line_list)

        f2.close()
        f2w.close()

        f5 = open(self.filename_5g,"r+")

        line_list = f5.readlines()

        for line in line_list:
            if "assign 2G.Disable" in line:
                index2 = line_list.index(line)
                line_list[index2] = "assign 2G.Disable = 1\n"
            if "assign 5G.Disable" in line:
                index5 = line_list.index(line)
                line_list[index5] = "assign 5G.Disable = 1\n"


        f5w = open(self.filename_5g,"w+")
        f5w.writelines(line_list)

        f5.close()
        f5w.close()


    def only_5g_jiaozhun(self):
        f2 = open(self.filename_2g,"r+")

        line_list = f2.readlines()

        for line in line_list:
            if "assign 2G.Disable" in line:
                index2 = line_list.index(line)
                line_list[index2] = "assign 2G.Disable = 1\n"
            if "assign 5G.Disable" in line:
                index5 = line_list.index(line)
                line_list[index5] = "assign 5G.Disable = 1\n"


        f2w = open(self.filename_2g,"w+")
        f2w.writelines(line_list)

        f2.close()
        f2w.close()

        f5 = open(self.filename_5g,"r+")

        line_list = f5.readlines()

        for line in line_list:
            if "assign 2G.Disable" in line:
                index2 = line_list.index(line)
                line_list[index2] = "assign 2G.Disable = 1\n"
            if "assign 5G.Disable" in line:
                index5 = line_list.index(line)
                line_list[index5] = "assign 5G.Disable = 0\n"


        f5w = open(self.filename_5g,"w+")
        f5w.writelines(line_list)

        f5.close()
        f5w.close()

    # 修改art配置文件。2g和5g都进行校准。wb2622型号产测使用。
    def all_to_jiaozhun(self):
        f2 = open(self.filename_2g,"r+")

        line_list = f2.readlines()

        for line in line_list:
            if "assign 2G.Disable" in line:
                index2 = line_list.index(line)
                line_list[index2] = "assign 2G.Disable = 0\n"
            if "assign 5G.Disable" in line:
                index5 = line_list.index(line)
                line_list[index5] = "assign 5G.Disable = 1\n"


        f2w = open(self.filename_2g,"w+")
        f2w.writelines(line_list)

        f2.close()
        f2w.close()

        f5 = open(self.filename_5g,"r+")

        line_list = f5.readlines()

        for line in line_list:
            if "assign 2G.Disable" in line:
                index2 = line_list.index(line)
                line_list[index2] = "assign 2G.Disable = 1\n"
            if "assign 5G.Disable" in line:
                index5 = line_list.index(line)
                line_list[index5] = "assign 5G.Disable = 0\n"


        f5w = open(self.filename_5g,"w+")
        f5w.writelines(line_list)

        f5.close()
        f5w.close()



