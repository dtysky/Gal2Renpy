import sublime, sublime_plugin
import json,os,pickle,codecs
import sys
game_path=json.load(open(os.path.split(__file__)[0]+'/'+'Gal2Renpy.sublime-settings'))['game_gal2renpy_path']
sys.path.append(game_path+'Gal2Renpy')
from Class import *
from Keyword import *

US=User(game_path)

class Gal2RenpyCommand(sublime_plugin.TextCommand):
	if os.path.exists(os.path.split(__file__)[0]+'/'+'EditLast'):
		EditLast=pickle.load(codecs.open(game_path+'Gal2Renpy/EditLast','r','utf-8'))
	else:
		EditLast={
			'sc':(
					(),
					(('cp','None'),('sc':'None'))
				),
			'sw':(
					(),
					(('s','None'))
				),
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
			'date'::(
					(),
					(('m','None'))
				),
			'vd'::(
					(),
					(('m','None'))
				),
			'ef':(
					(('e':'None'),('args':'None')),
					(('m':'None'))
				),
			'gf':(
					(('l':'None')),
					(('m':'None'))
				),
			'key':(
					(('k':'None')),
					(('m':'None'),('n':'None'))
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
					(('a','None'),('b':'None'))
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
			EditLast['ch'][ch]=(
					(('l','None'),('t','None')),
					(('n','None'),('p','None'),('c','None'),('f','None'),('d':'None'))
					)
	ArgRange={
		'ch':US.ChrKeyword,
		'bg':US.BgKeyword,
		'cg':US.CgKeyword,
		'bgm':US.Bgm,
		'sound':US.SoundE,
		'ef':US.EffectSp,
		'gf':US.Graph,
		'key':US.KeyWord
	}

	def run(self, edit):
		#Functions
		def Insert(pt,s):
			self.view.insert(edit,pt,s)
		def GetNowLine():
			return self.view.line(self.view.sel()[0])
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
		Insert(pt,"<chr>\n\n</chr>")
		row,col = GetPointRC(pt)
		pt = SetPointRC(row+1,col)
		SetViewCursor(pt)
		Insert(GetNowPoint(),"\t")
		Insert(GetNowPoint(),game_path)