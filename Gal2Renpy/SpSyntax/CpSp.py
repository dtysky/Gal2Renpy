#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class CpSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		if 'm' not in Attrs:
			FS.Error("This flag '"+Flag+"' must have tag 'm' !")
		sw+="    $ store.chapter = '"+Attrs['m']+"'\n"
		return sw