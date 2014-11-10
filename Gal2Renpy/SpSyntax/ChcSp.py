#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ChcSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,UT,Tmp):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT)
		sw+='    $ '+Attrs['a']+'A = '+Attrs['b']+'A\n'
		sw+='    $ '+Attrs['a']+'V = '+Attrs['b']+'V\n'
		return sw