#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcMessaddSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		AttrsOrg=dict(Attrs)
		nameH,AttrsH=self.Check('hpc',Attrs['hpc'],UT,FS)
		AttrsH.update(self.Check(Flag,Attrs[Flag],UT,FS)[1])
		Attrs=AttrsH
		if Attrs['n'] not in [Attrs['o'],Attrs['ch']]:
			G2R.SourceError("This tag 'n' in flag '"+Flag+"' must have a vaule between tag 'o' and 'ch' value !") 
		sw+="    $ HPCMessAdd('"+AttrsOrg['hpc']['o']+"','"+AttrsOrg[Flag]['n']+"',"
		sw+="('"+AttrsOrg[Flag]['ch']+"','"+Attrs['p']+"','"+Attrs['t']+"'))\n"
		return sw