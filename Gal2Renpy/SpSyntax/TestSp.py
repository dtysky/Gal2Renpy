#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class TestSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT)
		if Tmp[Flag]:
			if Tmp[Flag]==name:
				G2R.TagError('Last test does not'+name+' !')
		Tmp[Flag]=name
		return sw