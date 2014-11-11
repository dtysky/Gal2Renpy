#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import re
import codecs
import sys   
reload(sys)
sys.setdefaultencoding('utf-8')

#A stack class
class Stack():
	def __init__(self):
		self.list=[]
	def Push(self,s):
		self.list.append(s)
	def Pop(self):
		return self.list.pop()
	def Check(self,s):
		return self.list[len(self.list)-1]==s
	def IsEmpty(self):
		return len(self.list)==0
	#A speical function!
	def AddLast(self,s):
		if isinstance(self.list[len(self.list)-1],Stack):
			self.list[len(self.list)-1].Push(s)
	def GetAll(self):
		return list(self.list)
	def Clear(self):
		self.list=[]

#Return a dict from one line depend on its syntax
def SpLineSyntax(Line):
	sr=None
	#</x>
	if re.match(r'\s*</\S+>',Line):
		sr=re.match(r'\s*</(?P<flag2>\S+?)>',Line).groupdict()
	#<x y>z</x>
	elif re.match(r'\s*<\S+\s+.+>.*</.+>',Line):
		sr=re.match(r'<(?P<flag>\S+?)\s+(?P<attrs1>.+)>(?P<attrs2>.*)</(?P<flag2>\S+)>',Line).groupdict()
	#<x>z</x>
	elif re.match(r'\s*<\S+>.*</\S+>',Line):
		sr=re.match(r'\s*<(?P<flag>\S+?)>(?P<attrs2>.*)</(?P<flag2>\S+)>',Line).groupdict()
	#<x y>
	elif re.match(r'\s*<\S+\s+.+>',Line):
		sr=re.match(r'\s*<(?P<flag>\S+?)\s+(?P<attrs1>.+)>',Line).groupdict()
	#<x>
	elif re.match(r'\s*<\S+>',Line):
		sr=re.match(r'\s*<(?P<flag>\S+?)>',Line).groupdict()
	#z
	else:
		sr={'attrs2':Line}
	return sr

#Return next block
def ReadBlock(FS):
	Block=[]
	def RefBlock(sr):
		B={'head':None,'flag':[],'attrs1':[],'attrs2':[]}
		if not sr:
			return
		for s in sr:
			if s in B:
				B[s]=sr[s]
		Block.append(B)

	s=FS.ReadLine()
	#Comment
	comment=re.search(r'.*\\#.*',s)
	if comment:
		s=s[comment.start():]
	#End of this file
	if FS.IsEnd():
		sr={'head':'end'}
		RefBlock(sr)
	#Null or comment
	elif s=='':
		sr={'head':'skip'}
		RefBlock(sr)
	#<*>*
	elif re.match(r'\s*<.*>',s):
		stack={'flag':Stack(),'attrs1':Stack(),'attrs2':Stack()}
		while  1:
			sr=SpLineSyntax(s)
			#'flag' stack and 'attrs1' stack must be sync
			if 'flag' in sr:
				stack['flag'].Push(sr['flag'])
				if 'attrs1' in sr:
					stack['attrs1'].Push(sr['attrs1'])
				else:
					stack['attrs1'].Push(None)
			if 'flag' in sr:
				stack['attrs2'].Push(Stack())
			if 'attrs2' in sr:
				stack['attrs2'].AddLast(sr['attrs2'])
			if 'flag2' in sr:
				if stack['flag'].Check(sr['flag2']):
					for attr in ['flag','attrs1']:
						if not stack[attr].IsEmpty():
							sr[attr]=stack[attr].GetAll()
							stack[attr].Pop()
					sr['attrs2']=stack['attrs2'].Pop().GetAll()
					sr['head']='sp'
					RefBlock(sr)
				else:
					FS.Error("This pair '"+stack['flag'].Pop()+"' and '"+sr['flag2']+"' are error !")
				if stack['flag'].IsEmpty():
					break
			s=FS.ReadLine()
			if FS.IsEnd():
				FS.Error("This flag '"+stack['flag'].Pop()+"' is not complete!")
	else:
		sr=None
		if re.match(ur'\S+\s+【.*】',s):
			sr=re.match(ur'(?P<attrs1>\S+)\s+【(?P<attrs2>.*)',s).groupdict()
			sr['head']='words'
			sr['flag']='say'
		elif re.match(ur'【.*】',s):
			sr=re.match(ur'【(?P<attrs2>.*)】',s).groupdict()
			sr['head']='words'
			sr['flag']='think'
		else:
			sr={'head':'words'}
			sr['flag']='text'
			sr['attrs2']=s.strip()}
		RefBlock(sr)
	return Block