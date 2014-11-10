#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgmDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/bgm.rpy'
		elepath=US.Args['pathmode']['BgmPath']
		Args=US.Args[Flag]
		so=''
		for ele in Args:
			so+='define bgm_'+os.splitext(Args[ele])[0]+' = '
			so+="'"elepath+Args[ele]+"'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash