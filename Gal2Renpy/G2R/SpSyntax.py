#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
from Error import *
import re

#The special-text-syntax super class
class SpSyntax():
	"""
	Creat ren'py script by flag and tags
	"""
	def __init__(self):
		self.attrs={}
	#Refresh attributes
	#Attrs1 is a dict content all attributes,attrs2 is a line
	#Attrs1:{flag1:attrs11,flag2:attrs12}
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
		for flag in Attrs1:
			tmp=Syntax(Attrs1['flag'])
			if tmp:
				self.attrs[flag]=tmp
		tmp=Syntax(Attrs2)
		if tmp:
			self.attrs[self.GetFlag()].update(tmp)
		#If no nesting, attrs will be a 1-level dict which content all attributes
		if len(self.attrs)==1:
			self.attrs=self.attrs[self.GetFlag()]
	#Return flag by class name 
	def GetFlag(self):
		s=self.__class__.__name__.replace('Sp')
		tmp=''
		for _s_ in s:
			tmp+=_s_ if _s_.islower() else '_'+_s_.lower()
		return tmp[1:]
	#A interface
	def Get(self):
		return dict(self.attrs)
	#Check all attributes and return a dict depended on flag
	#Only support one flag
	def Check(self,Flag,Attrs,UT):
		Attrs=dict(Attrs)
		for tag in Attrs:
			if tag not in UT[Flag]:
				TagError("This flag '"+Flag+"' does not have tag '"+tag+"' !")
		for tag in UT[Flag]:
			if tag not in Attrs:
				TagError("This flag '"+Flag+"' must have tag '"+tag+"' !")
		name=None
		#If 'm' tag enable, change it to 'name'
		if 'm' in Attrs:
			if Attrs['m'] not in UT[Flag]['m']:
				SourceError("This flag '"+Flag+"' does not have '"+Attrs['m']+"' !")
			name=UT[Flag]['m'][Attrs['m']]
			del Attrs['m']
		for tag in Attrs:
			#If no 'm' tag
			if not name:
				#If tag's value in UT is None, don't care it
				if UT[Flag][tag]):
					if not UT[Flag][tag].get(Attrs[tag]):
						SourceError("This flag '"+Flag+"' does not have tag'"+tag+"' valued '"+Attrs[tag]+"'' !")
					Attrs[tag]=UT[Flag][tag][Attrs[tag]]
				continue
			if Attrs[tag] not in UT[Flag][tag][name]:
				SourceError("This tag '"+tag+"' in flag '"+Flag+"' have no value named '"+Attrs[tag]+"' !") 
			Attrs[tag]=UT[Flag][tag][name][Attrs[tag]]
		return name,Attrs
	#Creat scripts which are related to charecters
	def Show(self,Flag,Attrs,US,UT,Tmp):
		return ''