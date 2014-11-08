#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ChcTag(G2R.TagSource):
	def Get(self,Flag,US):
		tags={'a':{},'b':{}}
		for m in US.Args['ch']:
			if m not in ['Common','Tag']:
				tags['a'][m]=US.Args['ch'][m]['Name']
		tags['b']=dict(tags['a'])
		return tags