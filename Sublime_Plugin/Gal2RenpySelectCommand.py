#coding utf-8
import sublime, sublime_plugin

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
		def FindNextPair(pt):
			pair = self.view.find('[a-z]+:.*?(?=&lt;|\n|\s+[a-z]+:)',pt)
			if not pair:
				return None
			pairt = self.view.substr(pair)
			return {'pair':pair,'tag':pairt.split(':')[0],'attr':pairt.split(':')[1]}
		#Run
		if action=='left':
			for i in range(4):
				self.view.run_command('move',args={"by": "words", "forward": False})

		pt=GetNowPoint()
		pair=FindNextPair(pt)
		ptrc=GetPointRC(pair['pair'].a)
		pt1=SetPointRC(ptrc[0],ptrc[1]+len(pair['tag'])+1)
		pt2=SetPointRC(ptrc[0],ptrc[1]+len(pair['tag'])+1+len(pair['attr']))
		reg=CreatReg(pt1,pt2)
		SetViewSelect(reg)

