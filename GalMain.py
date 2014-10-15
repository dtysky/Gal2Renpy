#-*-coding:utf-8-*- 

#Copyright(c) 2014 dtysky

#Writing to future me:
#You have only two chioces: rewriting, or closing


import re
import sys
import os
import codecs
import pickle
from ctypes import *
from Gal2Renpy.Class import *
from Gal2Renpy.Fun import *

Begin=None

Mode='A'

Fs=MyFS()

ChrNow=[]
FileNow=[]
FileAll=[]
ChrTmp=[]

US=User()
BgC=Bg(US,Fs)
CgC=Cg(US)
CreatDefine(US)


FileHash=open('Gal2Renpy/HashFile','r')
HashFile=pickle.load(FileHash)
FileHash.close()
FileList=open('Gal2Renpy/ListFile','r')
ListFile=pickle.load(FileList)
FileList.close()

#Ensure HashFile and ListFile are synchronous
if len(HashFile)==len(ListFile):
	pass
else:
	HashFile.clear()
	ListFile.clear()

#Add all '.gal' files
for root,dirs,files in os.walk(US.TextPath):
    for f in files:
        if os.path.splitext(f)[1]!='.gal':
        	pass
        else:
        	FileAll.append(root+'/'+f)

#Only a file had been changed will process it
for f in FileAll:
	Fs.open(f,'rb')
	if HashFile.get(f)==None:
		FileNow.append(f)
	else:
		if Fs.hash()==HashFile[f]:
			pass
		else:
			FileNow.append(f)
	Fs.close()

#Delete some invailed keys in HashFile and ListFile 
for f in sorted(HashFile):
	if f in FileAll:
		pass
	else:
		del HashFile[f]
		del ListFile[f]

