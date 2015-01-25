#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class PauseSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Attrs['p']=='None':
			sw+='    pause'+'\n'
		else:
			sw+='    pause '+Attrs['p']+'\n'
		return sw