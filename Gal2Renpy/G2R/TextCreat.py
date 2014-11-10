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
		self.say['type']=Type
		#Speaker/Thinker
		self.say['name']=Name
		#Text
		self.say['text']=Text
	#Creat scripts
	def Show(self,US,FS):
		if self.say['name']:
			if not US.Args['ch'].get(self.say['name']):
				FS.Error('This character name '+self.say['name']+' does not exit !')
		rn=''
		if self.say['mode']=='text':
			rn+=self.say['text']
		elif self.say['mode']=='say':
			rn+=self.say['name']+self.say['type']+' '
			n+="'"+self.say['text']+"'\n"
		elif self.say['mode']=='think':
			rn+=self.say['name']+self.say['type']+' '
			rn+="'（"+self.say['Text']+"）'\n"
		return '    '+rn