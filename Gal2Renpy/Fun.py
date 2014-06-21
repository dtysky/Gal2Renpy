#-*-coding:utf-8-*- 

import re
import codecs
import pickle
import json
from ctypes import *
from Keyword import *
from Class import *
from User import *

#Return hash for a dict which may contain a dict as its value
def DHash(Dict):
	dh=0
	for tmp in Dict:
		if isinstance(Dict[tmp],dict):
			dh+=hash(tmp)+hash(str(sorted(Dict[tmp],key=lambda d: d[0])))
		else:
			dh+=hash(tmp)+hash(str(Dict[tmp]))
	return dh

#Init dictionaries
def InitD():
	global ChrName,ChrClothes,ChrPose,ChrPosition,BgMain,BgSub,BgWeather,ChrFace
	global EffectSp,Trans,Bgm,SoundE,ScriptPath,TextPath,ChrPath,BgPath,BgmPath
	global TestMode
	#Bg
	jtmp=json.load(open(sys.path[0]+'/game/Gal2Renpy/User/Bg.json','r'))
	BgMain=jtmp['BgMain']
	BgSub=jtmp['BgSub']
	BgWeather=jtmp['BgWeather']
	#ChrFace
	ChrFace=json.load(open(sys.path[0]+'/game/Gal2Renpy/User/ChrFace.json','r'))
	#ChrOther
	jtmp=json.load(open(sys.path[0]+'/game/Gal2Renpy/User/ChrOther.json','r'))
	ChrName=jtmp['ChrName']
	for ch in sorted(ChrName):
		ChrName[ch].append(None)
	ChrName['Saying']= None 
	ChrClothes=jtmp['ChrClothes']
	ChrPose=jtmp['ChrPose']
	ChrPosition=jtmp['ChrPosition']
	#Effect
	jtmp=json.load(open(sys.path[0]+'/game/Gal2Renpy/User/Effect.json','r'))
	EffectSp=jtmp['EffectSp']
	Trans=jtmp['Trans']
	#Sound
	jtmp=json.load(open(sys.path[0]+'/game/Gal2Renpy/User/Sound.json','r'))
	Bgm=jtmp['Bgm']
	SoundE=jtmp['SoundE']
	#Path,Mode
	jtmp=json.load(open(sys.path[0]+'/game/Gal2Renpy/User/PathMode.json','r'))
	ScriptPath=jtmp['ScriptPath']
	ChrPath=jtmp['ChrPath']
	BgPath=jtmp['BgPath']
	BgmPath=jtmp['BgmPath']
	TextPath=jtmp['TextPath']
	if jtmp['TestMode']=='True':
		TestMode=True
	else:
		TestMode=False

	
#Return next block
def RBlock(Fs,Allow):
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
					content="'"+s+"'"
				else:
					head='words'
					if ChrName['Saying']==None:
						Fs.error('No speaker !')
					else:
						flag=ChrName['Saying']
					transition='think'
					content=tmp
			else:
				if ChrName.get(tmp.group(1))==None:
					Fs.error('This charecter doen not exist !')
				else:
					head='words'
					flag=tmp.group(1)
					transition='say'
					content=tmp.group(2)
					ChrName['Saying']=flag
		else:
			head='None'
			flag='None'
			transition='None'
			content='None'
	return [head,flag,transition,content]



#Return a string which changing special texts to scripts
def Sp2Script(Flag,Transition,Content,Fs):


	if Flag=='sc':
		return 'label '+Content.replace('，','')+' :\n'

	elif Flag=='bg':
		tmp=Content.replace('：',':').split(':')
		sr=tmp[0].replace('，',',').split(',')
		rn=''
		if BgMain.get(sr[0])==None:
			Fs.error('This Bg does not exist !')
		else:
			if len(tmp)==1:
				w=BgWeather[sr[0]]['default']
			else:
				if BgWeather[sr[0]].get(tmp[1])==None:
					Fs.error('This Weather does not exist !')
				else:
					w=BgWeather[sr[0]].get[tmp[1]]
			if len(sr)==2:
				if BgSub[sr[0]].get(sr[1])==None:
					Fs.error('This SubBg does not exist !')
				else:
					rn='    scene bg '+BgMain[sr[0]]+BgSub[sr[0]][sr[1]]+w+'\n'
			elif len(sr)==1:
				rn='    scene bg '+BgMain[sr[0]]+BgSub[sr[0]]['default']+w+'\n'
			else:
				Fs.error('Unsupport two and more subscenes !')
		if Transition!='None':
			if Trans.get(Transition)==None:
				Fs.error('This transition does not exist !')
			else:
				rn+='    with '+Trans[Transition]+'\n'
		return rn

	elif Flag=='bgm':
		rn=''
		if Bgm.get(Content)==None:
			Fs.error('This Bgm does not exist !')
		else:
			rn='play music '+'''"'''+BgmPath+Bgm[Content]+'''"\n'''
		if Transition!='None':
			if Trans.get(Transition)==None:
				Fs.error('This effect does not exist !')
			else:
				rn='with '+Trans[Transition]+'\n'
		return '    '+rn

	elif Flag=='ef':
		rn=''
		ef=Transition.replace('，',',').split(',')
		if ef[0] in EffectSp:
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
		if SoundE.get(Content)==None:
			Fs.error('This Sound does not exist !')
		else:
			rn='play sound '+'''"'''+SoundPath+SoundE[Content]+'''"\n'''
		if Transition!='None':
			if Trans.get(Transition)==None:
				Fs.error('This effect does not exist !')
			else:
				rn='with '+Trans[Transition]+'\n'
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

	elif Flag=='renpy':
		return '    '+Content+'\n'

	else:
		Fs.error('This flag does not exist or be supported in this fun !')

#Creat ren'py define script
def CreatDefine():
	f=codecs.open('E:/Follow wings/FW/game/script/debug.txt','w','utf-8')
	f.write(TextPath+'\r\n'+ScriptPath)
	f.close()
 	ChrDone=False
 	BgDone=False
 	FileHash=open(sys.path[0]+'/game/Gal2Renpy/Gal2Renpy/HashDict','r')
 	DictHash=pickle.load(FileHash)
 	FileHash.close()
 	for HashName in DictHash:
 		if DictHash[HashName]==DHash(eval(HashName)):
 			pass
 		else:
 			DictHash[HashName]=DHash(eval(HashName))
			rn=''
 			if  HashName=='ChrName':
 				fo=codecs.open(ScriptPath+'define/name.rpy','w','utf-8')
 				for Name in ChrName:
 					if Name!='Saying':
 						rn+='define '+ChrName[Name][0]+'A = Character('+"'"+Name+"',color='"+ChrName[Name][1]+"')\n"
						rn+='define '+ChrName[Name][0]+'V = Character('+"'"+Name+"',color='"+ChrName[Name][1]+"')\n"
				fo.write(rn)
				fo.close()

			elif (HashName=='ChrClothes') | (HashName=='ChrPose') | (HashName=='ChrFace'):
				if ChrDone==False:
					fo=codecs.open(ScriptPath+'define/char.rpy','w','utf-8')
					for Name in ChrName:
						if Name!='Saying':
							if ChrClothes.get(Name)!=None:
								for Clothes in ChrClothes[Name]:
									if ChrPose.get(Name)!=None:
 										for Poes in ChrPose[Name]:
 											if ChrFace.get(Name)!=None:
 												for Face in ChrFace[Name]:
 													rn+='image '+ChrName[Name][0]+ChrClothes[Name][Clothes]+ChrPose[Name][Poes]+ChrFace[Name][Face]+' = '+"'"+ChrPath+ChrName[Name][0]+'/'+ChrName[Name][0]+ChrClothes[Name][Clothes]+ChrPose[Name][Poes]+ChrFace[Name][Face] +".png'\n"
 					ChrDone=True
 					fo.write(rn)
 					fo.close()
 
 			elif (HashName=='Bg') | (HashName=='BgSub') | (HashName=='BgWeather'):
 				if BgDone==False:
 					fo=codecs.open(ScriptPath+'define/bg.rpy','w','utf-8')
 					for Bg in BgMain:
 						if BgSub.get(Bg)!=None:
 							for Sub in BgSub[Bg]:
								if BgWeather.get(Bg)!=None:
 									for Wh in BgWeather[Bg]:
										rn+='image bg '+BgMain[Bg]+BgSub[Bg][Sub]+BgWeather[Bg][Wh]+' = '+"'"+BgPath+'/'+BgMain[Bg]+BgSub[Bg][Sub]+BgWeather[Bg][Wh]+".png'\n"
 					BgDone=True
 					fo.write(rn)
 					fo.close()
  
  
 	FileHash=open(sys.path[0]+'/game/Gal2Renpy/Gal2Renpy/HashDict','w')
 	pickle.dump(DictHash,FileHash)
 	FileHash.close()