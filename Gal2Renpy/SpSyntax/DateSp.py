#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class DateSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		if 'm' not in Attrs:
			FS.Error("This flag '"+Flag+"' must have tag 'm' !")
		sw+="    $ store.date = '"+Attrs['m']+"'\n"
		if Flag not in Tmp.Args:
			Tmp.Args[Flag]={'Date1':Attrs['m'],'Date2':Attrs['m']}
		Tmp.Args[Flag]['Date1']=Tmp.Args[Flag]['Date2']
		Tmp.Args[Flag]['Date2']=Attrs['m']
		return sw