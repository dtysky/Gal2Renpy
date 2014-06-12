#-*-coding:utf-8-*- 

import re
import sys
import codecs
from ctypes import *
user32 = windll.LoadLibrary('user32.dll') 

MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

class MyFS():

	def __init__(self):
		pass
	def open(self,path):
		self.fs=codecs.open(path,'r','utf-8')
		self.path=path
		self.linepos=0
	def readline(self):
		self.linepos+=1
		return self.fs.readline()
	def error(self,e):
		MessageBox(e+'\n'+'file : '+self.path+'\n'+'line : '+str(self.linepos))
		sys.exit(0)


#Return next block
def RBlock(Fs):
	[head,flag,transition,content]=['','','','']
	s=Fs.readline()
	if re.match(r'<.*>',s)!=None:

		if re.match(r'<\S+\s+\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)\s*(\S+)>\s*(.*)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition=sr.group(2)
			content=sr.group(3)
		elif re.match(r'<\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)>\s*(\S+)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition='null'
			content=sr.group(2)
		elif re.match(r'<\S+\s+\S+>',s):
			sr=re.match(r'<(\S+)\s+(\S+)>',s)
			head='sp'
			flag=sr.group(1)
			transition=sr.group(2)
			while 1:
				s=Fs.readline()
				if (s[0]=='<') & (s[1]=='/'):
					break
				elif s[0]=='<':
					Fs.error('''Error! Please check the "</"" !''')
				else:
					content+=re.match('\s*(.+)',s).group(1)+'\n'
		elif re.match(r'<\S+>',s):
			sr=re.match(r'<(\S+)>',s)
			head='sp'
			flag=sr.group(1)
			transition='null'
			while 1:
				s=Fs.readline()
				if (s[0]=='<') & (s[1]=='/'):
					break
				elif s[0]=='<':
					Fs.error('''Error! Please check the "</"" !''')
				else:
					content+=re.match('\s*(.+)',s).group(1)+'\n'
		else:
			Fs.error('''Error! Please check the "<>"" !''')

	else:
		head='text'
		flag='null'
		transition='null'
		content=s

	return [head,flag,transition,content]



#Return a string which changing special texts to Script
def Sp2Script(Flag,Transition,Content,Fs):

	if Flag=='sc':
		return 'label '+Content.replace('，','')+' :\n'

	elif Flag=='bg':
		s=''
		for tmp in Content.split('：'):
			s+=tmp
		sr=s.split('，')
		rn=''
		if BgMain.get(sr[0])==None:
			Fs.error('This Bg does not exist ！')
		else:
			if len(sr)==2:
				if eval('Bg'+BgMain[sr[0]]).get(sr[1])==None:
					Fs.error('This Bg does not exist ！')
				else:
					rn='show bg '+BgMain[sr[0]]+eval('Bg'+BgMain[sr[0]])[sr[1]]+'\n'
			elif len(sr)==1:
				rn='show bg '+BgMain[sr[0]]+'\n'
			else:
				Fs.error('Unsupport two and more subscenes ！')
		if Transition!='null':
			if TransImage.get(Transition)==None:
				Fs.error('This transition does not exist !')
			else:
				rn+='with '+TransImage[Transition]+'\n'
		return 'wr\nNone'+rn

	elif Flag=='bgm':
		rn=''
		if Bgm.get(Content)==None:
			Fs.error('This Bgm does not exist ！')
		else:
			rn='play music '+BgmPath+Bgm[Content]+'\n'
		if Transition!='null':
			if TransSound.get(Transition)==None:
				Fs.error('This effect does not exist ！')
			else:
				rn='with '+TransSound[Transition]+'\n'
		return 'wr\n\t'+rn

	elif Flag=='mode':
		if Content=='None':
			return 'hide window\n'
		elif Content=='Re':
			return 'show window\n'
		elif Content=='ADV':
			return 'mode\nADV'

	elif Flag=='ch':
		rn=None
		[n,e,f,c,p,l]=[None,None,None,None,None,None]
		for sl in Content.splitlines():
			tmp=re.match(r'(\S+)\s+(\S+)',sl)
			if tmp==None:
				Fs.error('Please check your syntax ！')
			else:
				ch=tmp.group(1)
				attrs=tmp.group(2)
				if ChrName.get(ch)==None:
					Fs.error('This charecter does not exist !')
				else:
					c=ChrName[ch]
				for attr in attrs.split('，'):
					ttmp=attr.split('：')
					if ChrKeyword.get(ttmp[0])==None:
						Fs.error("This charecter's attribute does not exist !")
					else:
						if eval(ChrKeyword[ttmp[0]]).get(ttmp[1])==None:
							Fs.error("This "+ChrKeyword[ttmp[0]]+" does not exist !")
						else:
							eval(ttmp[0]+'='+ChrKeyword[ttmp[0]])[ttmp[1]]
			rn='show '+n+c+p+' at '+l+'\n'
			if e!=None:
				rn+='with '+e+'\n'
		return 'wr\n\t'+rn

	#elif Flag=='ef':
		#pass

	else:
		Fs.error('This flag does not exist !')










#Change normal texts to script
def Text2Script(Text,Mode):
	pass


def CreatDefine(Name,Mode):
	pass

