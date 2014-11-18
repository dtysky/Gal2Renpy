#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class DateSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Flag not in Tmp.Args:
			Tmp.Args[Flag]={'Auto':'Off'}
		if name=='Auto':
			Tmp.Args[Flag][name]=Attrs['s']
			if Attrs['s']=='Off':
				sw+='    hide screen '+US.Args['pathmode']['DateScreen']+'\n'
			return sw
		if 'DateLast' not in Tmp.Args[Flag]:
			Tmp.Args[Flag].update({'DateLast':Attrs['s'],'DateNow':Attrs['s']})
		sw+="    $ store.date = '"+Attrs['s']+"'\n"
		Tmp.Args[Flag]['DateLast']=Tmp.Args[Flag]['DateNow']
		Tmp.Args[Flag]['DateNow']=Attrs['s']
		path=US.Args['pathmode']['DatePath']
		sw+="    $ store.DateLast='"+path+Tmp.Args[Flag]['DateLast']+".png'\n"
		sw+="    $ store.DateNow='"+path+Tmp.Args[Flag]['DateNow']+".png'\n"
		return sw