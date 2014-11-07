#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

#A super class for user's tag by flag
class TagSource():
	def __init__(self):
		pass
	def GetFlag(self):
		return self.__class__.__name__.replace('Tag').lower()
	def Get(self,Flag,US):
		tags={}
		#'m' tag is a special tag which content all top-level attributes
		if Flag in US.Args:
			tags['m']=[]
			for m in US.Args[Flag]:
				tags['m'].append(m)
		if 'Tag' in US.Args[flag]:
			tmp=dict(US.Args[Flag]['Tag'])
			for arg in tmp:
				tmp[arg]={}
				for m in tags['m']:
					tmp[arg][m]=US.Args[Flag][m][US.Args[Flag]['Tag']]
			tags.update(tmp)
		return tags