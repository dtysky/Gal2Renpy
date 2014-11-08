#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ChTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags=G2R.TagSource.Get(self,Flag,US)
		for m in tags['m']:
			tags['m'][m]=US.Args[Flag][m]['Name']
		return tags