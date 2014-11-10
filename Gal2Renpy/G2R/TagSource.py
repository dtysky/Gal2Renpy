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
		s=self.__class__.__name__.replace('Define')
		tmp=''
		for _s_ in s:
			tmp+=_s_ if _s_.islower() else '_'+_s_.lower()
		return tmp[1:]
	def Get(self,Flag,US):
		tags={}
		#'m' tag is a special tag which content all top-level attributes
		if Flag in US.Args:
			tags['m']={}
			#If top-level key's value is not a dict or list,'m' tag's value will be as it's original set
			if isinstance(US.Args[Flag],list):
				for m in US.Args[Flag]:
					tags['m']=m
			else:
				for m in US.Args[Flag]:
					if isinstance(US.Args[Flag][m],dict) or isinstance(US.Args[Flag][m],list):
						tags['m'][m]=m
					else:
						tags['m'][m]=US.Args[Flag][m]
		if 'Tag' in US.Args[flag]:
			tmp=dict(US.Args[Flag]['Tag'])
			dtmp={}
			for arg in tmp:
				dtmp[arg]={}
				for m in tags['m']:
					dtmp[arg][m]=US.Args[Flag][m][tmp[m]]
			tags.update(dtmp)
		return tags