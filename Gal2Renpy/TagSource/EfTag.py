#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class EfTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'e':{},'args':None,'c':None}
		for e in US.Args[Flag]:
			tags['e'][e]=US.Args[Flag][e]
		return tags