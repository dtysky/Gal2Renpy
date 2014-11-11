#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ScTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'k':{'Main':'Main','Other':'Other'},'sc':None,'cp':None}
		return tags