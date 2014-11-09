#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R
import os

class GfDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/gf.rpy'
		elepath=US.Args['pathmode']['BgPath']
		Args=US.Args[Flag]
		so=''
		for ele in Args:
			for e in ['Name','Source','Type']:
				if e in Args[ele]:
					continue
				G2R.SourceError("This Gf '"+ele+"' must have child '"+e+"' !")
			if Args[ele]['Source'] not in ['Dir','File']:
				G2R.SourceError("Gf has no source type named '"+Args[ele]['Source']+"' !")
			if Args[ele]['Type']=='Dir':
				so+='image '+Args[ele]['Name']+':\n'
				if 'Delay' not in Args[ele]:
					G2R.SourceError("Gf '"+Args[ele]+"'' which source type is 'Dir' must define 'Delay' !")
				so+='image '+Args[ele]['Name']+':\n'
				for root,dirs,files in os.walk(Args['pathmode']['GamePath']+elepath+Args[ele]['Name']):
					for f in files:
						if os.path.splitext(f)[1]=='.png':
							US.Graph[gr]['Pause']+=float(Args[ele]['Delay'])
							so+="    '"+elepath+Args['ele']['Name']+'/'+f+"'\n    pause "+delay+'\n'
			elif Args[ele]['Source']=='File':
				if Args[ele]['Type'] not in ['Image']:
					G2R.SourceError("Gf '"+ele+"' can not have 'Type' which named '"+Args[ele]['Type']+"' !")
				if Args[ele]['Type']=='Image':
					so+='image '+Args[ele]['Name']+"='"+elepath+Args[ele]['Name']+".png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash