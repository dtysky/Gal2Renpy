#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class EfSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		for tag in ['e','args','m']:
			if tag not in Attrs:
				FS.Error("This flag '"+Flag+"' must have tag '"+tag+"' !") 
		sw+='    call '+UT.Args[Flag]['e'][Attrs['e']]+'('
		sw+=Attrs['args'].replace('this',Attrs['m'])
		sw+=')\n'
		return sw