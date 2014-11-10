#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT)
		if name!='Black':
			sw+='    scene bg Black01A with '+Attrs['t']+'\n'
		sw+='    scene bg '+name+Attrs['s']+Attrs['w']+' at '+Attrs['l']+'\n'
		sw+='    with '+Attrs['t']+'\n'
		return sw