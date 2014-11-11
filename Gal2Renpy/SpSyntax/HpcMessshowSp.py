#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcMessshowSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check('hpc',Attrs['hpc'],UT,FS)
		Attrs.update(self.Check(Flag,Attrs[Flag],UT,FS))[1]
		if Attrs['t']=='Hide':
			Attrs['t']='True'
		sw='    call HPC('
		sw+="ModeM='"+Attrs['mm']+"',ModeS='"+Attrs['ms']+"',Hide="+Attrs['hide']+','
		sw+="Owner='"+Attrs['o']+"Chr='"+Attrs['ch']
		sw+="',Pos="+Attrs['l']+',Trans='+Attrs['t']+')\n'
		return sw