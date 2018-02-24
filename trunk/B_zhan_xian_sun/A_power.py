#coding=gbk
import telnetlib
import time
import string
from ctypes import *

from trunk.logic import *
# from trunk.bdplug.dbop import *


test_mode = 2
#test_mode = 5
debug = 1

###check###
this_test_result_fail=2
cdi_in = 19.0
cdi = c_double(cdi_in)
pcdi = pointer(cdi)

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

tx_evm_limit = {"6":-5,"54":-25,"11s":-10,"t0":-7,"t4":-18,"t7":-27,"t8":-7,"t12":-18,"t15":-28,"t16":-7,"t20":-18,"t23":-28,"f0":-7,"f7":-28,"f8":-7,
    "f12":-18,"f15":-28,"f16":-7,"f20":-18,"f23":-28,"vt0":-5,"vt8":-30,"vt10":-5,"vt18":-30,"vt20":-5,"vt29":-32,"vf0":-5,"vf9":-32,"vf10":-5,"vf19":-32,
    "vf20":-5,"vf29":-32,"ve0":-5,"ve9":-32,"ve10":-5,"ve19":-32,"ve20":-5,"ve29":-32}


dict_2g_tx = {}


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
        
class Worker_A(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        # QThread.__init__(self, parent)
        conf = TestConf()
        self.ip = conf.get_default_ip()
    # def __del__(self):
    #     self.wait()
    # def render(self, myip):
    #     try:
    #         self.ip = str(myip)
    #     except  Exception as e:
    #         self.printstr(u'抱歉，测试出错了！\n',QColor(255, 0, 0, 220))
    #         self.printstr(u"error: {0}\n".format(e),QColor(255, 0, 0, 220))
    #         self.emit(SIGNAL("terminated()"))
    #         return
    #     self.start()
    def run_A(self):
        self.start()
    def run(self):
        # calculate = Calculate_B()

        self.emit(SIGNAL("begin_test"))
        ping_flag = self.ping_AP(self.ip)
        telnet_flag = self.telnet_default_ip_and_do_something()

        print ping_flag
        if ping_flag==1:
            if telnet_flag==0:
                #开始测试z
                self.do_protest()
            elif telnet_flag == 1:
                # self.printstr(u'抱歉，向AP发送命令时失败！请重试\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                # self.emit(SIGNAL("terminated()"))
                # self.emit(SIGNAL("error_telnet"))
                # self.__del__()
                self.emit(SIGNAL("get_power_false"))
                return
            elif telnet_flag == 3:
                # self.printstr(u'序列号不匹配！请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                # self.emit(SIGNAL("terminated()"))
                # self.emit(SIGNAL("error_telnet"))
                # self.__del__()
                return
            elif telnet_flag == 4:
                # self.printstr(u'基测数据未通过！请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                # self.emit(SIGNAL("terminated()"))
                # self.emit(SIGNAL("error_telnet"))
                # self.__del__()
                return
            elif telnet_flag == 5:
                # self.printstr(u'超出使用次数，请联系管理员\n',QColor(255, 0, 0, 220))
                # # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                # self.emit(SIGNAL("terminated()"))
                # self.emit(SIGNAL("error_telnet"))
                # self.__del__()
                return
            elif telnet_flag == 6:
                # self.printstr(u'老化信息未通过，请检查设备\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                # self.emit(SIGNAL("terminated()"))
                # self.emit(SIGNAL("error_telnet"))
                # self.__del__()
                return
            else:
                # self.printstr(u'抱歉，向AP发送命令式出错！请重试\n',QColor(255, 0, 0, 220))
                # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
                # self.emit(SIGNAL("terminated()"))
                # self.emit(SIGNAL("error_change_mode"))
                # self.__del__()
                return
        else:
            # self.printstr(u'连接错误！请检查设备是否连接正确\n',QColor(255, 0, 0, 220))
            # self.printstr(u"error: {0}\n",QColor(255, 0, 0, 220))
            # self.emit(SIGNAL("terminated()"))
            # self.emit(SIGNAL("error_ping"))
            # self.__del__()
            self.emit(SIGNAL("get_power_false"))
            return
    #
    # def printstr(self,mystr,color):
    #     self.emit(SIGNAL("output"),mystr,color)


    def ping_AP(self,telnet_ip):

        ping_flag = os.system("ping "+telnet_ip)
        if ping_flag:
            return 0
        else:
            return 1

    def get_this_mac_address(self):
        import uuid
        node = uuid.getnode()
        mac = uuid.UUID(int = node).hex[-12:]
        return mac

    #对AP进行telnet操作，并改变AP的模式
    def telnet_default_ip_and_do_something(self):
        global tn
        testconf = TestConf()
        telnet_ip = testconf.get_default_ip()
        # if self.ping_AP(telnet_ip):
        # myform = MyForm()
        myconf = MyConf()


        try:
            testconf = TestConf()
            username = testconf.get_username()
            password = testconf.get_password()

            telnet_ip = testconf.get_default_ip()

            tn = telnetlib.Telnet(telnet_ip)
            login_str = tn.read_until("login: ")
            tn.write(username+'\n')


            password_str = tn.read_until("Password: ")
            tn.write(password +'\n')
            tn.read_until("~#")

            time.sleep(1)

            # #获得序列号
            # tn.write("ar_protest --MB-SN -r\n")
            # sn_str = tn.read_until("~#")#需要具体查看str是什么
            #校验序列号是否匹配

            # print sn_str
            # input_sn = myconf.get_sn_num()
            # if input_sn not in sn_str:
            #     return 3#序列号不匹配

            #校验ipx使用次数是否合格

            this_mac = self.get_this_mac_address()#获得当前mac地址
            # this_mac_ipx = dbop_temp.getIPXInterfaceByMac(this_mac)#获得已经使用次数
            # this_mac_max_ipx = dbop_temp.getIPXMaxCount(this_mac)#获得最大使用次数
            # this_mac_ipx = 100
            # this_mac_max_ipx = 10000
            # if this_mac_ipx > this_mac_max_ipx:
            #     return 5#超出使用次数



            #老化信息是否通过
            # tn.write("agtest result\n")
            #
            # old_results = tn.read_until("~#")
            #
            # old_results_list = old_results.split("\n")
            #
            # old_hour = old_results_list[6].split(" ")
            # this_hour = old_hour[6].replace(' ','').replace('\r','')

            # if "Failed" in old_results_list[1] or "Failed" in old_results_list[3] or "Failed" in old_results_list[5]:
            #     return 6 #老化信息未通过

            #校验基测数据是否通过
            # base_test_resutlt = dbop_temp.getBaseTestBySN(sn_str)
            # base_test_resutlt = True
            # if base_test_resutlt == False:
            #     return 4#基测数据未通过

            # 在这块获得是否要执行ar_protest --art
            # 同时发送命令获得序列号，，和扫描后获得的序列号对比，如果相等返回成功，程序继续进行。
            # 否则返回错误。程序不继续进行。
            # time.sleep(5)
            #

            current_mode = "lsmod | grep art"#获得ap当前模式的命令
            tn.write(current_mode +'\n')
            current_mode_return = tn.read_until("~#")
            if "art  " not in current_mode_return :
                cmd_change_mode = "ar_protest --art"
                tn.write(cmd_change_mode +'\n')
                time.sleep(5)
            return 0
        except:
            return 1



    def do_protest(self):
        global test_mode
        global test_result_fail
        testconfig = TestConf()
        how_to_do_test = "2"
        test_result_fail = 0
        
        #初始化测试仪器的dll
        self.dll_init()
        self.dll_getversion()
        self.mask_dll_init()

        if(how_to_do_test == '0' or how_to_do_test == '2'):
            test_mode = 2
            self.protest()
        if(how_to_do_test == '1' or how_to_do_test == '2'):
            test_mode = 5
            self.protest()
        
        dll.LP_Term()#??????s

    def protest(self):
        global tn
        global dll
        global freq_2g_ht20, rate_2g_ht20, chain
        global debug
        global path_loss_2g, path_loss_5g
        myip = self.ip
        testconf = TestConf()
        testconfxml = TestConfigxml()
        #获取配置信息 2G和5G
        version = Version_ini()

        this_version = version.get_version()

        power_limit_ht20_2G = string.atof(testconfxml.get_2g_power_limit_ht20())
        power_limit_ht40_2G = string.atof(testconfxml.get_2g_power_limit_ht40())
        power_limit_ht20_5G = string.atof(testconfxml.get_5g_power_limit_ht20())
        power_limit_ht40_5G = string.atof(testconfxml.get_5g_power_limit_ht40())
        
        #self.do_get_setting()
        #测试模式不同选择不同的端口号。
        try:

            if(test_mode == 5):
                time.sleep(3)
                tn = telnetlib.Telnet(myip, port=testconf.get_5g_default_port())
            elif(test_mode == 2):
                time.sleep(3)
                tn = telnetlib.Telnet(myip, port=testconf.get_2g_default_port())

        except Exception as e:
            # self.printstr(u'抱歉，测试出错了！\n',QColor(255, 0, 0, 220))
            # self.printstr(u"error({0}): {1}\n".format(e.errno, e.strerror),QColor(255, 0, 0, 220))
            self.emit(SIGNAL("get_power_false"))
            return


        if(test_mode == 2):

            # self.printstr('\n\n###########  2G warmup 热身 ###############\n',QColor(0, 0, 0, 110))
            self.set_mac_command()
            print "load"
            self.warmup("2412")
            myconfig_a = Conf_A()
            freq_alls =myconfig_a.get_2g_items()
            # self.printstr('\n\n###########  2G HT20 测试项开始测试  ###############\n',QColor(0, 0, 0, 110))
            # tx_ht20_freq = ["2412", "2437", "2452", "2452", "2452", "2452", "2452", "2452", "2452", "2452"]
            tx_ht20_rate = ["54"]
            if this_version == "WE2622":
                tx_ht20_chain = ["1", "2"]
            else:
                tx_ht20_chain = ["1","2","4"]
            freq_all = {}
            self.emit(SIGNAL("testing"))

            for freqs in freq_alls:
            #     if string.atof(freqs[0])<5000:
                self.loop_tx(freqs[0], tx_ht20_rate, tx_ht20_chain)
            print "end++++++++++++++++++++++++"
        elif(test_mode == 5):

            # self.printstr('\n\n###########  5G warmup  ###############\n',QColor(0, 0, 0, 110))
            cmd_load_devid="load devid=3c;memory=flash;"
            self.telnet_exec_command(u"校准命令", cmd_load_devid, "CONTROL DONE ", 1, 0,1)

            self.telnet_exec_command(u"测试","hello","CONTROL DONE "+"hello", 1, 0, 1)

            myconfig_a = Conf_A()
            freq_alls =myconfig_a.get_5G_items()
            # self.printstr('\n\n###########  2G HT20 测试项开始测试  ###############\n',QColor(0, 0, 0, 110))
            # tx_ht20_freq = ["2412", "2437", "2452", "2452", "2452", "2452", "2452", "2452", "2452", "2452"]
            tx_ht20_rate = ["54"]
            if this_version == "WE2622":
                tx_ht20_chain = ["1", "2"]
            else:
                tx_ht20_chain = ["1","2","4"]
            freq_all = {}
            self.emit(SIGNAL("testing"))
            self.warmup("5180")
            for freqs in freq_alls:
                # if string.atof(freqs[0])>5000:
                self.loop_tx(freqs[0], tx_ht20_rate, tx_ht20_chain)
            print "end+++++++++++++++++++++++++++++++"
            # self.emit(SIGNAL("get_power_true"))
            self.emit(SIGNAL("get_power_true"))
    def telnet_exec_command(self, name, cmd, finish, print_a, start, read_s = 1):
        global tn
        s=""
        try:
            tn.write(cmd+"\n")
            if(start != 0):
                tn.write("START\n")
        except Exception as e:
            return
        if(read_s != 0):
            s = tn.read_until(finish)
        return s
    


    def telnet_exec_stop(self, finish, print_a = 1):
        try:
            tn.write("STOP\n")
        except Exception as e:
            return
        s = tn.read_until(finish)
        return s
    


    def set_mac_command(self):
        cmd_1="load devid=3f;memory=flash"
        cmd_4 = "hello"
        self.telnet_exec_command(u"加载——art文件之前", cmd_1, "CONTROL DONE", 1, 0,1)
        print cmd_1
        print cmd_4
        self.telnet_exec_command(u"加载——art文件之前", cmd_4, "CONTROL DONE", 1, 0,1)






    def t_geterr(self, errcode):
        dll = cdll.LoadLibrary('IQmeasure.dll');  
        pcName = c_char_p('/0'*200)
        pcName = dll.LP_GetErrorString(errcode)
        err = string_at(pcName,200)

    def dll_init(self):
        global dll
        dll = cdll.LoadLibrary('IQmeasure.dll');  
        ret = dll.LP_Init(c_int(1),c_int(0));
        # if(debug != 0):
        #     self.printstr("LP_Init:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        ret = dll.LP_InitTester("192.168.100.254", c_int(0));
        # if(debug != 0):
        #     self.printstr("LP_InitTester:"+str(ret)+'\n',QColor(0, 0, 0, 110))
    
    def mask_dll_init(self):
        #加载dll文件
        global mask_dll
        mask_dll = cdll.LoadLibrary('MaskDll.DLL');  
    
    def dll_getversion(self):
        global dll
        strMa = "/0"*200  
        FunPrint  = dll.LP_GetVersion  
        FunPrint.argtypes = [c_char_p, c_int]  
        nRst = FunPrint(strMa, len(strMa))  
        # self.printstr(strMa+'\n',QColor(0, 0, 0, 110))


    def dll_setvsa(self, rfFreqHz, rfAmplDb, port, extAttenDb = 0, triggerLevelDb = -25, triggerPreTime = 10e-6, dFreqShiftHz = 0.0, dTriggerGapTime = 6e-6):
        ret = dll.LP_SetVsa(c_double(rfFreqHz*1e6), c_double(rfAmplDb), c_int(port), c_double(extAttenDb), c_double(triggerLevelDb), c_double(triggerPreTime), c_double(dFreqShiftHz), c_double(dTriggerGapTime));
        # self.printstr("ret:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(ret != 0):
            self.t_geterr(ret)
    
    def str_find_tp(self, ttp_str):
        s = ttp_str.split("||")
        return s[3]
    
    def create_command_tx(self, freq, rate, chain, tp):
        cmd_tx = "tx f="+freq+";ir=0;gi=0;txch="+chain+";rxch=7;pc=1000000;pl=4000;bc=1;retry=0;att=0;iss=0;stat=3;ifs=1;dur=600000;dump=0;pro=0;bssid=50.55.55.55.55.05;mactx=20.22.22.22.22.02;macrx=10.11.11.11.11.01;deaf=0;reset=-1;duc=99;agg=1;ht40=2;r="+rate+";tp="+tp+";"
        return cmd_tx

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


    def loop_tx(self, freq, rate_all, chain_all):
        testconfxml = TestConfigxml()
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
        # for freqs in freq_all:
        # # for freq in freq_all:
        #     freq = freqs[0]
        rate_this = rate_all
        chain_this = chain_all
        for rate in rate_this:
            for chain in chain_this:
                list ={}

                testconf = TestConf()
                d_type = self.rate_to_type(rate)
                print freq+"***********"
                # print d_type+"++++++++++++++++"
                cmd_gettp = "gettp f="+freq+"; r="+rate+";"
                ttpstr = self.telnet_exec_command(u"测试",cmd_gettp,"CONTROL DONE "+cmd_gettp, 1, 0, 1)
                # self.printstr("ttpstr:"+ttpstr+'\n',QColor(0, 0, 0, 110))
                tp = self.str_find_tp(ttpstr)
                # print "+++++++++++"+str(tp)
                # self.printstr("tp:"+tp+'\n',QColor(0, 0, 0, 110))
                cmd = self.create_command_tx(freq, rate, chain, tp)

                self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 1, 0)

                if(rate == "f0" or rate == "f7" or rate == "vf0" or rate== "vf9"):

                    if d_type == "80211ac" or d_type =="80211ag" or d_type =="80211n":
                        self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+10, 2)
                    else:
                        self.dll_setvsa(string.atoi(freq)+10, string.atof(tp)+4, 2)
                else:

                    if d_type == "80211ac" or d_type =="80211ag"or d_type =="80211n":
                        self.dll_setvsa(string.atoi(freq), string.atof(tp)+10, 2)
                    else:
                        self.dll_setvsa(string.atoi(freq), string.atof(tp)+4, 2)

                time.sleep(0.2)
                r = rate.lower()
                time_var = capture_time[r]
                lost = self.get_lost_from_xiansunini(freq,chain)
                print "lost:"+str(lost)

                loop_capture = string.atoi(testconf.get_B_station_loop_capture())
                for i in range(loop_capture):
                    ret = dll.LP_VsaDataCapture(c_double(time_var*1e-6), c_int(6), c_double(160e6), c_int(0), c_int(0))
                    if(ret != 0):
                        self.t_geterr(ret)

                    dll.LP_GetScalarMeasurement.restype = c_double

                    P_av_no_gap_all_dBm = string.atof(self.get_power_2(rate)) + lost
                    P_av_no_gap_all_dBm = round(P_av_no_gap_all_dBm,2)

                    list[i] = P_av_no_gap_all_dBm
                    print "..."+str(i)+"..."+str(list[i])
                self.telnet_exec_stop("CONTROL DONE "+cmd)
                pav =round(sum(list.values())/len(list),2)
                print "_________"+str(pav)+"\n\n"


                conf_A = Conf_A()
                if string.atof(freq)>5000:
                    conf_A.set_5g_power(freq,chain,pav)
                else:

                    conf_A.set_2g_power(freq, chain, pav)








    def get_lost_from_xiansunini(self,this_freq, chain):
        xiansunini = Xian_Sun_ini()
        if string.atoi(this_freq) <5000:

            return xiansunini.get_xiansun_ini(this_freq, chain, "2G")
        else:
            return xiansunini.get_xiansun_ini(this_freq, chain, "5G")





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
        self.telnet_exec_command(u"测试",cmd,"CONTROL DONE ", 1, 1, 1)

    



    
    def get_power(self, rate):
        r = rate
        time = capture_time[r]
        # if(debug != 0):
        #     self.printstr("capture time:"+str(time)+'\n',QColor(0, 0, 0, 110))

        ret = dll.LP_VsaDataCapture(c_double(time*1e-6), c_int(6), c_double(160e6), c_int(0), c_int(0))
        # if(debug != 0):
        #     self.printstr("LP_VsaDataCapture:"+str(ret)+'\n',QColor(0, 0, 0, 110))
        if(ret != 0):
            self.t_geterr(ret)
        ret = dll.LP_AnalyzePower(c_double(0.0), c_double(0.0))
        if(ret != 0):
            self.t_geterr(ret)
        dll.LP_GetScalarMeasurement.restype = c_double
        P_av_no_gap_all_dBm = dll.LP_GetScalarMeasurement("P_av_no_gap_all_dBm", c_int(0));
        # if(debug != 0):
        #     self.printstr("P_av_no_gap_all_dBm:"+str(P_av_no_gap_all_dBm)+'\n',QColor(0, 0, 0, 110))
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
    

    def get_highter_frequency(self, freq, freq_pool):
        for fi in freq_pool:
            if(fi > freq):
                return fi
        return 2436.995804
    

    def get_frequency(self):
        r = "6"
        time = capture_time[r]
        ret = dll.LP_VsaDataCapture(c_double(time*1e-6), c_int(6), c_double(160e6), c_int(0), c_int(0))
        if(ret != 0):
            self.t_geterr(ret)
        ret = dll.LP_AnalyzeCWFreq()
        if(ret != 0):
            self.t_geterr(ret)

        dll.LP_GetScalarMeasurement.restype = c_double
        frequency = dll.LP_GetScalarMeasurement("frequency", c_int(0))
        return frequency
    

    # def after_rx(self):
    #     cmd = "commit"
    #     self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 0, 1)
    #     cmd = "pcie"
    #     self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 0, 1)
    #     cmd = "check"
    #     self.telnet_exec_command(u"测试",cmd,"CONTROL DONE "+cmd, 1, 0, 1)





