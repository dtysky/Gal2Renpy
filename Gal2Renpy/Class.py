#coding:utf-8

#Copyright(c) 2014 dtysky

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
		if jtmp['HPCSystem']=='True':
			self.HPCSystem=True
		else:
			self.HPCSystem=False
		#Chareter keywords!
		self.ChrKeyword={
			"t": self.Trans,
			"f": self.ChrFace,
			"c": self.ChrClothes,
			"p": self.ChrPose,
			"d": self.ChrDistance,
			"l": self.ChrPosition
		}
		#Keywords
		jtmp=json.load(open('User/KeyWord.json','r'))['KeyWord']
		self.KeyWord={}
		for k in jtmp:
			self.KeyWord[k]={'l':[]}
			for l in jtmp[k]:
				self.KeyWord[k]['l'].append(l[0])
				self.KeyWord[k][l[0]]=l[1:]


		self.Date='None'


#A class for charecter
class Chr():
	#One or two arguments 
	def __init__(self,US,Fs,orgname):
		self.fs=Fs
		self.us=US
		self.name=US.ChrName[orgname][0]
		self.orgname=orgname
		self.tDefault=US.Trans['ChrDefault']
		#'new' will be true if the attributes has been changed
		self.attrs={'t':self.tDefault,'f':None,'c':None,'p':None,'d':None,'l':None,'new':False}
		self.complete=False
		#Text,Say or Think,Mode,Is refreshed
		self.say={'Text':None,'Style':None,'Mode':None,'new':False}
	#Refresh attributes in this charecter
	def rfattrs(self,Attrs):
		for attr in Attrs.replace('，',',').split(','):
			ttmp=attr.replace('：',':').split(':')
			if ttmp[0] not in self.us.ChrKeyword==None:
				self.fs.error("This charecter's attribute does not exist !")
			else:
				if (ttmp[0]=='c') | (ttmp[0]=='p') | (ttmp[0]=='f'):

					if self.us.ChrKeyword[ttmp[0]][self.orgname].get(ttmp[1])==None:
						self.fs.error("This ChrAttribute "+str(self.name+' '+ttmp[0])+" does not exist !")
					else:
						self.attrs[ttmp[0]]=self.us.ChrKeyword[ttmp[0]][self.orgname][ttmp[1]]
				else:

					if self.us.ChrKeyword[ttmp[0]].get(ttmp[1])==None:
						self.fs.error("This ChrAttribute "+str(self.name+' '+ttmp[0])+" does not exist !")
					else:
						self.attrs[ttmp[0]]=self.us.ChrKeyword[ttmp[0]][ttmp[1]]

			self.attrs['new']=True
	#Refresh next word by this charecter
	def rftext(self,Text,Style,Mode):
		self.say['Text']=Text
		self.say['Style']=Style
		self.say['Mode']=Mode
		self.say['new']=True
	#Check whether the attributes completely
	def checkattrs(self):
		if self.attrs['new']:
			if self.complete==False:
				for attr in self.attrs:
					if self.attrs[attr]==None:
						self.fs.error("This charecter's attributes are not complete !")
	#A interface
	def getattrs(self):
		return self.attrs.update({'name':self.name})

	#Creat scripts which are related to charecters
	def show(self):
		rn=''
		if self.attrs['new']:
			self.complete==True
			if self.attrs['t']=='hide':
				self.attrs['t']='dissolve'
				rn='    hide '+self.name+'\n'#+' '+self.attrs['c']+self.attrs['p']+self.attrs['f']+self.attrs['d']+'\n'
			else:
				rn+='    show '+self.name+' '+self.attrs['p']+self.attrs['c']+self.attrs['f']+self.attrs['d']+' '
				rn+='at '+self.attrs['l']+'\n'
				rn+='    with '+self.attrs['t']+'\n'
			self.attrs['new']=False
			self.attrs['t']=self.tDefault
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
			self.fs.error('This charecter does not be created !')


#A class for Bg
class Bg():
	def __init__(self,US,Fs):
		self.fs=Fs
		self.us=US
		self.bg={'m':None,'s':None,'w':None}
		self.bgorg={'m':None,'s':None,'w':None}
		self.attrs={'l':US.BgKeyword['l']['default'],'t':US.BgKeyword['t']['BgDefault']}
		self.bgLast={'m':None,'s':None,'w':None}
	def refresh(self,Bgs,Attrs):
		Bgs=Bgs.replace('，',',').replace('：',':').split(',')
		Attrs=Attrs.replace('，',',').replace('：',':').split(',')
		for bg in Bgs:
			tmp=bg.split(':')
			if tmp[0]=='nc':
				pass
			elif tmp[0] not in self.bg:
				self.fs.error('This Bgkeyword '+tmp[0]+' does not exist !')
			else:
				if tmp[0]=='m':
					if self.us.BgKeyword[tmp[0]].get(tmp[1])==None:
						self.fs.error('This Bg '+tmp[1]+' does not exist !')
					else:
						self.bg[tmp[0]]=self.us.BgKeyword[tmp[0]][tmp[1]]
						self.bgorg[tmp[0]]=tmp[1]
				else:
					if self.bg['m']==None:
						self.fs.error('You must give a BgMain at first !')
					else:
						if self.us.BgKeyword[tmp[0]][self.bgorg['m']].get(tmp[1])==None:
							self.fs.error('This Bg '+tmp[1]+' in '+self.bgorg['m']+' does not exist !')
						else:
							self.bg[tmp[0]]=self.us.BgKeyword[tmp[0]][self.bgorg['m']][tmp[1]]
							self.bgorg[tmp[0]]=tmp[1]
		for attr in Attrs:
			tmp=attr.split(':')
			if tmp[0]=='None':
				pass
			elif tmp[0] not in self.attrs:
				self.fs.error('This Bgkeyword '+tmp[0]+' does not exist !')
			else:
				if self.us.BgKeyword[tmp[0]].get(tmp[1])==None:
					self.fs.error('This attribute '+tmp[1]+' does not exist !')
				else:
					self.attrs[tmp[0]]=self.us.BgKeyword[tmp[0]][tmp[1]]
	def checkattrs(self):
		for bg in self.bg:
			if self.bg[bg]==None:
				self.fs.error("Bg is not complete !")
		for bg in self.bgorg:
			if bg!='m':
				if self.us.BgKeyword[bg][self.bgorg['m']].get(self.bgorg[bg])==None:
					self.fs.error('This Bg '+self.bgorg[bg]+' which use your last seting in '+self.bgorg['m']+' does not exist !')
	
	def getattrs(self):
		return self.attrs.update(self.bg)

	def show(self):
		rn=''
		self.checkattrs()
		if self.bg!=self.bgLast:
			if self.bg['m']!='Black':
				rn+='    hide screen date\n'
				rn+='    scene bg Black01A with '+self.attrs['t']+'\n'
			if self.us.Date!='None':
				rn+="    show screen date(Date2)\n"
		rn+='    scene bg '+self.bg['m']+self.bg['s']+self.bg['w']+' at '+self.attrs['l']+'\n'
		rn+='    with '+self.attrs['t']+'\n'
		self.attrs={'l':self.us.BgKeyword['l']['default'],'t':self.us.BgKeyword['t']['BgDefault']}
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
						self.cg[tmp[0]]=US.CgKeyword[tmp[0]][tmp[1]]['Name']
						self.cgorg[tmp[0]]=tmp[1]
				else:
					if self.cg['m']==None:
						Fs.error('You must give a CgMain at first !')
					else:
						if tmp[1] not in US.CgKeyword[tmp[0]][self.cgorg['m']]==None:
							Fs.error('This Cg '+tmp[1]+' in '+self.cgorg['m']+' does not exist !')
						else:
							self.cg[tmp[0]]=tmp[1]
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
				if  self.cgorg[cg] not in US.CgKeyword[cg][self.cgorg['m']]==None:
					Fs.error('This Cg '+self.cgorg[cg]+' which use your last seting in '+self.cgorg['m']+' does not exist !')
		rn+='    scene cg '+self.cg['m']+self.cg['s']+' at '+self.attrs['l']+'\n'
		rn+='    with '+self.attrs['t']+'\n'
		self.attrs={'l':US.CgKeyword['l']['default'],'t':US.CgKeyword['t']['CgDefault']}
		return rn

