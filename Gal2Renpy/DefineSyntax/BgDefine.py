#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS,DictHash):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/bg.rpy'
		elepath=US.Args['pathmode']['BgPath']
		Args=US.Args[Flag]
		so=''
		for ele in Args:
			for e in ['Name','Sub','Weather']:
				if e in Args[ele]:
					continue
				G2R.SourceError("This bg '"+ele+"' must have child '"+e+"' !")
			for s in Args[ele]['Sub']:
				s=Args[ele]['Sub'][s]
				for w in Args[ele]['Weather']:
					w=Args[ele]['Weather'][w]
					so+='image bg '+Args[ele]['Name']+s+w+' = '
					so+="'"+elepath+Args[ele]['Name']+s+w+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash