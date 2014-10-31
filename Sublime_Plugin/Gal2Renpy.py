import sublime, sublime_plugin
import json,os,pickle,codecs
import sys
game_path=json.load(open(__file_path__+'/'+'Gal2Renpy.sublime-settings'))['game_gal2renpy_path']
sys.path.append(game_path+'Gal2Renpy')
from Class import *
from Keyword import *

US=User(game_path)

class Gal2RenpyCommand(sublime_plugin.TextCommand):
	if os.path.exists(os.path.split(__file__)[0]+'/'+'EditLast'):
		EditLast=pickle.load(codecs.open(game_path+'Gal2Renpy/EditLast','r','utf-8'))
	else:
		EditLast={
			'sc':('None','None'),
			'sw':'None',
			'ch':{},
			'bg':{},
			'cg':{},
			'bgm':'None',
			'sound':'None',
			'date':'None',
			'vd':'None',
			'ef':'None',
			'gf':{'m':'None','l':'None'},
			'key':{},
			'mode':'',
			'view':'',
			'chc':('None','None'),
			'renpy':''
		}
		for key in US.BgKeyword:
			EditLast['bg'][key]='None'
		for key in US.CgKeyword:
			EditLast['cg'][key]='None'
		for ch in US.ChrName:
			EditLast['ch'][ch]={}
			for key in US.ChrKeyword:
				EditLast['ch'][ch][key]='None'
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