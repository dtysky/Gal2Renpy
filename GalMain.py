#Writing to future me:
#You have only two chioces: rewriting, or closing

#-*-coding:utf-8-*- 


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

#特效必须做成label!
US=User()
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

#Only a file had been changed will process it
for root,dirs,files in os.walk(US.TextPath):
    for f in files:
        if os.path.splitext(f)[1]!='.gal':
        	pass
        else:
        	FileAll.append(root+'/'+f)

#Add files which will be processed
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
	Fo.write('label start:\n')
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
					
					if Flag=='mode':
						if Content=='Hide':
							Fo.write('    hide window\n')
						elif Content=='Re':
							Fo.write('    show window\n')
						elif Content=='ADV':
							Mode='A'
						elif Content=='NVL':
							Mode='N'
						else:
							Fs.error('This mode does not exist ！')

					elif Flag=='ch':
						for ch in Content.splitlines():
							name=re.match(r'(\S+)s+(\S+)',ch).group(1)
							attrs=re.match(r'(\S+)s+(\S+)',ch).group(2)
							if US.ChrName.get(name)==None:
								Fs.error('This charecter does not exist !')
							else:
								if US.ChrName[name][0] in ChrNow:
									pass
								else:
									US.ChrName[name][2]=Chr(US.ChrName[name][0],name,attrs,Fs)
									ChrNow.append(US.ChrName[name][0])
									US.ChrName[name][2].rfattrs(attrs,US,Fs)
							Fo.write(US.ChrName[name][2].show())

					elif Flag=='sc':
						pass

					else:
						Fo.write(Sp2Script(Flag,Transition,Content,US,Fs))

				elif Head=='words':
					if US.ChrName[Flag][0] in ChrNow:
						pass
					else:
						US.ChrName[Flag][2]=Chr(US.ChrName[Flag][0],Flag)
						ChrNow.append(US.ChrName[Flag][0])
					US.ChrName[Flag][2].rftext(Content,Transition,Mode)
					Fo.write(US.ChrName[Flag][2].show())

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

					if Flag=='mode':
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
								name=re.match(r'(\S+)s+(\S+)',ch).group(1)
								attrs=re.match(r'(\S+)s+(\S+)',ch).group(2)
								if US.ChrName.get(name)==None:
									Fs.error('This charecter does not exist !')
								else:
									if US.ChrName[name][0] in ChrNow:
										pass
									else:
										US.ChrName[name][2]=Chr(US.ChrName[name][0],name,attrs,Fs)
										ChrNow.append(US.ChrName[name][0])
										US.ChrName[name][2].rfattrs(attrs,US,Fs)
								Fo.write(US.ChrName[name][2].show())

					else:
						Fo.write(Sp2Script(Flag,Transition,Content,US,Fs))

				elif Head=='words':
					if US.ChrName[Flag][0] in ChrNow:
						pass
					else:
						US.ChrName[Flag][2]=Chr(US.ChrName[Flag][0],Flag)
						ChrNow.append(US.ChrName[Flag][0])
					US.ChrName[Flag][2].rftext(Content,Transition,Mode)
					Fo.write(US.ChrName[Flag][2].show())

				elif Head=='text':
					Fo.write('    '+Content)
			else:
				pass
			
	if os.path.exists(US.ScriptPath+'test.rpy'):
		os.remove(US.ScriptPath+'test.rpy')
		if os.path.exists(US.ScriptPath+'test.rpyc'):
			os.remove(US.ScriptPath+'test.rpyc')
	Fo=codecs.open(US.ScriptPath+'script.rpy','w','utf-8')
	Fo.write('label start:\n')
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






