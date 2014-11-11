#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class TestSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Tmp.Args.get(Flag):
			if Tmp.Args[Flag]==name:
				FS.Error('Last test does not'+name+' !')
		Tmp.Args[Flag]=name
		return sw