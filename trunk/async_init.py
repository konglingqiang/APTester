from ctypes import cdll, c_int

__author__ = 'kaikai'

from trunk.myconfig import *

if __name__ == "__main__":
    config = MyConf()
    IQ_connect = config.get_IQ_connect()
    global dll
    dll = cdll.LoadLibrary('./IQmeasure.dll');
    ret = dll.LP_Init(c_int(1),c_int(0));
    ret = dll.LP_InitTester(IQ_connect, c_int(0));

    async_ret = dll.LP_Async_Init()