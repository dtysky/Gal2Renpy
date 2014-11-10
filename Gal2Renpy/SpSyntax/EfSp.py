#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class EfSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp):
		sw=''
		for tag in ['e','args','m']:
			if tag not in Attrs:
				TagError("This flag '"+Flag+"' must have tag '"+tag+"' !") 
		sw+='    call '+UT[Flag]['e'][Attrs['e']]+'('
		sw+=Attrs[args].replace('this',Attrs['m'])
		sw+=')\n'
		return sw