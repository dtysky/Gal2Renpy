#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class KeySp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp,FS):
		sw=''
		for tag in Attrs:
			if tag not in UT.Args[Flag]:
				FS.Error("This flag '"+Flag+"' does not have tag '"+tag+"' !")
		for tag in UT.Args[Flag]:
			if tag not in Attrs:
				FS.Error("This flag '"+Flag+"' must have tag '"+tag+"' !")
		if Attrs['m'] not in UT.Args[Flag]['m']:
			FS.Error("This flag '"+Flag+"' does not have tag 'm' valued '"+Attrs['m']+"'' !")
		if Attrs['s'] not in UT.Args[Flag]['s'][Attrs['m']]:
			FS.Error("This flag '"+Flag+"' does not have tag 's' valued '"+Attrs['s']+"'' !")
		if Attrs['n'] not in UT.Args[Flag]['n'][Attrs['m']][Attrs['s']]:
			FS.Error("This key '"+Attrs['s']+"' does not have tag 'n' valued '"+Attrs['n']+"'' !")
		Attrs['n']=UT.Args[Flag]['n'][Attrs['m']][Attrs['s']][Attrs['n']]
		Attrs['s']=UT.Args[Flag]['s'][Attrs['m']][Attrs['s']]
		Attrs['m']=UT.Args[Flag]['m'][Attrs['m']]
		sw+="    $ SetMyKey('"+Attrs['m']+"','"+Attrs['s']+"',"+Attrs['n']+')\n'
		sw+='    $ renpy.notify(Image(Key_Update))\n'
		return sw