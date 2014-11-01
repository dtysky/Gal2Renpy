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
						(),
						(('cp','None'),('sc','None'))
					),
				'sw':(
						(),
						(('s','None'))
					),
				'chlast':'',
				'ch':{},
				'bg':(
						(('l','None'),('t','None')),
						(('m','None'),('s','None'),('w','None'))
					),
				'cg':(
						(('l','None'),('t','None')),
						(('m','None'),('s','None'))
					),
				'bgm':(
						(),
						(('m','None'))
					),
				'sound':(
						(),
						(('m','None'))
					),
				'date':(
						(),
						(('m','None'))
					),
				'vd':(
						(),
						(('m','None'))
					),
				'ef':(
						(('e','None'),('args','None')),
						(('m','None'))
					),
				'gf':(
						(('l','None')),
						(('m','None'))
					),
				'key':(
						(('k','None')),
						(('m','None'),('n','None'))
					),
				'mode':(
						(),
						(('m','None'))
					),
				'view':(
						(),
						(('m','None'))
					),
				'chc':(
						(),
						(('a','None'),('b','None'))
					),
				'renpy':(
						(),
						(('m','None'))
					),
				'test':(
						(),
						(('m','None'))
					)
			}
		for ch in US.ChrName:
			tmp['ch'][ch]=(
					(('l','None'),('t','None')),
					(('n','None'),('p','None'),('c','None'),('f','None'),('d','None'))
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

class Gal2RenpyTagCompletions(sublime_plugin.EventListener):
	def __init__(self):
		self.ArgsRange=RangeInit()

	def on_query_completions(self, view, prefix, locations):
		pass

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
		def SetViewCursor(pt):
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(pt))
			self.view.show(pt)
		#Run
		pt = GetNowPoint()
		line = GetNowLine()
		if GetLineText(line)=='bg':
			so='<bg'
			for t in self.EditLast['bg'][0]:
				so+=' '+t[0]+':'+t[1]
			so+='>'
			for t in self.EditLast['bg'][1]:
				so+=' '+t[0]+':'+t[1]
			so+='</bg>'
			Replace(line,so)
		SetViewCursor(pt)