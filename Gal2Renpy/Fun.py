#-*-coding:utf-8-*- 

import numpy
import re
import codecs
from ctypes import *
from Keyword import *
from Class import *
from ChrFace import *
from ChrOther import *
from Sound import *
from Bg import *
from Effect import *
from Path import *


#Return next block
def RBlock(Fs):
	[head,flag,transition,content]=['','','','']
	s=Fs.readline()
	if s=='':
		head='end'
	elif s=='\r\n':
		head='None'
	elif re.match(r'<.*>',s)!=None:

		if re.match(r'<\S+\s+\S+>.+</\S+>',s)!=None:
			sr=re.match(r'<(\S+)(.+)>(.*)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition=sr.group(2)
			content=sr.group(3)
		elif re.match(r'<\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)>(.+)</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition='None'
			content=sr.group(2)
		elif re.match(r'<\S+\s+\S+>',s)!=None:
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
		elif re.match(r'<\S+>',s)!=None:
			sr=re.match(r'<(\S+)>',s)
			head='sp'
			flag=sr.group(1)
			transition='None'
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
		tmp=re.match(ur'(\S+)\s+【(.*)】',s)
		if tmp==None:
			tmp=re.match(ur'【(.*)】',s)
			if tmp==None:
				head='text'
				flag='None'
				transition='None'
				content='''"'''+s+'''"'''
			else:
				head='words'
				if ChrName['Saying']==None:
					Fs.error('No speaker !')
				else:
					flag=ChrName['Saying']
				transition='think'
				content=tmp
		else:
			if ChrName.get(tmp.group(1))==None:
				Fs.error('This charecter doen not exist !')
			else:
				head='words'
				flag=ChrName[tmp.group(1)]
				transition='say'
				content=tmp.group(2)
				ChrName['Saying']=flag

	return [head,flag,transition,content]



#Return a string which changing special texts to scripts
def Sp2Script(Flag,Transition,Content,Fs):

	if Flag=='sc':
		return 'label '+Content.replace('，','')+' :\n'

	elif Flag=='bg':
		#Weather
		tmp=Content.replace('：',':').split(':')
		if len(tmp)==1:
			w=''
		else:
			if BgWeather.get(tmp[1])==None:
				Fs.error('This Weather does not exist !')
			else:
				w=BgWeather.get[tmp[1]]
		sr=tmp[0].replace('，',',').split(',')
		rn=''
		if BgMain.get(sr[0])==None:
			Fs.error('This Bg does not exist !')
		else:
			if len(sr)==2:
				if BgSub.get(sr[1])==None:
					Fs.error('This SubBg does not exist !')
				else:
					rn='    show bg '+BgMain[sr[0]]+BgSub[sr[1]]+w+'\n'
			elif len(sr)==1:
				rn='    show bg '+BgMain[sr[0]]+w+'\n'
			else:
				Fs.error('Unsupport two and more subscenes !')
		if Transition!='None':
			if TransImage.get(Transition)==None:
				Fs.error('This transition does not exist !')
			else:
				rn+='    with '+TransImage[Transition]+'\n'
		return rn

	elif Flag=='bgm':
		rn=''
		if Bgm.get(Content)==None:
			Fs.error('This Bgm does not exist !')
		else:
			rn='play music '+'''"'''+BgmPath+Bgm[Content]+'''"\n'''
		if Transition!='None':
			if TransSound.get(Transition)==None:
				Fs.error('This effect does not exist !')
			else:
				rn='with '+TransSound[Transition]+'\n'
		return '    '+rn

	elif Flag=='ef':
		rn=''
		ef=Transition.replace('，',',').split(',')
		if ef[0] in EffectSp:
			for s in Content.splitlines():
				rn+='    call '+ef[0]+'('
				for efc in range(2,len(ef)+1):
					if ef[efc-1]=='this':
						if ef[1]=='Text':
							rn+='''"'''+s+'''"'''+','
						else:
							if Graph.get(s)==None:
								Fs.error('This graph does not exist !')
							else:
								rn+=s+','
					elif efc>2:
						rn+=ef[efc-1]
						if efc<len(ef):
							rn+=','
					if efc==len(ef):
						rn+=')\n'
			return rn
		else:
			Fs.error('This effect does not exist !')

	else:
		Fs.error('This flag does not exist or be supported in this fun !')



def CreatDefine(Name,Mode):
	pass

