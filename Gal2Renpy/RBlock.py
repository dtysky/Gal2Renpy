#-*-coding:utf-8-*- 

#Copyright(c) 2014 dtysky

import re
import codecs
import sys   
reload(sys)
sys.setdefaultencoding('utf-8')

#Return hash for a dict which may contain a dict as its value or others
	
#Return next block
def RBlock(Fs,US):
	def PairJudge(f1,f2,Fs):
		if f1!=f2:
			Fs.Error('Error flag pair '+f1+'and '+f2+' !')
	def RefBlock(Block,sr):
		for s in sr:
			if s in Block:
				Block[s]=sr[s]
	Block={'head':None,'flag':None,'attrs1':None,'attrs2':None}
	sr=None
	s=Fs.readline()
	#comment
	comment=re.search(r'.*\\#.*',s)
	if comment:
		s=s[comment.start():]
	#End of this file
	elif Fs.End():
		Block['head']='end'
	#Null or comment
	elif s=='' or s[0]=='#':
		Block['head']='skip'
	#<*>*
	elif re.match(r'\s*<.*>',s):
		#<x y>z</x>
		if re.match(r'\s*<\S+\s+\S+>.*</\S+>',s):
			sr=re.match(r'<(?P<flag>\S+?)\s+(?P<attrs1>.+)>(?P<attrs2>.*)</(?P<flag2>\S+)>',s).groupdict()
			ErrorPair(sr['flag'],sr['flag2'],Fs)
		#<x>z</x>
		elif re.match(r'\s*<\S+>.*</\S+>',s):
			sr=re.match(r'\s*<(?P<flag>\S+?)>(?P<attrs2>.*)</(?P<flag2>\S+)>',s)
			ErrorPair(sr['flag'],sr['flag2'],Fs)
		#<x y>
		#z
		#</x>
		elif re.match(r'\s*<\S+\s+\S+>',s):
			sr=re.match(r'\s*<(?P<flag>\S+?)\s+(?P<attrs1>.+)>',s)
			sr['attrs2']=''
			while 1:
				sl=Fs.readline()
				slr=re.match(r'\s*</(?P<flag2>\S+)>',s)
				if slr:
					ErrorPair(sr['flag'],slr['flag2'],Fs)
					break
				elif s[0]=='<':
					Fs.error("Error! Please check the '</' tag !")
				else:
					sr['attrs2']+=re.match(r'\s*(\S[.*]+)',s).group(1)+'\r\n'
		#<x>
		#z
		#</x>
		elif re.match(r'\s*<\S+>',s):
			sr=re.match(r'<(?P<flag>\S+?)>',s)
			sr['attrs2']=''
			while 1:
				sl=Fs.readline()
				slr=re.match(r'\s*</(?P<flag2>\S+)>',s)
				if slr:
					ErrorPair(sr['flag'],slr['flag2'],Fs)
					break
				elif s[0]=='<':
					Fs.error("Error! Please check the '</' tag !")
				else:
					sr['attrs2']+=re.match(r'\s*(\S[.*]+)',s).group(1)+'\n'
		else:
			Fs.error("Error! Please check the '<>' tag !")
		sr['head']='sp'
	else:
		if re.match(ur'\S+\s+【.*】',s):
			sr=re.match(ur'(?P<flag>\S+)\s+?P<attrs2>【(.*)】',s)
			if sr['flag'] not in US.args['ch']:
				Fs.error('This charecter '+sr['flag']+' doen not exist !')
			sr['head']='words'
			sr['attrs1']='say'
		elif re.match(ur'【.*】',s):
			sr=re.match(ur'【?P<attrs2>(.*)】',s)
			if sr:
				sr['head']='words'
				sr['attrs1']='think'
				if not US.ChrName['Saying']:
					Fs.error('No speaker !')
				sr['flag']=US.args['Saying']
			else:
				sr['head']='text'
				sr['attrs2']="n '"+s.strip()+"'\n"
	RefBlock(Block,sr)
	return Block