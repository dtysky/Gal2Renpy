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
	def __init__(self,path=''):
		#Effect
		jtmp=json.load(codecs.open(path+'User/Effect.json','r','utf-8'))
		self.EffectSp=jtmp['EffectSp']
		self.Trans=jtmp['Trans']
		self.Graph=jtmp['Graph']
		for gr in self.Graph:
			self.Graph[gr]['Pause']=0
		#Bg
		jtmp=json.load(codecs.open(path+'User/Bg.json','r','utf-8'))
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
		self.ChrFace=json.load(codecs.open(path+'User/ChrFace.json','r','utf-8'))
		#ChrOther
		jtmp=json.load(codecs.open(path+'User/ChrOther.json','r','utf-8'))
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
		jtmp=json.load(codecs.open(path+'User/Sound.json','r','utf-8'))
		self.Bgm=jtmp['Bgm']
		self.SoundE=jtmp['SoundE']
		#Cg
		jtmp=json.load(codecs.open(path+'User/Cg.json','r','utf-8'))
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
		jtmp=json.load(codecs.open(path+'User/PathMode.json','r','utf-8'))
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
			"l": self.ChrPosition,
			"m": self.ChrName
		}
		#Keywords
		jtmp=json.load(codecs.open(path+'User/KeyWord.json','r','utf-8'))['KeyWord']
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
		rn=self.attrs
		rn.update({'name':self.name})
		return rn

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
							self.fs.error('This Bg '+tmp[0]+' '+tmp[1]+' in '+self.bgorg['m']+' does not exist !')
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
		rn=self.attrs
		rn.update(self.bg)
		return rn

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
	def __init__(self,US,Fs):
		self.us=US
		self.fs=Fs
		self.cg={'m':None,'s':None}
		self.cgorg={'m':None,'s':None}
		self.attrs={'l':US.CgKeyword['l']['default'],'t':US.CgKeyword['t']['CgDefault']}
	def refresh(self,Cgs,Attrs):
		Cgs=Cgs.replace('，',',').replace('：',':').split(',')
		Attrs=Attrs.replace('，',',').replace('：',':').split(',')
		for cg in Cgs:
			tmp=cg.split(':')
			if tmp[0]=='nc':
				pass
			elif tmp[0] not in self.cg:
				self.fs.error('This Cgkeyword '+tmp[0]+' does not exist !')
			else:
				if tmp[0]=='m':
					if self.us.CgKeyword[tmp[0]].get(tmp[1])==None:
						self.fs.error('This Cg '+tmp[1]+' does not exist !')
					else:
						self.cg[tmp[0]]=self.us.CgKeyword[tmp[0]][tmp[1]]['Name']
						self.cgorg[tmp[0]]=tmp[1]
				else:
					if self.cg['m']==None:
						self.fs.error('You must give a CgMain at first !')
					else:
						if tmp[1] not in self.us.CgKeyword[tmp[0]][self.cgorg['m']]==None:
							self.fs.error('This Cg '+tmp[1]+' in '+self.cgorg['m']+' does not exist !')
						else:
							self.cg[tmp[0]]=tmp[1]
							self.cgorg[tmp[0]]=tmp[1]
		for attr in Attrs:
			tmp=attr.split(':')
			if tmp[0]=='None':
				pass
			elif tmp[0] not in self.attrs:
				self.fs.error('This Cgkeyword '+tmp[0]+' does not exist !')
			else:
				if self.us.CgKeyword[tmp[0]].get(tmp[1])==None:
					self.fs.error('This attribute '+tmp[1]+' does not exist !')
				else:
					self.attrs[tmp[0]]=self.us.CgKeyword[tmp[0]][tmp[1]]
	def show(self):
		rn='    hide screen date\n'
		for cg in self.cg:
			if self.cg[cg]==None:
				self.fs.error("Cg is not complete !")
		for cg in self.cgorg:
			if cg!='m':
				if  self.cgorg[cg] not in self.us.CgKeyword[cg][self.cgorg['m']]==None:
					self.fs.error('This Cg '+self.cgorg[cg]+' which use your last seting in '+self.cgorg['m']+' does not exist !')
		rn+='    scene cg '+self.cg['m']+self.cg['s']+' at '+self.attrs['l']+'\n'
		rn+='    with '+self.attrs['t']+'\n'
		self.attrs={'l':self.us.CgKeyword['l']['default'],'t':self.us.CgKeyword['t']['CgDefault']}
		return rn

