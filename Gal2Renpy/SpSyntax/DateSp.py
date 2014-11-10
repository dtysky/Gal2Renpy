#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class DateSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp):
		sw=''
		if 'm' not in Attrs:
			G2R.TagError("This flag '"+Flag+"' must have tag 'm' !")
		sw+="    $ store.date = '"+Attrs['m']+"'\n"
		if Flag not in Tmp:
			Tmp[Flag]={'Data1':Attrs['m'],'Data2':Attrs['m']}
		Tmp[Flag]['Date1']=Tmp[Flag]['Date2']
		Tmp[Flag]['Date2']=Attrs['m']
		return sw