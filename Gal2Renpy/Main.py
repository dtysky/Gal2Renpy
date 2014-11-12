#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################


import sys
import os
import pickle
from G2R import *

FileAll=[]
Files=[]

FS=MyFS()
FO=MyFS()
US=UserSource('../User')
UT=UserTag(US)
TxtC=TextCreat()
SpC=SpCreat()
Tmp=TmpC()

sys.path.append(US.Args['pathmode']['Gal2RenpyPath']+'Gal2Renpy')


def CheckSpFile(fp):
	if not os.path.exists(fp):
		FH=open(fp,'w')
		pickle.dump({},FH)
		FH.close()

#Creat all definitions and refresh DictHash
#Only a dict had been changed will re-creat it
CheckSpFile('DictHash')
FH=open('DictHash','r')
DictHash=pickle.load(FH)
FH.close()
DictHash=DefineCreat(US,FO,DictHash)
FH=open('DictHash','w')
pickle.dump(DictHash,FH)
FH.close()

#FileList: A dict for storing scenes in all files
CheckSpFile('FileHash')
CheckSpFile('FileList')
FH=open('FileHash','r')
FileHash=pickle.load(FH)
FH.close()
FH=open('FileList','r')
FileList=pickle.load(FH)
FH.close()

#Ensure FileHash and FileList are synchronous
if len(FileHash)>len(FileList):
	for f in FileHash:
		if f not in FileList:
			FileList[f]=[]
if len(FileHash)<len(FileList):
	for f in FileList:
		if f not in FileHash:
			FileList[f]=0

#Add all '.gal' files
for root,dirs,files in os.walk(US.Args['pathmode']['TextPath']):
    for f in files:
        if os.path.splitext(f)[1]=='.gal':
        	FileAll.append(root+'/'+f)

#Only a file had been changed will process it
for f in FileAll:
	FS.Open(f,'rb')
	if not FileHash.get(f):
		Files.append(f)
	elif FS.hash()!=FileHash[f]:
		Files.append(f)
	FS.Close()

#Delete all invailed files in FileHash and FileList 
for f in FileHash:
	if f not in FileAll:
		del FileHash[f]
		del FileList[f]

"""
Files/Dicts prepare end
"""

#Format line for using
def ChangeSp(Line):
	rn={'flag':'','attrs1':{},'attrs2':Line['attrs2']}
	f=''
	i=0
	for flag in Line['flag']:
		f+='_'+flag
		rn['attrs1'][f[1:]]=Line['attrs1'][i]
		i+=1
	rn['flag']=f[1:]
	return rn

ScriptPath=US.Args['pathmode']['ScriptPath']
if US.Args['pathmode']['TestMode']:
	#In test mode, remove start.rpy first
	if os.path.exists(ScriptPath+'start.rpy'):
		os.remove(ScriptPath+'start.rpy')
		if os.path.exists(ScriptPath+'start.rpyc'):
			os.remove(ScriptPath+'start.rpyc')
	#Creat the only script in this mode
	FO.Open(ScriptPath+'test.rpy','w')
	FO.Write('label start:\n')
	if US.Args['pathmode']['KeySystem']:
		FO.Write("    $ InitMyKey()\n")
	if US.Args['pathmode']['HPCSystem']:
		FO.Write('    $ HPCMessInit()\n')
	FO.Write("    $ store.chapter='Chapter.test'\n")
	#Begin
	j=0
	for fp in Files:
		FS.Open(fp,'r')
		FileList[fp]=[]
		FrameEnd=False
		TestBegin=False
		while not FrameEnd:
			block=ReadBlock(FS)
			for line in block:
				#Check whether test had begined
				if TestBegin:
					if line['head']=='words':
						if not Tmp.Args['mode']:
							FS.Error("You must define a mode with 'mode' tag first !")
						if line['flag']=='text':
							TxtC.Refresh(line['flag'],Tmp.Args['mode'],line['attrs2'])
						elif line['flag']=='say':
							TxtC.Refresh(line['flag'],Tmp.Args['mode'],line['attrs2'],line['attrs1'])
						elif line['flag']=='think':
							if not Tmp.Args['view']:
								FS.Error("You must define a view with 'view' tag first !")
							TxtC.Refresh(line['flag'],Tmp.Args['mode'],line['attrs2'],Tmp.Args['view'])
						FO.Write(TxtC.Show(US,FS))
					elif line['head']=='sp':
						for flag in line['flag']:
							if flag not in US.Keywords:
								FS.Error("This flag '"+flag+"' does not be supported !")
						line=ChangeSp(line)
						SpCNow=SpC[line['flag']]
						SpCNow.Refresh(line['attrs1'],line['attrs2'])
						if line['flag']=='sc' and SpCNow.Get()['k']=='Main':
							sc=(int(SpCNow.Get()['cp'].replace('Cp','')),int(SpCNow.Get()['sc'].replace('Sc','')))
							FileList[fp].append(sc)
						FO.Write(SpCNow.Show(SpCNow.GetFlag(),SpCNow.Get(),US,UT,Tmp,FS))
					elif line['head']=='skip':
						pass
					elif line['head']=='end':
						if Tmp.Args['test']=='Begin':
							FS.Error('Test mode does not end until this file end !')
						FrameEnd=True
				else:
					if line['head']=='end':
						FrameEnd=True
					if line['head']=='sp' and line['flag']==['test']:
						line=ChangeSp(line)
						SpC['test'].Refresh(line['attrs1'],line['attrs2'])
						SpC['test'].Show(SpC['test'].GetFlag(),SpC['test'].Get(),US,UT,Tmp,FS)
					if 'test' in Tmp.Args and Tmp.Args['test']=='Begin':
						TestBegin=True
	FO.Close()

