#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ScSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Attrs['k']=='Main':
			sw+='    $ store.chapter='
			sw+="'Chapter."+Attrs['cp']+Attrs['sc']+"'\n"
		return sw