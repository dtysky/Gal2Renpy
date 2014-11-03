#coding utf-8
import sublime, sublime_plugin
import json,os,pickle,codecs,locale
import sys
sys.path.append(os.path.split(__file__)[0])
game_path=json.load(open(os.path.split(__file__)[0]+'/'+'Path.json'))['game_gal2renpy_path']
sys.path.append(game_path+'Gal2Renpy')
from Class import *
from Keyword import *
from xpinyin import Pinyin
Py=Pinyin()
US=User(game_path)


def RangeInit():
	return {
		'ch':US.ChrKeyword,
		'bg':US.BgKeyword,
		'cg':US.CgKeyword,
		'bgm':US.Bgm,
		'sound':US.SoundE,
		'ef':US.EffectSp,
		'gf':US.Graph,
		'key':US.KeyWord,
		'chrname':US.ChrName
	}

class Gal2RenpyCompletions(sublime_plugin.EventListener):
	def __init__(self):
		self.ArgsRange=RangeInit()
		if 'Saying' in self.ArgsRange['chrname']:
			del  self.ArgsRange['chrname']['Saying']

	def on_query_completions(self, view, prefix, locations):
		def GetNowLine():
			return view.line(view.sel()[0])
		def GetLineText(line):
			return view.substr(line)
		def ToList(ds):
			tmp=[]
			for d in sorted(ds):
				tmp.append((Py.get_pinyin(d, '')+'\t'+d,d))
			return tmp
		# Only trigger within Gal2Renpy
		if not view.match_selector(locations[0],"source.Gal2Renpy"):
			return []
		if re.match(r'\s*ch\.',GetLineText(GetNowLine())):
			return (ToList(self.ArgsRange['chrname']),sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)
		
		return ([],sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)