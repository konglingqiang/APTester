from trunk.bdplug.dbop import *
#
data_base = DataBaseOP()
# import trunk.bdplug.exchangeData
jsonstr='{"_evm": -99999.99, "_freq": -1.92, "_evmDelta": 99989.99, "_standardRF": "11B", "_sn": "yyyyy", "_powerDelta": -0.3299999999999983, "_frequency": "2412", "_isFreqPass": 1, "_freqDelta": 16.92, "_power": 26.67, "_currentTime": "2017/12/06 14:07:58", "_targetPower": "27.0", "_rate": "11s", "_isEvmPass": 1, "_channelNo": "2", "_targetFreq": 15.0, "_isPass": 1, "_isPowerPass": 1, "_spectrum": 4.523267165636186, "_excessivePower": 0, "_targetEvm": -10}'


# edata =trunk.bdplug.exchangeData.ExchangeData()
try:
    data_base.saveRFTestLog(jsonstr)

    # resList=edata.getDataBySql('select * from rftest')

    # print resList
except Exception as e:
    print e
    pass
