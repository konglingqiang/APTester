#coding=gbk
__author__ = 'hero'
import datetime
import json

#产测软件log bean
class RFtest(object):
    #初始化方法
    def __init__(self,serialNo):
        self.setSN(serialNo)
        currentTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.setCurrentTime(currentTime)

    def setSN(self,serialNo):
        self._sn = serialNo

    def getSN(self):
        return self._sn

    def setCurrentTime(self,ctime):
        self._currentTime = ctime

    def getCurrentTime(self):
        return self._currentTime

    def setChannelNo(self,channelNo):
        self._channelNo = channelNo

    def getChannelNo(self):
        return self._channelNo

    def setFrequency(self,frequency):
        self._frequency = frequency

    def getFrequency(self):
        return self._frequency

    def setStandardRF(self,standardRF):
        self._standardRF = standardRF

    def getStandardRF(self):
        return self._standardRF

    def setRate(self,rate):
        self._rate = rate

    def getRate(self):
        return self._rate

    def setPower(self,power):
        self._power = power

    def getPower(self):
        return self._power

    def setTargetPower(self,targetPower):
        self._targetPower = targetPower

    def getTargetPower(self):
        return self._targetPower

    def setPowerDelta(self,powerDelta):
        self._powerDelta = powerDelta

    def getPowerDelta(self):
        return self._powerDelta

    def setIsPowerPass(self,isPowerPass):
        self._isPowerPass = isPowerPass

    def getIsPowerPass(self):
        return self._isPowerPass

    def setEvm(self,evm):
        self._evm = evm

    def getEvm(self):
        return self._evm

    def setTargetEvm(self,targetEvm):
        self._targetEvm = targetEvm

    def getTargetEvm(self):
        return self._targetEvm

    def setEvmDelta(self,evmDelta):
        self._evmDelta = evmDelta

    def getEvmDelta(self):
        return self._evmDelta

    def setIsEvmPass(self,isEvmPass):
        self._isEvmPass = isEvmPass

    def getIsEvmPass(self):
        return self._isEvmPass

    def setFreq(self,freq):
        self._freq = freq

    def getFreq(self):
        return self._freq

    def setTargetFreq(self,targetFreq):
        self._targetFreq = targetFreq

    def getTargetFreq(self):
        return self._targetFreq

    def setFreqDelta(self,freqDelta):
        self._freqDelta = freqDelta

    def getFreqDelta(self):
        return self._freqDelta

    def setIsFreqPass(self,isFreqPass):
        self._isFreqPass = isFreqPass

    def setSpectrum(self,spectrum):
        self._spectrum = spectrum

    def getSpectrum(self):
        return self._spectrum

    def setExcessivePower(self,excessivePower):
        self._excessivePower = excessivePower

    def getExcessivePower(self):
        return self._excessivePower

    def setIsPass(self,isPass):
        self._isPass = isPass

    def getIsPass(self):
        return self._isPass