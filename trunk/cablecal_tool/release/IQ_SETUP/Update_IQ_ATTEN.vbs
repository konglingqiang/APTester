IQ_file="IQ_ATTEN.txt"
Set fso = CreateObject("Scripting.FileSystemObject")
Set myfile = fso.OpenTextFile(IQ_file,1,False)
readFile = myfile.ReadAll
myfile.Close
readFile = Replace(readFile,"IQ_FIXED_ATTEN_2_4_CHAIN0 	= 0.00","IQ_FIXED_ATTEN_2_4_CHAIN0 	= 0.00")
readFile = Replace(readFile,"IQ_FIXED_ATTEN_2_4_CHAIN1 	= 0.00","IQ_FIXED_ATTEN_2_4_CHAIN1 	= 0.00")
readFile = Replace(readFile,"IQ_FIXED_ATTEN_5_CHAIN0 	= 0.00","IQ_FIXED_ATTEN_5_CHAIN0 	= 0.00")
readFile = Replace(readFile,"IQ_FIXED_ATTEN_5_CHAIN1 	= 0.00","IQ_FIXED_ATTEN_5_CHAIN1 	= 0.00")
IQ_ATTEN_file = Split(readFile,VBCrLf)
For Each IQ_ATTEN_Line In IQ_ATTEN_file
	If Left(IQ_ATTEN_Line,"2")="24" Then
		tempstr = Split(IQ_ATTEN_Line,"  ")
		IQ_ATTEN_Line = tempstr(0) & "  " & tempstr(2) & "  " & tempstr(1) & "  " & tempstr(3) & "  " & tempstr(4) & "  " & tempstr(5) & "  " & tempstr(6) 
	End If	
	temp = temp & IQ_ATTEN_Line & VbCrLf
Next	

Set write_IQ = fso.OpenTextFile(IQ_file,2,True)
write_IQ.Write temp
write_IQ.Close
Set write_IQ = Nothing

msgbox "OK"

