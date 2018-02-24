#coding=gbk
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
import telnetlib
import os
import time
import string
from ctypes import *
from trunk.myconfig import *
from trunk.logic import *
from bdplug.dbop import *
import subprocess
#how_to_do_test 0:only 2.4G;  1:only 5G;  2:both 2.4G and 5G
how_to_do_test = 2
system_halted = 0
#
# curPath = os.path.abspath(__file__)
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
# def get_rootPath():
#     global rootPath
#     return rootPath
# print rootPath
print os.getcwd()
test_mode = 2
#test_mode = 5
debug = 0

fail_mssage = '\n' #失败时显示信息
###check###
this_test_result_fail=2
cdi_in = 19.0
cdi = c_double(cdi_in)
pcdi = pointer(cdi)
###check###
this_mac = 0
s = '''
global_pcdac_2G = "30"
global_pcdac_5G = "40"
#global_pcdac = "30"
global_pcdac = ""
'''

s = '''
freq_5g = ["5180", "5500", "5805"]
rate_5g = ["54", "t7"]
chain_5g = ["1" "2"]

freq_2g_ht20 = ["2412","2437","2462"]
rate_2g_ht20 = ["11s","6","t0","t7"]

freq_2g_ht40 = ["2412","2437","2452"]
rate_2g_ht40 = ["f0", "f7"]

chain = ["1", "2"]
'''

rate_80211b = ["1l", "2l", "5.5l", "11l", "11s","5l"]
rate_80211g = ["6","9","12","18","24","36","48","54"]
rate_80211a = ["6","9","12","18","24","36","48","54"]
rate_80211n_ht20 = ["t0","t1","t2","t3","t4","t5","t6","t7","t8","t9","t10","t11","t12","t13","t14","t15","t16","t23"]
rate_80211n_ht40 = ["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15","f16","f23"]
rate_80211ac_ht20 = ["vt0","vt5","vt6","vt7","vt8","vt9","vt10","vt19","vt20","vt29"]
rate_80211ac_ht40 = ["vf0","vf5","vf6","vf7","vf8","vf9","vf10","vf19","vf20","vf29"]
rate_80211ac_ht80 = ["ve0","ve5","ve6","ve7","ve8","ve9","ve10","ve19","ve20","ve29"]


capture_time = {"1l":800, "2l":600, "5.5l":400, "11l":200, "11s":200,
    "6":690,"9":620,"12":550,"18":480,"24":410,"36":340,"48":270,"54":200,"ve0":650,"vt0":650,"vf0":650,"vt5":400,"vf5":400,"ve5":400,"vt6":350,"vf6":350,"ve6":350,"vt7":300,"vf7":300,"ve7":300,"vf9":600,"vt8":650,"ve9":600,"vt9":600,"vf8":650,"ve8":650,
    "t0":550,"t1":500,"t2":450,"t3":400,"t4":350,"t5":300,"t6":250,"t7":200,"t8":200,"t9":200,"t10":200,"t11":200,"t12":200,"t13":200,"t14":200,"t15":200,
    "f0":550,"f1":500,"f2":450,"f3":400,"f4":350,"f5":300,"f6":250,"f7":200,"f8":200,"f9":200,"f10":200,"f11":200,"f12":200,"f13":200,"f14":200,"f15":200}
s = '''
vsg_power_level = {"5l":-90,"11l":-90,"6":-82,"54":-65,"t7":-65,"t8":-82,"t15":-64,"t16":-82,"t23":-64,"f7":-64,"f8":-79,"f15":-61,"f16":-79,"f23":-61,
    "vt0":-82,"vt8":-59,"vt10":-82,"vt18":-59,"vt20":-82,"vt29":-59,"vf0":-79,"vf9":-54,"vf10":-79,"vf19":-54,"vf20":-79,"vf29":-54,"ve0":-76,"ve9":-51,
    "ve10":-76,"ve19":-51,"ve20":-76,"ve29":-51,"vt7":-65,"vf7":-62,"ve7":-59}
'''

tx_evm_limit = {"6":-5,"54":-25,"11s":-10,"t0":-7,"t4":-18,"t7":-27,"t8":-7,"t12":-18,"t15":-28,"t16":-7,"t20":-18,"t23":-28,"f0":-7,"f7":-28,"f8":-7,
    "f12":-18,"f15":-28,"f16":-7,"f20":-18,"f23":-28,"vt0":-5,"vt8":-30,"vt10":-5,"vt18":-30,"vt20":-5,"vt29":-32,"vf0":-5,"vf9":-32,"vf10":-5,"vf19":-32,
    "vf20":-5,"vf29":-32,"ve0":-5,"ve9":-32,"ve10":-5,"ve19":-32,"ve20":-5,"ve29":-32}

#txppm_limit = 20

dict_2g_tx = {}

#path_loss = 16
#limit = 2.5

path_loss_2g = 18
path_loss_5g = 20

#setting: lost, limit
ht20_2g_setting = (path_loss_2g, 2.5)
ht40_2g_setting = (path_loss_2g, 2)
ht20_5g_setting = (path_loss_5g, 2.5)
ht40_5g_setting = (path_loss_5g, 2)
no_setting = (0,0)

#最后的测试结果
test_result_fail = 0

# 校准结果
jiaozhun_result = 0
def set_fail_mssage(msg):
    global  fail_mssage
    fail_mssage = msg

def get_fail_massage():
    global fail_mssage
    return fail_mssage

def set_jiaozhun_result(result):
    global jiaozhun_result
    jiaozhun_result = result

def get_jiaozhun_result():
    global jiaozhun_result
    return jiaozhun_result
def set_test_result(result):
    global test_result_fail
    test_result_fail = result

def get_test_result():
    global test_result_fail
    return test_result_fail
jiaozhun_5g_power = {"5180_1":(1.4, 18.3),"5180_2":(4.9, 18.2),"5240_1":(3.7, 18.1),"5240_2":(6.2, 17.5),"5260_1":(4.4, 18.3),"5260_2":(5.9, 18.1),
    "5320_1":(5.9, 18.2),"5320_2":(6.1, 17.7),"5500_1":(9.6, 16.8),"5500_2":(6.8, 17.1),"5700_1":(9.1, 15.7),"5700_2":(3.0, 16.2),"5745_1":(8.9, 16.1),
    "5745_2":(2.6, 15.7),"5805_1":(7.9, 16.1),"5805_2":(0.8, 15.8)}

