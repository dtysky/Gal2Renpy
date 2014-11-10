#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

#The special-text-syntax super class
class ChSp(G2R.SpSyntax):
	#Creat scripts which are related to charecters
	def Show(self,Flag,Attrs,UT,Tmp):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT)
		if Attrs['t']=='hide':
			sw+='    hide '+name+'\n'
		else:
			sw+='    show '+name+' '+Attrs['p']+Attrs['c']+Attrs['f']+Attrs['d']+' '
			sw+='at '+Attrs['l']+'\n'
			sw+='    with '+Attrs['t']+'\n'
		return sw