#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ChDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS,DictHash):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/ch.rpy'
		elepath=US.Args['pathmode']['ChPath']
		Args=US.Args[Flag]
		so=''
		for ele in Args:
			for e in ['Name','Face','Pose','Clothes','Distance']:
				if e not in Args[ele]:
					G2R.SourceError("This ch '"+ele+"' must have child '"+e+"' !")
			for p in Args[ele]['Pose']:
				p=Args[ele]['Pose'][p]
				for c in Args[ele]['Clothes']:
					c=Args[ele]['Clothes'][c]
					for f in Args[ele]['Face']:
						f=Args[ele]['Face'][f]
						for d in Args[ele]['Distance']:
							d=Args[ele]['Distance'][d]
							so+='image '+Args[ele]['Name']+' '+p+c+f+d+' = '
							so+="'"+elepath+Args[ele]['Name']+'/'+p+c+f+d+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash