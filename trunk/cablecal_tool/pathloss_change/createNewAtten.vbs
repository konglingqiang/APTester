ScriptFullName = WScript.ScriptFullName
path = Left(ScriptFullName,InStrRev(ScriptFullName,"\"))
allStr = GetAllStr(path & "\IQ_ATTEN.txt") '��ȡ��ǰĿ¼·����IQ_ATTEN.txt��ȫ���ַ���
pointList2G = "2412,2417,2422,2427,2432,2437,2442,2447,2452,2457,2462,2467,2472,2484"  '2.4G��λ
pointList5G = "5180,5190,5210,5240,5260,5290,5320,5500,5510,5520,5530,5600,5610,5640,5700,5745,5775,5780,5785,5795,5825"  '5.8G��λ
Set point2GDic = GetPointLost(pointList2G,allStr)  '��ȡ����IQ_ATTEN.txt�е�2.4G����ֵ
Set point5GDic = GetPointLost(pointList5G,allStr)  '��ȡ����IQ_ATTEN.txt�е�5.8G����ֵ
WritedownFile path,"[2G]" 'д��2G��ͷ��
point2GArr = Split(pointList2G,",") '�ָ�2G�ĵ�
For a = 0 To UBound(point2GArr)  '����2G�����е㣬д����Ϣ
	pointName = point2GArr(a)
	Set point = CalculateLost(pointName,point2GDic,point5GDic)
	WritedownFile path,pointName & " = " & Left(point.Item(pointName & "_0"),4) & "," & Left(point.Item(pointName & "_1"),4) & ",0,0,0,0"
Next 

WritedownFile path,VbCrlf & "[5G]"
point5GArr = Split(pointList5G,",") '�ָ�5G�ĵ�
For b = 0 To UBound(point5GArr)  '����2G�����е㣬д����Ϣ
	pointName = point5GArr(b)
	Set point = CalculateLost(pointName,point2GDic,point5GDic)
	WritedownFile path,pointName & " = " & Left(point.Item(pointName & "_0"),4) & "," & Left(point.Item(pointName & "_1"),4) & ",0,0,0,0"
Next 
msgbox "OK!"

Function GetPointLost(points,allStr)  '���ַ��ַ����ж�ȡ��֪�������ֵ
	Set tempDic = CreateObject("Scripting.Dictionary") '����һ���ֵ���󣬴�ŵ�λ��Ϣ
	pointArr = Split(points,",") '�����е�λ�ָ�  �������е�λ
	lineStrArr = Split(allStr,VbCrLf) '�������ַ������зָ�
	For i = 0 To UBound(pointArr) '����ÿһ����
		point = pointArr(i)
		For j = 0 To UBound(lineStrArr) '�������ַ����ָ���ȡ�����λһ�µ���
			lineStr = lineStrArr(j)
			If InStr(lineStr,point) <> 0 Then
				tempArr = Split(Trim(lineStr),"  ")
				canal0 = tempArr(1)
				canal1 = tempArr(2)
				tempDic.Item(point & "_0") = canal0 '��Ӧ��λ��canal0��ֵ
				tempDic.Item(point & "_1") = canal1 '��Ӧ��λ��canal1��ֵ
				Exit For 
			End If 
		Next 
	Next 
	Set GetPointLost = tempDic  '���ض���
	Set tempDic = Nothing 
End Function 


Function CalculateLost(thisPoint,point2GDic,point5GDic) '��������ֵ
	Set tempDic = CreateObject("Scripting.Dictionary") '����һ���ֵ���󣬴�ŵ�λ��Ϣ
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
	If (Not point2GDic.Exists(thisPoint & "_0")) And (Not point5GDic.Exists(thisPoint & "_0")) And (Not point2GDic.Exists(thisPoint & "_1")) And (Not point5GDic.Exists(thisPoint & "_1")) And thisPoint>2412 And thisPoint<2484 Then '��ȫ2.4G�ļ�����
		For Each pKey In point2GDic.keys
			intThisPoint = CInt(thisPoint) '����ǰ��λ��ϢתΪint
			intKey = CInt(Left(pkey,Len(pKey)-2))
			If intThisPoint > intKey then
				minValue0 = point2GDic.Item(intKey & "_0") '���ֵ��Ѿ�����������Ź�������ֻҪ�ҵ������Ƶ��С��ֵ��¼�����ҵ��������ֵʱ��ֹͣ���ҡ�����������
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
	If (Not point2GDic.Exists(thisPoint & "_0")) And (Not point5GDic.Exists(thisPoint & "_0")) And (Not point2GDic.Exists(thisPoint & "_1")) And (Not point5GDic.Exists(thisPoint & "_1")) And thisPoint>5180 And thisPoint<5825 Then '��ȫ5.8G�ļ�����
		For Each pKey In point5GDic.keys
			intThisPoint = CInt(thisPoint) '����ǰ��λ��ϢתΪint
			intKey = CInt(Left(pkey,Len(pKey)-2))
			If intThisPoint > intKey then
				minValue0 = point5GDic.Item(intKey & "_0") '���ֵ��Ѿ�����������Ź�������ֻҪ�ҵ������Ƶ��С��ֵ��¼�����ҵ��������ֵʱ��ֹͣ���ҡ�����������
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


Sub WritedownFile(path,tempStr) 'д���ı�
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set TextFile = fso.OpenTextFile(path & "\xiansun.ini", 8, True)
	TextFile.WriteLine tempStr
	TextFile.Close
End Sub  


Function GetAllStr(path) '��ȡ�����ַ���
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set TextFile = fso.OpenTextFile(path, 1)
	allStr = TextFile.ReadALL
	TextFile.Close
	GetAllStr = allStr
End Function 