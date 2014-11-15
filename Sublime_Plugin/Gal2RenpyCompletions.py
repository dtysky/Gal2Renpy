#coding:utf-8
#########################
#Copyright(c) 2014 dtysky
#########################

import sublime, sublime_plugin
import json,os,pickle,codecs,locale,re
import sys
sys.path.append(os.path.split(__file__)[0])
path=os.path.split(__file__)[0]+'/'+'User.json'
game_path=json.load(open(path,'r'))['game_gal2renpy_path']
sys.path.append(game_path+'Gal2Renpy/G2R')
sys.path.append(game_path+'Gal2Renpy')
from UserSource import UserSource
from UserTag import UserTag

from xpinyin import Pinyin
Py=Pinyin()
US=UserSource(game_path)
UT=UserTag(US,game_path+'Gal2Renpy/TagSource')

class Gal2RenpyCompletions(sublime_plugin.EventListener):
	def __init__(self):
		pass

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
			tmp=re.match(r'.*([a-z]+):[\.。]',GetLineText(GetNowLine()))
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
		def GetSpecial(flag,d):
			def GetFlag(ptrc):
				i=0
				while(i<10):
					line=GetLineText(GetPointLine(SetPointRC(ptrc[0]-i,0)))
					tmp=re.match(r'<(\S+?)[\s+>]',line)
					if tmp:
						return(tmp.group(1))
						break
					elif re.match(r'\s*[a-z]+:',line):
						i+=1
					else:
						return None
			i=0
			ptrc=GetPointRC(GetNowPoint())
			while(i<10):
				ptrc=GetPointRC(SetPointRC(ptrc[0]-i,0))
				nowflag=GetFlag(ptrc)
				if nowflag!=flag:
					break
				line=GetLineText(GetPointLine(SetPointRC(ptrc[0],0)))
				tmp=re.search(r'm:(.*?)(?=<|\n|\s+[a-z]+:)',line)
				if tmp:
					return d.get(tmp.group(1))
				elif re.search(r'[a-z]+:',line):
					i+=1
				else:
					break
			ptrc=GetPointRC(GetNowPoint())
			i=0
			while(i<10):
				ptrc=GetPointRC(SetPointRC(ptrc[0]+i,0))
				nowflag=GetFlag(ptrc)
				if nowflag!=flag:
					break
				line=GetLineText(GetPointLine(SetPointRC(ptrc[0],0)))
				tmp=re.search(r'm:(.*?)(?=<|\n|\s+[a-z]+:)',line)
				if tmp:
					return d.get(tmp.group(1))
				elif re.search(r'[a-z]+:',line):
					i+=1
				else:
					break
			return None
		def CreatList(FlagTag):
			flag,tag=FlagTag
			ds=None
			if flag not in UT.Args:
				return []
			ds=UT.Args[flag]
			if not ds:
				return []
			if tag not in ds:
				return []
			if flag=='m':
				return ToShow(ds['m'])
			if flag not in ['ch','bg','cg','key']:
				ds=ds[tag]
			else:
				ds=GetSpecial(flag,ds[tag])
				if not ds:
					return []
			return ToShow(ds)

		# Only trigger within Gal2Renpy
		if not view.match_selector(locations[0],"source.Gal2Renpy"):
			return []
		if re.match(r'\s*ch[\.。]',GetLineText(GetNowLine())):
			return (ToShow(UT.Args['ch']['m']),sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)
		else:
			FlagTag=GetFlagTag()
			if FlagTag:
				view.run_command('left_delete')
				return (CreatList(FlagTag),sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)
		
		return ([],sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)