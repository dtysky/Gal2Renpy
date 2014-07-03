#coding:utf-8

import re
import sys
import os
import json
import locale
from ctypes import *
import codecs
from Keyword import *
import hashlib
user32 = windll.LoadLibrary('user32.dll')

MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

class MyFS():

	def __init__(self):
		pass
	def open(self,path,mode):
		if os.path.exists(path):
			self.fs=codecs.open(path,mode,'utf-8')
			self.path=path
			self.linepos=0
		else:
			MessageBox('The file '+path+' does not exist !')
			sys.exit(0)

	def readline(self):
		self.linepos+=1
		return self.fs.readline()
	def error(self,e):
		MessageBox(e+'\r\n'+'file : '+self.path.encode(locale.getdefaultlocale()[1])+'\r\n'+'line : '+str(self.linepos))
		sys.exit(0)
	def error2(self,e):
		MessageBox(e+'\r\n'+'file : '+self.path.encode(locale.getdefaultlocale()[1])+'\r\n'+'line : '+str(self.linepos))
	def hash(self):
		md5obj=hashlib.md5()
		while 1:
			f=self.fs.read(8096)
			if not f:
				break
			else:
				md5obj.update(f.encode('utf-8'))
		hash=md5obj.hexdigest() 
		self.fs.seek(0)
		return hash
	def close(self):
		self.fs.close()

#User's source
class User():
	def __init__(self):
		#Bg
		jtmp=json.load(open('User/Bg.json','r'))
		self.BgMain=jtmp['BgMain']
		self.BgSub=jtmp['BgSub']
		self.BgWeather=jtmp['BgWeather']
		#ChrFace
		self.ChrFace=json.load(open('User/ChrFace.json','r'))
		#ChrOther
		jtmp=json.load(open('User/ChrOther.json','r'))
		self.ChrWindow=jtmp['ChrWindow']
		self.ChrName=jtmp['ChrName']
		for ch in sorted(self.ChrName):
			self.ChrName[ch].append(None)
		self.ChrName['Saying']= None 
		self.ChrClothes=jtmp['ChrClothes']
		self.ChrPose=jtmp['ChrPose']
		self.ChrDistance=jtmp['ChrDistance']
		self.ChrPosition=jtmp['ChrPosition']
		#Effect
		jtmp=json.load(open('User/Effect.json','r'))
		self.EffectSp=jtmp['EffectSp']
		self.Trans=jtmp['Trans']
		#Sound
		jtmp=json.load(open('User/Sound.json','r'))
		self.Bgm=jtmp['Bgm']
		self.SoundE=jtmp['SoundE']
		#Path,Mode
		jtmp=json.load(open('User/PathMode.json','r'))
		self.ScriptPath=jtmp['ScriptPath']
		self.ChrPath=jtmp['ChrPath']
		self.BgPath=jtmp['BgPath']
		self.BgmPath=jtmp['BgmPath']
		self.TextPath=jtmp['TextPath']
		self.WinPath=jtmp['WinPath']
		if jtmp['TestMode']=='True':
			self.TestMode=True
		else:
			self.TestMode=False
		#Chareter keywords!
		self.ChrKeyword={
			"t": self.Trans,
			"f": self.ChrFace,
			"c": self.ChrClothes,
			"p": self.ChrPose,
			"d": self.ChrDistance,
			"l": self.ChrPosition

		}


#A class for charecter
class Chr():
	#One or two arguments 
	def __init__(self,name,orgname):
		self.name=name
		self.orgname=orgname
		#'new' will be true if the attributes has been changed
		self.attrs={'t':None,'f':None,'c':None,'p':None,'d':None,'l':None,'new':False}
		self.complete=False
		#Text,Say or Think,Mode,Is refreshed
		self.say={'Text':None,'Style':None,'Mode':None,'new':False}
	#Refresh attributes in this charecter
	def rfattrs(self,Attrs,US,Fs):
		for attr in Attrs.replace('，',',').split(','):
			ttmp=attr.replace('：',':').split(':')
			if US.ChrKeyword.get(ttmp[0])==None:
				Fs.error("This charecter's attribute does not exist !")
			else:
				if (ttmp[0]=='c') | (ttmp[0]=='p') | (ttmp[0]=='f'):

					if US.ChrKeyword[ttmp[0]][self.orgname].get(ttmp[1])==None:
						Fs.error("This "+US.ChrKeyword[ttmp[0]]+" does not exist !")
					else:
						self.attrs[ttmp[0]]=US.ChrKeyword[ttmp[0]][self.orgname][ttmp[1]]
				else:

					if US.ChrKeyword[ttmp[0]].get(ttmp[1])==None:
						Fs.error("This "+US.ChrKeyword[ttmp[0]]+" does not exist !")
					else:
						self.attrs[ttmp[0]]=US.ChrKeyword[ttmp[0]][ttmp[1]]

			self.attrs['new']=True
	#Refresh next word by this charecter
	def rftext(self,Text,Style,Mode):
		self.say['Text']=Text
		self.say['Style']=Style
		self.say['Mode']=Mode
		self.say['new']=True
	#Creat scripts which are related to charecters
	def show(self,Fs):
		rn=''
		if self.attrs['new']:
			if self.complete==False:
				for attr in self.attrs:
					if self.attrs[attr]==None:
						Fs.error("This charecter's attributes are not complete !")
					self.complete==True
			rn+='    show '+self.name+self.attrs['c']+self.attrs['p']+self.attrs['f']+self.attrs['d']+' '
			rn+='at '+self.attrs['l']+'\n'
			rn+='    with '+self.attrs['t']+'\n'
			self.attrs['new']=False
			return rn
		elif self.say['new']:
			rn+=self.name+self.say['Mode']+' '
			if self.say['Style']=='Say':
				rn+="'"+self.say['Text']+"'\n"
			else:
				rn+="'（"+self.say['Text']+"）'\n"
			self.say['new']=False
			return '    '+rn
		else:
			MessageBox('This charecter does not be created !')
			sys.exit(0)




