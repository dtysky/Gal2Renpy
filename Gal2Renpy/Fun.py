import re
from ctypes import *
user32 = windll.LoadLibrary('user32.dll') 

MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 


#CreatScript
def CreatSp(Str,Mode):
	pass

#Return next block
def RBlock(Fs):
	[head,flag,effect,content]=['','','','']
	s=Fs.readline()
	if re.match(r'<.*>',s)!=None:

		if re.match(r'<\S+\s+\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)\s*(\S+)>\s*(.*)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			effect=sr.group(2)
			content=sr.group(3)
		elif re.match(r'<\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)>\s*(\S+)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			effect='null'
			content=sr.group(2)
		elif re.match(r'<\S+\s+\S+>',s):
			sr=re.match(r'<(\S+)\s+(\S+)>',s)
			head='sp'
			flag=sr.group(1)
			effect=sr.group(2)
			while 1:
				s=Fs.readline()
				if (s[0]=='<') & (s[1]=='/'):
					break
				elif s[0]=='<':
					MessageBox('''Error! Please check the "</"" !''')
				else:
					content+=re.match('\s*(.+)',s).group(1)+'\n'
		elif re.match(r'<\S+>',s):
			sr=re.match(r'<(\S+)>',s)
			head='sp'
			flag=sr.group(1)
			effect='null'
			while 1:
				s=Fs.readline()
				if (s[0]=='<') & (s[1]=='/'):
					break
				elif s[0]=='<':
					MessageBox('''Error! Please check the "</"" !''')
				else:
					content+=re.match('\s*(.+)',s).group(1)+'\n'
		else:
			MessageBox('''Error! Please check the "<>"" !''')

	else:
		head='text'
		flag='null'
		effect='null'
		content=s

	return [head,flag,effect,content]






#Effect
def Effect(Name,Num,ThEle,ThPos,OtEle):
	pass