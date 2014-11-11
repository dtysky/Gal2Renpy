#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ChNameDefine(G2R.DefineSyntax):
	def Creat(self,Flag,US,FS,DictHash):
		DictHash=G2R.DefineSyntax.Creat(self,'ch',US,FS,DictHash)
		if DictHash['ch']==G2R.DHash(US.Args['ch']):
			return DictHash
		path=US.Args['pathmode']['ScriptPath']+'define/chname.rpy'
		Args=US.Args['ch']
		so=''
		win={'adv':[],'nvl':[]}
		for ele in Args:
			for e in ['Name','N_Color','T_Color','N_OutLineColor','T_OutLineColor','N_Bold','T_Bold']:
				if e not in Args[ele]:
					G2R.SourceError("This ch '"+ele+"' must have child '"+e+"' !")
			soa='define '+Args[ele]['Name']+'A = Character('+"'"+ele
			son='define '+Args[ele]['Name']+'V = Character('+"'"+ele
			sot="',who_color='"+Args[ele]['N_Color']+"',what_color='"+Args[ele]['T_Color']
			sot+="',who_bold="+Args[ele]['N_Bold']+",what_bold="+Args[ele]['T_Bold']
			sot+=",who_outlines=[ (2, '"+Args[ele]['N_OutLineColor']+"') ],what_outlines=[ (1,'"+Args[ele]['T_OutLineColor']+"') ]"
			soa+=sot
			son+=sot
			if 'WindowADV' in Args[ele]:
				soa+=",show_bg="+Args[ele]['WindowADV']+"S)"
				win['adv'].append(Args[ele]['WindowADV'])
			else:
				soa+=')'
			if 'WindowNVL' in Args[ele]:
				son+=",show_bg="+Args[ele]['WindowNVL']+"S)"
				win['nvl'].append(Args[ele]['WindowNVL'])
			else:
				son+=')'
			soa+='\n'
			son+='\n'
			so+=soa+son
		so+='define n=Character()'
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		so=''
		path=US.Args['pathmode']['ScriptPath']+'define/0chwin.rpy'
		for w in win['adv']:
			so+='define '+w+"S='"+US.Args['pathmode']['WinPath']+'adv/'+w+"S.png'\n"
			so+='define '+w+"N='"+US.Args['pathmode']['WinPath']+'adv/'+w+"N.png'\n"
		# for w in win['nvl']:
		# 	so+='define '+w+"S='"+US.Args['pathmode']['WinPath']+'nvl/'+w+"S.png'\n"
		# 	so+='define '+w+"N='"+US.Args['pathmode']['WinPath']+'nvl/'+w+"N.png'\n"
		FS.Open(path,'w')
		FS.Write(so)
		FS.Close()
		return DictHash