#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class EfSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		sw+='    call '+UT.Args[Flag]['e'][Attrs['e']]+'('
		sw+=Attrs['args'].replace('this',Attrs['c'])
		sw+=')\n'
		return sw