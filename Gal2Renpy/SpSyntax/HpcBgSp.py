#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcBgSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,UT,Tmp,FS):
		sw=''
		nameHpc,AttrsHpc=self.Check(Flag['hpc'],Attrs['hpc'],UT,FS)
		nameBg,AttrsBg=self.Check(Flag,Attrs[Flag],UT,FS)
		if Attrs['t']=='Hide':
			Attrs['t']='True'
		sw='    call HPC('
		sw+="ModeM='"+AttrsHpc['mm']+"',ModeS='"+AttrsHpc['ms']+"',Hide="+AttrsHpc['hide']+','
		sw+="Owner='"+AttrsHpc['o']+"',Pos="+AttrsHpc['l']+',Trans='+AttrsHpc['t']+','
		sw+='Bg=('+nameBg+AttrsBg['s']+AttrsBg['w']+'HPC,'+AttrsBg['l']+','
		if AttrsHpc['mm']=='PC':
			sw+=AttrsBg['l']+',0.9)\n'
		else:
			sw+=AttrsBg['l']+',0.8)\n'
		return sw