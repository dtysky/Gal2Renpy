#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ChSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Attrs['t']=='hide':
			sw+='    show '+name+' '
			sw+='at '+Attrs['l']+'\n'
			sw+='    with MoveTransition(0.5)\n'
			sw+='    hide '+name+'\n'
		else:
			sw+='    show '+name+' '+Attrs['p']+Attrs['c']+Attrs['f']+Attrs['d']+' '
			sw+='at '+Attrs['l']+'\n'
			sw+='    with '+Attrs['t']+'\n'
		return sw