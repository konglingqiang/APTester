#coding=gbk

from trunk.bdplug.exchangeData import *
import time
import json

###无线校准软件，数据库相关操作
class DataBaseOP(object):
    ###根据用户名密码，验证用户权限###
    def loginApTester(self,username,password):
        loginSql = 'SELECT rid FROM bdcomemployee WHERE bdcomLoginName = \''+username+'\' AND bdcomPassword = \''+password+'\''
        loginSql = self.dbTrim(loginSql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(loginSql)
        if len(dataRows)==0 or dataRows[0] is None:
            return 0
        elif dataRows[0][0]==17:
            return 2
        else:
            return 1

    ###读取SN码对应的基测测试状态###
    def getBaseTestBySN(self,sn):
        querySql = 'SELECT boardStatus FROM substrate WHERE boardID = \''+sn+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if dataRows is None or len(dataRows)==0:
            return False

        dataRow = dataRows[0]
        boardStatus = str(dataRow[0])
        if boardStatus.__contains__('1Y'):
            return True
        else:
            return False

    def getWorkOrderInfoBySn(self,sn):
        querySql = 'select workorderno,lineflag from subworkorder where id = (SELECT subworkorderno FROM substrate WHERE  boardid = \''+sn+'\')'
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if dataRows is None or len(dataRows)==0:
            return ''
        dataRow = dataRows[0]
        orderNo = str(dataRow[0])
        orderLineNo = str(dataRow[0])
        return orderNo,orderLineNo

    ###获取初始化sn###
    def getBoardTestInfo(self,sn):
        querySql = 'select * from rftest where baseSerialNo = \''+sn+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        print 'Query Sql'
        print querySql
        dataRows = eData.getDataBySql(querySql)
        if dataRows is None or len(dataRows)==0:
            # (workOrderNo,workOrderLineNo) = self.getWorkOrderInfoBySn(sn)
            # insertSql = 'insert into rftest(baseSerialNo,workOrderNo,workOrderLineNo) values (\''+sn+'\',\''+workOrderNo+'\',\''+workOrderLineNo+'\')'
            insertSql = 'insert into rftest(baseSerialNo,testTime) values (\'' + sn + '\',\''+time.strftime("%Y-%m-%d %H:%M:%S")+'\')'
            insertSql = self.dbTrim(insertSql)
            print 'insrtSql:'+insertSql
            eData.setDataBySql(insertSql)
        return sn

    ###添加测试数据###
    def saveRFTestLog(self,testSQLJson):
        eData = ExchangeData()
        json_data = json.loads(self.dbTrim(testSQLJson))
        sn = json_data['_sn']
        sn = self.getBoardTestInfo(sn)
        setSql = 'insert into rftestItem(rfTest,itemTestTime,channelNo,frequency,standard_rf,targetPower,power_rf,delta,isPowerPass,evm,targetEvm,evm_delta,isEvmPass,freq,targetFreq,freq_delta,isFreqPass,spectrum,excessivePower,isPass) values (\''+sn+'\',\''+str(json_data['_currentTime'])+'\',\''+str(json_data['_channelNo'])+'\',\''+str(json_data['_frequency'])+'\',\''+str(json_data['_standardRF'])+'\',\''+str(json_data['_targetPower'])+'\',\''+str(json_data['_rate'])+'\',\''+str(json_data['_powerDelta'])+'\',\''+str(json_data['_isPowerPass'])+'\',\''+str(json_data['_evm'])+'\',\''+str(json_data['_targetEvm'])+'\',\''+str(json_data['_evmDelta'])+'\',\''+str(json_data['_isEvmPass'])+'\',\''+str(json_data['_freq'])+'\',\''+str(json_data['_targetFreq'])+'\',\''+str(json_data['_freqDelta'])+'\',\''+str(json_data['_isFreqPass'])+'\',\''+str(json_data['_spectrum'])+'\',\''+str(json_data['_excessivePower'])+'\',\''+str(json_data['_isPass'])+'\')'
        setSql = self.dbTrim(setSql)
        print setSql
        eData.setDataBySql(setSql)

    ###读取对应mac的ipx使用次数###
    def getIPXInterfaceByMac(self,macStr):
        querySql = 'SELECT useCount FROM ipxinfo WHERE pc_mac = \''+macStr+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if dataRows is None or len(dataRows)==0:
            return 0
        else:
            useCountData = dataRows[0]
            return int(useCountData[0])

    ###设置mac对应的IPX使用次数###
    def setIPXInterfaceByMac(self,macStr):
        setSql = 'SELECT useCount FROM ipxinfo WHERE pc_mac = \''+macStr+'\''
        setSql = self.dbTrim(setSql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(setSql)
        useCount = 1
        if len(dataRows)>0:
            currentCount = dataRows[len(dataRows)-1][0]
            useCount = currentCount+useCount
            setSql = 'UPDATE ipxinfo SET useCount = '+str(useCount)+' where pc_mac = \''+macStr+'\''
        else:
            setSql = 'INSERT INTO ipxinfo(useCount,pc_mac) VALUES ('+str(useCount)+',\''+macStr+'\')'
        setSql = self.dbTrim(setSql)
        return eData.setDataBySql(setSql)

    ###读取指定mac的最新测试状态###
    def getAPLatestStatusByApSn(self,snStr):
        querySql = 'SELECT status FROM aptesterinfo WHERE sn = \''+snStr+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if len(dataRows)>0:
            return dataRows[0][0]
        else:
            return None

    ###读取指定mac的最新测试状态###
    def getAPLatestStatusByApMac(self,apMacStr):
        querySql = 'SELECT status FROM aptesterinfo WHERE ap_mac = \''+apMacStr+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if len(dataRows)>0:
            return dataRows[0][0]
        else:
            return None
    def getAPPreTestStateBySN(self,sn):
        querySql = 'SELECT state FROM testResultTable WHERE sn = \''+sn+'\' and ( testStep = \'test2G\' or testStep = \'test5G\' )'
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if len(dataRows)>0:
            return dataRows[-1]
        else:
            return None
    ###读取指定sn的最新测试状态###
    def getAPLatestStatusBySN(self,sn,testStep_str):
        querySql = 'SELECT state FROM testResultTable WHERE sn = \''+sn+'\' and testStep = \''+testStep_str+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if len(dataRows)>0:
            return dataRows[0][0]
        else:
            return None

    ###设置AP最新测试状态###
    ###参数：SN，最新状态，用户名，pcmac，站点（A/B）###
    def setAPStatusBySn(self,snStr,status,userName,pcMac,station,rate):
        setSql = ""
        testStep_str = ""
        testTime = time.time()
        stime = time.localtime(testTime)
        strtime = time.strftime("%Y-%m-%d %H:%M:%S",stime)
        tTime = str(strtime)

        if station == 'test':
            if rate=='2.4':
                testStep_str = 'test2G'
            else:
                testStep_str = 'test5G'
        else:
            if rate=='2.4':
                testStep_str = 'check2G'
            else:
                testStep_str = 'check5G'
        # snStatus = self.getAPLatestStatusBySN(snStr,testStep_str)
        # if snStatus is None:
        setSql = 'INSERT INTO testResultTable(sn,testStep,state,testDate,randomId) VALUES (\''+snStr+'\',\''+testStep_str+'\',\''+status+'\',\''+tTime+'\',\''+pcMac+'\')'
        # else:
        #     setSql = 'UPDATE testResultTable SET state = \''+status+'\',testDate = \''+tTime+'\' WHERE sn= \''+snStr+'\' and testStep = \''+testStep_str+'\''
        self.dbTrim(setSql)
        eData = ExchangeData()
        return eData.setDataBySql(setSql)

    ###修改密码###
    def resetDBPwd(self,userName,oldPwd,newPwd):
        igStatus = self.loginApTester(userName,oldPwd)
        if igStatus>0:
            setSql = 'UPDATE bdcomemployee SET bdcomPassword = \''+newPwd+'\' WHERE bdcomLoginName = \''+userName+'\' AND bdcomPassword = \''+oldPwd+'\''
            self.dbTrim(setSql)
            eData = ExchangeData()
            return eData.setDataBySql(setSql)
        else:
            return False;


    ###读取IPX允许最大使用次数###
    def getIPXMaxCount(self,macStr):
        querySql = 'SELECT maxCount FROM ipxinfo WHERE pc_mac = \''+macStr+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if dataRows is None or len(dataRows)==0:
            ipxMaxCount = eData.loadTestConfig('IPX',macStr)
            setSql = 'INSERT INTO ipxinfo(useCount,maxCount,pc_mac) VALUES (0,'+str(ipxMaxCount)+',\''+macStr+'\')'
            setSql = self.dbTrim(setSql)
            eData.setDataBySql(setSql)
            return 0
        else:
            useCountData = dataRows[0]
            return int(useCountData[0])

    ###读取重复测试次数###
    def getRetestCount(self):
        eData = ExchangeData()
        return eData.loadTestConfig('RETEST',None)

    ###读取PING最大次数###
    def getPingMaxCount(self):
        eData = ExchangeData()
        return eData.loadTestConfig('PING',None)

    ###读取老化时间最大小时数###
    def getPingMaxCount(self):
        eData = ExchangeData()
        return eData.loadTestConfig('AGETEST',None)

    def dbTrim(self,trimStr):
        return str(trimStr).replace('\t','').replace('\n','').replace('\r','')

if __name__ == '__main__':
    dbop = DataBaseOP()
    result = dbop.getAPPreTestStateBySN('0259307200002')
    print str(result)
    # dbop.loginApTester('liuke_ap','liuke')