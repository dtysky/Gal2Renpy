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
			tags['s'][cg]=[]
			for k in US.Args[Flag][cg]['Kind']:
				for knum in range(k[1]):
					for bg in US.Args[Flag][cg]['Bg']:
						tags['s'][cg].append(k[0]+str(knum)+bg)