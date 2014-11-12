#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

#The normal-text-syntax super class
class TextCreat():
	def __init__(self):
		self.say={}
	#Refresh text
	def Refresh(self,Mode,Type,Text,Name=None):
		#say/think/text
		self.say['mode']=Mode
		#ADV/NVL
		if Type=='ADV':
			self.say['type']='A'
		else:
			self.say['type']='V'
		#Speaker/Thinker
		self.say['name']=Name
		#Text
		self.say['text']=Text
	#Creat scripts
	def Show(self,US,FS):
		if self.say['name']:
			if self.say['name'] not in US.Args['ch']:
				FS.Error('This character name '+self.say['name']+' does not exit !')
			self.say['name']=US.Args['ch'][self.say['name']]['Name']
		rn=''
		if self.say['mode']=='text':
			rn+="n '"+self.say['text']+"'\n"
		elif self.say['mode']=='say':
			rn+=self.say['name']+self.say['type']+' '
			rn+="'"+self.say['text']+"'\n"
		elif self.say['mode']=='think':
			rn+=self.say['name']+self.say['type']+' '
			rn+="'( "+self.say['text']+" )'\n"
		return '    '+rn