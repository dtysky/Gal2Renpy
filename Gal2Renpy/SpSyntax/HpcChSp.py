#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class HpcChSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,UT,Tmp,FS):
		sw=''
		nameHpc,AttrsHpc=self.Check(Flag['hpc'],Attrs['hpc'],UT,FS)
		nameCh,AttrsCh=self.Check(Flag,Attrs[Flag],UT,FS)
		if Attrs['t']=='Hide':
			Attrs['t']='True'
		sw='    call HPC('
		sw+="ModeM='"+AttrsHpc['mm']+"',ModeS='"+AttrsHpc['ms']+"',Hide="+AttrsHpc['hide']+','
		sw+="Owner='"+AttrsHpc['o']+"',Pos="+AttrsHpc['l']+',Trans='+AttrsHpc['t']+','
		sw+='Ch=('+nameCh+AttrsCh['p']+AttrsCh['c']+AttrsCh['f']+AttrsCh['d']+'HPC,'
		if AttrsHpc['mm']=='PC':
			sw+=AttrsCh['l']+',0.8)\n'
		else:
			sw+=AttrsCh['l']+',0.6)\n'
		return sw