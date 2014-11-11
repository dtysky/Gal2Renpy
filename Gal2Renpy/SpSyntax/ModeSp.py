#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ModeSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		Tmp.Args[Flag]=name
		return sw