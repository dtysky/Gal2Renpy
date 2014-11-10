#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class CgSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,UT,Tmp):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT)
		sw+='    scene cg '+name+Attrs['s']+' at '+Attrs['l']+'\n'
		sw+='    with '+Attrs['t']+'\n'
		return sw