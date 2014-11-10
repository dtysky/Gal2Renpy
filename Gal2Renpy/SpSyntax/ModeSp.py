#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ModeSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT)
		Tmp['Mode']=Attrs['m']
		return sw