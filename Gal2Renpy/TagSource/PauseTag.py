#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class PauseTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'p':None}
		return tags