else:

	#In normal mode, remove test.rpy first
	if os.path.exists(ScriptPath+'test.rpy'):
		os.remove(ScriptPath+'test.rpy')
		if os.path.exists(ScriptPath+'test.rpyc'):
			os.remove(ScriptPath+'test.rpyc')
	FO.Open(ScriptPath+'start.rpy','w')
	FO.Write('label start:\n')
	if US.Args['pathmode']['KeySystem']:
		FO.Write("    $ InitMyKey()\n")
	if US.Args['pathmode']['HPCSystem']:
		FO.Write('    $ HPCMessInit()\n')
	#Begin
	for fp in Files:
		FS.Open(fp,'r')
		FileList[fp]=[]
		CanWrite=False
		FrameEnd=False
		while not FrameEnd:
			block=ReadBlock(FS)
			for line in block:
				#Check whether a scene had been defined
				if not CanWrite:
					sc=ChangeSp(line)
					SpCNow=SpC['sc']
					SpCNow.Refresh(sc['attrs1'],sc['attrs2'])
					if sc['flag']=='sc':
						FO.Open(ScriptPath+'test/'+SpCNow.Get()['sc']+SpCNow.Get()['cp']+'.rpy')
						CanWrite=True
					else:
						FS.Error("You must define a scene with 'sc' tag first !")
					FO.Write(SpCNow.Show(SpCNow.GetFlag(),SpCNow.Get(),US,UT,Tmp,FS))
				if line['head']=='words':
					if not Tmp.Args['mode']:
						FS.Error("You must define a mode with 'mode' tag first !")
					if line['flag']=='text':
						TxtC.Refresh(line['flag'],Tmp.Args['mode'],line['attrs2'])
					elif line['flag']=='say':
						TxtC.Refresh(line['flag'],Tmp.Args['mode'],line['attrs2'],line['attrs1'])
					elif line['flag']=='think':
						if not Tmp.Args['view']:
							FS.Error("You must define a view with 'view' tag first !")
						TxtC.Refresh(line['flag'],Tmp.Args['mode'],line['attrs2'],line['attrs1'])
					FO.Write(TxtC.Show(US,FS))
				elif line['head']=='sp':
					line=ChangeSp(line)
					if line['flag'] not in US.Keywords:
						FS.Error("This flag '"+flag+"' does not be supported !")
					SpCNow=SpC[line['flag']]
					SpCNow.Refresh(line['attrs1'],line['attrs2'])
					if line['flag']=='sc' and SpCNow.Get()['k']=='Main':
						sc=(int(SpCNow.Get()['cp'].replace('Cp','')),int(SpCNow.Get()['sc'].replace('Sc','')))
						FileList[fp].append(sc)
					FO.Write(SpCNow.Show(SpCNow.GetFlag(),SpCNow.Get(),US,UT,Tmp,FS))
				elif line['head']=='skip':
					pass
				elif line['head']=='end':
					FrameEnd=True
	FO.Close()
	
	FileListAll=[]
	for l in FileList:
		FileListAll.extend(l)
	FileListDict={}
	for i in range(len(FileListAll)):
		if FileListAll[i][0] not in FileListDict:
			FileListDict[FileListAll[i][0]]=[]
		FileListDict[FileListAll[i][0]].append(FileListAll[i][1])
	FO.Open(ScriptPath+'start.rpy')
	for sc in sorted(FileListDict):
		for cp in sorted(FileListDict[sc]):
			sccp='Sc'+str(sc)+'Cp'+str(cp)
			Fo.write('    call '+sccp+'\n')
	FO.Close()

FH=open('FileList','w')
pickle.dump(FileList,FH)
FH.close()

for f in Files:
	FS.Open(f,'rb')
	FileHash[f]=FS.hash()
FH=open('FileHash','w')
pickle.dump(FileHash,FH)
FH.close()