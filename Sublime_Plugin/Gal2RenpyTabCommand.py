#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

import sublime, sublime_plugin
import json,os,codecs,locale,re
import sys
sys.path.append(os.path.split(__file__)[0])
path=os.path.split(__file__)[0]+'/'+'User.json'
game_path=json.load(open(path,'r'))['game_gal2renpy_path']
sys.path.append(game_path+'Gal2Renpy/G2R')
sys.path.append(game_path+'Gal2Renpy')
from UserSource import UserSource
from UserTag import UserTag
from EditFormat import *

US=UserSource(game_path)
UT=UserTag(US,game_path+'Gal2Renpy/TagSource')


class Gal2RenpyTabCommand(sublime_plugin.TextCommand):
	EditLast=EditFormat(US,UT)

	def run(self, edit):
		#Functions
		def Insert(pt,s):
			self.view.insert(edit,pt,s)
		def GetNowLine():
			return self.view.line(self.view.sel()[0])
		def GetLineText(line):
			return self.view.substr(line)	
		def GetNowPoint():
			return self.view.sel()[0].b
		def GetPointRC(pt):
			return self.view.rowcol(pt)
		def SetPointRC(r,c):
			return self.view.text_point(r,c)
		def CreatReg(pt1,pt2):
			return sublime.Region(pt1,pt2)
		def SetViewSelect(reg):
			self.view.sel().clear()
			self.view.sel().add(reg)
			self.view.show(reg)
		def FindNextPair(pt):
			pair = self.view.find('[a-z]+:.*?(?=<|>|\n|\s+[a-z]+:)',pt)
			pairt = self.view.substr(pair)
			return {'pair':pair,'tag':pairt.split(':')[0],'attr':pairt.split(':')[1]}
		#Run
		pt = GetNowPoint()
		ptrc=GetPointRC(pt)
		if ptrc[0]<200:
			buf=GetLineText(CreatReg(SetPointRC(0,0),pt))
		else:
			buf=GetLineText(CreatReg(SetPointRC(ptrc[0]-200,0),pt))
		line = GetNowLine()
		lt = GetLineText(line)
		if not self.Complete(edit,line,lt,buf):
			Insert(pt,'\t')
			return
		ptrc=GetPointRC(pt)
		pt=SetPointRC(ptrc[0],0)
		pair=FindNextPair(pt)
		ptrc=GetPointRC(pair['pair'].a)
		pt1=SetPointRC(ptrc[0],ptrc[1]+len(pair['tag'])+1)
		pt2=SetPointRC(ptrc[0],ptrc[1]+len(pair['tag'])+1+len(pair['attr']))
		reg=CreatReg(pt1,pt2)
		SetViewSelect(reg)


	def Complete(self,edit,reg,lt,buf):
		def Replace(reg,s):
			self.view.replace(edit,reg,s)
		def SetEditLast(flag,buf,ch=None):
			flag_tmp=flag
			if flag=='chrlast':
				buf=re.findall(r'<'+'ch'+r'[\S\s]*?>[\S\s]*?</'+'ch'+'>',buf)
			elif flag=='ch':
				buf=re.findall(r'<ch[\S\s]*?>\s*'+'m:'+ch+r'[\S\s]*?</ch>',buf)
				flag_tmp='ch-'+ch
			else:
				buf=re.findall(r'<'+flag+r'[\S\s]*?>[\S\s]*?</'+flag+'>',buf)
			if not buf:
				return
			tmp={}
			for b in re.findall(r'[a-z]+:.*?(?=<|>|\n|\s+[a-z]+:)',buf[len(buf)-1]):
				[tag,attr]=b.split(':')
				if tag in self.EditLast[flag_tmp][2]:
					self.EditLast[flag_tmp][2][tag]=attr
				elif tag in self.EditLast[flag_tmp][4]:
					self.EditLast[flag_tmp][4][tag]=attr
			#sublime.message_dialog(str(buf))
		if lt not in self.EditLast:
			#ch.xx.0/ch.xx.1
			if re.match(r'\s*ch\.\S+\.\d',lt):
				ch=lt.split('.')[1]
				self.EditLast['ch-'+ch][0]=int(lt.split('.')[2])
				SetEditLast('ch',buf,ch)
				Replace(reg,self.CreatInsertCh(ch))
			#ch.xx
			elif re.match(r'\s*ch\.\S+',lt):
				ch=lt.split('.')[1]
				SetEditLast('ch',buf,ch)
				Replace(reg,self.CreatInsertCh(ch))
			#xx.0/xx.1
			elif re.match(r'\s*\S+\.\d',lt):
				flag=lt.split('.')[0]
				self.EditLast[flag][0]=int(lt.split('.')[1])
				SetEditLast(lt,buf)
				Replace(reg,self.CreatInsertNormal(flag))
			else:
				return False
		elif lt=='hpc':
			pass
		elif lt=='ch':
			SetEditLast('chrlast',buf)
			Replace(reg,self.CreatInsertNormal('chrlast'))
		else:
			SetEditLast(lt,buf)
			Replace(reg,self.CreatInsertNormal(lt))
		return True

	def CreatInsert(self,flag,buf):
		so ='<' + flag+' '
		for t in buf[1]:
			so+=t+':'+buf[2][t]+' '
		so=so[:-1]+'>'
		if buf[0]==1:
			so+='\n\t'
		for t in buf[3]:
			so+=t+':'+buf[4][t]+' '
		so=so[:-1]
		if buf[0]==1:
			so+='\n'
		so+='</'+flag+'>'
		return so

	def CreatInsertNormal(self,lt):
		buf=self.EditLast[lt]
		if lt=='chrlast':
			return self.CreatInsert('ch',buf)
		return self.CreatInsert(lt,buf)

	def CreatInsertCh(self,ch):
		buf=self.EditLast['ch-'+ch]
		return self.CreatInsert('ch',buf)
