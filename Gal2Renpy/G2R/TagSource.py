#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

#A super class for user's tag by flag
class TagSource():
	"""
	Creat tags for flag from user's source
	"""
	def __init__(self):
		pass
	def GetFlag(self):
		return self.__class__.__name__.replace('Tag').lower()
	def Get(self,Flag,US):
		tags={}
		#'m' tag is a special tag which content all top-level attributes
		if Flag in US.Args:
			tags['m']={}
			#If top-level key's value is not a dict or list,'m' tag's value will be as it's original set
			for m in US.Args[Flag]:
				if isinstance(US.Args[Flag][m],dict) or isinstance(US.Args[Flag][m],list):
					tags['m'][m]=m
				else:
					tags['m']=US.Args[Flag][m]
		if 'Tag' in US.Args[flag]:
			tmp=dict(US.Args[Flag]['Tag'])
			for arg in tmp:
				tmp[arg]={}
				for m in tags['m']:
					tmp[arg][m]=dict(US.Args[Flag][m][US.Args[Flag]['Tag']])
			tags.update(tmp)
		return tags