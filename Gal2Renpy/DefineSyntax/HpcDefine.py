#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS,DictHash):
		DictHash=G2R.DefineSyntax.Creat(self,'bg',US,FS,DictHash)
		if DictHash['bg']==G2R.DHash(US.Args['bg']):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/hpcbg.rpy'
		elepath=US.Args['pathmode']['BgPath']
		Args=US.Args['bg']
		so=''
		for ele in Args:
			for e in ['Name','Sub','Weather']:
				if e in Args[ele]:
					continue
				G2R.SourceError("This bg '"+ele+"' must have child '"+e+"' !")
			so+='define '+Args[ele]['Name']+Args[ele]['Sub']+Args[ele]['Weather']+'HPC = '
			so+="'"+elepath+Args[ele]['Name']+Args[ele]['Sub']+Args[ele]['Weather']+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()

		DictHash=G2R.DefineSyntax.Creat(self,'ch',US,FS,DictHash)
		if DictHash['ch']==G2R.DHash(US.Args['ch']):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/ch.rpy'
		elepath=US.Args['pathmode']['ChPath']
		Args=US.Args['ch']
		so=''
		for ele in Args:
			for e in ['Name','Face','Pose','Clothes','Distance']:
				if e in Args[ele]:
					continue
				G2R.SourceError("This ch '"+ele+"' must have child '"+e+"' !")
			so+='define '+Args[ele]['Name']+Args[ele]['Pose']+Args[ele]['Clothes']+Args[ele]['Face']++Args[ele]['Distance']+'HPC = '
			so+="'"+elepath+Args[ele]['Name']+Args[ele]['Pose']+Args[ele]['Clothes']+Args[ele]['Face']++Args[ele]['Distance']+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash