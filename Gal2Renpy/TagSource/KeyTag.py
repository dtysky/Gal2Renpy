#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class KeyTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags=G2R.TagSource.Get(self,Flag,US)
		tags['s']={}
		tags['n']={}
		for k in tags['m']:
			tags['s'][k]={}
			tags['n'][k]={}
			for s in US.Args[Flag][k]:
				tags['s'][k][s[0]]=s[0]
				tags['n'][k][s[0]]={}
				for i in range(len(s)-1):
					tags['n'][k][s[0]][str(i)]=str(i)
		return tags