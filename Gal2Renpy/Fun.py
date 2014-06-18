#Return a string which changing special texts to scripts
def Sp2Script(Flag,Transition,Content,Fs):

	if Flag=='sc':
		return 'label '+Content.replace('，','')+' :\n'

	elif Flag=='bg':
		#Weather
		tmp=Content.replace('：',':').split(':')
		sr=tmp[0].replace('，',',').split(',')
		if len(tmp)==1:
			w=BgWeather[sr[0]]['default']
		else:
			if BgWeather[sr[0]].get(tmp[1])==None:
				Fs.error('This Weather does not exist !')
			else:
				w=BgWeather[sr[0]].get[tmp[1]]
		rn=''
		if BgMain.get(sr[0])==None:
			Fs.error('This Bg does not exist !')
		else:
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

	elif Flag=='renpy':
		return '    '+Content+'\n'

	else:
		Fs.error('This flag does not exist or be supported in this fun !')


#Creat ren'py define script
def CreatDefine():
 	ChrDone=False
 	BgDone=False
 	FileHash=open('Gal2Renpy/HashDict','r')
 	DictHash=pickle.load(FileHash)
 	FileHash.close()
 	for HashName in DictHash:
 		if DictHash[HashName][0]==DHash(DictHash[HashName][1]):
 			pass
 		else:
			DictHash[HashName][0]=DHash(DictHash[HashName][1])
			rn=''
 			if  HashName=='ChrName':
 				fo=codecs.open(ScriptPath+'define/name.rpy','w')
 				for Name in ChrName:
 					if Name!='Saying':
 						rn+='define '+ChrName[Name][0]+'A = Character('+"'"+Name+"',color='"+ChrName[Name][1]+"')\n"
						rn+='define '+ChrName[Name][0]+'V = Character('+"'"+Name+"',color='"+ChrName[Name][1]+"')\n"
				fo.write(rn)
				fo.close()

			elif (HashName=='ChrClothes') | (HashName=='ChrPose') | (HashName=='ChrFace'):
				if ChrDone==False:
					fo=codecs.open(ScriptPath+'define/char.rpy','w')
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
 					fo=codecs.open(ScriptPath+'define/bg.rpy','w')
 					for Bg in BgMain:
 						if BgSub.get(Bg)!=None:
 							for Sub in BgSub[Bg]:
								if BgWeather.get(Bg)!=None:
 									for Wh in BgWeather[Bg]:
										rn+='image bg '+BgMain[Bg]+BgSub[Bg][Sub]+BgWeather[Bg][Wh]+' = '+"'"+BgPath+'/'+BgMain[Bg]+BgSub[Bg][Sub]+BgWeather[Bg][Wh]+".png'\n"
 					BgDone=True
 					fo.write(rn)
 					fo.close()
  
  
 	FileHash=open('Gal2Renpy/HashDict','w')
 	pickle.dump(DictHash,FileHash)
 	FileHash.close()