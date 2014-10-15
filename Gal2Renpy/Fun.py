#-*-coding:utf-8-*- 

#Copyright(c) 2014 dtysky

import re
import codecs
import pickle
from ctypes import *
from Keyword import *
from Class import *
import sys   
reload(sys)
sys.setdefaultencoding('utf-8')

#Return hash for a dict which may contain a dict as its value or others
def DHash(Dict):
	dh=0
	if isinstance(Dict,dict):
		for tmp in Dict:
			if isinstance(Dict[tmp],dict):
				dh+=hash(tmp)
				for sub in Dict[tmp]:
					dh+=hash(sub+str(Dict[tmp][sub]))
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
	elif (s=='\r\n') | (s[0]=='#'):
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
		rn='label '+Content.replace('，',',').replace(',','')+' :\n'
		rn+="    $ chpater='Chpater."+Content.replace('，',',').split(',')[0].split('p')[1]+"'\n"
		return rn

	elif Flag=='bgm':
		rn=''
		if US.Bgm.get(Content)==None:
			Fs.error('This Bgm does not exist !')
		elif US.Bgm[Content]=='StopBgm':
			rn+='    stop music fadeout 1.0\n'
		else:
			rn+='    play music '+"'"+US.BgmPath+US.Bgm[Content]+"'"
			if Transition!='None':
				if US.Trans.get(Transition)==None:
					Fs.error('This effect does not exist !')
				else:
					rn+='    with '+US.Trans[Transition]+'\n'
			else:
				rn+='    fadein 1.0\n'
		return rn

	elif Flag=='ef':
		rn=''
		ef=Transition.replace('，',',').split(',')
		if ef[0] in US.EffectSp:
			for s in Content.splitlines():
				rn+='    call '+ef[0]+'('
				for efc in range(1,len(ef)+1):
					if ef[efc-1]=='this':
						rn+=s
					elif efc>1:
						rn+=ef[efc-1]
					if efc<len(ef) and efc>1:
						rn+=','
					elif efc==len(ef):
						rn+=')\n'
			return rn
		else:
			Fs.error('This effect does not exist !')

	elif Flag=='gf':
		if US.Graph.get(Content)==None:
 			Fs.error('This Graph does not exist !')
		elif US.Graph[Content]['Type']=='Frame':
			if Transition!='None':
				if US.BgPosition.get(Transition)==None:
					Fs.error('This Postion does not exist !')
				else:
					return '    show '+US.Graph[Content]['Name']+' at '+US.BgPosition[Transition]+'\n'+'    pause '+str(US.Graph[Content]['Pause'])+'\n'+'    hide '+US.Graph[Content]['Name']+'\n'+'    pause 0.2\n'
			else:
				return '    show '+Content+'\n'+'    pause '+str(US.Graph[Content]['Pause'])+'\n'+'    hide '+Content+'\n'+'    pause 0.5\n'
		elif US.Graph[Content]['Type']=='Image':
			if Transition!='None':
				if US.BgPosition.get(Transition)==None:
					Fs.error('This Postion does not exist !')
				else:
					if US.BgPosition[Transition]=='hide':
						return '    hide '+US.Graph[Content]['Name']+'\n'
					else:
						return '    show '+US.Graph[Content]['Name']+' at '+US.BgPosition[Transition]+' with dissolve\n'
			else:
				return '    show '+US.Graph[Content]['Name']+' with dissolve\n'
		elif US.Graph[Content]['Type']=='Chapter':
			return '    hide screen date\n    scene bg Black01A with dissolve\n    scene '+US.Graph[Content]['Name']+'\n'+'    with dissolve\n'+'    pause '+str(US.Graph[Content]['Pause'])+'\n'+'    pause 2.0\n'+'    scene bg Black01A with dissolve\n'


	elif Flag=='sound':
		rn=''
		if US.SoundE.get(Content)==None:
			Fs.error('This Sound does not exist !')
		else:
			rn="    play sound '"+US.SoundPath+US.SoundE[Content]+"'\n"
		if Transition!='None':
			if US.Trans.get(Transition)==None:
				Fs.error('This effect does not exist !')
			else:
				rn='    with '+US.Trans[Transition]+'\n'
		rn+="    hide screen say\n"
		return rn

	elif Flag=='sw':
		rn='    menu:\n'
		if Transition=='normal':
			for sw in Content.splitlines():
				tmp=sw.replace('：',':').split(':')
				rn+='        '+"'"+tmp[0]+"':\n"
				rn+='            call '+tmp[1].lstrip()+'\n'
		else:
			Fs.error('This Mode does not be supported !')
		return rn

	elif Flag=='date':
		rn=''
		if US.Date!='None':
			rn+="    $ Date1='"+US.WinPath+'date/'+US.Date+".png'\n"
		rn+="    $ Date2='"+US.WinPath+'date/'+Content+".png'\n"
		rn+="    $ date='"+Content.replace('-','.')+"'\n"
		US.Date=Content
		return rn

	elif Flag=='renpy':
		return '    '+Content+'\n'

	elif Flag=='key':
		rn=''
		lines=Content.splitlines()
		for line in lines:
			tmp=line.replace('：',':').split(':')
			if US.KeyWord.get(Transition)==None:
				Fs.error("This kind of KeyWord does not exist!")
			else:
				if US.KeyWord[Transition].get(tmp[0])==None:
					Fs.error("This KeyWord does not exist!")
				else:
					if int(tmp[1].encode('utf-8'))>(len(US.KeyWord[Transition][tmp[0]])-1):
						Fs.error("Your Keyword does not have such many information!")
					else:
						rn+="    $ SetMyKey('"+Transition+"','"+tmp[0]+"',"+tmp[1]+')\n'
		rn+='    call EfTextKey()\n'
		return rn

	else:
		Fs.error('This flag does not exist or be supported in this Fun !')

