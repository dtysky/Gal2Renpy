#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Flag not in Tmp.Args:
			Tmp.Args[Flag]={}
			for tag in ['m','s','w']:
				Tmp.Args[Flag][tag]=None
		Changed=False
		if Tmp.Args[Flag]['m']!=name:
			Changed=True
		for tag in ['s','w']:
			if Tmp.Args[Flag][tag]!=Attrs[tag]:
				Changed=True
		if name!='Black' and Changed:
			if Tmp.Args.get('date') and Tmp.Args['date']['Auto']=='On':
				sw+='    hide screen '+US.Args['pathmode']['DateScreen']+'\n'
			sw+='    scene bg Black01A with '+Attrs['t']+'\n'
		sw+='    scene bg '+name+Attrs['s']+Attrs['w']+' at '+Attrs['l']+'\n'
		sw+='    with '+Attrs['t']+'\n'
		if Tmp.Args.get('date') and Tmp.Args['date']['Auto']=='On':
			sw+='    show screen '+US.Args['pathmode']['DateScreen']+'\n'
		Tmp.Args[Flag]['m']=name
		for tag in ['s','w']:
			Tmp.Args[Flag][tag]=Attrs[tag]
		return sw