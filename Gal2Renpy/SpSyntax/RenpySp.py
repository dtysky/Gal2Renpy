#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class RenpySp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		return '    '+Attrs['m']+'\n'