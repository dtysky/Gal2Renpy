#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class KeyDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/mykey.rpy'
		Args=US.Args[Flag]
		so='define mykeyinit={'
		for ele in Args:
			l=[]
			so+="\n    '"+k+"':{\n        'l':["
			for s in Args[ele]:
				so+="'"+s[0]+"',"
			so=so[:-1]+'],\n'
			for s in Args[ele]:
				so+="\n        '"+s[0]+"':{'Unlock':'0','New':'False',["
				for sk in s[1:]:
					so+="'"+sk+"',"
				so=so[:-1]+']},'
			so=so[:-1]+'\n    },'
		so=so[:-1]+'\n}\n'
		#define a function to set mykey's station in renpy
		so+='init python:\n'
		so+='    def SetMyKey(kn,k,i):\n'
		so+="        if i>persistent.mykey[kn][k]['Unlock']:\n"
		so+="           persistent.mykey[kn][k][Unlock]=i\n"
		so+="            persistent.mykey[kn][k]['New']=True\n"
		so+='    def InitMyKey():\n'
		so+='        if persistent.mykey==None:\n'
		so+='            persistent.mykey=mykeyinit\n'
		so+='    class ReStMyKey(Action):\n'
		so+='        def __init__(self,kn,k):\n'
		so+='            self.kn=kn\n'
		so+='            self.k=k\n'
		so+='        def __call__(self):\n'
		so+="            persistent.mykey[self.kn][self.k]['New']=False\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash