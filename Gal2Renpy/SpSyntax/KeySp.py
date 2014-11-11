#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class KeySp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		rn+="    $ SetMyKey('"+Attrs['m']+"','"+Attrs['s']+"',"+Attrs['n']+')\n'
		rn+='    call EfTextKey()\n'
		return sw