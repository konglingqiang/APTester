#coding=gbk

from trunk.bdplug.exchangeData import *
import time
import json

###����У׼��������ݿ���ز���
class DataBaseOP(object):
    ###�����û������룬��֤�û�Ȩ��###
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

    ###��ȡSN���Ӧ�Ļ������״̬###
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

    ###��ȡ��ʼ��sn###
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

    ###��Ӳ�������###
    def saveRFTestLog(self,testSQLJson):
        eData = ExchangeData()
        json_data = json.loads(self.dbTrim(testSQLJson))
        sn = json_data['_sn']
        sn = self.getBoardTestInfo(sn)
        setSql = 'insert into rftestItem(rfTest,itemTestTime,channelNo,frequency,standard_rf,targetPower,power_rf,delta,isPowerPass,evm,targetEvm,evm_delta,isEvmPass,freq,targetFreq,freq_delta,isFreqPass,spectrum,excessivePower,isPass) values (\''+sn+'\',\''+str(json_data['_currentTime'])+'\',\''+str(json_data['_channelNo'])+'\',\''+str(json_data['_frequency'])+'\',\''+str(json_data['_standardRF'])+'\',\''+str(json_data['_targetPower'])+'\',\''+str(json_data['_rate'])+'\',\''+str(json_data['_powerDelta'])+'\',\''+str(json_data['_isPowerPass'])+'\',\''+str(json_data['_evm'])+'\',\''+str(json_data['_targetEvm'])+'\',\''+str(json_data['_evmDelta'])+'\',\''+str(json_data['_isEvmPass'])+'\',\''+str(json_data['_freq'])+'\',\''+str(json_data['_targetFreq'])+'\',\''+str(json_data['_freqDelta'])+'\',\''+str(json_data['_isFreqPass'])+'\',\''+str(json_data['_spectrum'])+'\',\''+str(json_data['_excessivePower'])+'\',\''+str(json_data['_isPass'])+'\')'
        setSql = self.dbTrim(setSql)
        print setSql
        eData.setDataBySql(setSql)

    ###��ȡ��Ӧmac��ipxʹ�ô���###
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

    ###����mac��Ӧ��IPXʹ�ô���###
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

    ###��ȡָ��mac�����²���״̬###
    def getAPLatestStatusByApSn(self,snStr):
        querySql = 'SELECT status FROM aptesterinfo WHERE sn = \''+snStr+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if len(dataRows)>0:
            return dataRows[0][0]
        else:
            return None

    ###��ȡָ��mac�����²���״̬###
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
    ###��ȡָ��sn�����²���״̬###
    def getAPLatestStatusBySN(self,sn,testStep_str):
        querySql = 'SELECT state FROM testResultTable WHERE sn = \''+sn+'\' and testStep = \''+testStep_str+'\''
        querySql = self.dbTrim(querySql)
        eData = ExchangeData()
        dataRows = eData.getDataBySql(querySql)
        if len(dataRows)>0:
            return dataRows[0][0]
        else:
            return None

    ###����AP���²���״̬###
    ###������SN������״̬���û�����pcmac��վ�㣨A/B��###
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

    ###�޸�����###
    def resetDBPwd(self,userName,oldPwd,newPwd):
        igStatus = self.loginApTester(userName,oldPwd)
        if igStatus>0:
            setSql = 'UPDATE bdcomemployee SET bdcomPassword = \''+newPwd+'\' WHERE bdcomLoginName = \''+userName+'\' AND bdcomPassword = \''+oldPwd+'\''
            self.dbTrim(setSql)
            eData = ExchangeData()
            return eData.setDataBySql(setSql)
        else:
            return False;


    ###��ȡIPX�������ʹ�ô���###
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

    ###��ȡ�ظ����Դ���###
    def getRetestCount(self):
        eData = ExchangeData()
        return eData.loadTestConfig('RETEST',None)

    ###��ȡPING������###
    def getPingMaxCount(self):
        eData = ExchangeData()
        return eData.loadTestConfig('PING',None)

    ###��ȡ�ϻ�ʱ�����Сʱ��###
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