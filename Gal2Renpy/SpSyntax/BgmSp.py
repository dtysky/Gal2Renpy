#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgmSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT)
		if name=='StopBgm':
			sw+='    stop music fadeout 1.0\n'
		else:
			sw+='    play music '+name+' fadein 1.0\n'
		return sw