#A class for HPCSystem
class HPC():
<<<<<<< HEAD
	def __init__(self,US,Fs):
		self.fs=Fs
		self.us=US
		self.tPhoneDefault=US.Trans['PhoneDefault']
		self.tPCDefault=US.Trans['PCDefault']
		self.modemlist=('Phone','PC')
		self.modeslist=('Call','Message','Web')
		self.argrange={
			'modem':('Phone','PC'),
			'modes':('Call','Message','Web'),
			'owner':US.CharName,
			'hide':(True,False),
			'pos':US.BgPosition,
			'trans':US.Trans
		}
		self.args={
			'modem':None,
			'modes':None,
			'owner':None,
			'hide':False,
			'pos':'center',
			'trans':None,
			'bg':Bg(),
			'bgz':0.6,
			'chr':None,
			'chrs':None,
			'messadd':None
		}
	#def decode(self,Transition,Content):

	def setvalue(self,Modem=None,Modes=None,Owner=None,Hide=None,Pos=None,Trans=None,Bg=None,Chr=None,Chrs=None,MessAdd=None):
		def set(e,v):
			if v:
				self.args[e]=v
		set('modem',Modem)
		set('modes',Modes)
		set('owner',Owner)
		set('hide',Hide)
		set('pos',Pos)
		set('trans',Trans)
		set('bg',Bg)
		set('chr',Chr)
		set('chrs',Chrs)
		set('messadd',MessAdd)
	def check(self,Fs):
		for arg in argrange:
			if self.args[arg] not in self.argrange[arg]:
				Fs.error('This HPC argument '+arg+' is out of its range !')

	def show(self):
		self.check(self.fs)
		if self.args['modem']=='Phone':
			if self.args['modes']=='Call':
				return self.phonecall()
			elif self.args['modes']=='Message':
				return self.phonemess()
			elif self.args['modes']=='Web':
				return self.phoneweb()
		elif self.args['modem']=='PC':
			if self.args['modes']=='Call':
				return self.pccall()
			elif self.args['modes']=='Message':
				return self.pcmess()
			elif self.args['modes']=='Web':
				return self.pcweb()

	def phonecall(self):
		rn=''
		ChrAttrs=[]
		self.args['bg'].checkattrs()
		BgAttrs=self.args['bg'].getattrs()
		for char in self.args['chrs']:
			char.checkattrs()
			ChrAttrs.append(char.getattrs())
		rn+='    $ call HPC('
		rn+="ModeM='"+self.args['modem']+"',Modes='"+self.args['modes']+"',"
		rn+="Owner='"+self.args['owner']+"',Pos="+self.args['pos']+',Trans='+self.args['trans']+','
		rn+='Bg=(bg'+BgAttrs['m']+BgAttrs['s']+BgAttrs['w']+'HPC,'+BgAttrs['l']+','+self.args['bgz']+'),'
		rn+='Chrs=['
		for charattr in ChrAttrs:
			rn+='('+chrattr['name']+chrattr['p']+chrattr['c']+chrattr['f']+chrattr['d']+'HPC,'+chrattr['l']+',0.8),'
		rn=rn[:-1]+'])\n'


=======
	def __init__(self,US):
		self.modem=None
		self.modes=None
		self.owner=None
		self.hide=False
		self.pos=center
		self.trans=None
		self.tPhoneDefault=US.Trans['PhoneDefault']
		self.tPCDefault=US.Trans['PCDefault']
		self.bg=None
		self.chr=None
		self.chrs=None
		self.messadd=None
	def setvalue(US,Fs,Modem=None,Modes=None,Owner=None,Hide=None,Pos=None,Trans=None,Bg=None,Chr=None,Chrs=None,MessAdd=None):
		if Modem:
			self.modem=Modem
		if Modes:
			self.modes=Modes
>>>>>>> ec5fc04ccf38a396c198d74d1b5aedbf7224226b