#中英文unicode宽度，用于输出对齐
widths = [
    (126,    1), (159,    0), (687,     1), (710,   0), (711,   1),
    (727,    0), (733,    1), (879,     0), (1154,  1), (1161,  0),
    (4347,   1), (4447,   2), (7467,    1), (7521,  0), (8369,  1),
    (8426,   0), (9000,   1), (9002,    2), (11021, 1), (12350, 2),
    (12351,  1), (12438,  2), (12442,   0), (19893, 2), (19967, 1),
    (55203,  2), (63743,  1), (64106,   2), (65039, 1), (65059, 0),
    (65131,  2), (65279,  1), (65376,   2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]

def get_width( o ):
    """Return the screen column width for unicode ordinal o."""
    global widths
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1

def total_width( s ):
    t = 0
    i = 0
    while(i<len(s)):
        t+=get_width(ord(s[i]))
        i=i+1
    return t

myconfig = {"mac":"00:11:22:33:44:88",
            "rate":"HT20",
            "channel":"1",
            "country":"CN",
            "ssid":"BDCOM",
            "wanip":"172.16.20.216"}

class Worker(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        conf = TestConf()
        self.ip = conf.get_default_ip()
    def __del__(self):
        self.wait()
    def stop(self):
        self.exit(0)
    def render(self,myip):

        try:
            self.ip = str(myip)
        except  Exception as e:
            self.emit(SIGNAL("result_fail"))
            set_test_result(1)
            self.printstr(u'傻子，Ip填错了！\n',QColor(255, 0, 0, 220))
            self.printstr(u"error: {0}\n".format(e),QColor(255, 0, 0, 220))
            # self.emit(SIGNAL("terminated()"))
            return
        self.start()
    def run(self):
        # ttime = time.time()
        # stime = time.localtime(ttime)
        # # strtime = str(ttime)
        # strtime = time.strftime("%Y-%m-%d %H:%M:%S",stime)
        # print strtime
        global test_result_fail
        test_result_fail = 0

        self.emit(SIGNAL("testing2"))
        ping_flag = self.ping_AP(self.ip)
        # ping_flag = 1
        # telnet_flag = self.telnet_default_ip_and_do_something()
        time.sleep(3)
        telnet_flag = self.do_test()
        # telnet_flag = 0
        # self.save_all_to_data_base()

        print ping_flag
        if ping_flag==1:
            if telnet_flag==0:
                #开始测试z
                self.do_protest()
            elif telnet_flag == 1:
                self.printstr(u'抱歉，登录AP失败！请重试\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))

                # self.emit(SIGNAL("terminated()"))
                test_result_fail = 8888
                self.emit(SIGNAL("error_telnet"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                # self.__del__()
                return
            elif telnet_flag == 3:
                self.printstr(u'序列号不匹配！请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                test_result_fail = 8888
                # self.emit(SIGNAL("terminated()"))
                self.emit(SIGNAL("error_sn"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                # self.__del__()
                return
            elif telnet_flag == 4:
                self.printstr(u'基测数据未通过！请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))

                test_result_fail = 8888
                # self.emit(SIGNAL("terminated()"))
                self.emit(SIGNAL("error_base_info"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                return
            elif telnet_flag == 5:
                self.printstr(u'超出使用次数，请联系管理员\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))

                test_result_fail = 8888
                # self.emit(SIGNAL("terminated()"))
                self.emit(SIGNAL("error_ipuse"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                return
            elif telnet_flag == 6:
                self.printstr(u'老化信息未通过，请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                test_result_fail = 8888
                # self.emit(SIGNAL("terminated()"))
                self.emit(SIGNAL("error_old_info"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                return
            elif telnet_flag == 7:
                self.printstr(u'老化时间不合格，请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))

                test_result_fail = 8888
                # self.emit(SIGNAL("terminated()"))
                self.emit(SIGNAL("error_old_hours"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                return
            elif telnet_flag == 8:
                self.printstr(u'前一站状态为空或失败，请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))

                test_result_fail = 8888
                # self.emit(SIGNAL("terminated()"))
                self.emit(SIGNAL("error_old_hours"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                return
            else:
                self.printstr(u'抱歉，AP执行命令时出错！请重试\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))

                test_result_fail = 8888
                # self.emit(SIGNAL("terminated()"))
                self.emit(SIGNAL("error_change_mode"))
                self.emit(SIGNAL("set_focus"))
                self.emit(SIGNAL("zhunbei_txt"))
                return
        else:
            self.printstr(u'连接错误！请检查设备是否连接正确\n',QColor(255, 0, 0, 220))
            # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))

            test_result_fail = 8888
            # self.emit(SIGNAL("terminated()"))
            self.emit(SIGNAL("error_ping"))
            self.emit(SIGNAL("set_focus"))
            self.emit(SIGNAL("zhunbei_txt"))
            return






        #开始测试
        # self.do_protest()
    def printstr(self,mystr,color):
        self.emit(SIGNAL("output"),mystr,color)


    def ping_AP(self,telnet_ip):
        ping_num = 0
        time_begin = time.time()
        # for j in range(4):
        while ping_num == 0:
            time_end = time.time()
            self.emit(SIGNAL("testing2"))
            ping_flag = os.popen("ping "+telnet_ip+ " -n 6").read()
            self.emit(SIGNAL("testing3"))
            print ping_flag

            # ping_flag = ping_flag.split('\n')
            # for i in ping_flag:
            #     print str(i)+"********************************"
            # line_str_list = ping_flag[8].split('=')
            # sent_str = line_str_list[1].strip()[0]
            # received = line_str_list[2].strip()[0]
            ping_up_result = str(ping_flag).count('TTL')
            ping_lower_result = str(ping_flag).count('ttl')
            print str(ping_up_result) +"********************"
            print ping_lower_result
            # if string.atoi(sent_str)==string.atoi(received):
            if ping_up_result>=6 or ping_lower_result>=6:
                ping_num = 1
                return 1

            if time_end-time_begin >180:
                ping_num = 1
                return 0
            # if not ping_flag:
            #     return 1


        # if ping_num ==4:
        #     return 1

    def get_this_mac_address(self):
        import uuid
        node = uuid.getnode()
        mac = uuid.UUID(int = node).hex[-12:]
        self.printstr(u'**************mac地址: '+mac+" **************\n",QColor(255, 0, 0, 220))
        return mac

    def test_sn(self):
        global myconf
        myconf = MyConf()
        tn.write("ar_protest --MB-SN -r\n")

        print "test sn \n"

        sn_str = tn.read_until("~#",10)#需要具体查看str是什么
        #校验序列号是否匹配
        print sn_str
        global input_sn
        input_sn = myconf.get_sn_num()
        self.printstr(u'**************当前AP_sn序列号: '+str(input_sn)+" **************\n",QColor(255, 0, 0, 220))

        if input_sn.lower() not in sn_str.lower():
            return 3#序列号不匹配


    #校验ipx使用次数是否合格
    def test_ipx(self,dbop_temp):
        global this_mac
        this_mac = self.get_this_mac_address()#获得当前mac地址
        this_mac_ipx = dbop_temp.getIPXInterfaceByMac(this_mac)#获得已经使用次数
        this_mac_max_ipx = dbop_temp.getIPXMaxCount(this_mac)#获得最大使用次数
        self.printstr(u'\n**************mac可用次数: '+str(this_mac_max_ipx)+" **************\n",QColor(255, 0, 0, 220))
        self.printstr(u'**************mac已用次数: '+str(this_mac_ipx)+" **************\n",QColor(255, 0, 0, 220))
        # this_mac_ipx = 100
        # this_mac_max_ipx = string.atoi(myconf.get_max_ip_use())

        print str(this_mac_ipx)
        print str(this_mac_max_ipx)
        if this_mac_ipx > this_mac_max_ipx:
            return 5#超出使用次数

    def test_previous_result(self,dbop_temp):
        myconf = MyConf()
        input_sn = myconf.get_sn_num()
        previous_result = dbop_temp.getAPPreTestStateBySN(input_sn)
        if previous_result is None:
            return 8
        # last_previous_result_list = previous_result.split(',')
        self.printstr(u'\n************** 此AP前一站状态: '+str(previous_result)+" **************\n",QColor(255, 0, 0, 220))
        if 'fail' in previous_result:
            return 8#初站为通过


    def test_old_result(self,myconf):
        # 老化信息是否通过
        print "test old result \n"
        tn.write("agtest result\n")

        old_results = tn.read_until("~#",20)

        print old_results
        self.printstr(u'\n************** 老化结果: \n'+str(old_results)+" **************\n",QColor(255, 0, 0, 220))

        if 'cpu error number' in old_results or 'switch error number' in old_results or '!!!Error' in old_results:
            return 6

        old_results_list = old_results.split("\n")

        old_hour = old_results_list[6].split(" ")
        this_hour = old_hour[6].replace(' ','').replace('\r','')

        if "Failed" in old_results_list[1] or "Failed" in old_results_list[3] or "Failed" in old_results_list[5]:
            return 6 #老化信息未通过

        int_this_hour = string.atoi(this_hour)
        norm_hour = string.atoi(myconf.get_old_hour())
        self.printstr(u'\n************** 老化时间: '+str(int_this_hour)+" **************\n",QColor(255, 0, 0, 220))
        self.printstr(u'************** 标准老化时间: '+str(myconf.get_old_hour())+" **************\n",QColor(255, 0, 0, 220))

        if int_this_hour < norm_hour: #22应可配置
            return 7#老化时间未通过

    def test_base_result(self,dbop_temp):
        #校验基测数据是否通过
        base_test_resutlt = dbop_temp.getBaseTestBySN(input_sn)
        # base_test_resutlt = True
        if base_test_resutlt == False:
            return 4#基测数据未通过

    def test_art(self):
        print "test art  \n"
        current_mode = "lsmod | grep art"#获得ap当前模式的命令
        tn.write(current_mode +'\n')
        current_mode_return = tn.read_until("~#",10)
        if "art  " not in current_mode_return :
            print"****** art"
            cmd_change_mode = "ar_protest --art"
            tn.write(cmd_change_mode +'\n')
            time.sleep(5)
    def telnet_ap(self,testconf):
        global tn
        try:
            print "login AP \n"
            telnet_ip = testconf.get_default_ip()       ##获取IP
            ##登录,telnet AP##
            username = testconf.get_username()
            password = testconf.get_password()
            tn = telnetlib.Telnet(telnet_ip)
            login_str = tn.read_until("login: ",20)
            tn.write(username+'\n')
            password_str = tn.read_until("Password: ",10)
            tn.write(password +'\n')
            tn.read_until("~#",10)
            time.sleep(1)
            print "login AP ok !"
        except Exception,e:
            print(e)
            return 1


    ##AP校准测试及准备##
    def do_test(self):
        try:
            testconf = TestConf()
            myconf = MyConf()
            checkTelnet = self.telnet_ap(testconf)
            pmgr_link =  myconf.get_pmgr_link()

            zhiju_sttr = myconf.get_zhiju_id()
            self.printstr(u'**************当前治具标识: '+str(zhiju_sttr)+" **************\n",QColor(255, 0, 0, 220))

            if checkTelnet==1:
                time.sleep(5)
                checkTelnet = self.telnet_ap(testconf)
                if checkTelnet == 1:
                    return checkTelnet
                # return checkTelnet
            # ##加载数据库操作文件文件##
            if pmgr_link =='1':
                dbop = DataBaseOP();
            # ##校验序列号##
            if pmgr_link =='1':
                checkSN = self.test_sn()
                if checkSN==3:
                    return 3
            ##校验IPX使用次数##
            if pmgr_link =='1':
                checkIPX = self.test_ipx(dbop)
                if checkIPX==5:
                    return 5;

            ##测试站点区分##
            ##A 站
            if pmgr_link =='1':
                if int(testconf.get_is_or_not_jiaozhun()) == 1:
                    ##读取基板测试数据
                    checkBT = self.test_base_result(dbop)
                    if checkBT==4:
                        return 4
                    ##校验老化数据
                    checkOLD = self.test_old_result(myconf)
                    if checkOLD>=6:
                        return checkOLD
            # B 站
            if pmgr_link =='1':
                if int(testconf.get_is_or_not_jiaozhun()) == 0:
                    print('do_test b')
                    checkAS = self.test_previous_result(dbop)
                    if checkAS==8:
                        return 8
            print "ok"
            self.test_art()
            return 0
        except Exception,e:
            print(e)
            return 1

    #对AP进行telnet操作，并改变AP的模式
    def telnet_default_ip_and_do_something(self):
        testconf = TestConf()
        telnet_ip = testconf.get_default_ip()
        # if self.ping_AP(telnet_ip):
        # myform = MyForm()
        myconf = MyConf()
        dbop_temp = DataBaseOP()


        try:
            testconf = TestConf()
            username = testconf.get_username()
            password = testconf.get_password()


            tn = telnetlib.Telnet(telnet_ip)
            login_str = tn.read_until("login: ")
            tn.write(username+'\n')


            password_str = tn.read_until("Password: ")
            tn.write(password +'\n')
            tn.read_until("~#")

            time.sleep(0.5)


            # #获得序列号
            self.test_sn()

            self.test_ipx()
            if testconf.get_is_or_not_jiaozhun() == '0':
                self.test_base_result()
                self.test_old_result()
            # if testconf.get_is_or_not_jiaozhun() == '1':
            #     self.test_previous_result()
            self.test_art()



            # 在这块获得是否要执行ar_protest --art
            # 同时发送命令获得序列号，，和扫描后获得的序列号对比，如果相等返回成功，程序继续进行。
            # 否则返回错误。程序不继续进行。
            # time.sleep(5)
            #


            return 0
        except:
            return 1





    def do_protest(self):
        global test_mode
        global test_result_fail
        global how_to_do_test
        global jiaozhun_result
        testconfig = TestConf()
        myconf = MyConf()
        fail_stop_flag = myconf.get_fail_stop()
        how_to_do_test = testconfig.get_howtotest()
        # test_result_fail = 0
        jiaozhun_result = 0
        pmgr_link = myconf.get_pmgr_link()
        #初始化测试仪器的dll
        self.dll_init()
        self.dll_getversion()
        self.mask_dll_init()


        if(how_to_do_test == '0' or how_to_do_test == '2'):
            test_mode = 2
            self.protest()
        print "testresult ++++++=" + str(get_test_result())
        if fail_stop_flag == '1':
            if test_result_fail != 0 or jiaozhun_result != 0:
                self.emit(SIGNAL("result_fail"))
                self.printstr("\n\n\n********************************************\n", QColor(0, 0, 0, 110))
                self.printstr("********************************************\n\n", QColor(0, 0, 0, 110))
                self.printstr("                     fail\n\n", QColor(255, 0, 0, 220))
                self.printstr("********************************************\n", QColor(0, 0, 0, 110))
                self.printstr('\n'+fail_mssage +'\n', QColor(255, 0, 0, 220))
                self.printstr("********************************************\n", QColor(0, 0, 0, 110))

                if pmgr_link == '1':
                    self.save_all_to_data_base('2.4')
                return
        if pmgr_link == '1':
                    self.save_all_to_data_base('2.4')
        if jiaozhun_result == 8888:
            set_test_result(1)
            self.emit(SIGNAL("result_fail"))
            self.printstr("\n\n\n********************************************\n", QColor(0, 0, 0, 110))
            self.printstr("********************************************\n\n", QColor(0, 0, 0, 110))
            self.printstr("                     fail\n\n", QColor(255, 0, 0, 220))
            self.printstr("********************************************\n", QColor(0, 0, 0, 110))
            self.printstr('\n'+fail_mssage +'\n', QColor(255, 0, 0, 220))
            self.printstr("********************************************\n", QColor(0, 0, 0, 110))

            if pmgr_link == '1':
                self.save_all_to_data_base('2.4')
            return
        if(how_to_do_test == '1' or how_to_do_test == '2'):
            test_mode = 5
            self.protest()
            print str(get_test_result())+" #### test result####"
            # if pmgr_link == '1':
            #         self.save_result_to_data_base()
        if fail_stop_flag == '1':
            if test_result_fail != 0 or jiaozhun_result != 0:
                self.emit(SIGNAL("result_fail"))
                if pmgr_link == '1':
                    self.save_all_to_data_base('5')
                return
            else:
                if pmgr_link == '1':
                    self.save_all_to_data_base('5')
        else:
            #保存数据库
            if pmgr_link == '1':
                self.save_all_to_data_base('5')
        #判断成功失败
        if test_result_fail == 0  and jiaozhun_result == 0:
            self.printstr("\n\n\n********************************************\n", QColor(0, 0, 0, 110))
            self.printstr("********************************************\n\n", QColor(0, 0, 0, 110))
            self.printstr("                     success\n\n", QColor(0, 0, 0, 110))
            self.printstr("********************************************\n", QColor(0, 0, 0, 110))
            self.printstr("********************************************\n\n", QColor(0, 0, 0, 110))
            self.emit(SIGNAL("result_success"))
        else:
            self.printstr("\n\n\n********************************************\n", QColor(0, 0, 0, 110))
            self.printstr("********************************************\n\n", QColor(0, 0, 0, 110))
            self.printstr("                     fail\n\n", QColor(255, 0, 0, 220))
            self.printstr("********************************************\n", QColor(0, 0, 0, 110))
            self.printstr('\n'+fail_mssage +'\n', QColor(255, 0, 0, 220))
            self.printstr("********************************************\n", QColor(0, 0, 0, 110))
            self.emit(SIGNAL("result_fail"))


        print str(get_test_result())+" #### test result####"
        #结束测试仪指令
        dll.LP_Term()#??????s
        # write_art = testconfig.get_write_art()
        # if(write_art == "1"):#1daibiao
        #     if(test_result_fail == 0):
        #         self.after_rx()
        # else:
        #     self.after_rx()

    def do_get_setting(self):
        global test_mode
        global global_pcdac_2G,global_pcdac_5G, global_pcdac
        if(test_mode == 2):
            global_pcdac = global_pcdac_2G
        else:
            global_pcdac = global_pcdac_5G

    def get_table_line_num(self, testmode, testwhat):
        testconfig = TestConf()
        testconfigxml = TestConfigxml()
        if(testmode == "2G"):
            if(testwhat == "jiaozhun"):
                return 0
            elif(testwhat == "pinpian_jiaozhun"):
                return 1
            elif(testwhat == "tx_ht20"):
                line = 1+testconfigxml.get_num_of_2g_tx_ht20_freq()
                #line = 1+testconfig.get_num_of_something("2G","tx_ht20_freq")*testconfig.get_num_of_something("2G","tx_ht20_rate")*testconfig.get_num_of_something("2G","tx_ht20_chain")
                return line
            elif(testwhat == "tx_ht40"):
                line = 1+testconfigxml.get_num_of_2g_tx_ht20_freq()+testconfigxml.get_num_of_2g_tx_ht40_freq()

                # line = 1+testconfig.get_num_of_something("2G","tx_ht20_freq")*testconfig.get_num_of_something("2G","tx_ht20_rate")*testconfig.get_num_of_something("2G","tx_ht20_chain")+\
                #          testconfig.get_num_of_something("2G","tx_ht40_freq")*testconfig.get_num_of_something("2G","tx_ht40_rate")*testconfig.get_num_of_something("2G","tx_ht40_chain")
                return line
            elif(testwhat == "rx"):
                line = 1+testconfigxml.get_num_of_2g_tx_ht20_freq()+testconfigxml.get_num_of_2g_tx_ht40_freq()+testconfigxml.get_num_of_2g_rx_freq()
                # line = 1+testconfig.get_num_of_something("2G","tx_ht20_freq")*testconfig.get_num_of_something("2G","tx_ht20_rate")*testconfig.get_num_of_something("2G","tx_ht20_chain")+\
                #          testconfig.get_num_of_something("2G","tx_ht40_freq")*testconfig.get_num_of_something("2G","tx_ht40_rate")*testconfig.get_num_of_something("2G","tx_ht40_chain")+\
                #          testconfig.get_num_of_something("2G","rx_freq")*testconfig.get_num_of_something("2G","rx_rate")*testconfig.get_num_of_something("2G","rx_chain")
                return line
        else:
            how_to_test = testconfig.get_howtotest()
            if(how_to_test == "1"):
                if(testwhat == "jiaozhun"):
                    return 0
                elif(testwhat == "pinpian_jiaozhun"):
                    return 1
                elif(testwhat == "tx_ht20"):
                    line = 1+testconfigxml.get_num_of_5g_tx_ht20_freq()
                    # line = 1+testconfig.get_num_of_something("5G","tx_ht20_freq")*testconfig.get_num_of_something("5G","tx_ht20_rate")*testconfig.get_num_of_something("5G","tx_ht20_chain")
                    return line
                elif(testwhat == "tx_ht40"):
                    line = 1+testconfigxml.get_num_of_5g_tx_ht20_freq()+testconfigxml.get_num_of_5g_tx_ht40_freq()
                    # line = 1+testconfig.get_num_of_something("5G","tx_ht20_freq")*testconfig.get_num_of_something("5G","tx_ht20_rate")*testconfig.get_num_of_something("5G","tx_ht20_chain")+\
                    #      testconfig.get_num_of_something("5G","tx_ht40_freq")*testconfig.get_num_of_something("5G","tx_ht40_rate")*testconfig.get_num_of_something("5G","tx_ht40_chain")
                    return line
                elif(testwhat == "rx"):
                    line = 1+testconfigxml.get_num_of_5g_tx_ht20_freq()+testconfigxml.get_num_of_5g_tx_ht40_freq()+testconfigxml.get_num_of_5g_rx_freq()
                    # line = 1+testconfig.get_num_of_something("5G","tx_ht20_freq")*testconfig.get_num_of_something("5G","tx_ht20_rate")*testconfig.get_num_of_something("5G","tx_ht20_chain")+\
                    #      testconfig.get_num_of_something("5G","tx_ht40_freq")*testconfig.get_num_of_something("5G","tx_ht40_rate")*testconfig.get_num_of_something("5G","tx_ht40_chain")+\
                    #      testconfig.get_num_of_something("5G","rx_freq")*testconfig.get_num_of_something("5G","rx_rate")*testconfig.get_num_of_something("5G","rx_chain")
                    return line
            elif(how_to_test == "2"):
                num_2G = 2+testconfigxml.get_num_of_2g_tx_ht20_freq()+testconfigxml.get_num_of_2g_tx_ht40_freq()+testconfigxml.get_num_of_2g_rx_freq()
                # num_2G = 2+testconfig.get_num_of_something("2G","tx_ht20_freq")*testconfig.get_num_of_something("2G","tx_ht20_rate")*testconfig.get_num_of_something("2G","tx_ht20_chain")+\
                #          testconfig.get_num_of_something("2G","tx_ht40_freq")*testconfig.get_num_of_something("2G","tx_ht40_rate")*testconfig.get_num_of_something("2G","tx_ht40_chain")+\
                #          testconfig.get_num_of_something("2G","rx_freq")*testconfig.get_num_of_something("2G","rx_rate")*testconfig.get_num_of_something("2G","rx_chain")
                if(testwhat == "jiaozhun"):
                    return num_2G
                elif(testwhat == "pinpian_jiaozhun"):
                    return 1+num_2G
                elif(testwhat == "tx_ht20"):
                    line = 1+testconfigxml.get_num_of_5g_tx_ht20_freq()
                    # line = 1+testconfig.get_num_of_something("5G","tx_ht20_freq")*testconfig.get_num_of_something("5G","tx_ht20_rate")*testconfig.get_num_of_something("5G","tx_ht20_chain")
                    return line+num_2G
                elif(testwhat == "tx_ht40"):
                    line = 1+testconfigxml.get_num_of_5g_tx_ht20_freq()+testconfigxml.get_num_of_5g_tx_ht40_freq()
                    # line = 1+testconfig.get_num_of_something("5G","tx_ht20_freq")*testconfig.get_num_of_something("5G","tx_ht20_rate")*testconfig.get_num_of_something("5G","tx_ht20_chain")+\
                    #      testconfig.get_num_of_something("5G","tx_ht40_freq")*testconfig.get_num_of_something("5G","tx_ht40_rate")*testconfig.get_num_of_something("5G","tx_ht40_chain")
                    return line+num_2G
                elif(testwhat == "rx"):
                    line = 1+testconfigxml.get_num_of_5g_tx_ht20_freq()+testconfigxml.get_num_of_5g_tx_ht40_freq()+testconfigxml.get_num_of_5g_rx_freq()
                    # line = 1+testconfig.get_num_of_something("5G","tx_ht20_freq")*testconfig.get_num_of_something("5G","tx_ht20_rate")*testconfig.get_num_of_something("5G","tx_ht20_chain")+\
                    #      testconfig.get_num_of_something("5G","tx_ht40_freq")*testconfig.get_num_of_something("5G","tx_ht40_rate")*testconfig.get_num_of_something("5G","tx_ht40_chain")+\
                    #      testconfig.get_num_of_something("5G","rx_freq")*testconfig.get_num_of_something("5G","rx_rate")*testconfig.get_num_of_something("5G","rx_chain")
                    return line+num_2G

    def protest(self):
        global dll
        global freq_2g_ht20, rate_2g_ht20, chain
        global debug
        global rootPath
        #global ht20_2g_setting, ht40_2g_setting, ht20_5g_setting, ht40_5g_setting
        global path_loss_2g, path_loss_5g
        # global how_to_do_test
        global tn
        global jiaozhun_result
        global fail_mssage
        global test_result_fail
        # jiaozhun_result = 0
        # set_jiaozhun_result(0)
        myip = self.ip
        testconf = TestConf()
        testconfxml = TestConfigxml()
        art_jiaozhun = ART_jiaozhun()
        myconf = MyConf()
        fail_stop_flag = myconf.get_fail_stop()
        #获取配置信息 2G和5G
        power_limit_ht20_2G = string.atof(testconfxml.get_2g_power_limit_ht20())
        power_limit_ht40_2G = string.atof(testconfxml.get_2g_power_limit_ht40())
        power_limit_ht20_5G = string.atof(testconfxml.get_5g_power_limit_ht20())
        power_limit_ht40_5G = string.atof(testconfxml.get_5g_power_limit_ht40())

        #self.do_get_setting()
        #测试模式不同选择不同的端口号。
        try:

            if(test_mode == 5):
                time.sleep(2)
                tn = telnetlib.Telnet(myip, port=testconf.get_5g_default_port())
            elif(test_mode == 2):
                time.sleep(2)
                tn = telnetlib.Telnet(myip, port=testconf.get_2g_default_port())

        except Exception as e:
            self.emit(SIGNAL("result_fail"))
            jiaozhun_result == 8888
            set_test_result(8888)
            fail_mssage = 'telnet 失败！'
            self.printstr(u'抱歉，测试出错了！登录端口失败！\n',QColor(255, 0, 0, 220))
            self.printstr(u"error({0}): {1}\n".format(e.errno, e.strerror),QColor(255, 0, 0, 220))
            return

        if(test_mode == 2):
            #热身

            self.set_mac_command()


            #校准

            if(testconf.get_is_or_not_jiaozhun() == '1'):
                if testconf.get_use_art2() == '1':
                    # 修改art配置文件。2g和5g都进行校准
                    art_jiaozhun.all_to_jiaozhun()

                    time_start_jiaozhun = time.time()
                    this_jiaozhun_item = 0
                    self.emit(SIGNAL("jiaozhuning1"))
                    print  'use  art'

                    # 修改art线损文件
                    art_xiansun = ART_xiansun()
                    art_xiansun.change_ART_xiansun()
                    # 修改art配置文件
                    this_version = Version_ini()
                    this_version.change_ART2_config_folder()

                    print 'change pathloss ok'
                    old_path =  os.getcwd()
                    print old_path
                    os.chdir(old_path+'\\ART2\\art2_ver_4_9_844_release\\bin')
                    self.printstr('\n  ----use ART2 begin-----\n',QColor(0, 0, 0, 110))
                    print os.getcwd()
                    popen = subprocess.Popen(["cart.exe"], stdout=subprocess.PIPE)
                    # popen = subprocess.Popen(['ping '], stdout=subprocess.PIPE)
                    # print rootPath

                    # popen = subprocess.Popen([ "D:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe"], stdout=subprocess.PIPE)

                    while True:
                        self.emit(SIGNAL("jiaozhuning2"))

                        buff = popen.stdout.readline()
                        # print buff
                        # if '4003' in buff:
                        self.printstr(buff+'\n',QColor(0, 0, 0, 220))

                        self.emit(SIGNAL("jiaozhuning3"))

                        if 'Device Type:      20-Y7555-H1-A_2' in buff:
                            this_jiaozhun_item = 2
                        temp_message = '\n2G Calibration  failed!!!\n'
                        if this_jiaozhun_item == 2:
                            temp_message = '\n5G Calibration failed!!!\n'



                        time_end_jiaozhun = time.time()

                        time_jiaozhun = time_end_jiaozhun - time_start_jiaozhun
                        if time_jiaozhun > 120:
                            self.printstr('\n  ----use ART2 end-----\n',QColor(0, 0, 0, 110))
                            os.chdir(old_path)
                            jiaozhun_result = 1
                            test_result_fail = 8888
                            fail_mssage += temp_message
                            print os.getcwd()
                            popen.kill()
                            break

                        if buff == '' and popen.poll() is not None:
                            self.printstr('\n  ----use ART2 end-----\n',QColor(0, 0, 0, 110))
                            os.chdir(old_path)
                            print os.getcwd()
                            break
                        if 'LP_VsaDataCapture() returned error: 8' in buff:
                            os.chdir(old_path)
                            jiaozhun_result = 1
                            test_result_fail = 8888
                            fail_mssage += temp_message
                            popen.kill()
                            break
                        if 'Test Error        FAIL' in buff:
                            os.chdir(old_path)
                            jiaozhun_result = 1
                            test_result_fail = 8888
                            popen.kill()
                            fail_mssage += temp_message
                            break

                        if 'NO CARD Loaded    FAIL' in buff:
                            os.chdir(old_path)
                            test_result_fail = 8888
                            jiaozhun_result = 1
                            popen.kill()
                            fail_mssage += temp_message
                            break
                else:

                    self.load_ref_file_art()
                    self.load_ctl_table_art()
                    self.load_trg_pwr_art();
                    self.load_cal_scheme_art()
                    self.load_alpha_therm_art()

                    cmd_5 = "load"
                    cmd_6 = "hello"
                    self.telnet_exec_command(u"校准命令——load", cmd_5, "CONTROL DONE "+cmd_5, 1, 0,1)
                    self.telnet_exec_command(u"校准命令——hello", cmd_6, "CONTROL DONE "+cmd_6, 1, 0,1)


                    cmd_0="get txmask;"
                    self.telnet_exec_command(u"校准命令——get txmask", cmd_0, "CONTROL DONE "+cmd_0, 1, 0,1)

                    self.printstr('\n\n****************  2G warmup 热身 ****************\n',QColor(0, 0, 0, 110))

                    if testconf.get_jiaozhun_warmup() == '1':
                        self.warmup("2412")
                    cmd = "sw a=BB_heavy_clip_1.heavy_clip_enable; v=0;"
                    self.telnet_exec_command(u"校准后——sw",cmd,"CONTROL DONE ", 1, 0, 1)
                    self.loop_jiaozhun(["2412","2437","2472"],["1","2"])
                    self.after_jiaozhun()
            if jiaozhun_result == 0:
                line = self.get_table_line_num("2G","jiaozhun")
                self.emit(SIGNAL("table_color"), line, "success")
            else:
                line = self.get_table_line_num("2G","jiaozhun")
                self.emit(SIGNAL("table_color"), line, "fail")
                return
            #time.sleep(1)
            if(testconf.get_is_or_not_jiaozhun() =='1'):

                if testconf.get_use_art2() == '1':
                    self.printstr('\n  ----pinpian jiaozhun  end-----\n',QColor(0, 0, 0, 110))
                else:
                    # cmd_1="tx attenuation=0;carrier=1;txgain=10;chain=1;f=2437;xtalcal=1;"
                    # self.telnet_exec_command(u"校准命令——频偏校准", cmd_1, "CONTROL DONE", 1, 1,1)

                    self.loop_pinpian_jiaozhun()
                    cmd_2="set FeatureEnable.TuningCaps=1;"
                    self.telnet_exec_command(u"校准命令——频偏校准", cmd_2, "CONTROL DONE", 1, 0,1)

                    cmd_3 = "commit"
                    self.telnet_exec_command(u"commit",cmd_3,"CONTROL DONE ", 1, 0, 1)


            line = self.get_table_line_num("2G","pinpian_jiaozhun")
            self.emit(SIGNAL("table_color"), line, "success")

            self.telnet_exec_command(u"hello","hello","CONTROL DONE "+"hello", 1, 0, 1)
            if(testconf.get_is_or_not_jiaozhun() == '0'):
                self.printstr('\n\n****************   2G warmup  ****************\n\n',QColor(0, 0, 0, 110))

                self.warmup("2412")
            # print rootPath
            # os.chdir(rootPath)
            self.printstr('\n\n****************  2G HT20 start  ****************\n',QColor(0, 0, 0, 110))
            tx_ht20_freq = testconfxml.get_2g_tx_ht20_freq()
            tx_ht20_rate = []
            tx_ht20_chain = []
            time.sleep(0.5)
            pre_line = self.get_table_line_num("2G","pinpian_jiaozhun")
            if testconf.get_run_2g_tx() == '1':
                self.loop_tx(tx_ht20_freq, tx_ht20_rate, tx_ht20_chain, power_limit_ht20_2G,pre_line)
            if fail_stop_flag == '1':
                if test_result_fail != 0:
                    return

            self.printstr('\n\n****************  2G HT40 start ****************\n',QColor(0, 0, 0, 110))
            tx_ht40_freq = testconfxml.get_2g_tx_ht40_freq()
            tx_ht40_rate = []
            tx_ht40_chain = []
            pre_line = self.get_table_line_num("2G","tx_ht20")
            if testconf.get_run_2g_tx() == '1':
                self.loop_tx(tx_ht40_freq, tx_ht40_rate, tx_ht40_chain, power_limit_ht40_2G,pre_line)
            if fail_stop_flag == '1':
                if test_result_fail != 0:
                    return

            self.printstr('\n\n****************  2G rx start  ****************\n',QColor(0, 0, 0, 110))
            rx_freq = testconfxml.get_2g_tx_rx_freq()
            rx_rate = []
            rx_chain =[]
            pre_line = self.get_table_line_num("2G","tx_ht40")
            if testconf.get_run_2g_rx() == '1':
                self.loop_rx(rx_freq, rx_rate, rx_chain, pre_line)
            if fail_stop_flag == '1':
                if test_result_fail != 0:
                    self.printstr("\n\n\nfail\n",QColor(0, 0, 0, 110))
                    return
            if how_to_do_test == '0':
                if test_result_fail == 0:
                    self.printstr("\n\n\npass\n",QColor(0, 0, 0, 110))
                    self.emit(SIGNAL("result_success"))
                else:
                    self.emit(SIGNAL("result_fail"))
                    self.printstr("\n\n\nfail\n", QColor(0, 0, 0, 110))

        elif(test_mode == 5):
            print str(get_test_result())+" #### test result####"
            cmd_load_devid="load devid=3c;memory=flash;"
            self.telnet_exec_command(u"加载 load", cmd_load_devid, "CONTROL DONE ", 0, 0,1)


            if testconf.get_is_or_not_jiaozhun() =='1':

                if testconf.get_use_art2() == '1':
                    # if jiaozhun_result ==1:
                    #     return
                    self.printstr('\n ----5g jiaozhun end--- \n\n\n',QColor(0, 0, 0, 110))
                else:
                    self.load_ref_file_art()
                    self.load_ctl_table_art()
                    self.load_trg_pwr_art()
                    self.load_cal_scheme_art()
                    self.load_alpha_therm_art()

                    # cmd_0="get txmask;"
                    # # cmd_1="sw a=BB_heavy_clip_1.heavy_clip_enable;v=0"
                    # self.telnet_exec_command(u"校准命令", cmd_0, "CONTROL DONE", 1, 1,1)
                    # self.telnet_exec_command(u"校准命令", cmd_1, "CONTROL DONE", 1, 1,1)
                    cmd_get_txmask="get txmask;"
                    self.telnet_exec_command(u"校准命令", cmd_get_txmask, "CONTROL DONE", 1, 0,1)

                    self.printstr('\n\n****************  5G warmup  ****************\n',QColor(0, 0, 0, 110))
                    if testconf.get_jiaozhun_warmup_5G() == '1':
                        self.warmup("5180")

                    cmd_sw = "sw a=BB_heavy_clip_1.heavy_clip_enable; v=0;"
                    self.telnet_exec_command(u"校准",cmd_sw,"CONTROL DONE ", 1, 0, 1)

                    self.loop_jiaozhun(["5180","5240","5320","5520","5640","5745","5785","5825"],["1","2"])
                    #校准完后
                    self.after_jiaozhun()

            line = self.get_table_line_num("5G","jiaozhun")
            self.emit(SIGNAL("table_color"), line, "success")

            if testconf.get_is_or_not_jiaozhun()=='1':

                if testconf.get_use_art2() == '1':
                    self.printstr('\n  ----5g pinpian jiaozhun end ----\n',QColor(0, 0, 0, 110))
                else:
                    cmd_sw_a_v="sw a=bb_b0_BB7.DACFULLSCALE;v=0x1;"
                    cmd_reset="reset f = 5180;"
                    self.telnet_exec_command(u"频偏校准之前", cmd_sw_a_v, "CONTROL DONE ", 1, 0,1)
                    self.telnet_exec_command(u"频偏校准之前", cmd_reset, "CONTROL DONE ", 1, 0,1)
                    self.loop_pinpian_jiaozhun()

                    cmd_set_featureEnable = "set FeatureEnable.TuningCaps=1;"
                    cmd_a_bb_b0 = "sc a=bb_b0_BB7.DACFULLSCALE;"
                    cmd_reset_last = "reset f=5180"

                    self.telnet_exec_command(u"频偏校准之后",cmd_set_featureEnable,"CONTROL DONE "+cmd_set_featureEnable, 1, 0, 1)
                    self.telnet_exec_command(u"频偏校准之后",cmd_a_bb_b0,"CONTROL DONE "+cmd_a_bb_b0, 1, 0, 1)
                    self.telnet_exec_command(u"频偏校准之后",cmd_reset_last,"CONTROL DONE "+cmd_reset_last, 1, 0, 1)

                    cmd_commit = "commit"
                    self.telnet_exec_command(u"保存",cmd_commit,"CONTROL DONE "+cmd_commit, 1, 0, 1)
            line = self.get_table_line_num("5G","pinpian_jiaozhun")
            self.emit(SIGNAL("table_color"), line, "success")

            self.telnet_exec_command(u"hello","hello","CONTROL DONE "+"hello", 1, 0, 1)

            if(testconf.get_is_or_not_jiaozhun() == '0'):
                self.printstr('\n\n****************   5G warmup  ****************\n\n',QColor(0, 0, 0, 110))
                self.warmup("5180")

            self.printstr('\n\n**************** 5GHz ht20 ******************\n',QColor(0, 0, 0, 110))
            tx_ht20_freq = testconfxml.get_5g_tx_ht20_freq()
            tx_ht20_rate = []
            tx_ht20_chain = []
            pre_line = self.get_table_line_num("5G","pinpian_jiaozhun")
            time.sleep(0.5)
            if testconf.get_run_5g_tx() == '1':
                self.loop_tx(tx_ht20_freq, tx_ht20_rate, tx_ht20_chain, power_limit_ht20_5G,pre_line)
            if fail_stop_flag == '1':
                if test_result_fail != 0:
                    return

            self.printstr('\n\n**************** 5GHz ht40****************\n',QColor(0, 0, 0, 110))
            tx_ht40_freq = testconfxml.get_5g_tx_ht40_freq()
            tx_ht40_rate = []
            tx_ht40_chain = []
            pre_line = self.get_table_line_num("5G","tx_ht20")
            if tx_ht40_freq!="" and tx_ht40_freq is not None:
                if testconf.get_run_5g_tx() == '1':
                    self.loop_tx(tx_ht40_freq, tx_ht40_rate, tx_ht40_chain, power_limit_ht40_5G,pre_line)
                if fail_stop_flag == '1':
                    if test_result_fail != 0:
                        return

            self.printstr('\n\n**************** 5G rx  ****************\n',QColor(0, 0, 0, 110))
            rx_freq = testconfxml.get_5g_tx_rx_freq()
            rx_rate = []
            rx_chain = []
            pre_line = self.get_table_line_num("5G","tx_ht40")
            if testconf.get_run_5g_rx() == '1':
                self.loop_rx(rx_freq, rx_rate, rx_chain,pre_line)
            #self.after_rx()
            if fail_stop_flag == '1':
                if test_result_fail != 0:
                    return

    def get_this_mac_address(self):
        import uuid
        node = uuid.getnode()
        mac = uuid.UUID(int = node).hex[-12:]
        return mac


    def save_all_to_data_base(self,rate):
        myconf = MyConf()
        testconf = TestConf()
        data_base = DataBaseOP()

        global this_mac
        snStr = myconf.get_sn_num()

        jiaozhun_str = testconf.get_is_or_not_jiaozhun()

        # a = '1'
        station = "test"
        # prevoius_result = data_base.getAPLatestStatusBySN(snStr)
        # if prevoius_result is None:
        #     prevoius_result = ''
        if jiaozhun_str == '0':
            # a = '2'
            station = "retest"
        if test_result_fail == 0:
            # status = prevoius_result + a+"Y,"
            status =  "pass"
        else:
            # status = prevoius_result + a + 'N,'
            status = 'fail'
        userName = myconf.get_username()
        pcMac = self.get_this_mac_address()
        data_base.setAPStatusBySn(snStr,status,userName,pcMac,station,rate)

    def telnet_exec_command(self, name, cmd, finish, print_a, start, read_s = 1):
        global fail_mssage
        global system_halted
        global test_result_fail
        s = ''
        try:
            tn.write(cmd+"\n")
            if(start != 0):
                # time.sleep(0.1)
                tn.write("START\n")

        except Exception as e:
            self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
            self.printstr('[ERR]\n',QColor(255, 0, 0, 220))
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            self.printstr(u"error: {0}\n\n".format(e),QColor(255, 0, 0, 220))
            return
        if(read_s != 0):
            print "read_until  "+finish +'\n'
            try:
                s = tn.read_until(finish,20)

                print "read until " +finish + 'ok ! \n'
            except Exception as e:
                fail_mssage += " the system halted !!! \n"
                system_halted = 1
                test_result_fail = 8888
                self.printstr(fail_mssage,QColor(255, 0, 0, 220))
                self.emit(SIGNAL("result_fail"))
            print s
        if(print_a != 0):
            self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
            self.printstr('[OK]\n',QColor(0, 255, 0, 220))
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            # if(read_s != 0):
            #     self.printstr(s+'\n', QColor(139, 101, 8, 255))
        return s

    def telnet_exec_command_t(self, name, cmd, finish, print_a, start, read_s = 1, t=0):
        global fail_mssage
        global system_halted
        global test_result_fail
        s = ''
        try:
            tn.write(cmd+"\n")
            if(start != 0):
                if(time != 0):
                    time.sleep(0.05)
                tn.write("START\n")
                if(time != 0):
                    time.sleep(t)
        except Exception as e:
            self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
            self.printstr('[ERR]\n',QColor(255, 0, 0, 220))
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            self.printstr(u"error: {0}\n\n".format(e),QColor(255, 0, 0, 220))
            return
        if(read_s != 0):
            try:
                print "read_until  " + finish + '\n'
                s = tn.read_until(finish,10)
                print "read_until  " + finish+ "   ok! \n"
            except Exception as e:
                fail_mssage += " the system halted !!! \n"
                system_halted = 1
                test_result_fail = 8888
                self.printstr(fail_mssage,QColor(255, 0, 0, 220))
                self.emit(SIGNAL("result_fail"))
        if(print_a != 0):
            self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
            self.printstr('[OK]\n',QColor(0, 255, 0, 220))
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            if(read_s != 0):
                self.printstr(s+'\n', QColor(139, 101, 8, 255))
        return s

    def telnet_exec_command_start_3(self, name, cmd, finish):
        global dll
        try:
            tn.write(cmd+"\n")
            #dll = cdll.LoadLibrary('IQmeasure.dll');
            ret = dll.LP_SetFrameCnt(c_int(5))
            # self.printstr(str(ret)+'\n',QColor(0, 0, 0, 110))
            while(dll.LP_TxDone()):
                continue
            tn.write("START\n")
        except Exception as e:
            self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
            self.printstr('[ERR]\n',QColor(255, 0, 0, 220))
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            self.printstr(u"error: {0}\n\n".format(e),QColor(255, 0, 0, 220))
            return
        self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
        self.printstr('[OK]\n',QColor(0, 255, 0, 220))
        self.printstr(cmd+'\n',QColor(0, 0, 0, 110))

    def telnet_exec_stop(self, finish, print_a = 0):
        global fail_mssage
        global system_halted
        global test_result_fail
        try:
            tn.write("STOP\n")
            print "stop"
        except Exception as e:
            self.printstr('[ERR]\n',QColor(255, 0, 0, 220))
            return
        try:
            print "read_until  " +finish + '\n'

            s = tn.read_until(finish,10)

            print "read_until  " + finish + "  ok! \n"
        except Exception as e:

            fail_mssage += " the system halted !!! \n"
            system_halted = 1
            test_result_fail = 8888
            self.printstr(fail_mssage,QColor(255, 0, 0, 220))
            self.emit(SIGNAL("result_fail"))
        if(print_a != 0):
            self.printstr(s+'\n', QColor(139, 101, 8, 255))
        return s

    def telnet_exec_command_start_noread(self, name, cmd, finish):
        try:
            tn.write(cmd+"\n")
            tn.write("START\n")
        except Exception as e:
            self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
            self.printstr('[ERR]\n',QColor(255, 0, 0, 220))
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            self.printstr(u"error: {0}\n\n".format(e),QColor(255, 0, 0, 220))
            return
        self.printstr(name.ljust(40+len(name)-total_width(name)),QColor(0, 0, 0, 235))
        self.printstr('[OK]\n',QColor(0, 255, 0, 220))
        self.printstr(cmd+'\n',QColor(0, 0, 0, 110))

    # def load_set_command(self):
    #
    #     #加载配置文件
    #     if(test_mode == 2):
    #         self.printstr('\n\n###########  Loading 2G setting  ###############\n',QColor(0, 0, 0, 110))
    #         f = open("test_cmd_2g.txt")
    #     elif(test_mode == 5):
    #         self.printstr('\n\n###########  Loading 5G setting  ###############\n',QColor(0, 0, 0, 110))
    #         f = open("test_cmd_5g.txt")
    #     line = f.readline()
    #     while line:
    #         line = f.readline()
    #         if(len(line) == 1 or len(line) == 0):continue
    #         cmd = line.replace("\n","")#替换换行符。
    #         cmd = line.replace(";","")
    #         self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 0, 0, 1)

    def set_mac_command(self):
    #         load cal=flash;
    #         set mac=00:11:22:33:44:55;
    #         load
    #         hello
        cmd_1="load devid=3f;memory=flash"
        cmd_2 = "set mac=00:11:22:33:44:55"
        cmd_3 = "load"
        cmd_4 = "hello"
        self.telnet_exec_command(u"加载——art文件之前", cmd_1, "CONTROL DONE", 1, 0,1)
        # self.telnet_exec_command(u"加载——art文件之前", cmd_2, "CONTROL DONE", 1, 1,1)
        # self.telnet_exec_command(u"加载——art文件之前", cmd_3, "CONTROL DONE", 1, 1,1)
        self.telnet_exec_command(u"加载——art文件之前", cmd_4, "CONTROL DONE", 1, 0,1)


    def load_ref_file_art(self):
        if test_mode==2:
            self.printstr('\n\n###########  Loading 2G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_2g_art/ref_file.art")
        else:
            self.printstr('\n\n###########  Loading 5G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_5g_art/ref_file.art")
        line = f.readline()
        while line:
            line = f.readline()
            # print line
            if(len(line)==1 or len(line)== 0 ):continue
            elif "#" in line:continue
            elif "assign" in line:continue
            else:
                print line
                cmd = line.replace("\n","")
                if "i=$inst;" in cmd :
                    cmd = cmd.replace("i=$inst;", "")
                self.telnet_exec_command(u"加载——art文件", cmd, "CONTROL DONE", 0, 0,1)

    def load_ctl_table_art(self):
        if test_mode==2:
            self.printstr('\n\n###########  Loading 2G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_2g_art/ctl_table.art")
        else:
            self.printstr('\n\n###########  Loading 5G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_5g_art/ctl_table.art")
        line = f.readline()
        while line:
            line = f.readline()
            if(len(line)==1 or len(line)== 0 ):continue
            elif "assign" in line:continue
            elif "#" in line:continue
            else:
                print line

                cmd = line.replace("\n","")
                if "i=$inst;" in cmd :
                    cmd = cmd.replace("i=$inst;", "")
                self.telnet_exec_command(u"加载——art文件", cmd, "CONTROL DONE", 0,0,1)
    def load_trg_pwr_art(self):
        if test_mode==2:
            self.printstr('\n\n###########  Loading 2G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_2g_art/trg_pwr.art")
        else:
            self.printstr('\n\n###########  Loading 5G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_5g_art/trg_pwr.art")
        line = f.readline()
        while line:
            line = f.readline()
            print line
            if(len(line)==1 or len(line)== 0 ):continue
            elif "#" in line:continue
            elif "assign" in line:continue
            else:
                print line
                cmd = line.replace("\n","")
                if "i=$inst;" in cmd :
                    cmd = cmd.replace("i=$inst;", "")
                self.telnet_exec_command(u"加载——art文件", cmd, "CONTROL DONE", 0, 0,1)

    def load_cal_scheme_art(self):
        if test_mode==2:
            self.printstr('\n\n###########  Loading 2G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_2g_art/cal_scheme.art")
        else:
            self.printstr('\n\n###########  Loading 5G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_5g_art/cal_scheme.art")
        line = f.readline()
        while line:
            line = f.readline()
            if(len(line)==1 or len(line)== 0 ):continue
            elif "#" in line:continue
            elif "assign" in line:continue
            else:
                print line
                cmd = line.replace("\n","")
                if "i=$inst;" in cmd :
                    cmd = cmd.replace("i=$inst;", "")
                self.telnet_exec_command(u"加载——art文件", cmd, "CONTROL DONE", 0, 0,1)
    def load_alpha_therm_art(self):
        if test_mode==2:
            self.printstr('\n\n###########  Loading 2G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_2g_art/alpha_therm.art")
        else:
            self.printstr('\n\n###########  Loading 5G setting for ref_file.art  ###############\n',QColor(0, 0, 0, 110))
            f = open("set_5g_art/alpha_therm.art")
        line = f.readline()
        while line:
            line = f.readline()
            if(len(line)==1 or len(line)== 0 ):continue
            elif "#" in line:continue
            elif "assign" in line:continue
            else:
                print line
                cmd = line.replace("\n","")
                if "i=$inst;" in cmd :
                    cmd = cmd.replace("i=$inst;", "")
                self.telnet_exec_command(u"加载——art文件", cmd, "CONTROL DONE", 0, 0,1)



    def load_set_command_all(self):
        f = open("test_cmd_2g.txt")
        line = f.readline()
        while line:
            line = f.readline()
            if(len(line) == 1 or len(line) == 0):continue
            cmd = line.replace("\n","")
            self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 0, 0, 1)
        f.close()
        f = open("test_cmd_5g.txt")
        line = f.readline()
        while line:
            line = f.readline()
            if(len(line) == 1 or len(line) == 0):continue
            cmd = line.replace("\n","")
            self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 0, 0, 1)
        f.close()

    def t_geterr(self, errcode):
        dll = cdll.LoadLibrary('./IQmeasure.dll');
        pcName = c_char_p('/0'*200)
        pcName = dll.LP_GetErrorString(errcode)
        err = string_at(pcName,200)
        self.printstr(err,QColor(255, 0, 0, 220))
        self.printstr("\n",QColor(255, 0, 0, 220))

    def test_wanip_del(self):
        self.ssh2_exec_command(u"恢复wan口配置：","protest --wanip -del")
        self.ssh2_exec_command_poor('''sed -n "/config interface 'wan'/{p;:a;n;/config/q;p;ba;}" /etc/config/network''');
        self.emit(SIGNAL("table_color"), 20, "success")

    def test_restore(self):
        self.ssh2_exec_command(u"执行恢复出厂默认配置操作：","protest --restore")


    def dll_init(self):
        config = MyConf()
        IQ_connect = config.get_IQ_connect()
        global dll
        dll = cdll.LoadLibrary('./IQmeasure.dll');
        ret = dll.LP_Init(c_int(1),c_int(0));
        if(debug != 0):
            self.printstr("LP_Init:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        ret = dll.LP_InitTester(IQ_connect, c_int(0));
        if(debug != 0):
            self.printstr("LP_InitTester:"+str(ret)+'\n',QColor(0, 0, 0, 110))

    def mask_dll_init(self):
        #加载dll文件
        global mask_dll
        mask_dll = cdll.LoadLibrary('./MaskDll.DLL');

    def dll_getversion(self):
        global dll
        strMa = "/0"*200
        FunPrint  = dll.LP_GetVersion
        FunPrint.argtypes = [c_char_p, c_int]
        nRst = FunPrint(strMa, len(strMa))
        self.printstr(strMa+'\n',QColor(0, 0, 0, 110))

    def dll_setvsa_1(self, rfFreqHz, rfAmplDb, port, extAttenDb = 0, triggerLevelDb = -25, triggerPreTime = 10e-6, dFreqShiftHz = 0.0, dTriggerGapTime = 6e-6):
        ret = dll.LP_SetVsa(c_double(rfFreqHz*1e6), rfAmplDb, c_int(port), c_double(extAttenDb), c_double(triggerLevelDb), c_double(triggerPreTime), c_double(dFreqShiftHz), c_double(dTriggerGapTime));
        # self.printstr("ret:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(ret != 0):
            self.t_geterr(ret)

    def dll_setvsa(self, rfFreqHz, rfAmplDb, port, extAttenDb = 0, triggerLevelDb = -25, triggerPreTime = 10e-6, dFreqShiftHz = 0.0, dTriggerGapTime = 6e-6):
        ret = dll.LP_SetVsa(c_double(rfFreqHz*1e6), c_double(rfAmplDb), c_int(port), c_double(extAttenDb), c_double(triggerLevelDb), c_double(triggerPreTime), c_double(dFreqShiftHz), c_double(dTriggerGapTime));
        # self.printstr("ret:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(ret != 0):
            self.t_geterr(ret)

    def str_find_tp(self, ttp_str):
        global test_result_fail
        global system_halted
        global fail_mssage
        s = ttp_str.split("||")
        try:
            x = s[3]
        except:
            fail_mssage += " gettp error , please check and reTest !!! \n"
            system_halted = 1
            test_result_fail = 8888
            self.printstr(fail_mssage,QColor(255, 0, 0, 220))
            self.emit(SIGNAL("result_fail"))
        return x

    def create_command_tx(self, freq, rate, chain, tp):
        s = '''
        if(test == "power"):
            cmd_tx = "tx f="+freq+";ir=0;gi=0;txch="+chain+";rxch=7;pc=1000000;pl=4000;bc=1;retry=0;att=0;iss=0;stat=3;ifs=1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;duc=99;ht40=2;r="+rate+";tp="+tp+";"
        elif(test == "evm.ppm" and string.atoi(freq)>5000):
            cmd_tx = "tx f="+freq+";ir=0;gi=0;txch="+chain+";rxch=7;pc=1000000;pl=1500;bc=1;retry=0;att=0;iss=0;stat=3;ifs=1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;ht40=2;r="+rate+";tp="+tp+";"
        else:
            cmd_tx = "tx f="+freq+";ir=0;gi=0;txch="+chain+";rxch=7;pc=1000000;pl=4000;bc=1;retry=0;att=0;iss=0;stat=3;ifs=1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;ht40=2;r="+rate+";tp="+tp+";"
        '''
        cmd_tx = "tx f="+freq+";ir=0;gi=0;txch="+chain+";rxch=7;pc=1000000;pl=4000;bc=1;retry=0;att=0;iss=0;stat=3;ifs=1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;duc=99;agg=1;ht40=2;r="+rate+";tp="+tp+";"
        return cmd_tx

    def get_lost_from_xiansunini(self,this_freq, chain):
        xiansunini = Xian_Sun_ini()
        if string.atoi(this_freq) <5000:

            return xiansunini.get_xiansun_ini(this_freq, chain, "2G")
        else:
            return xiansunini.get_xiansun_ini(this_freq, chain, "5G")

    def get_lost(self, this_freq, chain):
        testconf = TestConf()
        testconfxml = TestConfigxml()
        tree = testconfxml.read_xml()
        tests = testconfxml.get_all_test(tree)
        lost_str = ""
        if(string.atoi(this_freq)<5000):#2g的
            # index = testconf.get_2G_freq_for_lost().split(",").index(freq)#频率
            # lost_str = testconf.get_2G_lost_for_freq().split(",")[index]#线损
            #获得当前频率的线损
            # key = 当前频率的freq
            #获得所有线损的freq

            for test in tests:

                if test.get('name') == '2G':
                    freq_for_losts = testconfxml.get_freq_for_lost(test)
                    freqs = testconfxml.get_all_freq(freq_for_losts)
                    for freq in freqs:
                        val = freq.find('val').text
                        lost = freq.find('lost').text
                        if val == this_freq:
                            lost_str = lost.split(',')[int(chain)-1]

            lost = string.atof(lost_str)
            return lost
        else:#5g的
            # index = testconf.get_5G_freq_for_lost().split(",").index(this_freq)
            # lost_str = testconf.get_5G_lost_for_freq().split(",")[index]
            for test in tests:
                if test.get('name') == '5G':
                    freq_for_losts = testconfxml.get_freq_for_lost(test)
                    freqs = testconfxml.get_all_freq(freq_for_losts)
                    for freq in freqs:
                        val = freq.find('val').text
                        lost = freq.find('lost').text
                        if val == this_freq:
                            lost_str = lost.split(',')[int(chain)-1]

            lost = string.atof(lost_str)
            return lost

    def get_powerlevel(self, this_freq, this_rate):
        testconf = TestConf()
        lost_str = ""
        level_str = ""
        testconfxml = TestConfigxml()
        tree = testconfxml.read_xml()
        tests = testconfxml.get_all_test(tree)

        if(string.atoi(this_freq)<5000):
            #index = testconf.get_2G_rate_for_powerlevel().split(",").index(rate)
            #level_str = testconf.get_2G_powerlevel_for_rate().split(",")[index]
            # index = testconf.get_something("2G","rate_for_powerlevel").split(",").index(rate)
            # level_str = testconf.get_something("2G","powerlevel_for_rate").split(",")[index]
            for test in tests:
                if test.get('name') == "2G":
                    power_rate = testconfxml.get_power_rate(test)
                    pr_items = testconfxml.get_all_pr_items(power_rate)
                    for pr_item in pr_items:
                        level = pr_item.find('level').text
                        rate = pr_item.find('rate').text
                        if level == this_rate:
                            level_str = rate
            the_level = string.atof(level_str)
            print the_level
            return the_level
        else:
            # index = testconf.get_something("5G","rate_for_powerlevel").split(",").index(rate)
            # level_str = testconf.get_something("5G","powerlevel_for_rate").split(",")[index]

            for test in tests:
                if test.get('name') == "5G":
                    power_rate = testconfxml.get_power_rate(test)
                    pr_items = testconfxml.get_all_pr_items(power_rate)
                    for pr_item in pr_items:
                        level = pr_item.find('level').text
                        rate = pr_item.find('rate').text
                        if level == this_rate:
                            level_str = rate

            the_level = string.atof(level_str)
            return the_level

    def loop_tx(self, freq_all, rate_all, chain_all, setting_limit, pre_line=None):
        testconfxml = TestConfigxml()
        myconf = MyConf()
        testconf = TestConf()

        loop_tx_sleep = string.atof(testconf.get_loop_tx_sleep())
        loop_capture = string.atoi(testconf.get_loop_capture())
        fail_stop_flag = myconf.get_fail_stop()
        global capture_time
        global tx_evm_limit
        global test_result_fail
        #global txppm_limit
        global dll
        global mask_dll
        result = 0
        freq_val_list = []
        #frea_all={(key:value),}
        # freq_val_list = freq_all.values()
        global fail_mssage


        sp_line = pre_line
        for i in range(len(freq_all)):
            for key, freq in freq_all[i].items():
                rate_this = testconfxml.get_rate_this(key)
                chain_this = testconfxml.get_chain_this(key)
                for rate in rate_this:
                    self.emit(SIGNAL("testing3"))
                    for chain in chain_this:
                        self.emit(SIGNAL("testing1"))
                        this_freq_fail_mssage = "*** "+freq+" * "+ rate+" * "+chain+" ***\n"
                        testconf = TestConf()
                        d_type = self.rate_to_type(rate)
                        result = 0
                        if(string.atoi(freq)<5000):
                            #获得2G配置文件信息
                            txppm_limit = string.atof(testconfxml.get_2g_ppm_limit())
                            #txppm_limit = testconf.get_2G_ppm_limit()
                        else:
                            txppm_limit = string.atof(testconfxml.get_5g_ppm_limit())
                            # txppm_limit = testconf.get_5G_ppm_limit()
                        if(sp_line!=None):
                            sp_line = sp_line+1#行标加1，下一行
                        #添加一行测试项
                        self.printstr("\n\n########## No: "+str(sp_line+1)+' ########## '+"frequency: "+freq+' #### rate:'+rate+ ' #### chain: ' + chain+' ####\n',QColor(0, 0, 0, 110))
                        #index_str = freq+"_"+rate+"_"+chain
                        #if(debug != 0):
                        #    self.printstr("freq:"+freq+",rate:"+rate+","+"chain:"+chain+'\n',QColor(0, 0, 0, 110))

                        cmd_gettp = "gettp f="+freq+"; r="+rate+";"
                        ttpstr = self.telnet_exec_command(u"测试",cmd_gettp,"CONTROL DONE "+cmd_gettp, 0, 0, 1)
                        # self.printstr("ttpstr:"+ttpstr+'\n',QColor(0, 0, 0, 110))
                        tp = self.str_find_tp(ttpstr)
                        self.printstr("Target Power:        "+tp+'\n',QColor(0, 0, 0, 110))

                        stand_evm = tx_evm_limit[rate]
                        # self.printstr("stand_evm:"+str(stand_evm)+'\n',QColor(0, 0, 0, 110))

                        cmd = self.create_command_tx(freq, rate, chain, tp)
                        if(debug != 0):
                            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))

                        self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 0, 1, 0)

                        lost = self.get_lost_from_xiansunini(freq,chain)

                        if(rate == "f0" or rate == "f7" or rate == "vf0" or rate== "vf9"):
                            if d_type == "80211ac" or d_type =="80211ag" or d_type =="80211n":
                                self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+10-lost, 2)
                            else:
                                self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+4-lost, 2)
                        else:
                            if d_type == "80211ac" or d_type =="80211ag"or d_type =="80211n":
                                self.dll_setvsa(string.atoi(freq), string.atof(tp)+10-lost, 2)
                            else:
                                self.dll_setvsa(string.atoi(freq), string.atof(tp)+4-lost, 2)

                        time.sleep(loop_tx_sleep)
                        r = rate.lower()
                        time_var = capture_time[r]
                        if(debug != 0):
                            self.printstr("capture time::"+str(time_var)+'\n',QColor(0, 0, 0, 110))


                        temp_list = {}
                        for i in range(loop_capture):
                            ret = dll.LP_VsaDataCapture(c_double(time_var*1e-6), c_int(6), c_double(160e6), c_int(0), c_int(0))

                            dll.LP_GetScalarMeasurement.restype = c_double

                            if(debug != 0):
                                self.printstr("LP_VsaDataCapture:"+str(ret)+'\n',QColor(0, 0, 0, 110))
                            P_av_no_gap_all_dBm_temp = self.get_power_2(rate)

                            temp_list[i] = P_av_no_gap_all_dBm_temp
                            print "..."+str(i)+"..."+str(temp_list[i])
                            if(ret != 0):
                                self.t_geterr(ret)

                        print "sum---"+str(sum(temp_list.values()))
                        print "len---"+str(len(temp_list))
                        P_av_no_gap_all_dBm = round(sum(temp_list.values())/len(temp_list),2)
                        print "_________"+str(P_av_no_gap_all_dBm)+"\n\n"

                        self.emit(SIGNAL("testing2"))
                        #返回8 打印出data capturefaild

                        #time.sleep(200)
                        mask_dll.LP_AnalyzeMASK.restype = c_double
                        #if(test == "special_mask"):
                        if(d_type == "80211n"):
                            if(rate[0]=="f"):
                                self.printstr('11N_40      \n',QColor(0, 0, 0, 110))
                                mymask = mask_dll.LP_AnalyzeMASK(c_int(4))
                                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                                if(mymask <1):
                                    special_mask_result = 0
                                else:
                                    special_mask_result = 1
                            else:
                                self.printstr('IQ_MODE_11N_20       \n',QColor(0, 0, 0, 110))
                                mymask = mask_dll.LP_AnalyzeMASK(c_int(3))
                                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                                if(mymask < 1):
                                    special_mask_result = 0
                                else:
                                    special_mask_result = 1
                        elif(d_type == "80211b"):
                            self.printstr('11B     \n',QColor(0, 0, 0, 110))
                            mymask = mask_dll.LP_AnalyzeMASK(c_int(0))
                            self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                            if(mymask < 1):
                                special_mask_result = 0
                            else:
                                special_mask_result = 1
                        elif(d_type == "80211ag"):
                            if(string.atoi(freq)<5000):
                                self.printstr('11G     \n',QColor(0, 0, 0, 110))
                                mymask = mask_dll.LP_AnalyzeMASK(c_int(1))
                                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                                if(mymask < 1):
                                    special_mask_result = 0
                                else:
                                    special_mask_result = 1
                            else:
                                self.printstr('11A     \n',QColor(0, 0, 0, 110))
                                mymask = mask_dll.LP_AnalyzeMASK(c_int(2))
                                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                                if(mymask < 1):
                                    special_mask_result = 0
                                else:
                                    special_mask_result = 1
                        else:#此为11ac
                            if(rate[1]=='t'):
                                self.printstr('11AC_HT20  \n',QColor(0, 0, 0, 110))
                                mymask = mask_dll.LP_AnalyzeMASK(c_int(5))
                                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                                if(mymask < 1):
                                    special_mask_result = 0
                                else:
                                    special_mask_result = 1
                            elif(rate[1]=='f'):
                                self.printstr('11AC_HT40  \n',QColor(0, 0, 0, 110))
                                mymask = mask_dll.LP_AnalyzeMASK(c_int(7))
                                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                                if mymask < 1:
                                    special_mask_result = 0
                                else:
                                    special_mask_result = 1
                            else:
                                self.printstr('11AC_HT80   \n',QColor(0, 0, 0, 110))
                                mymask = mask_dll.LP_AnalyzeMASK(c_int(7))
                                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                                if mymask < 1:
                                    special_mask_result = 0
                                else:
                                    special_mask_result = 1

                        if d_type == "80211b":
                            ret = dll.LP_Analyze80211b(c_int(1), c_int(0), c_int(1), c_double(8.8e-6), c_double(15.2e-6))

                            if debug != 0:
                                self.printstr("LP_Analyze80211b:"+str(ret)+'\n',QColor(0, 0, 0, 110))

                            if ret != 0:
                                self.t_geterr(ret)
                        elif d_type == "80211ag":
                            ret = dll.LP_Analyze80211ag(c_int(2), c_int(3), c_int(2), c_int(2), c_int(1), c_double(8.8e-6), c_double(15.2e-6))
                            if debug != 0:
                                self.printstr("LP_Analyze80211ag:"+str(ret)+'\n', QColor(0, 0, 0, 110))
                            if ret != 0:
                                self.t_geterr(ret)

                        elif d_type == "80211ac":
                            ret = dll.LP_Analyze80211ac("nxn", c_int(1), c_int(1), c_int(0), c_int(0), c_int(1), c_int(2), "NULL", c_int(0),c_int(1), c_double(8.8e-6), c_double(15.2e-6))#方法要变  analyze80211ac（）
                            if debug != 0:
                                self.printstr("LP_Analyze80211ac:"+str(ret)+'\n', QColor(0, 0, 0, 110))
                            if ret != 0:
                                self.t_geterr(ret)
                        else:
                            ret = dll.LP_Analyze80211n("EWC", "nxn", c_int(1), c_int(1), c_int(0), c_int(1), c_int(1), "", c_int(0), c_int(2), c_double(8.8e-6), c_double(15.2e-6))
                            if debug != 0:
                                self.printstr("LP_Analyze80211n:"+str(ret)+'\n',QColor(0, 0, 0, 110))
                            if ret != 0:
                                self.t_geterr(ret)

                        dll.LP_GetScalarMeasurement.restype = c_double

                        evmAvgAll_0 = dll.LP_GetScalarMeasurement("evmAvgAll", c_int(0))
                        evmAll_0 = dll.LP_GetScalarMeasurement("evmAll", c_int(0))
                        rmsPower_0 = dll.LP_GetScalarMeasurement("rmsPower", c_int(0));
                        pkPower_0 = dll.LP_GetScalarMeasurement("pkPower", c_int(0));
                        freqErrorHz_0 = dll.LP_GetScalarMeasurement("freqErrorHz", c_int(0));
                        freqErr_0 = dll.LP_GetScalarMeasurement("freqErr", c_int(0));
                        clockErr_0 = dll.LP_GetScalarMeasurement("clockErr", c_int(0));
                        symClockErrorPpm_0 = dll.LP_GetScalarMeasurement("symClockErrorPpm", c_int(0));
                        rxRmsPowerDb_4 = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(0));


                        valid_3 = self.get_power_param("valid")
                        P_av_each_burst_3 = self.get_power_param("P_av_each_burst")
                        P_pk_each_burst_3 = self.get_power_param("P_pk_each_burst")
                        P_av_all_3 = self.get_power_param("P_av_all")
                        P_peak_all_3 = self.get_power_param("P_peak_all")
                        P_av_no_gap_all_3 = self.get_power_param("P_av_no_gap_all")
                        P_av_all_dBm_3 = self.get_power_param("P_av_all_dBm")
                        P_peak_all_dBm_3 = self.get_power_param("P_peak_all_dBm")

                        rmsMaxAvgPower_0 = dll.LP_GetScalarMeasurement("rmsMaxAvgPower", c_int(0));
                        rxRmsPowerDb_0 = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(0));
                        rmsMaxAvgPower = dll.LP_GetScalarMeasurement("rmsMaxAvgPower", c_int(1));
                        rxRmsPowerDb = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(1));


                        self.telnet_exec_stop("CONTROL DONE "+cmd)

                        limit = setting_limit
                        meas_pwr = lost + P_av_no_gap_all_dBm
                        self.printstr("Cable Lost:          "+str(lost)+' db         \n',QColor(0, 0, 0, 110))
                        # self.printstr("meas_pwr:"+str(meas_pwr)+'\n',QColor(0, 0, 0, 110))
                        target = string.atof(tp)
                        delta = meas_pwr - target

                        # self.printstr("##############################################\n",QColor(0, 0, 0, 110))
                        self.printstr("Power:               "+str(meas_pwr)+' dbm     \n',QColor(0, 0, 0, 110))
                        self.printstr("delta:               "+str(delta)+'       ',QColor(0, 0, 0, 110))

                        if abs(delta) <= limit:
                            self.printstr('      ('+str(limit) +')                    Power PASS\n',QColor(0, 255, 0, 220))
                            power_result = 0
                        else:
                            this_freq_fail_mssage = this_freq_fail_mssage +'---Power failed---' + str(delta)+'\n'
                            self.printstr('      ('+str(limit) +')                    Power FAIL   ('+str(limit)+')\n',QColor(255, 0, 0, 220))
                            power_result = 1


                        # self.printstr("stand_evm:"+str(stand_evm)+'\n', QColor(0, 0, 0, 110))

                        if d_type == "80211n" or d_type == "80211ac" :
                            if evmAvgAll_0 > float(stand_evm) or evmAvgAll_0 < -99 :
                                this_freq_fail_mssage = this_freq_fail_mssage + '---evm failed---' +str(round(evmAvgAll_0,2))+'\n'
                                self.printstr("EVM:                 "+str(round(evmAvgAll_0,2))+'          ',QColor(255, 0, 0, 220))
                                self.printstr('(' + str(stand_evm) + ')                     EVM FAIL\n',QColor(255, 0, 0, 220))
                                evm_result = 1
                            else:
                                self.printstr("EVM:                 "+str(round(evmAvgAll_0,2))+'           ',QColor(0, 255, 0, 220))
                                self.printstr('(' + str(stand_evm) + ')                     EVM PASS\n',QColor(0, 255, 0, 220))
                                evm_result = 0
                        else:
                            if evmAll_0 > float(stand_evm) or evmAll_0 < -99 :
                                this_freq_fail_mssage = this_freq_fail_mssage + '---evm failed---' +str(round(evmAll_0,2))+'\n'
                                self.printstr("EVM:                 "+str(round(evmAll_0,2))+'          ',QColor(255, 0, 0, 220))
                                self.printstr('(' + str(stand_evm) + ')                     EVM FAIL\n',QColor(255, 0, 0, 220))
                                evm_result = 1
                            else:
                                self.printstr("EVM:                 "+str(round(evmAll_0,2))+'          ',QColor(0, 255, 0, 220))
                                self.printstr('(' + str(stand_evm) + ')                     EVM PASS\n',QColor(0, 255, 0, 220))
                                evm_result = 0

                        # self.printstr("txppm_limit:"+str(txppm_limit)+'\n',QColor(0, 0, 0, 110))

                        if d_type == "80211n" or d_type == "80211ac":

                            if abs(freqErrorHz_0/string.atoi(freq)) > txppm_limit :
                                this_freq_fail_mssage = this_freq_fail_mssage +'---evm_ppm failed---'+'\n'
                                self.printstr("Freq err:            "+str(round(freqErrorHz_0/string.atoi(freq),2))+"    "+"         ("+str(txppm_limit)+")"+'          ',QColor(255, 0, 0, 220))
                                self.printstr('          EVM_ppm FAIL\n',QColor(255, 0, 0, 220))
                                evm_ppm_result = 1
                            else:
                                self.printstr("Freq err:            "+str(round(freqErrorHz_0/string.atoi(freq),2))+"    "+"        ("+str(txppm_limit)+")"+'         ',QColor(0, 255, 0, 220))
                                self.printstr('          EVM_ppm PASS\n',QColor(0, 255, 0, 220))
                                evm_ppm_result = 0

                        else:
                            if abs(freqErr_0/string.atoi(freq)) > txppm_limit:
                                this_freq_fail_mssage = this_freq_fail_mssage +'---evm_ppm failed---'+'\n'
                                self.printstr("Freq err:             "+str(round(freqErr_0/string.atoi(freq),2))+"    "+"         ("+str(txppm_limit)+")"+'          ',QColor(255, 0, 0, 220))
                                self.printstr('          EVM_ppm FAIL\n',QColor(255, 0, 0, 220))
                                evm_ppm_result = 1
                            else:
                                self.printstr("Freq err:             "+str(round(freqErr_0/string.atoi(freq),2))+"    "+"         ("+str(txppm_limit)+")"+'          ',QColor(0, 255, 0, 220))
                                self.printstr('          EVM_ppm PASS\n',QColor(0, 255, 0, 220))
                                evm_ppm_result = 0

                        if special_mask_result != 0:
                            this_freq_fail_mssage = this_freq_fail_mssage+'---mask_result  failed(10%)---\n'
                            self.printstr('           mask_result  failed(10%)\n',QColor(255, 0, 0, 220))

                        self.emit(SIGNAL("testing3"))
                        #判断成功失败
                        if sp_line != None:
                            if special_mask_result == 0 and power_result == 0 and evm_result == 0 and evm_ppm_result == 0:
                                self.emit(SIGNAL("table_color"), sp_line, "success")
                                this_freq_fail_mssage = ""
                            else:
                                self.emit(SIGNAL("table_color"), sp_line, "fail")
                                test_result_fail = test_result_fail + 1
                                global this_test_result_fail
                                this_test_result_fail = 1
                                retest_num = string.atoi(testconf.get_fail_retest_num())
                                for i in range(retest_num):
                                    if this_test_result_fail==0:
                                        test_result_fail = test_result_fail-1
                                        this_freq_fail_mssage = ""
                                        self.emit(SIGNAL("table_color"), sp_line, "success")
                                        break
                                    else:
                                        self.loop_loop_tx(freq,rate,chain,setting_limit)
                                        if this_test_result_fail ==0:
                                            test_result_fail = test_result_fail-1
                                            this_freq_fail_mssage = ""
                                            self.emit(SIGNAL("table_color"), sp_line, "success")
                                            break

                        fail_mssage += this_freq_fail_mssage
                        self.printstr('\n',QColor(0, 0, 0, 110))
                        if fail_stop_flag == '1':
                            if test_result_fail != 0:
                                break
                    if fail_stop_flag == '1':
                        if test_result_fail != 0:
                            break
                if fail_stop_flag == '1':
                    if test_result_fail != 0:
                        break
            if fail_stop_flag == '1':
                if test_result_fail != 0:
                    break
            #中断程序
            # finish = self.finished()
            # print finish

    def loop_loop_tx(self,freq,rate,chain,setting_limit):
        testconfxml = TestConfigxml()
        global capture_time
        global tx_evm_limit
        global test_result_fail
        #global txppm_limit
        global dll
        global mask_dll
        result = 0
        freq_val_list = []
        global  this_test_result_fail
        testconf = TestConf()
        d_type = self.rate_to_type(rate)
        result = 0

        testconfxml = TestConfigxml()
        myconf = MyConf()
        testconf = TestConf()

        loop_tx_sleep = string.atof(testconf.get_loop_tx_sleep())
        loop_capture = string.atoi(testconf.get_loop_capture())
        fail_stop_flag = myconf.get_fail_stop()

        self.emit(SIGNAL("testing1"))
        if(string.atoi(freq)<5000):
            #获得2G配置文件信息
            txppm_limit = string.atof(testconfxml.get_2g_ppm_limit())
            #txppm_limit = testconf.get_2G_ppm_limit()
        else:
            txppm_limit = string.atof(testconfxml.get_5g_ppm_limit())
            # txppm_limit = testconf.get_5G_ppm_limit()
        # if(sp_line!=None):
        #     sp_line = sp_line+1#行标加1，下一行
        #添加一行测试项
        self.printstr("\n\n***** frequency: "+freq+ ' **** rate: '+rate+ ' **** chain: ' + chain+' *****\n',QColor(0, 0, 0, 110))
        #index_str = freq+"_"+rate+"_"+chain
        #if(debug != 0):
        #    self.printstr("freq:"+freq+",rate:"+rate+","+"chain:"+chain+'\n',QColor(0, 0, 0, 110))
        cmd_gettp = "gettp f="+freq+"; r="+rate+";"
        ttpstr = self.telnet_exec_command(u"测试",cmd_gettp,"CONTROL DONE "+cmd_gettp, 0, 0, 1)
        # self.printstr("ttpstr:"+ttpstr+'\n',QColor(0, 0, 0, 110))
        tp = self.str_find_tp(ttpstr)
        self.printstr("Target Power:     "+tp+'\n',QColor(0, 0, 0, 110))

        stand_evm = tx_evm_limit[rate]
        # self.printstr("stand_evm:"+str(stand_evm)+'\n',QColor(0, 0, 0, 110))

        cmd = self.create_command_tx(freq, rate, chain, tp)
        if(debug != 0):
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))

        self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 0, 1, 0)
        lost = self.get_lost_from_xiansunini(freq,chain)

        if(rate == "f0" or rate == "f7" or rate == "vf0" or rate== "vf9"):
            if d_type == "80211ac" or d_type =="80211ag" or d_type =="80211n":
                self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+10-lost, 2)
            else:
                self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+4-lost, 2)
        else:
            if d_type == "80211ac" or d_type =="80211ag"or d_type =="80211n":
                self.dll_setvsa(string.atoi(freq), string.atof(tp)+10-lost, 2)
            else:
                self.dll_setvsa(string.atoi(freq), string.atof(tp)+4-lost, 2)

        time.sleep(loop_tx_sleep)
        r = rate.lower()
        time_var = capture_time[r]
        if(debug != 0):
            self.printstr("capture time::"+str(time_var)+'\n',QColor(0, 0, 0, 110))


        temp_list = {}
        for i in range(loop_capture):
            ret = dll.LP_VsaDataCapture(c_double(time_var*1e-6), c_int(6), c_double(160e6), c_int(0), c_int(0))

            dll.LP_GetScalarMeasurement.restype = c_double

            if(debug != 0):
                self.printstr("LP_VsaDataCapture:"+str(ret)+'\n',QColor(0, 0, 0, 110))
            P_av_no_gap_all_dBm_temp = self.get_power_2(rate)

            temp_list[i] = P_av_no_gap_all_dBm_temp
            print "..."+str(i)+"..."+str(temp_list[i])


        P_av_no_gap_all_dBm = round(sum(temp_list.values())/len(temp_list),2)
        print "_________"+str(P_av_no_gap_all_dBm)+"\n\n"
        self.emit(SIGNAL("testing2"))
        if(ret != 0):
            self.t_geterr(ret)
        #返回8 打印出data capturefaild

        #time.sleep(200)
        mask_dll.LP_AnalyzeMASK.restype = c_double
        #if(test == "special_mask"):
        if(d_type == "80211n"):
            if(rate[0]=="f"):
                self.printstr('11N_40      \n',QColor(0, 0, 0, 110))
                mymask = mask_dll.LP_AnalyzeMASK(c_int(4))
                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                if(mymask <1):
                    special_mask_result = 0
                else:
                    special_mask_result = 1
            else:
                self.printstr('IQ_MODE_11N_20       \n',QColor(0, 0, 0, 110))
                mymask = mask_dll.LP_AnalyzeMASK(c_int(3))
                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                if(mymask < 1):
                    special_mask_result = 0
                else:
                    special_mask_result = 1
        elif(d_type == "80211b"):
            self.printstr('11B     \n',QColor(0, 0, 0, 110))
            mymask = mask_dll.LP_AnalyzeMASK(c_int(0))
            self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
            if(mymask < 1):
                special_mask_result = 0
            else:
                special_mask_result = 1
        elif(d_type == "80211ag"):
            if(string.atoi(freq)<5000):
                self.printstr('11G     \n',QColor(0, 0, 0, 110))
                mymask = mask_dll.LP_AnalyzeMASK(c_int(1))
                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                if(mymask < 1):
                    special_mask_result = 0
                else:
                    special_mask_result = 1
            else:
                self.printstr('11A     \n',QColor(0, 0, 0, 110))
                mymask = mask_dll.LP_AnalyzeMASK(c_int(2))
                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                if(mymask < 1):
                    special_mask_result = 0
                else:
                    special_mask_result = 1
        else:#此为11ac
            if(rate[1]=='t'):
                self.printstr('11AC_HT20  \n',QColor(0, 0, 0, 110))
                mymask = mask_dll.LP_AnalyzeMASK(c_int(5))
                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                if(mymask < 1):
                    special_mask_result = 0
                else:
                    special_mask_result = 1
            elif(rate[1]=='f'):
                self.printstr('11AC_HT40  \n',QColor(0, 0, 0, 110))
                mymask = mask_dll.LP_AnalyzeMASK(c_int(7))
                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                if mymask < 1:
                    special_mask_result = 0
                else:
                    special_mask_result = 1
            else:
                self.printstr('11AC_HT80   \n',QColor(0, 0, 0, 110))
                mymask = mask_dll.LP_AnalyzeMASK(c_int(7))
                self.printstr('Mask Err:            '+str(mymask)+'\n',QColor(0, 0, 110, 110))
                if mymask < 1:
                    special_mask_result = 0
                else:
                    special_mask_result = 1

        if d_type == "80211b":
            ret = dll.LP_Analyze80211b(c_int(1), c_int(0), c_int(1), c_double(8.8e-6), c_double(15.2e-6))

            if debug != 0:
                self.printstr("LP_Analyze80211b:"+str(ret)+'\n',QColor(0, 0, 0, 110))

            if ret != 0:
                self.t_geterr(ret)
        elif d_type == "80211ag":
            ret = dll.LP_Analyze80211ag(c_int(2), c_int(3), c_int(2), c_int(2), c_int(1), c_double(8.8e-6), c_double(15.2e-6))
            if debug != 0:
                self.printstr("LP_Analyze80211ag:"+str(ret)+'\n', QColor(0, 0, 0, 110))
            if ret != 0:
                self.t_geterr(ret)

        elif d_type == "80211ac":
            ret = dll.LP_Analyze80211ac("nxn", c_int(1), c_int(1), c_int(0), c_int(0), c_int(1), c_int(2), "NULL", c_int(0),c_int(1), c_double(8.8e-6), c_double(15.2e-6))#方法要变  analyze80211ac（）
            if debug != 0:
                self.printstr("LP_Analyze80211ac:"+str(ret)+'\n', QColor(0, 0, 0, 110))
            if ret != 0:
                self.t_geterr(ret)
        else:
            ret = dll.LP_Analyze80211n("EWC", "nxn", c_int(1), c_int(1), c_int(0), c_int(1), c_int(1), "", c_int(0), c_int(2), c_double(8.8e-6), c_double(15.2e-6))
            if debug != 0:
                self.printstr("LP_Analyze80211n:"+str(ret)+'\n',QColor(0, 0, 0, 110))
            if ret != 0:
                self.t_geterr(ret)

        dll.LP_GetScalarMeasurement.restype = c_double

        evmAvgAll_0 = dll.LP_GetScalarMeasurement("evmAvgAll", c_int(0))
        evmAll_0 = dll.LP_GetScalarMeasurement("evmAll", c_int(0))
        rmsPower_0 = dll.LP_GetScalarMeasurement("rmsPower", c_int(0));
        pkPower_0 = dll.LP_GetScalarMeasurement("pkPower", c_int(0));
        freqErrorHz_0 = dll.LP_GetScalarMeasurement("freqErrorHz", c_int(0));
        freqErr_0 = dll.LP_GetScalarMeasurement("freqErr", c_int(0));
        clockErr_0 = dll.LP_GetScalarMeasurement("clockErr", c_int(0));
        symClockErrorPpm_0 = dll.LP_GetScalarMeasurement("symClockErrorPpm", c_int(0));
        rxRmsPowerDb_4 = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(0));


        valid_3 = self.get_power_param("valid")
        P_av_each_burst_3 = self.get_power_param("P_av_each_burst")
        P_pk_each_burst_3 = self.get_power_param("P_pk_each_burst")
        P_av_all_3 = self.get_power_param("P_av_all")
        P_peak_all_3 = self.get_power_param("P_peak_all")
        P_av_no_gap_all_3 = self.get_power_param("P_av_no_gap_all")
        P_av_all_dBm_3 = self.get_power_param("P_av_all_dBm")
        P_peak_all_dBm_3 = self.get_power_param("P_peak_all_dBm")

        rmsMaxAvgPower_0 = dll.LP_GetScalarMeasurement("rmsMaxAvgPower", c_int(0));
        rxRmsPowerDb_0 = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(0));
        rmsMaxAvgPower = dll.LP_GetScalarMeasurement("rmsMaxAvgPower", c_int(1));
        rxRmsPowerDb = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(1));


        self.telnet_exec_stop("CONTROL DONE "+cmd)

        limit = setting_limit
        meas_pwr = lost + P_av_no_gap_all_dBm
        self.printstr("Cable loss:     "+str(lost)+'          \n',QColor(0, 0, 0, 110))
        # self.printstr("meas_pwr:"+str(meas_pwr)+'\n',QColor(0, 0, 0, 110))
        target = string.atof(tp)
        delta = meas_pwr - target

        # self.printstr("##############################################\n",QColor(0, 0, 0, 110))
        self.printstr("Power:     "+str(meas_pwr)+'      \n',QColor(0, 0, 0, 110))
        self.printstr("delta:     "+str(delta)+'       ',QColor(0, 0, 0, 110))

        if abs(delta) <= limit:
            self.printstr('      ('+str(limit) +')                    power PASS\n',QColor(0, 255, 0, 220))
            power_result = 0
        else:
            self.printstr('      ('+str(limit) +')                    power FAIL   ('+str(limit)+')\n',QColor(255, 0, 0, 220))
            power_result = 1


        # self.printstr("stand_evm:"+str(stand_evm)+'\n', QColor(0, 0, 0, 110))

        if d_type == "80211n" or d_type == "80211ac" :
            if evmAvgAll_0 > float(stand_evm) or evmAvgAll_0 < -99:
                self.printstr("EVM:     "+str(round(evmAvgAll_0,2))+'          ',QColor(255, 0, 0, 220))
                self.printstr('(' + str(stand_evm) + ')                     evm FAIL\n',QColor(255, 0, 0, 220))
                evm_result = 1
            else:
                self.printstr("EVM:     "+str(round(evmAvgAll_0,2))+'           ',QColor(0, 255, 0, 220))
                self.printstr('(' + str(stand_evm) + ')                     evm PASS\n',QColor(0, 255, 0, 220))
                evm_result = 0
        else:
            if evmAll_0 > float(stand_evm) or evmAll_0 < -99:
                self.printstr("EVM:     "+str(round(evmAll_0,2))+'          ',QColor(255, 0, 0, 220))
                self.printstr('(' + str(stand_evm) + ')                     evm failed\n',QColor(255, 0, 0, 220))
                evm_result = 1
            else:
                self.printstr("EVM:     "+str(round(evmAll_0,2))+'          ',QColor(0, 255, 0, 220))
                self.printstr('(' + str(stand_evm) + ')                     evm PASS\n',QColor(0, 255, 0, 220))
                evm_result = 0

        # self.printstr("txppm_limit:"+str(txppm_limit)+'\n',QColor(0, 0, 0, 110))

        if d_type == "80211n" or d_type == "80211ac":

            if abs(freqErrorHz_0/string.atoi(freq)) > txppm_limit :
                self.printstr("Freq Err:     "+str(round(freqErrorHz_0/string.atoi(freq),2))+"    "+"      ("+str(txppm_limit)+")"+'          ',QColor(255, 0, 0, 220))
                self.printstr('          EVM_ppm FAIL\n',QColor(255, 0, 0, 220))
                evm_ppm_result = 1
            else:
                self.printstr("Freq Err:     "+str(round(freqErrorHz_0/string.atoi(freq),2))+"    "+"      ("+str(txppm_limit)+")"+'         ',QColor(0, 255, 0, 220))
                self.printstr('          EVM_ppm PASS\n',QColor(0, 255, 0, 220))
                evm_ppm_result = 0

        else:
            if abs(freqErr_0/string.atoi(freq)) > txppm_limit:
                self.printstr("freqErr_0:"+str(round(freqErr_0/string.atoi(freq),2))+"    "+"      ("+str(txppm_limit)+")"+'          ',QColor(255, 0, 0, 220))
                self.printstr('          EVM_ppm FAIL\n',QColor(255, 0, 0, 220))
                evm_ppm_result = 1
            else:
                self.printstr("freqErr_0:"+str(round(freqErr_0/string.atoi(freq),2))+"    "+"      ("+str(txppm_limit)+")"+'          ',QColor(0, 255, 0, 220))
                self.printstr('          EVM_ppm PASS\n',QColor(0, 255, 0, 220))
                evm_ppm_result = 0

        if special_mask_result != 0:
            self.printstr('mask_result  failed(10%)\n',QColor(255, 0, 0, 220))
        self.emit(SIGNAL("testing3"))
        # cmd_gettp = "gettp f="+freq+"; r="+rate+";"
        # ttpstr = self.telnet_exec_command(u"测试",cmd_gettp,"CONTROL DONE "+cmd_gettp, 0, 0, 1)
        # # self.printstr("ttpstr:"+ttpstr+'\n',QColor(0, 0, 0, 110))
        # tp = self.str_find_tp(ttpstr)
        # self.printstr("tp:     "+tp+'\n',QColor(0, 0, 0, 110))
        # stand_evm = tx_evm_limit[rate]
        # self.printstr("stand_evm:"+str(stand_evm)+'\n', QColor(0, 0, 0, 110))
        #
        # cmd = self.create_command_tx(freq, rate, chain, tp)
        # if(debug != 0):
        #     self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
        #
        # self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 0, 1, 0)
        #
        # if(rate == "f0" or rate == "f7" or rate == "vf0" or rate== "vf9"):
        #     if d_type == "80211ac" or d_type =="80211ag" or d_type =="80211n":
        #         self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+10, 2)
        #     else:
        #         self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+4, 2)
        # else:
        #     if d_type == "80211ac" or d_type =="80211ag"or d_type =="80211n":
        #         self.dll_setvsa(string.atoi(freq), string.atof(tp)+10, 2)
        #     else:
        #         self.dll_setvsa(string.atoi(freq), string.atof(tp)+4, 2)
        #
        # time.sleep(0.2)
        # r = rate.lower()
        # time_var = capture_time[r]
        # if(debug != 0):
        #     self.printstr("capture time::"+str(time_var)+'\n',QColor(0, 0, 0, 110))
        # ret = dll.LP_VsaDataCapture(c_double(time_var*1e-6), c_int(6), c_double(160e6), c_int(0), c_int(0))
        # if(debug != 0):
        #     self.printstr("LP_VsaDataCapture:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        # if(ret != 0):
        #     self.t_geterr(ret)
        # #返回8 打印出data capturefaild
        #
        # #time.sleep(200)
        # mask_dll.LP_AnalyzeMASK.restype = c_double
        # #if(test == "special_mask"):
        # if(d_type == "80211n"):
        #     if(rate[0]=="f"):
        #         self.printstr('11N_40     ',QColor(0, 0, 0, 110))
        #         mymask = mask_dll.LP_AnalyzeMASK(c_int(4))
        #         self.printstr('mymask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #         if(mymask < 1):
        #             special_mask_result = 0
        #         else:
        #             special_mask_result = 1
        #     else:
        #         self.printstr('IQ_MODE_11N_20     ',QColor(0, 0, 0, 110))
        #         mymask = mask_dll.LP_AnalyzeMASK(c_int(3))
        #         self.printstr('mask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #         if(mymask < 1):
        #             special_mask_result = 0
        #         else:
        #             special_mask_result = 1
        # elif(d_type == "80211b"):
        #     self.printstr('11B     ',QColor(0, 0, 0, 110))
        #     mymask = mask_dll.LP_AnalyzeMASK(c_int(0))
        #     self.printstr('mask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #     if(mymask < 1):
        #         special_mask_result = 0
        #     else:
        #         special_mask_result = 1
        # elif(d_type == "80211ag"):
        #     if(string.atoi(freq)<5000):
        #         self.printstr('11G     ',QColor(0, 0, 0, 110))
        #         mymask = mask_dll.LP_AnalyzeMASK(c_int(1))
        #         self.printstr('mask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #         if(mymask < 1):
        #             special_mask_result = 0
        #         else:
        #             special_mask_result = 1
        #     else:
        #         self.printstr('11A     ',QColor(0, 0, 0, 110))
        #         mymask = mask_dll.LP_AnalyzeMASK(c_int(2))
        #         self.printstr('mask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #         if(mymask < 1):
        #             special_mask_result = 0
        #         else:
        #             special_mask_result = 1
        # else:#此为11ac
        #     if(rate[1]=='t'):
        #         self.printstr('11AC_HT20     ',QColor(0, 0, 0, 110))
        #         mymask = mask_dll.LP_AnalyzeMASK(c_int(5))
        #         self.printstr('mask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #         if(mymask < 1):
        #             special_mask_result = 0
        #         else:
        #             special_mask_result = 1
        #     elif(rate[1]=='f'):
        #         self.printstr('11AC_HT40     ',QColor(0, 0, 0, 110))
        #         mymask = mask_dll.LP_AnalyzeMASK(c_int(7))
        #         self.printstr('mask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #         if mymask < 1:
        #             special_mask_result = 0
        #         else:
        #             special_mask_result = 1
        #     else:
        #         self.printstr('11AC_HT80     ',QColor(0, 0, 0, 110))
        #         mymask = mask_dll.LP_AnalyzeMASK(c_int(7))
        #         self.printstr('mask:     '+str(mymask)+'\n',QColor(0, 0, 110, 110))
        #         if mymask < 1:
        #             special_mask_result = 0
        #         else:
        #             special_mask_result = 1
        #
        # if d_type == "80211b":
        #     ret = dll.LP_Analyze80211b(c_int(1), c_int(0), c_int(1), c_double(8.8e-6), c_double(15.2e-6))
        #
        #     if debug != 0:
        #         self.printstr("LP_Analyze80211b:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        #
        #     if ret != 0:
        #         self.t_geterr(ret)
        # elif d_type == "80211ag":
        #     ret = dll.LP_Analyze80211ag(c_int(2), c_int(3), c_int(2), c_int(2), c_int(1), c_double(8.8e-6), c_double(15.2e-6))
        #     if debug != 0:
        #         self.printstr("LP_Analyze80211ag:"+str(ret)+'\n', QColor(0, 0, 0, 110))
        #     if ret != 0:
        #         self.t_geterr(ret)
        #
        # elif d_type == "80211ac":
        #     ret = dll.LP_Analyze80211ac("nxn", c_int(1), c_int(1), c_int(0), c_int(0), c_int(1), c_int(2), "NULL", c_int(0),c_int(1), c_double(8.8e-6), c_double(15.2e-6))#方法要变  analyze80211ac（）
        #     if debug != 0:
        #         self.printstr("LP_Analyze80211ac:"+str(ret)+'\n', QColor(0, 0, 0, 110))
        #     if ret != 0:
        #         self.t_geterr(ret)
        # else:
        #     ret = dll.LP_Analyze80211n("EWC", "nxn", c_int(1), c_int(1), c_int(0), c_int(1), c_int(1), "", c_int(0), c_int(2), c_double(8.8e-6), c_double(15.2e-6))
        #     if debug != 0:
        #         self.printstr("LP_Analyze80211n:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        #     if ret != 0:
        #         self.t_geterr(ret)
        #
        # dll.LP_GetScalarMeasurement.restype = c_double
        #
        # evmAvgAll_0 = dll.LP_GetScalarMeasurement("evmAvgAll", c_int(0))
        # evmAll_0 = dll.LP_GetScalarMeasurement("evmAll", c_int(0))
        # rmsPower_0 = dll.LP_GetScalarMeasurement("rmsPower", c_int(0));
        # pkPower_0 = dll.LP_GetScalarMeasurement("pkPower", c_int(0));
        # freqErrorHz_0 = dll.LP_GetScalarMeasurement("freqErrorHz", c_int(0));
        # freqErr_0 = dll.LP_GetScalarMeasurement("freqErr", c_int(0));
        # clockErr_0 = dll.LP_GetScalarMeasurement("clockErr", c_int(0));
        # symClockErrorPpm_0 = dll.LP_GetScalarMeasurement("symClockErrorPpm", c_int(0));
        # rxRmsPowerDb_4 = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(0));
        #
        # P_av_no_gap_all_dBm = self.get_power_2(rate)
        # valid_3 = self.get_power_param("valid")
        # P_av_each_burst_3 = self.get_power_param("P_av_each_burst")
        # P_pk_each_burst_3 = self.get_power_param("P_pk_each_burst")
        # P_av_all_3 = self.get_power_param("P_av_all")
        # P_peak_all_3 = self.get_power_param("P_peak_all")
        # P_av_no_gap_all_3 = self.get_power_param("P_av_no_gap_all")
        # P_av_all_dBm_3 = self.get_power_param("P_av_all_dBm")
        # P_peak_all_dBm_3 = self.get_power_param("P_peak_all_dBm")
        #
        # rmsMaxAvgPower_0 = dll.LP_GetScalarMeasurement("rmsMaxAvgPower", c_int(0));
        # rxRmsPowerDb_0 = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(0));
        # rmsMaxAvgPower = dll.LP_GetScalarMeasurement("rmsMaxAvgPower", c_int(1));
        # rxRmsPowerDb = dll.LP_GetScalarMeasurement("rxRmsPowerDb", c_int(1));
        #
        #
        # self.telnet_exec_stop("CONTROL DONE "+cmd)
        #
        # limit = setting_limit
        # lost = self.get_lost_from_xiansunini(freq,chain)
        # meas_pwr = lost + P_av_no_gap_all_dBm
        # self.printstr("lost:"+str(lost)+'                    \n',QColor(0, 0, 0, 110))
        # # self.printstr("meas_pwr:     "+str(meas_pwr)+'\n',QColor(0, 0, 0, 110))
        # target = string.atof(tp)
        # delta = meas_pwr - target
        #
        # # self.printstr("##############################################\n",QColor(0, 0, 0, 110))
        # self.printstr("delta:"+str(delta)+'              ',QColor(0, 0, 0, 110))

        # if abs(delta) <= limit:
        #     self.printstr('power PASS\n',QColor(0, 255, 0, 220))
        #     power_result = 0
        # else:
        #     self.printstr('power failed\n',QColor(255, 0, 0, 220))
        #     power_result = 1
        #
        #
        # if d_type == "80211n" or d_type == "80211ac" :
        #     if evmAvgAll_0 > stand_evm :
        #         self.printstr("evmAvgAll:"+str(evmAvgAll_0)+'            ',QColor(255, 0, 0, 220))
        #         self.printstr('evm failed\n',QColor(255, 0, 0, 220))
        #         evm_result = 1
        #     else:
        #         self.printstr("evmAvgAll:"+str(evmAvgAll_0)+'          ',QColor(0, 255, 0, 220))
        #         self.printstr('evm PASS\n',QColor(0, 255, 0, 220))
        #         evm_result = 0
        # else:
        #     if evmAll_0 > stand_evm:
        #         self.printstr("evmAll_0:"+str(evmAll_0)+'          ',QColor(255, 0, 0, 220))
        #         self.printstr('evm failed\n',QColor(255, 0, 0, 220))
        #         evm_result = 1
        #     else:
        #         self.printstr("evmAll_0:"+str(evmAll_0)+'          ',QColor(0, 255, 0, 220))
        #         self.printstr('evm PASS\n',QColor(0, 255, 0, 220))
        #         evm_result = 0
        #
        # # self.printstr("txppm_limit:"+str(txppm_limit)+'\n',QColor(0, 0, 0, 110))
        #
        # if d_type == "80211n" or d_type == "80211ac" :
        #
        #     if abs(freqErrorHz_0/string.atoi(freq)) > txppm_limit :
        #         self.printstr("freqErrorHz_0:"+str(freqErrorHz_0/string.atoi(freq))+'          ',QColor(255, 0, 0, 220))
        #         self.printstr('evm_ppm failed\n',QColor(255, 0, 0, 220))
        #         evm_ppm_result = 1
        #     else:
        #         self.printstr("freqErrorHz_0:"+str(freqErrorHz_0/string.atoi(freq))+'          ',QColor(0, 255, 0, 220))
        #         self.printstr('evm_ppm PASS\n',QColor(0, 255, 0, 220))
        #         evm_ppm_result = 0
        #
        # else:
        #     if abs(freqErr_0/string.atoi(freq)) > txppm_limit:
        #         self.printstr("freqErr_0:"+str(freqErr_0/string.atoi(freq))+'          ',QColor(255, 0, 0, 220))
        #         self.printstr('evm_ppm failed\n',QColor(255, 0, 0, 220))
        #         evm_ppm_result = 1
        #     else:
        #         self.printstr("freqErr_0:"+str(freqErr_0/string.atoi(freq))+'          ',QColor(0, 255, 0, 220))
        #         self.printstr('evm_ppm PASS\n',QColor(0, 255, 0, 220))
        #         evm_ppm_result = 0
        #
        # if special_mask_result != 0:
        #     self.printstr('mask_result  failed\n',QColor(255, 0, 0, 220))

        #判断成功失败
        # if(sp_line!= None):
        if(special_mask_result == 0 and power_result == 0 and evm_result == 0 and evm_ppm_result == 0):
            # self.emit(SIGNAL("table_color"), sp_line, "success")
            this_test_result_fail = 0
        else:
            # self.emit(SIGNAL("table_color"), sp_line, "fail")
            this_test_result_fail = 1
        # self.printstr('\n',QColor(0, 0, 0, 110))





    def rate_to_type(self, rate):
        global rate_80211b,rate_80211g,rate_80211a,rate_80211n_ht20,rate_80211n_ht40,rate_80211ac_ht20,rate_80211ac_ht40,rate_80211ac_ht80
        r = rate.lower()
        if(rate_80211b.count(r)!=0):
            return "80211b"
        elif(rate_80211a.count(r)!=0 or rate_80211g.count(r)!=0):
            return "80211ag"
        elif(rate_80211n_ht20.count(r)!=0 or rate_80211n_ht40.count(r)!=0):
            return "80211n"
        elif(rate_80211ac_ht20.count(r)!=0 or rate_80211ac_ht40.count(r)!=0 or rate_80211ac_ht80.count(r)!=0):
            return "80211ac"
        else :
            return "unknown"

    #获得速率对应的功率
    def get_pinlv_gonglv(self,this_freq,this_rate):
        testconfxml = TestConfigxml()
        tree = testconfxml.read_xml()
        tests = testconfxml.get_all_test(tree)
        level_str = ""
        # if(string.atoi(this_freq)<5000):#2g的
        #     # index = testconf.get_2G_freq_for_lost().split(",").index(freq)#频率
        #     # lost_str = testconf.get_2G_lost_for_freq().split(",")[index]#线损
        #     #获得当前频率的线损
        #     # key = 当前频率的freq
        #     #获得所有线损的freq

        for test in tests:
            if string.atoi(this_freq)<5000:
                if test.get('name') == '2G':
                    power_rate = testconfxml.get_power_rate(test)
                    freqs = testconfxml.get_all_pr_items(power_rate)
                    for freq in freqs:
                        level = freq.find('level').text
                        rate = freq.find('rate').text
                        if level == this_rate:
                            level_str = rate
            else:
                if test.get('name') == '5G':
                    power_rate = testconfxml.get_power_rate(test)
                    freqs = testconfxml.get_all_pr_items(power_rate)
                    for freq in freqs:
                        level = freq.find('level').text
                        rate = freq.find('rate').text
                        if level == this_rate:
                            level_str = rate

        levels = level_str
        return levels
        # else:#5g的
        #     # index = testconf.get_5G_freq_for_lost().split(",").index(this_freq)
        #     # lost_str = testconf.get_5G_lost_for_freq().split(",")[index]
        #     for test in tests:
        #
        #         if test.get('name') == '5G':
        #             power_rate = testconfxml.get_power_rate(test)
        #             freqs = testconfxml.get_all_pr_items(power_rate)
        #             for freq in freqs:
        #                 level = freq.find('level').text
        #                 rate = freq.find('rate').text
        #                 if rate == this_rate:
        #                     level_str = level
        #
        #     levels = string.atof(level_str)
        #     return levels

    def create_command_rx_5g(self, freq, rate, chain, stat):
        r = rate.lower()
        iss = self.get_pinlv_gonglv(freq,rate)

        # iss = self.get_rx_command_iss(rate)
        cmd_rx = "rx f="+freq+";ir=0;gi=0;txch=7;rxch="+chain+";pc=100;pl=1000;bc=1;retry=0;att=0;iss="+iss+";stat="+stat+";ifs=-1;dur=600000;dump=0;pro=0;bssid=01.00.00.c0.ff.ee; mactx=01.00.00.c0.ff.ee;macrx=01.00.00.c0.ff.ee;deaf=0;reset=-1;agg=1;ht40=2;r="+rate+";tp=8.0;"
        return cmd_rx

    def loop_rx(self, freq_all, rate_all, chain_all, pre_line=None):
        global dll
        global test_result_fail
        #global vsg_power_level
        global path_loss_2g
        global path_loss_5g
        global fail_mssage
        sp_line = pre_line
        testconfigxml = TestConfigxml()
        testconf = TestConf()
        myconf = MyConf()
        fail_stop_flag = myconf.get_fail_stop()
        for i in range(len(freq_all)):
            for key ,freq in freq_all[i].items():
                rate_this = testconfigxml.get_rate_this(key)
                print key
                chain_this = testconfigxml.get_chain_this(key)
                for rate in rate_this:
                    for chain in chain_this:
                        self.emit(SIGNAL("testing1"))
                        this_freq_fail_mssage = "*** "+freq+" * "+ rate+" * "+chain+" ***\n"
                        if(debug != 0):
                           self.printstr("freq:"+freq+",rate:"+rate+","+"chain:"+chain+'\n',QColor(0, 0, 0, 110))
                        if(sp_line!=None):
                            sp_line=sp_line+1
                        self.printstr("##########No: "+str(sp_line+1)+' ##### '+" frequency: "+freq+' ##### rate: '+rate+' ##### chain: '+chain+' ########## \n',QColor(0, 50, 110, 110))
                        r = rate.lower()
                        power_level_xml = self.get_powerlevel(freq, r)
                        lost_xml = self.get_lost_from_xiansunini(freq,chain)
                        power_level = power_level_xml + lost_xml
                        # s = '''
                        # if(string.atoi(freq)<5000):
                        #     power_level = power_level + self.get_lost
                        # else:
                        #     power_level = power_level + path_loss_5g
                        # '''
                        if(debug != 0):
                            self.printstr("power_level:"+str(power_level)+'\n',QColor(0, 0, 0, 110))
                        # self.printstr("LP_SetVsg freq:"+str(string.atoi(freq)*1e6)+'\n',QColor(0, 0, 0, 110))
                        self.printstr("\npower_level:     "+str(power_level_xml)+'\n',QColor(0, 0, 0, 110))
                        self.printstr("lost:              "+str(lost_xml)+'\n',QColor(0, 0, 0, 110))
                        d_type = self.rate_to_type(rate)
                        # if(d_type == "80211ac"):
                        if len(rate) > 1:
                            if rate[1]=='f' or rate[0] == 'f':
                                ret = dll.LP_SetVsg(c_double((string.atoi(freq)+10)*1e6), c_double(power_level), c_int(2))
                            else:
                                ret = dll.LP_SetVsg(c_double(string.atoi(freq)*1e6), c_double(power_level), c_int(2))
                        else:
                            ret = dll.LP_SetVsg(c_double(string.atoi(freq)*1e6), c_double(power_level), c_int(2))

                        if(debug != 0):
                            self.printstr("LP_SetVsg:"+str(ret)+'\n',QColor(0, 0, 0, 110))
                        filename = self.rx_rate_to_file(rate)
                        ret = dll.LP_SetVsgModulation(filename, c_int(0))
                        if(ret != 0):
                                self.t_geterr(ret)
                        if(debug != 0):
                            self.printstr("LP_SetVsgModulation:"+str(ret)+'\n',QColor(0, 0, 0, 110))
                        if(debug != 0):
                            self.printstr("filename:"+filename+'\n',QColor(0, 0, 0, 110))
                        self.rx_exec_cmd(freq, rate, chain, "0", 5, 0.2, 1, 1)
                        self.emit(SIGNAL("testing2"))
                        return_s = self.rx_exec_cmd(freq, rate, chain, "1", 100, 0.2, 1, 1)
                        self.emit(SIGNAL("testing3"))
                        # return_s = self.get_powerlevel(freq,rate)
                        # print("freq:"+freq+",rate:"+rate+","+"chain:"+chain+'\n')
                        correct = return_s.split("||")[2].split("|")[0]
                        # print "correct",return_s.split("||")[2].split("|")[0]
                        # correct = return_s
                        # print correct


                        if(d_type == "80211b"):
                            if(string.atoi(correct)>=92):
                                result = 0

                            else:
                                result = 1
                                this_freq_fail_mssage = this_freq_fail_mssage+str(freq)+'  rx  fail  \n'
                            self.printstr('correct:           '+correct+'       (92)\n\n', QColor(0, 0, 0, 110))

                        else:
                            if(string.atoi(correct)>=90):
                                result = 0
                            else:
                                this_freq_fail_mssage = this_freq_fail_mssage+str(freq)+'  rx  fail  \n'
                                result = 1
                            self.printstr('correct:           '+correct+'       (90)\n\n', QColor(0, 0, 0, 110))

                        if(sp_line!=None):
                            if(result == 0):
                                self.emit(SIGNAL("table_color"), sp_line, "success")
                                this_freq_fail_mssage = ""
                            else:
                                self.printstr('                  failed\n',QColor(255, 0, 0, 220))
                                self.emit(SIGNAL("table_color"), sp_line, "fail")
                                test_result_fail = test_result_fail+1
                                global this_test_result_fail
                                this_test_result_fail = 1
                                num = testconf.get_fail_retest_num()
                                retest_num = string.atoi(num)
                                for i in range(retest_num):
                                    if this_test_result_fail == 0:
                                        self.emit(SIGNAL("table_color"), sp_line, "success")
                                        test_result_fail = test_result_fail - 1
                                        this_freq_fail_mssage = ""
                                        break
                                    else:
                                        self.loop_loop_rx(freq,rate,chain)
                                        if this_test_result_fail == 0:
                                            self.emit(SIGNAL("table_color"), sp_line, "success")
                                            test_result_fail = test_result_fail-1
                                            this_freq_fail_mssage = ""
                                            break
                        fail_mssage += this_freq_fail_mssage
                        if fail_stop_flag == '1':
                            if test_result_fail != 0:
                                    #中断程序
                                break
                    if fail_stop_flag == '1':
                        if test_result_fail != 0:
                                    #中断程序
                            break
                if fail_stop_flag == '1':
                    if test_result_fail != 0:
                                    #中断程序
                        break
            if fail_stop_flag == '1':
                if test_result_fail != 0:
                                    #中断程序
                    break

    def loop_loop_rx(self, freq, rate, chain):
        global this_test_result_fail
        self.emit(SIGNAL("testing1"))
        self.printstr("########## frequency: "+freq+' ##### rate: '+rate+' ##### chain: '+chain+' ########## \n',QColor(0, 50, 110, 110))
        r = rate.lower()
        power_level = self.get_powerlevel(freq, r)
        power_level = power_level + self.get_lost_from_xiansunini(freq, chain)
        # s = '''
        # if(string.atoi(freq)<5000):
        #     power_level = power_level + self.get_lost
        # else:
        #     power_level = power_level + path_loss_5g
        # '''
        if(debug != 0):
            self.printstr("power_level:"+str(power_level)+'\n',QColor(0, 0, 0, 110))
        # self.printstr("LP_SetVsg freq:"+str(string.atoi(freq)*1e6)+'\n',QColor(0, 0, 0, 110))
        self.printstr("\npower_level:     "+str(power_level)+'\n',QColor(0, 0, 0, 110))
        d_type = self.rate_to_type(rate)
        # if(d_type == "80211ac"):
        if len(rate) > 1:
            if rate[1]=='f' or rate[0] == 'f':
                ret = dll.LP_SetVsg(c_double((string.atoi(freq)+10)*1e6), c_double(power_level), c_int(2))
            else:
                ret = dll.LP_SetVsg(c_double(string.atoi(freq)*1e6), c_double(power_level), c_int(2))
        else:
            ret = dll.LP_SetVsg(c_double(string.atoi(freq)*1e6), c_double(power_level), c_int(2))

        if(debug != 0):
            self.printstr("LP_SetVsg:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        filename = self.rx_rate_to_file(rate)
        ret = dll.LP_SetVsgModulation(filename, c_int(0))
        if(ret != 0):
                self.t_geterr(ret)
        if(debug != 0):
            self.printstr("LP_SetVsgModulation:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(debug != 0):
            self.printstr("filename:"+filename+'\n',QColor(0, 0, 0, 110))
        self.rx_exec_cmd(freq, rate, chain, "0", 5, 0.3, 1, 1)
        self.emit(SIGNAL("testing2"))
        return_s = self.rx_exec_cmd(freq, rate, chain, "1", 100, 0.5, 1, 1)
        self.emit(SIGNAL("testing3"))
        # return_s = self.get_powerlevel(freq,rate)
        # print("freq:"+freq+",rate:"+rate+","+"chain:"+chain+'\n')
        correct = return_s.split("||")[2].split("|")[0]
        # print "correct",return_s.split("||")[2].split("|")[0]
        # correct = return_s
        # print correct
        self.printstr('correct:           '+correct+'\n\n', QColor(0, 0, 0, 110))


        if(d_type == "80211b"):
            if(string.atoi(correct)>=92):
                result = 0
            else:
                result = 1
        else:
            if(string.atoi(correct)>=90):
                result = 0
            else:
                result = 1
        if(result == 0):
            this_test_result_fail = 0
        else:
            self.printstr('                  failed\n\n',QColor(255, 0, 0, 220))
            this_test_result_fail = 1
    # def loop_loop_rx(self, freq, rate, chain):
    #     global dll
    #
    #     i = 10
    #     while(i>0):
    #         i = i-1
    #         if(debug != 0):
    #             self.printstr("freq:"+freq+",rate:"+rate+","+"chain:"+chain+'\n',QColor(0, 0, 0, 110))
    #
    #         self.printstr("LP_SetVsg freq:"+str(string.atoi(freq)*1e6)+'\n',QColor(0, 0, 0, 110))
    #         ret = dll.LP_SetVsg(c_double(string.atoi(freq)*1e6), c_double(-30), c_int(2))
    #         if(debug != 0):
    #             self.printstr("LP_SetVsg:"+str(ret)+'\n',QColor(0, 0, 0, 110))
    #         filename = self.rx_rate_to_file(rate)
    #
    #         ret = dll.LP_SetVsgModulation(filename, c_int(0))
    #
    #         ret = dll.LP_SetFrameCnt(c_int(100))
    #         if(debug != 0):
    #             self.printstr("LP_SetFrameCnt:"+str(ret)+'\n',QColor(0, 0, 0, 110))
    #         while(dll.LP_TxDone()):
    #             continue
    #
    #         if(debug != 0):
    #             self.printstr("LP_SetVsgModulation:"+str(ret)+'\n',QColor(0, 0, 0, 110))
    #         if(debug != 0):
    #             self.printstr("filename:"+filename+'\n',QColor(0, 0, 0, 110))
    #
    #         self.rx_exec_cmd(freq, rate, chain, "3", 100, 0.5, 1, 1)
    #         self.printstr('\n\n',QColor(0, 0, 0, 110))

    def rx_exec_cmd(self, freq, rate, chain, stat, cnt, t, read_s, send_pk):
        global dll

        cmd = self.create_command_rx_5g(freq, rate, chain, stat)
        if(debug != 0):
            self.printstr("rx cmd:"+cmd+'\n',QColor(0, 0, 0, 110))
        self.telnet_exec_command_t(u"测试",cmd,"CONTROL OK", 0, 1, read_s, t)
        if(send_pk != 0):
            ret = dll.LP_SetFrameCnt(c_int(cnt))
            if(debug != 0):
                self.printstr("LP_SetFrameCnt:"+str(ret)+'\n',QColor(0, 0, 0, 110))
            while(dll.LP_TxDone()):
                continue
        return self.telnet_exec_stop("CONTROL DONE "+cmd)

    def rx_rate_to_file(self, rate):
        global rate_80211b,rate_80211g,rate_80211a,rate_80211n_ht20,rate_80211n_ht40,rate_80211ac_ht20,rate_80211ac_ht40,rate_80211ac_ht80
        rate_ = rate
        if(rate_ == "5l" or rate_ == "5L"):
            rate_ = "5.5l"
        elif(rate_ == "5s" or rate_ == "5S"):
            rate_ = "5.5s"
        r = rate_.lower()
        R = rate_.upper().replace(".","_")
        file = ""
        if(rate_80211b.count(r)!=0):
            file = os.getcwd()+"\\iqvsg\\WiFi_CCK-"+R+".iqvsg"
        elif(rate_80211a.count(r)!=0 or rate_80211g.count(r)!=0):
            file = os.getcwd()+"\\iqvsg\\WiFi_OFDM-"+R+".iqvsg"
        elif(rate_80211n_ht20.count(r)!=0):
            n = filter(str.isdigit, rate)
            file = os.getcwd()+"\\iqvsg\\WiFi_HT20_MCS"+n+".iqvsg"
        elif(rate_80211n_ht40.count(r)!=0 ):
            n = filter(str.isdigit, rate)
            file = os.getcwd()+"\\iqvsg\\WiFi_HT40_MCS"+n+".iqvsg"

        elif(rate_80211ac_ht20.count(r)!=0):
            n = filter(str.isdigit,rate)
            file = os.getcwd()+"\\iqvsg\\WiFi_VHT20-NSS1-MCS"+n+".iqvsg"
        elif(rate_80211ac_ht40.count(r)!=0):
            n = filter(str.isdigit,rate)
            file =os.getcwd()+ "\\iqvsg\\WiFi_VHT40-NSS1-MCS"+n+".iqvsg"
        elif(rate_80211ac_ht80.count(r)!=0):
            n = filter(str.isdigit,rate)
            file =os.getcwd()+ "\\iqvsg\\WiFi_VHT80-NSS1-MCS"+n+".iqvsg"
        return file
    #11ac 使用什么波形？
    def warmup(self, freq):
        testconfxml = TestConfigxml()
        testconf = TestConf()
        if(string.atoi(freq)<5000):
            pcdac = testconfxml.get_2g_pcdac()
            # pcdac=testconf.get_2G_pcdac()
        else:
            pcdac = testconfxml.get_5g_pcdac()
            # pcdac=testconf.get_5G_pcdac()
        print "pcdac",pcdac,"freq",freq
        cmd = "tx f="+freq+";ir=0;gi=0;txch=3;rxch=3;pc=5000;pl=1000;bc=1;retry=0;att=0;iss=0;stat=3;ifs=-1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;ht40=2;r=t0;pcdac="+pcdac+";pdgain=3;"
        self.telnet_exec_command(u"warmup",cmd,"CONTROL DONE "+cmd, 1, 1, 1)


    def after_jiaozhun(self):
        cmd = "sc a=BB_heavy_clip_1.heavy_clip_enable;"
        self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 0, 1)

    def create_command_jiaozhun(self, freq, chain):
        testconf = TestConf()
        testconfxml = TestConfigxml()
        if(string.atoi(freq)<5000):
            pcdac = testconfxml.get_2g_pcdac()
            # pcdac=testconf.get_2G_pcdac()
        else:
            pcdac = testconfxml.get_5g_pcdac()
            # pcdac=testconf.get_5G_pcdac()
        # print "pcdac",pcdac,"freq",freq
        if(string.atoi(freq)<5000):
            cmd_jiaozhun = "tx f="+freq+";ir=0;gi=0;txch="+chain+";rxch=1;pc=1000000;pl=1500;bc=1;retry=0;att=0;iss=0;stat=3;ifs=1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;cal=3;ht40=2;r=t0;pcdac="+pcdac+";pdgain=3;txgmaximum=80;"
        else:
            cmd_jiaozhun = "tx f="+freq+";ir=0;gi=0;txch="+chain+";rxch=1;pc=1000000;pl=1500;bc=1;retry=0;att=0;iss=0;stat=3;ifs=1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;cal=3;ht40=2;r=t0;pcdac="+pcdac+";pdgain=3;txgmaximum=416;"


        return cmd_jiaozhun

    def create_command_jiaozhun_cal(self, chain, power):
        cmd_jiaozhun_cal = "cal txchain="+chain+";power="+str(power)
        return cmd_jiaozhun_cal

    def create_command_jiaozhun_cal_last(self, chain, power):
        cmd_jiaozhun_cal = "cal txchain="+chain+";power="+str(power)+";last=1;"
        return cmd_jiaozhun_cal

    def get_power(self, rate):
        r = rate
        time = capture_time[r]
        if(debug != 0):
            self.printstr("capture time:"+str(time)+'\n',QColor(0, 0, 0, 110))

        ret = dll.LP_VsaDataCapture(c_double(time*1e-6), c_int(6), c_double(160e6), c_int(0), c_int(0))
        if(debug != 0):
            self.printstr("LP_VsaDataCapture:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(ret != 0):
            self.t_geterr(ret)
        ret = dll.LP_AnalyzePower(c_double(0.0), c_double(0.0))
        if(ret != 0):
            self.t_geterr(ret)
        dll.LP_GetScalarMeasurement.restype = c_double
        P_av_no_gap_all_dBm = dll.LP_GetScalarMeasurement("P_av_no_gap_all_dBm", c_int(0));
        if(debug != 0):
            self.printstr("P_av_no_gap_all_dBm:"+str(P_av_no_gap_all_dBm)+'\n',QColor(0, 0, 0, 110))
        return P_av_no_gap_all_dBm

    def get_power_2(self, rate):
        ret = dll.LP_AnalyzePower(c_double(0.0), c_double(0.0))
        if(ret != 0):
            self.t_geterr(ret)
        dll.LP_GetScalarMeasurement.restype = c_double
        P_av_no_gap_all_dBm = dll.LP_GetScalarMeasurement("P_av_no_gap_all_dBm", c_int(0));
        return P_av_no_gap_all_dBm

    def get_power_param(self, param):
        ret = dll.LP_AnalyzePower(c_double(0.0), c_double(0.0))
        if(ret != 0):
            self.t_geterr(ret)
        dll.LP_GetScalarMeasurement.restype = c_double
        power_param = dll.LP_GetScalarMeasurement(param, c_int(0));
        return power_param

    def loop_jiaozhun(self, freq_all, chain_all):

        testconf = TestConf()
        jiaozhun_sleep = string.atof(testconf.get_loop_jiaozhun_sleep())
        jiaozhun_power_add = string.atof(testconf.get_jiaozhun_power_add())
        for freq in freq_all:
            for chain in chain_all:
                path_lost = self.get_lost_from_xiansunini(freq,chain)

                print  str(path_lost) +"############"
                self.printstr("\n\n\nfreq :"+str(freq)+'\n',QColor(0, 0, 0, 110))
                self.printstr("lost :"+str(path_lost)+'\n',QColor(0, 0, 0, 110))
                cmd = self.create_command_jiaozhun(freq, chain)
                if(debug != 0):
                    self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
                self.telnet_exec_command(u"校准",cmd,"CONTROL DONE "+cmd, 0, 1, 0)
                global cdi
                global pcdi
                self.dll_setvsa_1(string.atoi(freq), cdi, 2)
                outstr = dll.LP_Agc(pcdi,c_bool(True))
                print(pcdi)       ##之后地址
                print(cdi)
                # outstr = dll.LP_Agc(pcdi,c_bool(True))
                print(cdi)
                global cdi_in
                cdi_flag = 0.0
                print cdi.value
                i = 0
                while (cdi.value < cdi_flag) and i < 100:
                    # time.sleep(1)
                    i = i+1
                    dll.LP_Agc(pcdi,c_bool(True))
                    print cdi.value

                if cdi.value<cdi_flag:
                    self.printstr('[ERR]: --------------' +str(cdi.value) + 'LP_Agc run fail!!!',QColor(255, 0, 0, 220))

                print(cdi)
                if string.atof(freq)>5000:
                    jiaozhun_power_add = string.atof(testconf.get_jiaozhun_power_add_5G())
                # time.sleep(jiaozhun_sleep)
                power = path_lost+self.get_power("t0")+jiaozhun_power_add

                while(power < -999):
                    power = path_lost+self.get_power("t0")
                # power = input("power:")
                print power
                self.printstr("power :"+str(power)+'\n',QColor(0, 0, 0, 110))
                if(freq == "2472" and chain == "2" or freq == "5825" and chain == "2"):
                    self.loop_send_cmd_cal_power_real_last(chain, power, path_lost,jiaozhun_power_add)
                else:
                    self.loop_send_cmd_cal_power_real(chain, power, path_lost,jiaozhun_power_add)

    def telnet_exec_command_fenzhi(self, cmd, fenzhi, t, s_old=''):
        try:
            tn.write(cmd+"\n")
            time.sleep(t)
        except Exception as e:
            self.printstr('[ERR]\n',QColor(255, 0, 0, 220))
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            self.printstr(u"error: {0}\n\n".format(e),QColor(255, 0, 0, 220))
            return ("",-2)
        try:
            s_new = tn.read_very_eager()

            s = s_old+s_new
            print s
            str_list = s_new.split('\n')
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
            for str in str_list:
                if "7504" in str:
                    if "tx" not in str:
                        # str.split("||")[0].split("|")
                        self.printstr(str+'\n',QColor(0, 0, 0, 110))
        except Exception as e:
            self.printstr('[ERR]\n',QColor(255, 0, 0, 220))
            self.printstr(u"error: {0}\n\n".format(e),QColor(255, 0, 0, 220))
            return ("",-2)
        for fi in fenzhi:
            if(fi in s):
                return (s,fenzhi.index(fi))
        return (s,-1)

    def loop_send_cmd_cal_power(self, chain, power=15.8, step=1, max_power=23):
        cmd = self.create_command_jiaozhun_cal(chain, power)
        (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.3, "")
        while(index != 0 and power <=max_power):
            if(index == -2 or index == -1):
                print "a: ", a
                print "index = ", index
                return index
            elif(index == 1):
                power = power + step
                cmd = self.create_command_jiaozhun_cal(chain, power)
                (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.3, a)

    def loop_send_cmd_cal_power_real(self, chain, power, path_lost,jiaozhun_power_add, max_power=60):
        testconf = TestConf()
        jiaozhun_sleep = string.atof(testconf.get_loop_jiaozhun_sleep())
        cmd = self.create_command_jiaozhun_cal(chain, power)
        (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], jiaozhun_sleep, "")
        while(index != 0 and power <=max_power):
            if(index == -2 or index == -1):
                print "a: ", a
                print "index = ", index
                return index
            elif(index == 1):
                power = path_lost + self.get_power("t0")+jiaozhun_power_add
                # power = input("xiansun:")
                cmd = self.create_command_jiaozhun_cal(chain, power)
                (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], jiaozhun_sleep, a)

    def loop_send_cmd_cal_power_real_last(self, chain, power, path_lost,jiaozhun_power_add, max_power=30):
        testconf = TestConf()
        jiaozhun_sleep = string.atof(testconf.get_loop_jiaozhun_sleep())
        cmd = self.create_command_jiaozhun_cal_last(chain, power)
        (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], jiaozhun_sleep, "")
        while(index != 0 and power <=max_power):
            if(index == -2 or index == -1):
                print "a: ", a
                print "index = ", index
                return index
            elif(index == 1):
                # power = input("xiansun:")
                power = path_lost + self.get_power("t0")+jiaozhun_power_add
                cmd = self.create_command_jiaozhun_cal_last(chain, power)
                (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.1, a)

    def create_command_pinpian_jiaozhun(self):
        cmd_pinpian_jiaozhun = "tx f=2437;ir=0;gi=0;txch=1;rxch=1;pc=100;pl=1000;bc=1;retry=0;att=0;iss=0;stat=3;ifs=-1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;ht40=0;r=6;tp=target;carrier=1;xtalcal=1;"
        return cmd_pinpian_jiaozhun

    def create_command_pinpian_jiaozhun_5g(self):
        cmd_pinpian_jiaozhun = "tx f=5500;ir=0;gi=0;txch=1;rxch=1;pc=100;pl=1000;bc=1;retry=0;att=0;iss=0;stat=3;ifs=-1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;agg=1;ht40=0;r=6;tp=target;carrier=1;xtalcal=1;"
        return cmd_pinpian_jiaozhun

    def create_command_pinpian_jiaozhun_xtal(self, chain, frequency):
        cmd_jiaozhun_cal = "xtal txchain="+chain+"; frequency="+str(frequency)+";"
        return cmd_jiaozhun_cal

    def get_highter_frequency(self, freq, freq_pool):
        for fi in freq_pool:
            if(fi > freq):
                return fi
        return 2436.995804

    def loop_send_cmd_xtal(self, chain, f=2436.905962):
        freq = f
        cmd = self.create_command_pinpian_jiaozhun_xtal(chain, f)
        (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.3, "")
        while(index != 0):
            if(index == -2 or index == -1):
                print "a: ", a
                print "index = ", index
                return index
            elif(index == 1):
                freq = self.get_highter_frequency(freq, [2436.905962,2436.950734,2436.979350,2436.995804])
                cmd = self.create_command_pinpian_jiaozhun_xtal(chain, freq)
                (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.3, a)

    def get_frequency(self):
        r = "6"
        time = capture_time[r]
        if(debug != 0):
            self.printstr("capture time::"+str(time)+'\n',QColor(0, 0, 0, 110))
        ret = dll.LP_VsaDataCapture(c_double(time*1e-6), c_int(1), c_double(160e6), c_int(0), c_int(0))
        if(debug != 0):
            self.printstr("LP_VsaDataCapture:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(ret != 0):
            self.t_geterr(ret)
        ret = dll.LP_AnalyzeCWFreq()
        if(debug != 0):
            self.printstr("LP_AnalyzeCWFreq:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(ret != 0):
            self.t_geterr(ret)

        dll.LP_GetScalarMeasurement.restype = c_double
        frequency = dll.LP_GetScalarMeasurement("frequency", c_int(0))
        if(debug != 0):
            self.printstr("frequency:"+str(frequency)+'\n',QColor(0, 0, 0, 110))
        return frequency

    def loop_send_cmd_xtal_real(self, chain, freq):
        frequency = self.get_frequency()
        f = frequency/1000000 + freq
        if(debug != 0):
            self.printstr("f:"+str(f)+'\n',QColor(0, 0, 0, 110))
        cmd = self.create_command_pinpian_jiaozhun_xtal(chain, f)
        (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.1, "")
        while(index != 0):
            if(index == -2 or index == -1):
                print "a: ", a
                print "index = ", index
                return index
            elif(index == 1):
                r = "6"
                time = capture_time[r]
                if(debug != 0):
                    self.printstr("capture time::"+str(time)+'\n',QColor(0, 0, 0, 110))
                if freq< 5000:
                    ret = dll.LP_VsaDataCapture(c_double(time*1e-6), c_int(1), c_double(160e6), c_int(0), c_int(0))
                ret = dll.LP_VsaDataCapture(c_double(5000*1e-6), c_int(1), c_double(160e6), c_int(0), c_int(0))
                #注意：由于此处telnet返回字符串慢一拍，CONTROL DONE出现在下一次read_very_eager中，所以这里特殊处理
                if(ret != 0):
                    s = a+tn.read_very_eager()
                    if("7506 CONTROL DONE" in s):
                        return

                if(debug != 0):
                    self.printstr("LP_VsaDataCapture:"+str(ret)+'\n',QColor(0, 0, 0, 110))
                if(ret != 0):
                    self.t_geterr(ret)
                ret = dll.LP_AnalyzeCWFreq()
                if(debug != 0):
                    self.printstr("LP_AnalyzeCWFreq:"+str(ret)+'\n',QColor(0, 0, 0, 110))
                if(ret != 0):
                    self.t_geterr(ret)

                dll.LP_GetScalarMeasurement.restype = c_double
                frequency = dll.LP_GetScalarMeasurement("frequency", c_int(0))
                if(debug != 0):
                    self.printstr("frequency:"+str(frequency)+'\n',QColor(0, 0, 0, 110))

                f = frequency/1000000 + freq
                if(debug != 0):
                    self.printstr("f:"+str(f)+'\n',QColor(0, 0, 0, 110))
                cmd = self.create_command_pinpian_jiaozhun_xtal(chain, f)
                (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.1, a)
            else:
                return


    def loop_send_cmd_xtal_5g(self, chain, f=5499.873147):
        freq = f
        cmd = self.create_command_pinpian_jiaozhun_xtal(chain, f)
        (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.3, "")
        while(index != 0):
            if(index == -2 or index == -1):
                print "a: ", a
                print "index = ", index
                return index
            elif(index == 1):
                freq = self.get_highter_frequency(freq, [5499.873147,5499.949711,5499.994834])
                cmd = self.create_command_pinpian_jiaozhun_xtal(chain, freq)
                (a, index) = self.telnet_exec_command_fenzhi(cmd, ["7506 CONTROL DONE", "7511 INFO"], 0.3, a)

    def loop_pinpian_jiaozhun(self):
        global dll
        global test_mode
        if(test_mode == 2):
            cmd = self.create_command_pinpian_jiaozhun()
        else:
            cmd = self.create_command_pinpian_jiaozhun_5g()
        if(debug != 0):
            self.printstr(cmd+'\n',QColor(0, 0, 0, 110))
        self.telnet_exec_command(u"频偏校准",cmd,"CONTROL DONE "+cmd, 0, 1, 0)

        if(test_mode == 2):
            self.dll_setvsa(2437, 19, 2)
        else:
            self.dll_setvsa(5500, 19, 2)

        global cdi
        global pcdi
        global cdi_in
        dll.LP_Agc(pcdi,c_bool(True))
        cdi_flag = 0

        i = 0
        while(cdi.value < cdi_flag) and i < 100:
            i = i+1
            dll.LP_Agc(pcdi,c_bool(True))
            # if i>100:
            #     break

        if(test_mode == 2):
            self.loop_send_cmd_xtal_real("1", 2437)
        else:
            self.loop_send_cmd_xtal_real("1", 5500)

    def get_rx_command_iss(self, rate):
        r_list = ["5l","11l","6","54","t7","t8","t15","t16","t23","f7","f8","f15","f16","f23","vt0","vt8","vt10","vt18","vt20","vt29","vf0","vf9","vf10","vf19","vf20","vf29","ve0","ve9","ve10","ve19","ve20","ve29","vt7","vf7","ve7"]
        iss_list = ["-90","-90","-82","-65","-65","-82","-64","-82","-64","-64","-79","-61","-79","-61","-82","-59","-82","-59","-82","-59","-79","-54","-79","-54","-79","-54","-76","-51","-76","-51","-76","-51","-65","-62","-59"]
        r_lower = rate.lower()
        r_lowers = str(r_lower)
        index = r_list.index(r_lowers)
        return iss_list[index]

    def after_rx(self):
        cmd = "commit"
        self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 0, 1)
        cmd = "pcie"
        self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 0, 1)
        cmd = "check"
        self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 0, 1)

    def get_5g_jiaozhun_power(self, freq, chain):
        global jiaozhun_5g_power
        index = freq+"_"+chain
        (first, second) = jiaozhun_5g_power[index]
        return (first, second)









