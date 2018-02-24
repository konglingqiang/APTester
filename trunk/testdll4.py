from ctypes import *  
dll = cdll.LoadLibrary('IQmeasure.dll');  

ret = dll.LP_Init(1,0);
print(ret)
ret = dll.LP_InitTester("192.168.100.254",1);
print(ret)

strMa = "/0"*200  
FunPrint  = dll.LP_GetVersion  
FunPrint.argtypes = [c_char_p, c_int]  
#FunPrint.restypes = c_void_p  
nRst = FunPrint(strMa, len(strMa))  
print strMa,len(strMa)  

#ret = dll.LP_MptaAvailable()
#print(ret)

#intPara = c_int(9)
#dll.LP_GetSessionID(byref(intPara))  
#print intPara.value  

s='''
strMa = "/0"*100  
FunPrint  = dll.LP_GetVersion  
FunPrint.argtypes = [c_char_p, c_int]
nRst = FunPrint(strMa, len(strMa))  
print strMa,len(strMa) 
'''

s = '''
pcName = c_char_p('')
pcSize = 25
windll.kernel32.GetComputerNameA(pcName,byref(c_int(pcSize)))
print(pcName.value)
'''
s  = '''
pcName = c_char_p('/0'*200)
pcSize = 100
#print pcName.value
pcName = dll.LP_GetErrorString(2)
a = string_at(pcName,200)
print a
'''

s='''
foo = create_string_buffer(200)
pfoo = addressof(foo)
dll.LP_GetVersion(pfoo, 200)
'''

s='''
strMa = "/0"*200  
FunPrint  = dll.LP_GetVersion  
FunPrint.argtypes = [c_char_p, c_int]  
#FunPrint.restypes = c_void_p  
nRst = FunPrint(strMa, len(strMa))  
print strMa,len(strMa)  
'''

#get_path=dll.LP_GetVersion
#get_path.argtypes=[ctypes.c_char_p, ctypes.c_int]
#path=ctypes.create_string_buffer(100)
#print type(path)
#print get_path
#get_path(path, 100)
#b = ctypes.byref(path)
#print type(b)
#get_path(b, 100)
#get_path(a, 100)
#print path.value
s='''
szPara = create_string_buffer('/0'*100)  
dll.LP_GetVersion(byref(szPara), 100);  
print szPara.value  
'''

s = '''
ret = dll.LP_InitTester("192.168.100.254");
print(ret)
foo = create_string_buffer(50)
pfoo = addressof(foo)
s = dll.LP_GetErrorString(ret)
#print(ret)
#s = string_at(pfoo, 50)
#print foo.value
ret = dll.LP_SetVsa(0x2412e6, 18, 0, 0, -25);
#ret = dll.IntAdd(2, 4);  
print(ret)
ret = dll.LP_VsaDataCapture(200)
print(ret)
ret = dll.LP_Analyze80211ag()
print(ret)
ret = dll.LP_GetScalarMeasurement("evmAll")
print("EVM for OFDM-54 = %.2f\n" % ret)
'''