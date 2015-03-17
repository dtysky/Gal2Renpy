#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R,os

class MovieTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'m':{},'k':{}}
		for m in US.Args[Flag]:
			tags['m'][m]='movie_'+os.path.splitext(US.Args[Flag][m])[0]
			tags['k'][m]={'special':'special','normal':'normal','back':'back'}
		return tags