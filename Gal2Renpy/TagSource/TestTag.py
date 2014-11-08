#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class TestTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'m':['Begin','End']}
		return tags
