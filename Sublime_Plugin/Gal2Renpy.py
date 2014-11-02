import sublime, sublime_plugin
import json,os,pickle,codecs
import sys
game_path=json.load(open(os.path.split(__file__)[0]+'/'+'Gal2Renpy.sublime-settings'))['game_gal2renpy_path']
sys.path.append(game_path+'Gal2Renpy')
from Class import *
from Keyword import *
US=User(game_path)

def EditInit():
	tmp=None
	if os.path.exists(os.path.split(__file__)[0]+'/'+'EditLast'):
		tmp=pickle.load(codecs.open(game_path+'Gal2Renpy/EditLast','r','utf-8'))
	else:
		tmp={
				'sc':(
						0,(),
						(('cp','None'),('sc','None'))
					),
				'sw':(
						0,(),
						(('s','None'),)
					),
				'chlast':'',
				'ch':{},
				'bg':(
						0,(('l','None'),('t','None')),
						(('m','None'),('s','None'),('w','None'))
					),
				'cg':(
						0,(('l','None'),('t','None')),
						(('m','None'),('s','None'))
					),
				'bgm':(
						0,(),
						(('m','None'),)
					),
				'sound':(
						0,(),
						(('m','None'),)
					),
				'date':(
						0,(),
						(('m','None'),)
					),
				'vd':(
						0,(),
						(('m','None'),)
					),
				'ef':(
						1,(('e','None'),('args','None')),
						(('m','None'),)
					),
				'gf':(
						0,(('l','None'),),
						(('m','None'),)
					),
				'key':(
						0,(('k','None'),),
						(('m','None'),('n','None'))
					),
				'mode':(
						0,(),
						(('m','None'),)
					),
				'view':(
						0,(),
						(('m','None'),)
					),
				'chc':(
						0,(),
						(('a','None'),('b','None'))
					),
				'renpy':(
						0,(),
						(('m','None'),)
					),
				'test':(
						0,(),
						(('m','None'),)
					)
			}
		for ch in US.ChrName:
			tmp['ch'][ch]=(
					1,(('l','None'),('t','None')),
					(('n',ch),('p','None'),('c','None'),('f','None'),('d','None'))
					)
	return tmp

def RangeInit():
	return {
		'ch':US.ChrKeyword,
		'bg':US.BgKeyword,
		'cg':US.CgKeyword,
		'bgm':US.Bgm,
		'sound':US.SoundE,
		'ef':US.EffectSp,
		'gf':US.Graph,
		'key':US.KeyWord
	}

class Gal2RenpyCompletions(sublime_plugin.EventListener):
	def __init__(self):
		self.ArgsRange=RangeInit()

	def on_query_completions(self, view, prefix, locations):
		return ['1','2']

class Gal2RenpyCommand(sublime_plugin.TextCommand):
	EditLast=EditInit()

	def run(self, edit):
		#Functions
		def Insert(pt,s):
			self.view.insert(edit,pt,s)
		def Replace(reg,s):
			self.view.replace(edit,reg,s)
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
		def SetAllFront(s):
			#for line in self.view.sel():
			lines = self.view.lines(self.view.sel()[0])
			for line in lines:
				self.view.replace(edit, line, s+self.view.substr(line))
		def SetViewCursor(pt):
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(pt))
			self.view.show(pt)
		#Run
		pt = GetNowPoint()
		line = GetNowLine()
		lt = GetLineText(line)
		if lt not in Keywords:
			if re.match(r'\s*ch\.\S+',lt):
				ch=lt.split('.')[1]
				Replace(line,self.CreatInsertCh(ch))
			else:
				SetAllFront('\t')	
		elif lt=='hpc':
			pass
		elif lt=='ef':
			pass
		elif lt=='ch':
			Replace(line,self.CreatInsertCh(self.EditLast['chlast']))
		else:
			Replace(line,self.CreatInsertNormal(lt))

	def CreatInsertNormal(self,lt):
		def IsEmpty(tup):
			if len(tup)==0:
				return True
			return False

		so ='<' + lt+' '
		for t in self.EditLast[lt][1]:
			if not IsEmpty(t):
				so+=t[0]+':'+t[1]+' '
		so=so[:-1]+'>'
		if self.EditLast[lt][0]==1:
			so+='\n\t'
		for t in self.EditLast[lt][2]:
			if not IsEmpty(t):
				so+=t[0]+':'+t[1]+' '
		so=so[:-1]
		if self.EditLast[lt][0]==1:
			so+='\n'
		so+='</'+lt+'>'
		return so

	def CreatInsertCh(self,ch):
		def IsEmpty(tup):
			if len(tup)==0:
				return True
			return False
		if IsEmpty(ch):
			pass
		else:
			so ='<ch '
			for t in self.EditLast['ch'][ch][1]:
				if not IsEmpty(t):
					so+=t[0]+':'+t[1]+' '
			so=so[:-1]+'>'
			if self.EditLast['ch'][ch][0]==1:
				so+='\n\t'
			for t in self.EditLast['ch'][ch][2]:
				if not IsEmpty(t):
					so+=t[0]+':'+t[1]+' '
			so=so[:-1]
			if self.EditLast['ch'][ch][0]==1:
				so+='\n'
			so+='</ch>'
			return so
		return 'This ch does not exits or init !'