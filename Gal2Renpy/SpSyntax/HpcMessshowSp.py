#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcMessshowSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		AttrsOrg=dict(Attrs)
		name,AttrsH=self.Check('hpc',Attrs['hpc'],UT,FS)
		AttrsH.update(self.Check(Flag,Attrs[Flag],UT,FS)[1])
		Attrs=AttrsH
		Attrs['hide']='False'
		if Attrs['t']=='Hide':
			Attrs['hide']='True'
		sw='    call HPC('
		sw+="ModeM='"+Attrs['mm']+"',ModeS='"+Attrs['ms']+"',Hi="+Attrs['hide']+','
		sw+="Owner='"+AttrsOrg['hpc']['o']+"',Chr='"+AttrsOrg[Flag]['ch']
		sw+="',Pos="+Attrs['l']+',Trans='+Attrs['t']+')\n'
		return sw