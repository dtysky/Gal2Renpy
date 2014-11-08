#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class KeyTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags=G2R.TagSource.Get(self,Flag,US)
		tags['s']=[]
		tags['n']={}
		for k in tags['m']:
			tags['s'][k]={}
			for s in US.Args[Flag][k]:
				tags['s'][k].qppend(s[0])
				tags['n'][k][s[0]]=['Total: '+len(s)-1]
		return tags