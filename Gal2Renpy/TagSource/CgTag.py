#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class CgTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags=G2R.TagSource.Get(self,Flag,US)
		for cg in US.Args[Flag]:
			tags[]['s']=[]
			for ch in US.Args[Flag][cg]['Character']:
				for chnum in range(ch[1]):
					for bg in US.Args[Flag][cg]['Bg']:
						self.CgSub[cg].append(char[0]+str(charnum)+bg)

		