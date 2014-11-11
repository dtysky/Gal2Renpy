#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class CgDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS,DictHash):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/cg.rpy'
		elepath=US.Args['pathmode']['CgPath']
		Args=US.Args[Flag]
		so=''
		for ele in Args:
			for e in ['Name','Background','Scene']:
				if e not in Args[ele]:
					G2R.SourceError("This cg '"+ele+"' must have child '"+e+"' !")
			for s in Args[ele]['Scene']:
				for knum in range(s[1]):
					for bg in Args[ele]['Background']:
						n=s[0]+str(knum)+bg
						so+='image cg '+Args[ele]['Name']+n+' = '
						so+="'"+elepath+Args[ele]['Name']+n+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash