#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R,os

class BgmTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'m':{}}
		for m in US.Args[Flag]:
			tags['m'][m]='bgm_'+os.path.splitext(US.Args[Flag][m])[0]
		return tags