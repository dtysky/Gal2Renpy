#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import G2R

class ViewSp(G2R.SpSyntax):
	def Show(self,Flag,Attrs,US,UT,Tmp):
		sw=''
		Tmp[Flag]=Attrs['m']
		orgname=Attrs['m']
		self.Check(Flag,Attrs,UT)
		soa='define '+US.Args['ch'][orgname]['Name']+'A = Character('
		son='define '+US.Args['ch'][orgname]['Name']+'V = Character('
		sot="who_color="+US.Args['ch'][orgname]['N_Color']+"',what_color="+US.Args['ch'][orgname]['T_Color']
		sot+="',who_bold="+US.Args['ch'][orgname]['N_Bold']+"',what_bold="+US.Args['ch'][orgname]['T_Bold']
		sot+="',who_outlines=[ (2, '"+US.Args['ch'][orgname]['N_OutLineColor']+"') ],what_outlines=[ (1,'"+US.Args['ch'][orgname]['T_OutLineColor']+"') ]"
		soa+=sot
		son+=sot
		if 'WindowADV' in US.Args['ch'][orgname]:
			soa+=",show_bg="+US.Args['ch'][orgname]['WindowADV']+"S)"
		else:
			soa+=')'
		if 'WindowNVL' in US.Args['ch'][orgname]:
			son+=",show_bg="+US.Args['ch'][orgname]['WindowNVL']+"S)"
		else:
			son+=')'
		soa+='\n'
		son+='\n'
		sw+=soa+son
		return sw