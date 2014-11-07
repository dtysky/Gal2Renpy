#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import re

#The special-text-syntax super class
class SpSyntax():
	def __init__(self):
		self.attrs={}
	#Refresh attributes
	#attrs1 is a list content all attributes,attrs2 is a line
	def Refresh(self,Attrs1,Attrs2):
		def Syntax(attrs):
			r={}
			attrs=re.findall(r'[a-z]+:.*',attrs)
			if not attrs:
				return None
			for attr in attrs:
				attr=attr.split(':')
				r[attr[0]]=r[attr[1]]
			return r
		for attrs in attrs1:
			tmp=Syntax(attrs)
			if tmp:
				self.attrs.update(tmp)
		tmp=Syntax(attrs1)
		attrs1=re.findall(r'[a-z]+:.*',attrs1)
		if tmp:
			self.attrs.update(tmp)
		return self.attrs
	#Check whether the attributes completely
	def Check(self):
		if self.attrs['new']:
			if self.complete==False:
				for attr in self.attrs:
					if self.attrs[attr]==None:
						self.fs.error("This charecter's attributes are not complete !")
	#A interface
	def Get(self):
		rn=self.attrs
		rn.update({'name':self.name})
		return rn

	#Creat scripts which are related to charecters
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