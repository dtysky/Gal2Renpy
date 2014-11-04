#coding utf-8
import sublime, sublime_plugin
import re

class Gal2RenpySelectCommand(sublime_plugin.TextCommand):

	def run(self, edit, action='left'):
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
		def NoSelected():
			return self.view.sel()[0].a==self.view.sel()[0].b
		def FindNextPair(pt):
			pair = self.view.find('[a-z]+:.*?(?=<|>|\n|\s+[a-z]+:)',pt)
			if not pair:
				return None
			pairt = self.view.substr(pair)
			return {'pair':pair,'pairt':pairt,'tag':pairt.split(':')[0],'attr':pairt.split(':')[1]}
		def InBlock():
			return re.match(r'.*[a-z]+:',GetLineText(GetNowLine()))
		def MoveOne(right):
			self.view.run_command('move',args={"by": "characters", "forward": right})
		def MoveWord(right):
			self.view.run_command('move',args={"by": "words", "forward": right})
		def ViewSelect():
			pair=FindNextPair(GetNowPoint())
			ptrc=GetPointRC(pair['pair'].a)
			pt1=SetPointRC(ptrc[0],ptrc[1]+len(pair['tag'])+1)
			pt2=SetPointRC(ptrc[0],ptrc[1]+len(pair['tag'])+1+len(pair['attr']))
			reg=CreatReg(pt1,pt2)
			SetViewSelect(reg)
		#Run
		if not InBlock():
			if action=='left':
				MoveOne(False)
			else:
				MoveOne(True)
			return
		if action=='left':
			if not FindNextPair(GetNowPoint()):
				if NoSelected():
					tagnow='None'
				else:
					MoveWord(False)
					MoveWord(False)
					tagnow=FindNextPair(GetNowPoint())['pairt']
			else:
				MoveWord(False)
				MoveWord(False)
				tagnow=FindNextPair(GetNowPoint())['pairt']
			while 1:
				MoveWord(False)
				tagnext=FindNextPair(GetNowPoint())
				if tagnext:
					if FindNextPair(GetNowPoint())['pairt']!=tagnow:
						break
					elif not InBlock():
						break
			ViewSelect()
			return
		MoveOne(True)
		MoveOne(True)
		if not InBlock():
			return
		MoveOne(False)
		ViewSelect()


