# -*- coding: utf-8 -*-
__author__ = 'hero'
import pymssql
import xml.dom.minidom
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
class ExchangeData(object):
    global CONFIGTYPE_RETEST
    global CONFIGTYPE_PING
    global CONFIGTYPE_AGETEST
    global CONFIGTYPE_IPX

    CONFIGTYPE_RETEST = 'RETEST'
    CONFIGTYPE_PING = 'PING'
    CONFIGTYPE_AGETEST = 'AGETEST'
    CONFIGTYPE_IPX = 'IPX'

    def loadTestConfig(self,configtype,mac_add):
        try:
            xmlDoc = xml.dom.minidom.parse(os.getcwd()+'\\conf\\TestConfig.xml')
            root = xmlDoc.documentElement
            if configtype == CONFIGTYPE_IPX:
                ipxEle = root.getElementsByTagName(configtype)[0]
                countInfos = ipxEle.getElementsByTagName('COUNT_INFO')
                for countInfo in countInfos:
                    if(countInfo.getElementsByTagName('MAC_ADD')[0].firstChild.data==mac_add):
                        return countInfo.getElementsByTagName('MAX_COUNT')[0].firstChild.data
                return 0
            else:
                cdate = root.getElementsByTagName(configtype)[0]
                return cdate.getElementsByTagName('MAX_COUNT')[0].firstChild.data
        except Exception,e:
            print(e)
            return 0

    ###加载数据库连接数据
    def loadDBConfig(self,dbType):
        # xmlDoc = xml.dom.minidom.parse('DBConfig.xml')
        xmlDoc = xml.dom.minidom.parse(os.getcwd() +'\\conf\\/DBConfig.xml')
        # xmlDoc = xml.dom.minidom.parse(os.getcwd() +'\\conf\\/DBConfig.xml')如果找不到配置文件则使用这个
        root = xmlDoc.documentElement
        sql_element = root.getElementsByTagName(dbType)[0]
        return sql_element

    def __exchangeDataByDBConnection(self):
        sqlInfo = self.loadDBConfig('MSSQL')
        db_host = sqlInfo.getElementsByTagName('HOST')[0].firstChild.data
        db_database = sqlInfo.getElementsByTagName('DATABASE')[0].firstChild.data
        db_user = sqlInfo.getElementsByTagName('USERNAME')[0].firstChild.data
        db_pwd = sqlInfo.getElementsByTagName('PASSWORD')[0].firstChild.data
        conn = pymssql.connect(user=db_user,password=db_pwd,database=db_database,host=db_host)
        conn.autocommit(True)
        return conn


    ###读取数据###
    def getDataBySql(self,sqlStr):
        try:
            conn = self.__exchangeDataByDBConnection()
            if not conn:
                raise(NameError,'数据库连接失败')
            else:
                cur = conn.cursor()
                cur.execute(sqlStr)
                resList = cur.fetchall()
                conn.close()
                return resList
        except Exception,e:
            print(e)
            raise(NameError,'数据库操作失败')

    ###更改数据库###
    def setDataBySql(self,sqlStr):
        try:
            conn = self.__exchangeDataByDBConnection()
            if not conn:
                raise(NameError,'数据库连接失败')
                return False
            else:
                cur = conn.cursor()
                cur.execute(sqlStr)
                conn.commit()
                conn.close()
                return True
        except Exception,e:
            print(e)
            raise(NameError,'数据库操作失败')
            return False

if __name__ == '__main__':
    pn = 'BYAUX-CTN0003'
    sqlStr = "select * from producttype where productNo = '"+pn+"'"
    edata = ExchangeData()
    resList = edata.getDataBySql(sqlStr=sqlStr)
    for dataRow in resList:
        print(dataRow[0])