#-*-coding:utf-8-*- 
import re
import sys
import os
from ctypes import *
import codecs
from Keyword import *
from User import *
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
		MessageBox(e+'\n'+'file : '+self.path+'\n'+'line : '+str(self.linepos))
		sys.exit(0)
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


#A class for charecter
class Chr():
	#One or two arguments 
	def __init__(self,*Text):
		if len(Text)==2:
			self.name=Text[0]
			self.orgname=Text[1]
			#'new' will be true if the attributes has been changed
			self.attrs={'e':None,'f':None,'c':None,'p':None,'l':None,'new':False}
			self.complete=False
		elif len(Text)==4:
			self.name=Text[0]
			self.orgname=Text[1]
			self.attrs={'e':None,'f':None,'c':None,'p':None,'l':None,'new':False}
			self.rfattrs(Text[2],Text[4])
		#Text,Say or Think,Mode,Is refreshed
		self.say={'Text':None,'Style':None,'Mode':None,'new':False}
	#Refresh attributes in this charecter
	def rfattrs(self,Attrs,Fs):
		for attr in Attrs.replace('，',',').split(','):
			ttmp=attr.replace('：',':').split(':')
			if ChrKeyword.get(ttmp[0])==None:
				Fs.error("This charecter's attribute does not exist !")
			else:
				if ChrKeyword[ttmp[0]][self.orgname].get(ttmp[1])==None:
					Fs.error("This "+ChrKeyword[ttmp[0]]+" does not exist !")
				else:
					self.attrs[ttmp[0]]=ChrKeyword[ttmp[0]][self.orgname][ttmp[1]]
			self.attrs['new']=True
	#Refresh next word by this charecter
	def rftext(self,Text,Style,Mode):
		self.say['Text']=Text
		self.say['Style']=Style
		self.say['Mode']=Mode
		self.say['new']=True
	#Creat scripts which are related to charecters
	def show(self):
		rn=''
		if self.attrs['new']:
			if self.complete==False:
				for attr in self.attrs:
					if self.attrs[attr]==None:
						MessageBox("This charecter's attributes are not complete !")
						sys.exit(0)
					self.complete==True
			rn+='    show '+self.name+self.attrs['c']+self.attrs['p']+self.attrs['f']
			rn+=' at '+self.attrs['l']+'\n'
			rn+='    with '+self.attrs['e']+'\n'
			self.attrs['new']=False
			return rn
		elif self.say['new']:
			rn+=self.name+self.say['Mode']+' '
			if self.say['Style']=='Say':
				rn+='''"'''+self.say['Text']+'''"'''+'\n'
			else:
				rn+='''"（'''+self.say['Text']+'''）"'''+'\n'
			self.say['new']=False
			return '    '+rn
		else:
			MessageBox('This charecter does not be created !')
			sys.exit(0)




