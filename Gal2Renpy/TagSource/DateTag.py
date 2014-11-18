#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class DateTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={}
		tags['m']={'Auto':'Auto','Value':'Value'}
		tags['s']={}
		tags['s']['Auto']={'On':'On','Off':'Off'}
		tags['s']['Value']=None
		return tags