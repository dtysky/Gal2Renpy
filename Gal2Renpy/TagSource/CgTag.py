#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class CgTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags=G2R.TagSource.Get(self,Flag,US)
		tags['s']={}
		for cg in tags['m']:
			tags['s'][cg]={}
			for s in US.Args[Flag][cg]['Scene']:
				for knum in range(s[1]):
					for bg in US.Args[Flag][cg]['Background']:
						n=s[0]+str(knum)+bg
						tags['s'][cg][n]=n
		return tags