#Creat ren'py define script
def CreatDefine(US):
 	ChrDone=False
 	BgDone=False
 	FileHash=open('Gal2Renpy/HashDict','r')
 	DictHash=pickle.load(FileHash)
 	FileHash.close()
 	
 	for HashName in DictHash:
 		if DictHash[HashName]==DHash(eval('US.'+HashName)):
 			pass
 		else:
			rn=''
			foHPC=None
 			rnHPC=''
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
				rn+="define n=Character('none',show_bg=None)"
				fo.write(rn)
				fo.close()

			elif (HashName=='ChrClothes') | (HashName=='ChrPose') | (HashName=='ChrFace') | (HashName=='ChrDistance'):
				if ChrDone==False:
					fo=codecs.open(US.ScriptPath+'define/char.rpy','w','utf-8')
					if US.HPCSystem:
 						foHPC=codecs.open(US.ScriptPath+'define/hpcchar.rpy','w','utf-8')
					for Name in US.ChrName:
						if Name!='Saying':
							if US.ChrClothes.get(Name)!=None:
								for Clothes in US.ChrClothes[Name]:
									if US.ChrPose.get(Name)!=None:
 										for Poes in US.ChrPose[Name]:
 											if US.ChrFace.get(Name)!=None:
 												for Face in US.ChrFace[Name]:
 													for Dist in US.ChrDistance:
 														rn+='image '+US.ChrName[Name][0]+' '+US.ChrPose[Name][Poes]+US.ChrClothes[Name][Clothes]+US.ChrFace[Name][Face]+US.ChrDistance[Dist]+' = '+"'"+US.ChrPath+US.ChrName[Name][0]+'/'+US.ChrName[Name][0]+US.ChrPose[Name][Poes]+US.ChrClothes[Name][Clothes]+US.ChrFace[Name][Face]+US.ChrDistance[Dist] +".png'\n"
 														if US.HPCSystem:
 															rnHPC+='define '+US.ChrName[Name][0]+' '+US.ChrPose[Name][Poes]+US.ChrClothes[Name][Clothes]+US.ChrFace[Name][Face]+US.ChrDistance[Dist]+'HPC = '+"'"+US.ChrPath+US.ChrName[Name][0]+'/'+US.ChrName[Name][0]+US.ChrPose[Name][Poes]+US.ChrClothes[Name][Clothes]+US.ChrFace[Name][Face]+US.ChrDistance[Dist] +".png'\n"
 					ChrDone=True
 					fo.write(rn)
 					foHPC.write(rnHPC)
 					foHPC.close()
 					fo.close()
 
 			elif (HashName=='Bg') | (HashName=='BgSub') | (HashName=='BgWeather'):
 				if BgDone==False:
 					fo=codecs.open(US.ScriptPath+'define/bg.rpy','w','utf-8')
 					print US.HPCSystem
 					if US.HPCSystem:
 						foHPC=codecs.open(US.ScriptPath+'define/hpcbg.rpy','w','utf-8')
 					for Bg in US.BgMain:
 						if US.BgSub.get(Bg)!=None:
 							for Sub in US.BgSub[Bg]:
								if US.BgWeather.get(Bg)!=None:
 									for Wh in US.BgWeather[Bg]:
										rn+='image bg '+US.BgMain[Bg]+US.BgSub[Bg][Sub]+US.BgWeather[Bg][Wh]+' = '+"'"+US.BgPath+'/'+US.BgMain[Bg]+US.BgSub[Bg][Sub]+US.BgWeather[Bg][Wh]+".png'\n"
										if US.HPCSystem:
											rnHPC+='define '+US.BgMain[Bg]+US.BgSub[Bg][Sub]+US.BgWeather[Bg][Wh]+'HPC = '+"'"+US.BgPath+'/'+US.BgMain[Bg]+US.BgSub[Bg][Sub]+US.BgWeather[Bg][Wh]+".png'\n"
 					BgDone=True
 					fo.write(rn)
 					foHPC.write(rnHPC)
 					foHPC.close()
 					fo.close()

 			elif HashName=='Graph':
 				fo=codecs.open(US.ScriptPath+'define/graph.rpy','w','utf-8')
 				rn=''
 				for gr in US.Graph:
 					if US.Graph[gr]['Source']=='Dir':
 						rn+='image '+US.Graph[gr]['Name']+':\n'
						delay=US.Graph[gr]['Delay']
 						for root,dirs,files in os.walk(US.GamePath+US.EfPath+US.Graph[gr]['Name']):
 							for f in files:
 								if os.path.splitext(f)[1]=='.png':
 									US.Graph[gr]['Pause']+=float(delay)
	 								rn+="    '"+US.EfPath+US.Graph[gr]['Name']+'/'+f+"'\n    pause "+delay+'\n'
	 				elif US.Graph[gr]['Source']=='File':
	 					if US.Graph[gr]['Type']=='Image':
	 						rn+='image '+US.Graph[gr]['Name']+"='"+US.EfPath+US.Graph[gr]['Name']+".png'\n"
				fo.write(rn)
				fo.close()

			elif HashName=='Cg':
				fo=codecs.open(US.ScriptPath+'define/cg.rpy','w','utf-8')
				rn=''
				for cg in US.Cg:
					for sub in US.CgSub[cg]:
						rn+='image cg '+US.Cg[cg]['Name']+sub+"='"+US.CgPath+US.Cg[cg]['Name']+'/'+sub+".png'\n"
				fo.write(rn)
				fo.close()

			elif HashName=='KeyWord':
				fo=codecs.open(US.ScriptPath+'define/mykey.rpy','w','utf-8')
				rn='define mykeyinit={'
				for k in US.KeyWord:
				    rn+="\n    '"+k+"':{\n        'l':["
				    for l in US.KeyWord[k]['l']:
				    	rn+="'"+l+"',"
				    rn=rn[:-1]+"],"
				    for l in US.KeyWord[k]['l']:
				    	rn+="\n        '"+l+"':[0,False,"
				    	for lk in US.KeyWord[k][l]:
				    		rn+="'"+lk+"',"
				    	rn=rn[:-1]+"],"
				    rn=rn[:-1]+'\n    },'
				rn=rn[:-1]+'\n}\n'
				#define a function to set mykey's station in renpy
				rn+='init python:\n'
				rn+='    def SetMyKey(kn,k,i):\n'
				rn+='        if i>persistent.mykey[kn][k][0]:\n'
				rn+='            persistent.mykey[kn][k][0]=i\n'
				rn+='            persistent.mykey[kn][k][1]=True\n'
				rn+='    def InitMyKey():\n'
				rn+='        if persistent.mykey==None:\n'
				rn+='            persistent.mykey=mykeyinit\n'
				rn+='    class ReStMyKey(Action):\n'
				rn+='        def __init__(self,kn,k):\n'
				rn+='            self.kn=kn\n'
				rn+='            self.k=k\n'
				rn+='        def __call__(self):\n'
				rn+='            persistent.mykey[self.kn][self.k][1]=False\n'

				fo.write(rn)
				fo.close()
  
  			DictHash[HashName]=DHash(eval('US.'+HashName))
 	FileHash=open('Gal2Renpy/HashDict','w')
 	pickle.dump(DictHash,FileHash)
 	FileHash.close()