if US.TestMode==True:
	if os.path.exists(US.ScriptPath+'script.rpy'):
		os.remove(US.ScriptPath+'script.rpy')
		if os.path.exists(US.ScriptPath+'script.rpyc'):
			os.remove(US.ScriptPath+'script.rpyc')
	Fo=codecs.open(US.ScriptPath+'test.rpy','w','utf-8')
	Fo.write('label start:\n'+"    $ chapter='Chapter.test'\n    $ date='10.09'\n    $ InitMyKey()\n")
	for path in FileNow:
		Fs.open(path,'r')
		ListFile[f]=[]
		Begin=False
		while 1:
			[Head,Flag,Transition,Content]=RBlock(Fs,Begin,US)
			if Head=='end':
				Fo.flush()
				HashFile[f]=Fs.hash()
				Fs.close()
				break
			elif (Head=='sp') & (Flag=='test'):
				if Content=='Begin':
					if Begin==True:
						Fs.error('A file can only contain one test module !')
					else:
						Begin=True
				elif Content=='End':
					if Begin==False:
						Fs.error('Your test module does not been created !')
					Fs.close()
					break
				else:
					Fs.error('This test mode does not exist !')
			elif Begin:
				if Head=='sp':
					
					if Flag not in Keywords:
						Fs.error('This keyword does not exit!')

					elif Flag=='mode':
						if Content=='Hide':
							Fo.write('    hide window\n')
						elif Content=='Re':
							Fo.write('    show window\n')
						elif Content=='ADV':
							Mode='A'
						elif Content=='NVL':
							Mode='N'
						else:
							Fs.error('This mode does not exist !')

					elif Flag=='bg':
						BgC.refresh(Content,Transition)
						Fo.write(BgC.show())

					elif Flag=='cg':
						CgC.refresh(Content,Transition,US,Fs)
						Fo.write(CgC.show(US,Fs))

					elif Flag=='ch':
						for ch in Content.splitlines():
							name=re.match(r'(\S+)\s+(\S+)',ch).group(1)
							attrs=re.match(r'(\S+)\s+(\S+)',ch).group(2)
							if US.ChrName.get(name)==None:
								Fs.error('This charecter does not exist !')
							else:
								if US.ChrName[name][0] in ChrNow:
									pass
								else:
									US.ChrName[name][len(US.ChrName[name])-1]=Chr(US,Fs,name)
									ChrNow.append(US.ChrName[name][0])
									US.ChrName[name][len(US.ChrName[name])-1].rfattrs(attrs)
							US.ChrName[name][len(US.ChrName[name])-1].rfattrs(attrs)
							Fo.write(US.ChrName[name][len(US.ChrName[name])-1].show())

					elif Flag=='view':
						if US.ChrName.get(Content)==None:
							Fs.error('This charecter does not exist !')
						else:
							US.ChrName['Saying']=Content
						if len(US.ChrName[Content])==4:
							Fo.write('    $ n=Character(show_bg='+US.ChrName[Content][2]+"N,what_outlines=[(1,'"+US.ChrName[Content][1]+"')])\n")

					elif Flag=='chc':
						if Transition=='Begin':
							NameC=Content.replace('：',':').split(':')
							for na in NameC:
								if na not in US.ChrName:
									Fs.error('This Character does not exist !')
							ChrTmp.append(NameC[0])
							Fo.write('    $ '+US.ChrName[NameC[0]][0]+"A=Character('"+NameC[0]+"',show_bg="+US.ChrName[NameC[1]][2]+"S,what_outlines=[(1,'"+US.ChrName[NameC[1]][1]+"')],who_bold=False,who_outlines=[ (2,'"+US.ChrName[NameC[1]][1]+"')])\n")
						elif Transition=='End':
							if Content not in ChrTmp:
								Fs.error('This Character did not be changed !')
							else:
								ChrTmp.remove(Content)
								Fo.write('    $ '+US.ChrName[Content][0]+"A=Character('"+Content+"',show_bg="+US.ChrName[Content][2]+"S,what_outlines=[(1,'"+US.ChrName[Content][1]+"')],who_bold=False,who_outlines=[ (2,'"+US.ChrName[Content][1]+"')])\n")
						else:
							Fs.error('Wrong using this keyword !')

					elif Flag=='sc':
						pass


					else:
						Fo.write(Sp2Script(Flag,Transition,Content,US,Fs))

				elif Head=='words':
					if US.ChrName[Flag][0] in ChrNow:
						pass
					else:
						US.ChrName[Flag][len(US.ChrName[Flag])-1]=Chr(US,Fs,Flag)
						ChrNow.append(US.ChrName[Flag][0])
					US.ChrName[Flag][len(US.ChrName[Flag])-1].rftext(Content,Transition,Mode)
					Fo.write(US.ChrName[Flag][len(US.ChrName[Flag])-1].show())

				elif Head=='text':
					Fo.write('    '+Content)

				else:
					pass
			else:
				pass
	Fo.close()


