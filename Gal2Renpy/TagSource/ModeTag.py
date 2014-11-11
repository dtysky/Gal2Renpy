#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ModeTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'m':{'ADV':'ADV','NVL':'NVL'}}
		return tags