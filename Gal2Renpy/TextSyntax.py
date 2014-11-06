#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

#The normal-text-syntax super class
class TextSyntax():
	def __init__(self):
		self.attrs={}
	#Refresh text
	def Refresh(self,Text,Style,Mode):
		self.say['Text']=Text
		self.say['Style']=Style
		self.say['Mode']=Mode
	#Creat scripts
	def Show(self):
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