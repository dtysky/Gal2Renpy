#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ChNameDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS):
		DictHash=G2R.DefineSyntax.Creat(self,Flag,US,FS,DictHash)
		if DictHash[Flag]==G2R.DHash(US.Args[Flag]):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/chname.rpy'
		Args=US.Args['ch']
		so=''
		for ele in Args:
			for e in ['Name','N_Color','T_Color','N_OutLineColor','T_OutLineColor','N_Bold','T_Bold']:
				if e in Args[ele]:
				G2R.SourceError("This ch '"+ele+"' must have child '"+e+"' !")
			soa='define '+Args[ele]['Name']+'A = Character('+"'"+ele
			son='define '+Args[ele]['Name']+'V = Character('+"'"+ele
			sot="',who_color="+Args[ele]['N_Color']+"',what_color="+Args[ele]['T_Color']
			sot+="',who_bold="+Args[ele]['N_Bold']+"',what_bold="+Args[ele]['T_Bold']
			sot+="',who_outlines=[ (2, '"+Args[ele]['N_OutLineColor']+"') ],what_outlines=[ (1,'"+Args[ele]['T_OutLineColor']+"') ])"
			soa+=sot
			son+=sot
			if 'WindowADV' in Args[ele]:
				soa+=",show_bg="+Args[ele]['WindowADV']+"S)"
			if 'WindowNVL' in Args[ele]:
				son+=",show_bg="+Args[ele]['WindowNVL']+"S)"
			soa+='\n'
			son+='\n'
			so=+soa+son
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash