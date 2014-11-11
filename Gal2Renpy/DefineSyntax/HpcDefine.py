#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class BgDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS,DictHash):
		DictHash=G2R.DefineSyntax.Creat(self,'bg',US,FS,DictHash)
		if DictHash['bg']==G2R.DHash(US.Args['bg']):
			if DictHash['ch']==G2R.DHash(US.Args['ch']):
				return DictHash
		else:
			path=US.Args['pathmode']['ScriptPath']+'define/hpcbg.rpy'
			elepath=US.Args['pathmode']['BgPath']
			Args=US.Args['bg']
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
						so+='define '+Args[ele]['Name']+s+w+'HPC = '
						so+="'"+elepath+Args[ele]['Name']+s+w+".png'\n"
			FS.Open(path,'w')
			FS.Write(so)
			FS.Close()

		DictHash=G2R.DefineSyntax.Creat(self,'ch',US,FS,DictHash)
		if DictHash['ch']==G2R.DHash(US.Args['ch']):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/hpcch.rpy'
		elepath=US.Args['pathmode']['ChPath']
		Args=US.Args['ch']
		so=''
		for ele in Args:
			for e in ['Name','Face','Pose','Clothes','Distance']:
				if e in Args[ele]:
					continue
				G2R.SourceError("This ch '"+ele+"' must have child '"+e+"' !")
			for p in Args[ele]['Pose']:
				p=Args[ele]['Pose'][p]
				for c in Args[ele]['Clothes']:
					c=Args[ele]['Clothes'][c]
					for f in Args[ele]['Face']:
						f=Args[ele]['Face'][f]
						for d in Args[ele]['Distance']:
							d=Args[ele]['Distance'][d]
							so+='image '+Args[ele]['Name']+' '+p+c+f+d+'HPC = '
							so+="'"+elepath+Args[ele]['Name']+p+c+f+d+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash