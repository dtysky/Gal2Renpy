import sublime, sublime_plugin
import json,os,pickle,codecs,locale
import sys
sys.path.append(os.path.split(__file__)[0])
path=os.path.split(__file__)[0]+'/'+'User.json'
game_path=json.load(open(path))['game_gal2renpy_path']
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
		'bgm':{'m':US.Bgm},
		'sound':US.SoundE,
		'ef':US.EffectSp,
		'gf':US.Graph,
		'key':US.KeyWord,
		'chc':{'m':US.ChrName,'s':US.ChrName},
		'view':{'m':US.ChrName},
		'chrname':US.ChrName
	}

class Gal2RenpyCompletions(sublime_plugin.EventListener):
	def __init__(self):
		self.ArgsRange=RangeInit()
		if 'Saying' in self.ArgsRange['chrname']:
			del  self.ArgsRange['chrname']['Saying']

	def on_query_completions(self, view, prefix, locations):
		def GetNowPoint():
			return view.sel()[0].b
		def GetPointRC(pt):
			return view.rowcol(pt)
		def SetPointRC(r,c):
			return view.text_point(r,c)
		def GetPointLine(pt):
			return view.line(pt)
		def GetNowLine():
			return view.line(view.sel()[0])
		def GetLineText(line):
			return view.substr(line)
		def ToShow(ds):
			tmp=[]
			for d in sorted(ds):
				tmp.append((Py.get_pinyin(d, '')+'\t'+d,d))
			return tmp
		def GetFlagTag():
			tmp=re.match(r'.*([a-z]+):\.',GetLineText(GetNowLine()))
			if not tmp:
				return None
			tag=tmp.group(1)
			i=0
			ptrc=GetPointRC(GetNowPoint())
			while(i<10):
				line=GetLineText(GetPointLine(SetPointRC(ptrc[0]-i,0)))
				tmp=re.match(r'<(\S+?)[\s+>]',line)
				if tmp:
					return (tmp.group(1),tag)
				elif re.match(r'\s*[a-z]+:',line):
					i+=1
				else:
					break
			return None
		def GetSpecial(d):
			i=0
			ptrc=GetPointRC(GetNowPoint())
			while(i<10):
				line=GetLineText(GetPointLine(SetPointRC(ptrc[0]-i,0)))
				tmp=re.match(r'.*m:(.*?)(?=<|\n|\s+[a-z]+:)',line)
				if tmp:
					return d.get(tmp.group(1))
				elif re.match(r'\s*[a-z]+:',line):
					i+=1
				else:
					break
			while(i>0):
				line=GetLineText(GetPointLine(SetPointRC(ptrc[0]+i,0)))
				tmp=re.match(r'.*m:(.*?)(?=<|\n|\s+[a-z]+:)',line)
				if tmp:
					return d.get(tmp.group(1))
				elif re.match(r'\s*[a-z]+:',line):
					i-=1
				else:
					break
			return None
		def CreatList(FlagTag):
			flag,tag=FlagTag
			ds=None
			if not self.ArgsRange.get(flag):
				return []
			ds=self.ArgsRange[flag]
			if not ds:
				return []
			if not ds.get(tag):
				return []
			if flag not in ['ch','bg','cg']:
				ds=ds[tag]
			else:
				if tag in ['m','l','t','d']:
					ds=ds[tag]
				else:
					ds=GetSpecial(ds[tag])
			return ToShow(ds)

		# Only trigger within Gal2Renpy
		if not view.match_selector(locations[0],"source.Gal2Renpy"):
			return []
		if re.match(r'\s*ch\.',GetLineText(GetNowLine())):
			return (ToShow(self.ArgsRange['chrname']),sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)
		else:
			FlagTag=GetFlagTag()
			if FlagTag:
				view.run_command('left_delete')
				return (CreatList(FlagTag),sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)
		
		return ([],sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)