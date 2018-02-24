ScriptFullName = WScript.ScriptFullName
path = Left(ScriptFullName,InStrRev(ScriptFullName,"\"))
allStr = GetAllStr(path & "\IQ_ATTEN.txt") '获取当前目录路径下IQ_ATTEN.txt的全部字符串
pointList2G = "2412,2417,2422,2427,2432,2437,2442,2447,2452,2457,2462,2467,2472,2484"  '2.4G点位
pointList5G = "5180,5190,5210,5240,5260,5290,5320,5500,5510,5520,5530,5600,5610,5640,5700,5745,5775,5780,5785,5795,5825"  '5.8G点位
Set point2GDic = GetPointLost(pointList2G,allStr)  '获取已在IQ_ATTEN.txt中的2.4G线损值
Set point5GDic = GetPointLost(pointList5G,allStr)  '获取已在IQ_ATTEN.txt中的5.8G线损值
WritedownFile path,"[2G]" '写下2G的头部
point2GArr = Split(pointList2G,",") '分割2G的点
For a = 0 To UBound(point2GArr)  '遍历2G的所有点，写下信息
	pointName = point2GArr(a)
	Set point = CalculateLost(pointName,point2GDic,point5GDic)
	WritedownFile path,pointName & " = " & Left(point.Item(pointName & "_0"),4) & "," & Left(point.Item(pointName & "_1"),4) & ",0,0,0,0"
Next 

WritedownFile path,VbCrlf & "[5G]"
point5GArr = Split(pointList5G,",") '分割5G的点
For b = 0 To UBound(point5GArr)  '遍历2G的所有点，写下信息
	pointName = point5GArr(b)
	Set point = CalculateLost(pointName,point2GDic,point5GDic)
	WritedownFile path,pointName & " = " & Left(point.Item(pointName & "_0"),4) & "," & Left(point.Item(pointName & "_1"),4) & ",0,0,0,0"
Next 
msgbox "OK!"

Function GetPointLost(points,allStr)  '从字符字符串中读取已知点的线损值
	Set tempDic = CreateObject("Scripting.Dictionary") '设置一个字典对象，存放点位信息
	pointArr = Split(points,",") '将所有点位分割  遍历所有点位
	lineStrArr = Split(allStr,VbCrLf) '将所有字符串按行分割
	For i = 0 To UBound(pointArr) '遍历每一个点
		point = pointArr(i)
		For j = 0 To UBound(lineStrArr) '将完整字符串分割后获取到与点位一致的行
			lineStr = lineStrArr(j)
			If InStr(lineStr,point) <> 0 Then
				tempArr = Split(Trim(lineStr),"  ")
				canal0 = tempArr(1)
				canal1 = tempArr(2)
				tempDic.Item(point & "_0") = canal0 '对应点位的canal0的值
				tempDic.Item(point & "_1") = canal1 '对应电位的canal1的值
				Exit For 
			End If 
		Next 
	Next 
	Set GetPointLost = tempDic  '返回对象
	Set tempDic = Nothing 
End Function 


Function CalculateLost(thisPoint,point2GDic,point5GDic) '计算线损值
	Set tempDic = CreateObject("Scripting.Dictionary") '设置一个字典对象，存放点位信息
	If point2GDic.Exists(thisPoint & "_0") Then
		tempDic.Item(thisPoint & "_0") = point2GDic.Item(thisPoint & "_0")
	End If 
	If point5GDic.Exists(thisPoint & "_0") Then
		tempDic.Item(thisPoint & "_0") = point5GDic.Item(thisPoint & "_0")
	End If 
	If point2GDic.Exists(thisPoint & "_1") Then
		tempDic.Item(thisPoint & "_1") = point2GDic.Item(thisPoint & "_1")
	End If 
	If point5GDic.Exists(thisPoint & "_1") Then
		tempDic.Item(thisPoint & "_1") = point5GDic.Item(thisPoint & "_1")
	End If 
	If (Not point2GDic.Exists(thisPoint & "_0")) And (Not point5GDic.Exists(thisPoint & "_0")) And (Not point2GDic.Exists(thisPoint & "_1")) And (Not point5GDic.Exists(thisPoint & "_1")) And thisPoint>2412 And thisPoint<2484 Then '补全2.4G的几个点
		For Each pKey In point2GDic.keys
			intThisPoint = CInt(thisPoint) '将当前点位信息转为int
			intKey = CInt(Left(pkey,Len(pKey)-2))
			If intThisPoint > intKey then
				minValue0 = point2GDic.Item(intKey & "_0") '因字典已经将相关数据排过序，所以只要找到比这个频段小的值记录。当找到比它大的值时，停止查找。计算结果即可
				minValue1 = point2GDic.Item(intKey & "_1")
				minPoint = intKey
			ElseIf  intThisPoint < intKey Then 
				maxValue0 = point2GDic.Item(intKey & "_0")
				maxValue1 = point2GDic.Item(intKey & "_1")
				maxPoint = intKey
				Exit For 
			End If 
		Next 
		tempDic.Item(thisPoint & "_0") = (maxValue0 - minValue0)/(maxPoint - minPoint)*(thisPoint - minPoint) + minValue0 
		tempDic.Item(thisPoint & "_1") = (maxValue1 - minValue1)/(maxPoint - minPoint)*(thisPoint - minPoint) + minValue1 
	End If 
	If (Not point2GDic.Exists(thisPoint & "_0")) And (Not point5GDic.Exists(thisPoint & "_0")) And (Not point2GDic.Exists(thisPoint & "_1")) And (Not point5GDic.Exists(thisPoint & "_1")) And thisPoint>5180 And thisPoint<5825 Then '补全5.8G的几个点
		For Each pKey In point5GDic.keys
			intThisPoint = CInt(thisPoint) '将当前点位信息转为int
			intKey = CInt(Left(pkey,Len(pKey)-2))
			If intThisPoint > intKey then
				minValue0 = point5GDic.Item(intKey & "_0") '因字典已经将相关数据排过序，所以只要找到比这个频段小的值记录。当找到比它大的值时，停止查找。计算结果即可
				minValue1 = point5GDic.Item(intKey & "_1")
				minPoint = intKey
			ElseIf intThisPoint < intKey Then
				maxValue0 = point5GDic.Item(intKey & "_0")
				maxValue1 = point5GDic.Item(intKey & "_1")
				maxPoint = intKey
				Exit For 
			End If 
		Next 
		tempDic.Item(thisPoint & "_0") = (maxValue0 - minValue0)/(maxPoint - minPoint)*(thisPoint - minPoint) + minValue0 
		tempDic.Item(thisPoint & "_1") = (maxValue1 - minValue1)/(maxPoint - minPoint)*(thisPoint - minPoint) + minValue1 
	End If
	Set CalculateLost = tempDic
	Set tempDic = Nothing 
End Function 


Sub WritedownFile(path,tempStr) '写下文本
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set TextFile = fso.OpenTextFile(path & "\xiansun.ini", 8, True)
	TextFile.WriteLine tempStr
	TextFile.Close
End Sub  


Function GetAllStr(path) '获取完整字符串
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set TextFile = fso.OpenTextFile(path, 1)
	allStr = TextFile.ReadALL
	TextFile.Close
	GetAllStr = allStr
End Function 