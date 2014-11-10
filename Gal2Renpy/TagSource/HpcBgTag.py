#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcBgTag(G2R.TagSource):
	def Get(self,Flag,US):
		return G2R.TagSource.Get(self,'bg',US)