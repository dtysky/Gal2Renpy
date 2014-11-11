#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

#The special-text-syntax super class
class GfSp(G2R.SpSyntax):
	#Creat scripts which are related to charecters
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		orgname=Attrs['m']
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if Attrs['t']=='hide':
			sw+='    hide '+name+'\n'
			return sw
		Type=US.Args[Flag][orgname]['Type']
		if Type=='Frame':
			Pause=US.Args[Flag][orgname]['Pause']
			sw+='    show '+name+' at '+Attrs['l']+'\n'
			sw+='    pause '+Pause+'\n'
			sw+='    hide '+name+'\n'
			sw+='    pause 0.5\n'
		elif Type=='Image':
			sw+='    show '+name+' at '+Attrs['l']+'\n'
			sw+='    with '+Attrs['t']+'\n'
		elif Type=='Chapter':
			Pause=US.Args[Flag][orgname]['Pause']
			sw+='    scene bg Black01A with dissolve\n'
			sw+='    scene '+name+' with dissolve\n'
			sw+='    pause '+Pause+'\n'
			sw+='    pause 2.0\n'
			sw+='    scene bg Black01A with dissolve\n'
		return sw