class Conf_A():
    def __init__(self):
        myconfig = MyConf()
        power_A_address = myconfig.get_power_A_B_save_address()
        self.filename = power_A_address+"\\"+"power_A.ini"
    # def get_all_items(self):
    #     conf = Conf(self.filename)
    #     items = conf.getItems("power")
    #     return items
    def get_2g_items(self):
        conf = Conf(self.filename)
        items = conf.getItems("2G")
        return items


    def get_5G_items(self):
        conf = Conf(self.filename)
        items = conf.getItems("5G")
        return items

    def set_2g_power(self, freq, chain,power):
        conf = Conf(self.filename)
        conf.setSection("2G")
        powers = conf.getValue("2G",freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index-1] = str(power)
        power_str = ",".join(power_list)
        conf.setValue("2G", freq, power_str)
        # conf.write(open(self.filename,'r'))
    def set_5g_power(self, freq, chain,power):
        conf = Conf(self.filename)
        conf.setSection("5G")
        powers = conf.getValue("5G",freq)

        power_list = powers.split(',')
        index = string.atoi(chain)
        power_list[index-1] = str(power)
        power_str = ",".join(power_list)
        conf.setValue("5G", freq, power_str)
        # conf.write(open(self.filename,'r'))
    def get_2g_power(self, freq, chain):
        conf = Conf(self.filename)
        power_str = conf.getValue("2G", freq)
        power_list = power_str.split(',')

        return power_list[string.atoi(chain)-1]

    def get_5g_power(self, freq, chain):
        conf = Conf(self.filename)
        power_str = conf.getValue("5G", freq)
        power_list = power_str.split(',')

        return power_list[string.atoi(chain)-1]