else:

	for path in FileNow:
		Fs.open(path,'r')
		ListFile[path]=[]
		pathtmp=''
		Allow=False

		while 1:
			[Head,Flag,Transition,Content]=RBlock(Fs,Allow,US)
			if Head=='end':
				HashFile[path]=Fs.hash()
				if Allow:
					ListFile[path].append(pathtmp)
				if Allow:
					Fo.write('    return')
				Fs.close()
				Fo.close()
				break

			elif (Head=='sp') & (Flag=='sc'):
				if Transition=='None':
					pathtmp=Content.replace('，',',').replace(',','')
				else:
					pass
				Allow=True
				Fo=codecs.open(US.ScriptPath+'text/'+Content.replace('，',',').replace(',','')+'.rpy','w','utf-8')
				Fo.write(Sp2Script(Flag,Transition,Content,US,Fs))

			elif Allow:
				if Head=='sp':

					if Flag not in keywords:
						Fs.error('This keyword does not exit!')

					elif Flag=='mode':
						if Content=='Hide':
							sout='    hide window\n'
						elif Content=='Re':
							sout='    show window\n'
						elif Content=='ADV':
							Mode='A'
						elif Content=='NVL':
							Mode='N'
						else:
							Fs.error('This mode does not exist ！')

					elif Flag=='ch':
						for ch in Content.splitlines():
							name=re.match(r'(\S+)\s+(\S+)',ch).group(1)
							attrs=re.match(r'(\S+)\s+(\S+)',ch).group(2)
							if US.ChrName.get(name)==None:
								Fs.error('This charecter does not exist !')
							else:
								if US.ChrName[name][0] in ChrNow:
									pass
								else:
									US.ChrName[name][len(US.ChrName[name])-1]=Chr(US,Fs,name)
									ChrNow.append(US.ChrName[name][0])
									US.ChrName[name][len(US.ChrName[name])-1].rfattrs(attrs)
							US.ChrName[name][len(US.ChrName[name])-1].rfattrs(attrs)
							Fo.write(US.ChrName[name][len(US.ChrName[name])-1].show())

					elif Flag=='bg':
						BgC.refresh(Content,Transition)
						Fo.write(BgC.show())

					elif Flag=='cg':
						CgC.refresh(Content,Transition,US,Fs)
						Fo.write(CgC.show(US,Fs))
					
					elif Flag=='test':
						Fs.error2('This flag does not exist or be supported in this Mode,ignoring... ')

					elif Flag=='view':
						if US.ChrName.get(Content)==None:
							Fs.error('This charecter does not exist !')
						else:
							US.ChrName['Saying']=Content
						if len(US.ChrName[Content])==4:
							Fo.write('    $ Bg_Ns='+US.ChrName[Content][2]+'N\n')
					elif Flag=='chc':
						if Transition=='Begin':
							NameC=Content.replace('：',':').split(':')
							for na in NameC:
								if na not in US.ChrName:
									Fs.error('This Character does not exist !')
							ChrTmp.append(NameC[0])
							Fo.write('    $ '+US.ChrName[NameC[0]][0]+"A=Character('"+NameC[0]+"',show_bg="+US.ChrName[NameC[1]][2]+"S,what_outlines=[(1,'"+US.ChrName[NameC[1]][1]+"')],who_bold=False,who_outlines=[ (2,'"+US.ChrName[NameC[1]][1]+"')])\n")
						elif Transition=='End':
							if Content not in ChrTmp:
								Fs.error('This Character did not be changed !')
							else:
								ChrTmp.remove(Content)
								Fo.write('    $ '+US.ChrName[Content][0]+"A=Character('"+Content+"',show_bg="+US.ChrName[NameC[1]][2]+"S,what_outlines=[(1,'""')],who_bold=False,who_outlines=[ (2,'"+US.ChrName[Content][1]+"')])\n")
						else:
							Fs.error('Wrong using this keyword !')
					else:
						Fo.write(Sp2Script(Flag,Transition,Content,US,Fs))
							

				elif Head=='words':
					if US.ChrName[Flag][0] in ChrNow:
						pass
					else:
						US.ChrName[Flag][len(US.ChrName[Flag])-1]=Chr(US,Fs,Flag)
						ChrNow.append(US.ChrName[Flag][0])
					US.ChrName[Flag][len(US.ChrName[Flag])-1].rftext(Content,Transition,Mode)
					Fo.write(US.ChrName[Flag][len(US.ChrName[Flag])-1].show())

				elif Head=='text':
					Fo.write('    '+Content)
			else:
				pass
			
	if os.path.exists(US.ScriptPath+'test.rpy'):
		os.remove(US.ScriptPath+'test.rpy')
		if os.path.exists(US.ScriptPath+'test.rpyc'):
			os.remove(US.ScriptPath+'test.rpyc')
	Fo=codecs.open(US.ScriptPath+'script.rpy','w','utf-8')
	Fo.write("label start:\n    $ date='10.09'\n    $ InitMyKey()\n")
	for f in sorted(ListFile):
		if len(f)==0:
			pass
		else:
			for Sc in ListFile[f]:
				Fo.write('    call '+Sc+'\n')

	Fo.close()

	FileList=open('Gal2Renpy/ListFile','w')
	pickle.dump(ListFile,FileList)
	FileList.close()

FileHash=open('Gal2Renpy/HashFile','w')
pickle.dump(HashFile,FileHash)
FileHash.close()






