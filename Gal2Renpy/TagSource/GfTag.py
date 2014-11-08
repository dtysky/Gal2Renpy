#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class GfTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'m':{}}
		for gf in US.Args[Flag]:
			tags['m'][gf]=US.Args[Flag][gf]['Name']