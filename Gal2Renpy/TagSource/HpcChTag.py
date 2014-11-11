#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcChTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags=G2R.TagSource.Get(self,'ch',US)
		for m in tags['m']:
			tags['m'][m]=US.Args['ch'][m]['Name']
		return tags