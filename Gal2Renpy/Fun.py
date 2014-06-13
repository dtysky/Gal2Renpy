import Gal2Renpy.imilb


#Return next block
def RBlock(Fs):
	[head,flag,transition,content]=['','','','']
	s=Fs.readline()
	if re.match(r'<.*>',s)!=None:

		if re.match(r'<\S+\s+\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)\s*(\S+)>\s*(.*)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition=sr.group(2)
			content=sr.group(3)
		elif re.match(r'<\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)>\s*(\S+)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition='None'
			content=sr.group(2)
		elif re.match(r'<\S+\s+\S+>',s):
			sr=re.match(r'<(\S+)\s+(\S+)>',s)
			head='sp'
			flag=sr.group(1)
			transition=sr.group(2)
			while 1:
				s=Fs.readline()
				if (s[0]=='<') & (s[1]=='/'):
					break
				elif s[0]=='<':
					Fs.error('''Error! Please check the "</"" !''')
				else:
					content+=re.match('\s*(.+)',s).group(1)+'\n'
		elif re.match(r'<\S+>',s):
			sr=re.match(r'<(\S+)>',s)
			head='sp'
			flag=sr.group(1)
			transition='None'
			while 1:
				s=Fs.readline()
				if (s[0]=='<') & (s[1]=='/'):
					break
				elif s[0]=='<':
					Fs.error('''Error! Please check the "</"" !''')
				else:
					content+=re.match('\s*(.+)',s).group(1)+'\n'
		else:
			Fs.error('''Error! Please check the "<>"" !''')

	else:
		tmp=re.match(r'(\S+)\s+(\S+)')
		if tmp==None:
			flag='None'
			content=s
			if ('【' in s) & ('】' in s):
				head='say'
			else:
				head='text'
		else:
			if ChrName.get(tmp.group(1))==None:
				Fs.error('This charecter doen not exist !')
			else:
				head='say'
				flag=ChrName[tmp.group(1)]
				content=tmp.group(2)
		transition='None'

	return [head,flag,transition,content]



#Return a string which changing special texts to Script
def Sp2Script(Flag,Transition,Content,Fs):

	if Flag=='sc':
		return 'label '+Content.replace('，','')+' :\n'

	elif Flag=='bg':
		s=''
		for tmp in Content..replace('：',':').split(':'):
			s+=tmp
		sr=s.replace('，',',').split(',')
		rn=''
		if BgMain.get(sr[0])==None:
			Fs.error('This Bg does not exist ！')
		else:
			if len(sr)==2:
				if eval('Bg'+BgMain[sr[0]]).get(sr[1])==None:
					Fs.error('This Bg does not exist ！')
				else:
					rn='show bg '+BgMain[sr[0]]+eval('Bg'+BgMain[sr[0]])[sr[1]]+'\n'
			elif len(sr)==1:
				rn='show bg '+BgMain[sr[0]]+'\n'
			else:
				Fs.error('Unsupport two and more subscenes ！')
		if Transition!='None':
			if TransImage.get(Transition)==None:
				Fs.error('This transition does not exist !')
			else:
				rn+='with '+TransImage[Transition]+'\n'
		return 'None'+rn

	elif Flag=='bgm':
		rn=''
		if Bgm.get(Content)==None:
			Fs.error('This Bgm does not exist ！')
		else:
			rn='play music '+BgmPath+Bgm[Content]+'\n'
		if Transition!='None':
			if TransSound.get(Transition)==None:
				Fs.error('This effect does not exist ！')
			else:
				rn='with '+TransSound[Transition]+'\n'
		return '\t'+rn

	elif Flag=='ef':
		rn=''
		ef=Transition.replace('，',',').split(',')
		if ef[0] in EffectSp:
			for s in Content.splitlines():
				rn+='\tcall label('
				for efc in range(2,len(ef)+1):
					if ef[efc]=='this':
						if ef[1]=='Text':
							rn+="'"+s+"'"
						else:
							if Graph.get(s)!=None
								rn+=s
							else:
								Fs.error('This graph does not exist !')
					else:
						rn+=ef[efc]
					if efc==len(ef):
						rn+=')\n'
					else:
						rn+=', '
			return rn
		else:
			Fs.error('This effect does not exist !')

	else:
		Fs.error('This flag does not exist or be supported in this fun !')



def CreatDefine(Name,Mode):
	pass

