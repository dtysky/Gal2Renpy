#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class SoundSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if name=='sound_StopSound':
			sw+='    stop sound fadeout 1.0\n'
			return sw
		sw+='    play sound '+name
		if Attrs['k']=='loop':
			sw+=' loop'
		sw+='\n'
		return sw