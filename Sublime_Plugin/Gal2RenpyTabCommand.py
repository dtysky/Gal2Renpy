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

def EditInit():
	tmp=None
	if os.path.exists(os.path.split(__file__)[0]+'/'+'EditLast'):
		tmp=pickle.load(codecs.open(game_path+'Gal2Renpy/EditLast','r','utf-8'))
	else:
		tmp={
				'sc':[
						0,(),
						(('cp','None'),('sc','None'))
					],
				'sw':[
						0,(),
						(('s','None'),)
					],
				'chlast':'',
				'ch':{},
				'bg':[
						0,(('l','None'),('t','None')),
						(('m','None'),('s','None'),('w','None'))
					],
				'cg':[
						0,(('l','None'),('t','None')),
						(('m','None'),('s','None'))
					],
				'bgm':[
						0,(),
						(('m','None'),)
					],
				'sound':[
						0,(),
						(('m','None'),)
					],
				'date':[
						0,(),
						(('m','None'),)
					],
				'vd':[
						0,(),
						(('m','None'),)
					],
				'ef':[
						1,(('e','None'),('args','None')),
						(('m','None'),)
					],
				'gf':[
						0,(('l','None'),),
						(('m','None'),)
					],
				'key':[
						0,(('k','None'),),
						(('m','None'),('n','None'))
					],
				'mode':[
						0,(),
						(('m','None'),)
					],
				'view':[
						0,(),
						(('m','None'),)
					],
				'chc':[
						0,(),
						(('a','None'),('b','None'))
					],
				'renpy':[
						0,(),
						(('m','None'),)
					],
				'test':[
						0,(),
						(('m','None'),)
					]
			}
		for ch in US.ChrName:
			tmp['ch'][ch]=[
					1,(('l','None'),('t','None')),
					(('n',ch),('p','None'),('c','None'),('f','None'),('d','None'))
					]
	return tmp

class Gal2RenpyTabCommand(sublime_plugin.TextCommand):
	EditLast=EditInit()

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
			pair = self.view.find('[a-z]+:.*?(?=&lt;|\n|\s+[a-z]+:)',pt)
			pairt = self.view.substr(pair)
			return {'pair':pair,'tag':pairt.split(':')[0],'attr':pairt.split(':')[1]}
		#Run
		pt = GetNowPoint()
		line = GetNowLine()
		lt = GetLineText(line)
		if not self.Complete(edit,line,lt):
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


	def Complete(self,edit,reg,lt):
		def Replace(reg,s):
			self.view.replace(edit,reg,s)
		if lt not in Keywords:
			#ch.xx.0/ch.xx.1
			if re.match(r'\s*ch\.\S+\.\d',lt):
				ch=lt.split('.')[1]
				self.EditLast['ch'][ch][0]=int(lt.split('.')[2])
				Replace(reg,self.CreatInsertCh(ch))
			#ch.xx
			elif re.match(r'\s*ch\.\S+',lt):
				ch=lt.split('.')[1]
				Replace(reg,self.CreatInsertCh(ch))
			#xx.0/xx.1
			elif re.match(r'\s*\S+\.\d',lt):
				tag=lt.split('.')[0]
				self.EditLast[tag][0]=int(lt.split('.')[1])
				Replace(reg,self.CreatInsertNormal(tag))
			else:
				return False
		elif lt=='hpc':
			pass
		elif lt=='ef':
			pass
		elif lt=='ch':
			Replace(reg,self.CreatInsertCh(self.EditLast['chlast']))
		else:
			Replace(reg,self.CreatInsertNormal(lt))
		return True


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
