#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Flag not in Tmp.Args:
			Tmp.Args[Flag]=None
		if name!='Black' and Tmp.Args[Flag]!=name:
			sw+='    scene bg Black01A with '+Attrs['t']+'\n'
		sw+='    scene bg '+name+Attrs['s']+Attrs['w']+' at '+Attrs['l']+'\n'
		sw+='    with '+Attrs['t']+'\n'
		Tmp.Args[Flag]=name
		return sw