#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class MovieSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		name,Attrs=self.Check(Flag,Attrs,UT,FS)
		if name=='movie_StopMovie':
			sw+='    hide movie with Dissolve(0.6)\n'
			sw+='    stop movie\n'
			return sw
		if Attrs['k']=='special':
			sw+='    image movie = Movie(size=(1920,1080),xcenter=0.5,ycenter=0.5)\n'
			sw+='    show movie\n'
			sw+='    play movie '+name+'\n'
		elif Attrs['k']=='back':
			sw+='    image movie = Movie(size=(1920,1080),xcenter=0.5,ycenter=0.5)\n'
			sw+='    play movie '+name+' loop\n'
			sw+='    show movie with Dissolve(1.0)\n'
		return sw