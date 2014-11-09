#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/ch.rpy'
		elepath=US.Args['pathmode']['ChPath']
		Args=US.Args[Flag]
		so=''
		for ele in Args:
			for e in ['Name','Face','Pose','Clothes','Distance']:
				if e in Args[ele]:
					continue
				G2R.SourceError("This ch '"+ele+"' must have child '"+e+"' !")
			so+='image '+Args[ele]['Name']+' '+Args[ele]['Pose']+Args[ele]['Clothes']+Args[ele]['Face']++Args[ele]['Distance']+' = '
			so+="'"+elepath+Args[ele]['Name']+Args[ele]['Pose']+Args[ele]['Clothes']+Args[ele]['Face']++Args[ele]['Distance']+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash