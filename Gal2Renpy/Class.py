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
		MessageBox(e.encode(locale.getdefaultlocale()[1])+'\r\n'+'file : '+self.path.encode(locale.getdefaultlocale()[1])+'\r\n'+'line : '+str(self.linepos))
		sys.exit(0)
	def error2(self,e):
		MessageBox(e.encode(locale.getdefaultlocale()[1])+'\r\n'+'file : '+self.path.encode(locale.getdefaultlocale()[1])+'\r\n'+'line : '+str(self.linepos))
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
		#Effect
		jtmp=json.load(open('User/Effect.json','r'))
		self.EffectSp=jtmp['EffectSp']
		self.Trans=jtmp['Trans']
		self.Graph=jtmp['Graph']
		for gr in self.Graph:
			self.Graph[gr]['Pause']=0
		#Bg
		jtmp=json.load(open('User/Bg.json','r'))
		self.BgMain=jtmp['BgMain']
		self.BgSub=jtmp['BgSub']
		self.BgWeather=jtmp['BgWeather']
		self.BgPosition=jtmp['BgPosition']
		#Bg keywords!
		self.BgKeyword={
			'm': self.BgMain,
			's': self.BgSub,
			'w': self.BgWeather,
			"t": self.Trans,
			"l": self.BgPosition
		}
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
		#Sound
		jtmp=json.load(open('User/Sound.json','r'))
		self.Bgm=jtmp['Bgm']
		self.SoundE=jtmp['SoundE']
		#Cg
		jtmp=json.load(open('User/Cg.json','r'))
		self.Cg=jtmp['Cg']
		self.CgSub={}
		for cg in self.Cg:
			self.CgSub[cg]=[]
			for char in self.Cg[cg]['Chr']:
				for charnum in range(char[1]):
					for bg in self.Cg[cg]['Bg']:
						self.CgSub[cg].append(char[0]+str(charnum)+bg)
						
		#Cg keywords!
		self.CgKeyword={
			'm': self.Cg,
			's': self.CgSub,
			"t": self.Trans,
			"l": self.BgPosition
		}
		#Path,Mode
		jtmp=json.load(open('User/PathMode.json','r'))
		self.GamePath=jtmp['GamePath']
		self.ScriptPath=jtmp['ScriptPath']
		self.ChrPath=jtmp['ChrPath']
		self.BgPath=jtmp['BgPath']
		self.BgmPath=jtmp['BgmPath']
		self.CgPath=jtmp['CgPath']
		self.SoundPath=jtmp['SoundPath']
		self.TextPath=jtmp['TextPath']
		self.WinPath=jtmp['WinPath']
		self.EfPath=jtmp['EfPath']
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
		self.Date='None'


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
			if ttmp[0] not in US.ChrKeyword==None:
				Fs.error("This charecter's attribute does not exist !")
			else:
				if (ttmp[0]=='c') | (ttmp[0]=='p') | (ttmp[0]=='f'):

					if US.ChrKeyword[ttmp[0]][self.orgname].get(ttmp[1])==None:
						Fs.error("This ChrAttribute "+str(self.name+' '+ttmp[0])+" does not exist !")
					else:
						self.attrs[ttmp[0]]=US.ChrKeyword[ttmp[0]][self.orgname][ttmp[1]]
				else:

					if US.ChrKeyword[ttmp[0]].get(ttmp[1])==None:
						Fs.error("This ChrAttribute "+str(self.name+' '+ttmp[0])+" does not exist !")
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
			if self.attrs['t']=='hide':
				self.attrs['t']='dissolve'
				rn='    hide '+self.name+' with dissolve\n'#+' '+self.attrs['c']+self.attrs['p']+self.attrs['f']+self.attrs['d']+'\n'
			else:
				rn+='    show '+self.name+' '+self.attrs['p']+self.attrs['c']+self.attrs['f']+self.attrs['d']+' '
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
			Fs.error('This charecter does not be created !')


#A class for Bg
class Bg():
	def __init__(self,US):
		self.bg={'m':None,'s':None,'w':None}
		self.bgorg={'m':None,'s':None,'w':None}
		self.attrs={'l':US.BgKeyword['l']['default'],'t':US.BgKeyword['t']['BgDefault']}
		self.bgLast={'m':None,'s':None,'w':None}
	def refresh(self,Bgs,Attrs,US,Fs):
		Bgs=Bgs.replace('，',',').replace('：',':').split(',')
		Attrs=Attrs.replace('，',',').replace('：',':').split(',')
		for bg in Bgs:
			tmp=bg.split(':')
			if tmp[0]=='nc':
				pass
			elif tmp[0] not in self.bg:
				Fs.error('This Bgkeyword '+tmp[0]+' does not exist !')
			else:
				if tmp[0]=='m':
					if US.BgKeyword[tmp[0]].get(tmp[1])==None:
						Fs.error('This Bg '+tmp[1]+' does not exist !')
					else:
						self.bg[tmp[0]]=US.BgKeyword[tmp[0]][tmp[1]]
						self.bgorg[tmp[0]]=tmp[1]
				else:
					if self.bg['m']==None:
						Fs.error('You must give a BgMain at first !')
					else:
						if US.BgKeyword[tmp[0]][self.bgorg['m']].get(tmp[1])==None:
							Fs.error('This Bg '+tmp[1]+' in '+self.bgorg['m']+' does not exist !')
						else:
							self.bg[tmp[0]]=US.BgKeyword[tmp[0]][self.bgorg['m']][tmp[1]]
							self.bgorg[tmp[0]]=tmp[1]
		for attr in Attrs:
			tmp=attr.split(':')
			if tmp[0]=='None':
				pass
			elif tmp[0] not in self.attrs:
				Fs.error('This Bgkeyword '+tmp[0]+' does not exist !')
			else:
				if US.BgKeyword[tmp[0]].get(tmp[1])==None:
					Fs.error('This attribute '+tmp[1]+' does not exist !')
				else:
					self.attrs[tmp[0]]=US.BgKeyword[tmp[0]][tmp[1]]
	def show(self,US,Fs):
		rn=''
		for bg in self.bg:
			if self.bg[bg]==None:
				Fs.error("Bg is not complete !")
		for bg in self.bgorg:
			if bg!='m':
				if US.BgKeyword[bg][self.bgorg['m']].get(self.bgorg[bg])==None:
					Fs.error('This Bg '+self.bgorg[bg]+' which use your last seting in '+self.bgorg['m']+' does not exist !')
		if self.bg!=self.bgLast:
			if self.bg['m']!='Black':
				rn+='    hide screen date\n'
				rn+='    scene bg Black01A with '+US.Trans['BgDefault']+'\n'
			if US.Date!='None':
				rn+="    show screen date(Date2)\n"
		rn+='    scene bg '+self.bg['m']+self.bg['s']+self.bg['w']+' at '+self.attrs['l']+'\n'
		rn+='    with '+self.attrs['t']+'\n'
		self.attrs={'l':US.BgKeyword['l']['default'],'t':US.BgKeyword['t']['BgDefault']}
		self.bgLast=self.bg.copy()
		return rn
 
#A class for Cg
class Cg():
	def __init__(self,US):
		self.cg={'m':None,'s':None}
		self.cgorg={'m':None,'s':None}
		self.attrs={'l':US.CgKeyword['l']['default'],'t':US.CgKeyword['t']['CgDefault']}
	def refresh(self,Cgs,Attrs,US,Fs):
		Cgs=Cgs.replace('，',',').replace('：',':').split(',')
		Attrs=Attrs.replace('，',',').replace('：',':').split(',')
		for cg in Cgs:
			tmp=cg.split(':')
			if tmp[0]=='nc':
				pass
			elif tmp[0] not in self.cg:
				Fs.error('This Cgkeyword '+tmp[0]+' does not exist !')
			else:
				if tmp[0]=='m':
					if US.CgKeyword[tmp[0]].get(tmp[1])==None:
						Fs.error('This Cg '+tmp[1]+' does not exist !')
					else:
						self.cg[tmp[0]]=US.CgKeyword[tmp[0]][tmp[1]]
						self.cgorg[tmp[0]]=tmp[1]
				else:
					if self.cg['m']==None:
						Fs.error('You must give a CgMain at first !')
					else:
						if US.CgKeyword[tmp[0]][self.cgorg['m']].get(tmp[1])==None:
							Fs.error('This Cg '+tmp[1]+' in '+self.cgorg['m']+' does not exist !')
						else:
							self.cg[tmp[0]]=US.CgKeyword[tmp[0]][self.cgorg['m']][tmp[1]]
							self.cgorg[tmp[0]]=tmp[1]
		for attr in Attrs:
			tmp=attr.split(':')
			if tmp[0]=='None':
				pass
			elif tmp[0] not in self.attrs:
				Fs.error('This Cgkeyword '+tmp[0]+' does not exist !')
			else:
				if US.CgKeyword[tmp[0]].get(tmp[1])==None:
					Fs.error('This attribute '+tmp[1]+' does not exist !')
				else:
					self.attrs[tmp[0]]=US.CgKeyword[tmp[0]][tmp[1]]
	def show(self,US,Fs):
		rn='    hide screen date\n'
		for cg in self.cg:
			if self.cg[cg]==None:
				Fs.error("Cg is not complete !")
		for cg in self.cgorg:
			if cg!='m':
				if US.CgKeyword[cg][self.cgorg['m']].get(self.cgorg[cg])==None:
					Fs.error('This Cg '+self.cgorg[cg]+' which use your last seting in '+self.cgorg['m']+' does not exist !')
		rn+='    scene cg '+self.cg['m']+self.cg['s']+self.cg['w']+' at '+self.attrs['l']+'\n'
		rn+='    with '+self.attrs['t']+'\n'
		self.attrs={'l':US.CgKeyword['l']['default'],'t':US.CgKeyword['t']['CgDefault']}
		return rn