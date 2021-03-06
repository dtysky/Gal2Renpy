#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcMessaddTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'n':{}}
		for m in US.Args['ch']:
			if m not in ['Common','Tag']:
				tags['n'][m]=US.Args['ch'][m]['Name']
		tags['ch']=dict(tags['n'])
		tags['p']=None
		tags['t']=None
		return tags