#A class for HPCSystem
class HPC():
	def __init__(self,US,Fs):
		self.fs=Fs
		self.us=US
		self.tDefault={
			'Phone':'HPCPhoneDefault',
			'PC':'HPCPCDefault'
			}
		self.keywords={
			'mm':'modem',
			'ms':'modes',
			'o':'owner',
			'h':'hide',
			'p':'pos',
			't':'trans'
		}
		self.modeslist=('Call','Message','Web')
		self.argrange={
			'modem':('Phone','PC'),
			'modes':('Call','Message','Web'),
			'owner':US.ChrName,
			'hide':('True','False'),
			'pos':US.BgPosition,
			'trans':US.Trans
		}
		self.args={
			'modem':None,
			'modes':None,
			'owner':None,
			'hide':'False',
			'pos':'HPCPhDefault',
			'trans':'HPCPhoneDefault',
			'bg':Bg(US,Fs),
			'bgz':{'Phone':'0.6','PC':'0.8'},
			'chrz':{'Phone':'0.8','PC':'0.9'},
			'chr':None,
			'chrs':[],
			'messadd':None
		}

	#Attrs={'bg':(bgs,attrs),'chrs':[(name,attrs),(name,attrs)...],'chr':...,'messadd':[]}
	#人物的显示顺序有待改进
	def decode(self,Bases,Attrs):
		Bases=Bases.replace('，',',').split(',')
		for base in Bases:
			base=base.replace('：',':').split(':')
			if base[0] not in self.keywords:
				self.fs.error('This HPC base attribute '+base[0]+' does not suppoted!')
			else:
				self.args[self.keywords[base[0]]]=base[1]
		if self.args['modes']=='Call':
			for attrs in Attrs:
				if attrs=='bg':
					self.args[attrs].refresh(Attrs[attrs][0],Attrs[attrs][1])
				elif attrs=='chrs':
					for attr in Attrs[attrs]:
						if self.us.ChrName[attr[0]][len(self.us.ChrName[attr[0]])-1] not in self.args[attrs]:
							self.args[attrs].append(self.us.ChrName[attr[0]][len(self.us.ChrName[attr[0]])-1])
						self.us.ChrName[attr[0]][len(self.us.ChrName[attr[0]])-1].rfattrs(attr[1])
				else:
					self.fs.error('This flag '+attrs+' does not exist !')
		elif self.args['modes']=='Message':
			for attrs in Attrs:
				if attrs=='chr':
					self.args[attrs]=Attrs[attrs]
				elif attrs=='messadd':
					self.args[attrs]=[]
					for mess in Attrs[attrs]:
						mess=re.match(r'\s*<n>(\S+)</n><p>(\S+)</p><t>(\S+)</t>',mess)
						if mess:
							mess=("'"+mess.group(1)+"'","'"+mess.group(2)+"'","'"+mess.group(3)+"'")
						else:
							self.fs.error('This message line is unexpected !')
						self.args[attrs].append(mess)
				else:
					self.fs.error('This flag '+attrs+' does not exist !')
		elif self.args['modes']=='Web':
			pass

	# def setvalue(self,Modem=None,Modes=None,Owner=None,Hide=None,Pos=None,Trans=None,Bg=None,Chr=None,Chrs=None,MessAdd=None):
	# 	def set(e,v):
	# 		if v:
	# 			self.args[e]=v
	# 	set('modem',Modem)
	# 	set('modes',Modes)
	# 	set('owner',Owner)
	# 	set('hide',Hide)
	# 	set('pos',Pos)
	# 	set('trans',Trans)
	# 	set('bg',Bg)
	# 	set('chr',Chr)
	# 	set('chrs',Chrs)
	# 	set('messadd',MessAdd)

	def check(self):
		for arg in self.argrange:
			if self.args[arg]==None:
				self.fs.error('This HPC base argument '+arg+' is None !')
			elif self.args[arg] not in self.argrange[arg]:
				self.fs.error('This HPC base argument '+arg+' is out of its range !')
			if self.args['modes']=='Call':
				if self.args['bg']==None or self.args['bgz']==None or self.args['chrs']==None:
					self.fs.error('This HPC necessary argument bg/bgz/chrs in '+self.args['modem']+self.args['modes']+' is None !')
			elif self.args['modes']=='Message':
				if self.args['chr']==None:
					self.fs.error('This HPC necessary argument chr in '+self.args['modem']+self.args['modes']+' is None !')
			elif self.args['modes']=='Web':
				pass

	def show(self):
		self.check()
		rn='    call HPC('
		rn+="ModeM='"+self.args['modem']+"',ModeS='"+self.args['modes']+"',Hide="+self.args['hide']+','
		rn+="Owner='"+self.args['owner']+"',Pos="+self.us.BgPosition[self.args['pos']]+',Trans='+self.us.Trans[self.args['trans']]+','
		if self.args['modes']=='Call':
			rn+=self.call()
		elif self.args['modes']=='Message':
			rn+=self.mess()
		elif self.args['modes']=='Web':
			rn+=self.web()
		return rn

	def call(self):
		rn=''
		ChrAttrs=[]
		self.args['bg'].checkattrs()
		BgAttrs=self.args['bg'].getattrs()
		for char in self.args['chrs']:
			char.checkattrs()
			ChrAttrs.append(char.getattrs())
		rn+='Bg=('+BgAttrs['m']+BgAttrs['s']+BgAttrs['w']+'HPC,'+BgAttrs['l']+','+self.args['bgz'][self.args['modem']]+'),'
		rn+='Chrs=['
		for chrattr in ChrAttrs:
			rn+='('+chrattr['name']+chrattr['p']+chrattr['c']+chrattr['f']+chrattr['d']+'HPC,'+chrattr['l']+','+self.args['chrz'][self.args['modem']]+'),'
		rn=rn[:-1]+'])\n'
		self.args['trans']=self.tDefault[self.args['modem']]
		return rn

	def mess(self):
		rn="Chr='"+self.args['chr']+"',"
		if self.args['messadd']:
			rn+='MessAdd=['
			for mess in self.args['messadd']:
				rn+='('
				for arg in mess:
					rn+=arg+','
				rn=rn[:-1]+'),'
			self.args['messadd']=None
			rn=rn[:-1]+'])\n'
		else:
			rn=rn=rn[:-1]+')\n'
		return rn

	def web(self):
		pass





