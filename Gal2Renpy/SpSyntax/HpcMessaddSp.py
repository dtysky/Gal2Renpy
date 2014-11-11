#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcMessaddSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check('hpc',Attrs['hpc'],UT,FS)
		Attrs.update(self.Check(Flag,Attrs[Flag],UT,FS)[1])
		if Attrs['n'] not in [Attrs['o'],Attrs['ch']]:
			G2R.SourceError("This tag 'n' in flag '"+Flag+"' must have a vaule between tag 'o' and 'ch' value !") 
		sw+="    $ HPCMessAdd('"+Attrs[o]+"','"+Attrs['ch']+"','"
		sw+="('"+Attrs['n']+"','"+Attrs['p']+"','"+Attrs['t']+"'))\n"
		return sw