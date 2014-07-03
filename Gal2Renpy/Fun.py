#coding:utf-8

import re
import codecs
import pickle
from ctypes import *
from Keyword import *
from Class import *

#Return hash for a dict which may contain a dict as its value or others
def DHash(Dict):
	dh=0
	if isinstance(Dict,dict):
		for tmp in Dict:
			if isinstance(Dict[tmp],dict):
				dh+=hash(tmp)+hash(str(sorted(Dict[tmp],key=lambda d: d[0])))
			else:
				dh+=hash(tmp)+hash(str(Dict[tmp]))
	else:
		dh+=hash(str(Dict))
	return dh
	
#Return next block
def RBlock(Fs,Allow,US):
	[head,flag,transition,content]=['','','','']
	s=Fs.readline()
	if s=='':
		head='end'
	elif s=='\r\n':
		head='None'
	elif re.match(r'<.*>',s)!=None:

		if re.match(r'<\S+\s+\S+>.+</\S+>',s)!=None:
			sr=re.match(r'<(\S+)\s*(.+)>\s*(.*)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition=sr.group(2)
			content=sr.group(3)
		elif re.match(r'<\S+>.*</\S+>',s)!=None:
			sr=re.match(r'<(\S+)>\s*(.+)\s*</\S+>',s)
			head='sp'
			flag=sr.group(1)
			transition='None'
			content=sr.group(2)
		elif re.match(r'<\S+\s+\S+>',s)!=None:
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
		elif re.match(r'<\S+>',s)!=None:
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
		if Allow:
			tmp=re.match(ur'(\S+)\s+【(.*)】',s)
			if tmp==None:
				tmp=re.match(ur'【(.*)】',s)
				if tmp==None:
					head='text'
					flag='None'
					transition='None'
					content="n '"+s.strip()+"'\n"
				else:
					head='words'
					if US.ChrName['Saying']==None:
						Fs.error('No speaker !')
					else:
						flag=US.ChrName['Saying']
					transition='think'
					content=tmp.group(1)
			else:
				if US.ChrName.get(tmp.group(1))==None:
					Fs.error('This charecter doen not exist !')
				else:
					head='words'
					flag=tmp.group(1)
					transition='Say'
					content=tmp.group(2)
		else:
			head='None'
			flag='None'
			transition='None'
			content='None'
	return [head,flag,transition,content]



#Return a string which changing special texts to scripts
def Sp2Script(Flag,Transition,Content,US,Fs):


	if Flag=='sc':
		return 'label '+Content.replace('，',',').replace(',','')+' :\n'

	elif Flag=='bg':
		tmp=Content.replace('：',':').split(':')
		sr=tmp[0].replace('，',',').split(',')
		rn=''
		if US.BgMain.get(sr[0])==None:
			Fs.error('This Bg does not exist !')
		else:
			if len(tmp)==1:
				w=US.BgWeather[sr[0]]['default']
			else:
				if US.BgWeather[sr[0]].get(tmp[1])==None:
					Fs.error('This Weather does not exist !')
				else:
					w=US.BgWeather[sr[0]][tmp[1]]
			if len(sr)==2:
				if US.BgSub[sr[0]].get(sr[1])==None:
					Fs.error('This SubBg does not exist !')
				else:
					rn='    scene bg '+US.BgMain[sr[0]]+US.BgSub[sr[0]][sr[1]]+w+'\n'
			elif len(sr)==1:
				rn='    scene bg '+US.BgMain[sr[0]]+US.BgSub[sr[0]]['default']+w+'\n'
			else:
				Fs.error('Unsupport two and more subscenes !')
		if Transition!='None':
			if US.Trans.get(Transition)==None:
				Fs.error('This transition does not exist !')
			else:
				rn+='    with '+US.Trans[Transition]+'\n'
		return rn

	elif Flag=='bgm':
		rn=''
		if US.Bgm.get(Content)==None:
			Fs.error('This US.Bgm does not exist !')
		else:
			rn='play music '+'''"'''+US.BgmPath+US.Bgm[Content]+'''"\n'''
		if Transition!='None':
			if US.Trans.get(Transition)==None:
				Fs.error('This effect does not exist !')
			else:
				rn='with '+US.Trans[Transition]+'\n'
		return '    '+rn

	elif Flag=='ef':
		rn=''
		ef=Transition.replace('，',',').split(',')
		if ef[0] in US.EffectSp:
			for s in Content.splitlines():
				rn+='    call '+ef[0]+'('
				for efc in range(2,len(ef)+1):
					if ef[efc-1]=='this':
						if ef[1]=='Text':
							rn+='''"'''+s+'''"'''+','
						elif ef[1]=='Image':
							if Graph.get(s)==None:
								Fs.error('This graph does not exist !')
							else:
								rn+=s+','
						else:
							pass
					elif efc>2:
						rn+=ef[efc-1]
						if efc<len(ef):
							rn+=','
					if efc==len(ef):
						rn+=')\n'
			return rn
		else:
			Fs.error('This effect does not exist !')

	elif Flag=='sound':
		rn=''
		if US.SoundE.get(Content)==None:
			Fs.error('This Sound does not exist !')
		else:
			rn='play sound '+'''"'''+SoundPath+US.SoundE[Content]+'''"\n'''
		if Transition!='None':
			if US.Trans.get(Transition)==None:
				Fs.error('This effect does not exist !')
			else:
				rn='with '+US.Trans[Transition]+'\n'
		return '    '+rn

	elif Flag=='sw':
		rn='    menu:\n'
		if Transition=='nomal':
			for sw in Content.splitlines():
				tmp=sw.replace('：',':').split(':')
				rn+='        '+"'"+tmp[0]+"':\n"
				rn+='            call '+tmp[1].lstrip()+'\n'
		else:
			Fs.error('This Mode does not be supported !')
		return rn

	elif Flag=='date':
		return "    $ Date='"+US.WinPath+'date/'+Content+".png'\n"

	elif Flag=='renpy':
		return '    '+Content+'\n'

	else:
		Fs.error('This flag does not exist or be supported in this Fun !')

#Creat ren'py define script
def CreatDefine(US):
 	ChrDone=False
 	BgDone=False
 	FileHash=open('Gal2Renpy/HashDict','r')
 	DictHash=pickle.load(FileHash)
 	
 	for HashName in DictHash:
 		if DictHash[HashName]==DHash(eval('US.'+HashName)):
 			pass
 		else:
 			DictHash[HashName]=DHash(eval('US.'+HashName))
			rn=''
			if HashName=='ChrWindow':
				fo=codecs.open(US.ScriptPath+'define/bgwin.rpy','w','utf-8')
				for Name in US.ChrWindow:
					rn+='define '+Name+"S='"+US.WinPath+'adv/'+Name+"S.png'\n"
					rn+='define '+Name+"N='"+US.WinPath+'adv/'+Name+"N.png'\n"
				fo.write(rn)
				fo.close()

 			elif  HashName=='ChrName':
 				fo=codecs.open(US.ScriptPath+'define/name.rpy','w','utf-8')
 				for Name in US.ChrName:
 					if Name!='Saying':
 						if len(US.ChrName[Name])==4:
 							rn+='define '+US.ChrName[Name][0]+'A = Character('+"'"+Name+"',who_bold=False,who_outlines=[ (2, '"+US.ChrName[Name][1]+"') ],what_outlines=[ (1,'"+US.ChrName[Name][1]+"') ],show_bg="+US.ChrName[Name][2]+"S)\n"
 							rn+='define '+US.ChrName[Name][0]+'V = Character('+"'"+Name+"',who_bold=False,who_outlines=[ (2, '"+US.ChrName[Name][1]+"') ],what_outlines=[ (1,'"+US.ChrName[Name][1]+"') ])\n"
 						else:
	 						rn+='define '+US.ChrName[Name][0]+'A = Character('+"'"+Name+"',who_bold=False,who_outlines=[ (2, '"+US.ChrName[Name][1]+"') ],what_outlines=[ (1,'"+US.ChrName[Name][1]+"') ])\n"
							rn+='define '+US.ChrName[Name][0]+'V = Character('+"'"+Name+"',who_bold=False,who_outlines=[ (2, '"+US.ChrName[Name][1]+"') ],what_outlines=[ (1,'"+US.ChrName[Name][1]+"') ])\n"
				rn+='define n=Character(show_bg=None)'
				fo.write(rn)
				fo.close()

			elif (HashName=='ChrClothes') | (HashName=='ChrPose') | (HashName=='ChrFace') | (HashName=='ChrDistance'):
				if ChrDone==False:
					fo=codecs.open(US.ScriptPath+'define/char.rpy','w','utf-8')
					for Name in US.ChrName:
						if Name!='Saying':
							if US.ChrClothes.get(Name)!=None:
								for Clothes in US.ChrClothes[Name]:
									if US.ChrPose.get(Name)!=None:
 										for Poes in US.ChrPose[Name]:
 											if US.ChrFace.get(Name)!=None:
 												for Face in US.ChrFace[Name]:
 													for Dist in US.ChrDistance:
 														rn+='image '+US.ChrName[Name][0]+US.ChrClothes[Name][Clothes]+US.ChrPose[Name][Poes]+US.ChrFace[Name][Face]+US.ChrDistance[Dist]+' = '+"'"+US.ChrPath+US.ChrName[Name][0]+'/'+US.ChrName[Name][0]+US.ChrClothes[Name][Clothes]+US.ChrPose[Name][Poes]+US.ChrFace[Name][Face]+US.ChrDistance[Dist] +".png'\n"
 					ChrDone=True
 					fo.write(rn)
 					fo.close()
 
 			elif (HashName=='Bg') | (HashName=='BgSub') | (HashName=='BgWeather'):
 				if BgDone==False:
 					fo=codecs.open(US.ScriptPath+'define/bg.rpy','w','utf-8')
 					for Bg in US.BgMain:
 						if US.BgSub.get(Bg)!=None:
 							for Sub in US.BgSub[Bg]:
								if US.BgWeather.get(Bg)!=None:
 									for Wh in US.BgWeather[Bg]:
										rn+='image bg '+US.BgMain[Bg]+US.BgSub[Bg][Sub]+US.BgWeather[Bg][Wh]+' = '+"'"+US.BgPath+'/'+US.BgMain[Bg]+US.BgSub[Bg][Sub]+US.BgWeather[Bg][Wh]+".png'\n"
 					BgDone=True
 					fo.write(rn)
 					fo.close()
  
  
 	FileHash=open('Gal2Renpy/HashDict','w')
 	pickle.dump(DictHash,FileHash)
 	FileHash.close()