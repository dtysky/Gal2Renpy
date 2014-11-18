#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import re,locale

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
			attrs=re.findall(r'[a-z]+:.*?(?=\n|\s+[a-z]+:)',attrs)
			if not attrs:
				return None
			for attr in attrs:
				attr=attr.split(':')
				r[attr[0]]=attr[1]
			return r
		self.attrs={}
		for flag in Attrs1:
			tmp=None
			if Attrs1[flag]:
				tmp=Syntax(Attrs1[flag])
			if tmp:
				self.attrs[flag]=tmp
			else:
				self.attrs[flag]={}
		tmp=Syntax(Attrs2)
		if tmp:
			self.attrs[self.GetFlag()].update(tmp)
		#If no nesting, attrs will be a 1-level dict which content all attributes
		if len(self.attrs)==1:
			self.attrs=self.attrs[self.GetFlag()]
	#Return flag by class name 
	def GetFlag(self):
		s=self.__class__.__name__.replace('Sp','')
		tmp=''
		for _s_ in s:
			tmp+=_s_ if _s_.islower() else '_'+_s_.lower()
		return tmp[1:]
	#A interface
	def Get(self):
		return dict(self.attrs)
	#Check all attributes and return a dict depended on flag
	#Only support one flag
	def Check(self,Flag,Attrs,UT,FS):
		Attrs=dict(Attrs)
		for tag in Attrs:
			if tag not in UT.Args[Flag]:
				FS.Error("This flag '"+Flag+"' does not have tag '"+tag+"' !")
		for tag in UT.Args[Flag]:
			if tag not in Attrs:
				FS.Error("This flag '"+Flag+"' must have tag '"+tag+"' !")
		name=None
		orgname=None
		#If 'm' tag enable, change it to 'name'
		if 'm' in Attrs:
			if Attrs['m'] not in UT.Args[Flag]['m']:
				FS.Error("This flag '"+Flag+"' does not have '"+Attrs['m']+"' !")
			name=UT.Args[Flag]['m'][Attrs['m']]
			orgname=Attrs['m']
			del Attrs['m']
		for tag in Attrs:
			#If no 'm' tag
			if not orgname:
				#If tag's value in UT is None, don't care it
				if UT.Args[Flag][tag]:
					if not UT.Args[Flag][tag].get(Attrs[tag]):
						FS.Error("This flag '"+Flag+"' does not have tag'"+tag+"' valued '"+Attrs[tag]+"'' !")
					Attrs[tag]=UT.Args[Flag][tag][Attrs[tag]]
				continue
			if UT.Args[Flag][tag][orgname]:
				if Attrs[tag] not in UT.Args[Flag][tag][orgname]:
					FS.Error("This tag '"+tag+"' in flag '"+Flag+"' have no value named '"+Attrs[tag]+"' !") 
				Attrs[tag]=UT.Args[Flag][tag][orgname][Attrs[tag]]
		return name,Attrs
	#Creat scripts which are related to charecters
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		return ''