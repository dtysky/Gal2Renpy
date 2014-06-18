#-*-coding:utf-8-*- 

import re
import sys
import os
import codecs
import pickle
from ctypes import *
from Gal2Renpy.Class import *
from Gal2Renpy.Fun import *
from Gal2Renpy.ChrOther import *
from Gal2Renpy.User import *

Begin=None

Mode='A'

Fs=MyFS()

ChrNow=[]
FileNow=[]

#特效必须做成label!

CreatDefine()

FileHash=open('Gal2Renpy/HashFile','r')
HashFile=pickle.load(FileHash)
FileHash.close()

#Only a file had been changed will process it
for root,dirs,files in os.walk(TextPath):
    for f in files:
        if os.path.splitext(f)[1]!='.gal':
        	pass
        else:
        	if HashFile.get(root+'/'+f)==None:
        		Fs.open(root+'/'+f)
        		HashFile[root+'/'+f]=Fs.hash()
        		Fs.close()
        		FileNow.append(root+'/'+f)
        	else:
        		Fs.open(root+'/'+f)
        		if Fs.hash()==HashFile[root+'/'+f]:
        			pass
        		else:
        			HashFile[root+'/'+f]=Fs.hash()
        			FileNow.append(root+'/'+f)
        			Fs.close()
FileHash=open('Gal2Renpy/HashFile','w')
pickle.dump(HashFile,FileHash)
FileHash.close()


if TestMode==True:
	if os.path.exists('../script/script.rpy'):
		os.remove('../script/script.rpy')
		if os.path.exists('../script/script.rpyc'):
			os.remove('../script/script.rpyc')
	Fo=codecs.open('../script/test.rpy','w')
	Fo.write('label start:\n')
	for path in FileNow:
		Fs.open(path)
		Begin=False
		while 1:
			[Head,Flag,Transition,Content]=RBlock(Fs)
			if Head=='end':
				Fo.flush()
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
			elif Begin==True:
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
							if ChrName.get(name)==None:
								Fs.error('This charecter does not exist !')
							else:
								if ChrName[name][0] in ChrNow:
									pass
								else:
									ChrName[name][2]=Chr(ChrName[name][0],name,attrs,Fs)
									ChrNow.append(ChrName[name][0])
									ChrName[name][2].rfattrs(attrs,Fs)
							Fo.write(ChrName[name][2].show())

					elif Flag=='sc':
						pass

					else:
						Fo.write(Sp2Script(Flag,Transition,Content,Fs))

				elif Head=='words':
					if ChrName[Flag][0] in ChrNow:
						pass
					else:
						ChrName[Flag][2]=Chr(ChrName[Flag][0],Flag)
						ChrNow.append(ChrName[Flag][0])
					ChrName[Flag][2].rftext(Content,Transition,Mode)
					Fo.write(ChrName[Flag][2].show())

				elif Head=='text':
					Fo.write('    '+Content)

				else:
					pass
			else:
				pass
	Fo.close()


else:
	FileList=open('Gal2Renpy/ListFile','r')
	ListFile=pickle.load(FileList)
	FileList.close()
	for path in FileNow:
		Fs.open(path)

		while 1:
			[Head,Flag,Transition,Content]=RBlock(Fs)
			if Head=='end':
				Fo.write('    return')
				Fs.close()
				Fo.flush()
				Fo.close()
				break

			if Head=='sp':
				
				if Flag=='sc':
					if Content in ListFile:
						pass
					else:
						ListFile.append(Content)
					Fo.open('./script/text/'+Content+'.rpy','r')
					Fo.write('label '+Content+' :\n')

				elif Flag=='mode':
					if Content=='None':
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
							if ChrName.get(name)==None:
								Fs.error('This charecter does not exist !')
							else:
								if ChrName[name][0] in ChrNow:
									pass
								else:
									ChrName[name][2]=Chr(ChrName[name][0],name,attrs,Fs)
									ChrNow.append(ChrName[name][0])
									ChrName[name][2].rfattrs(attrs,Fs)
							Fo.write(ChrName[name][2].show())

				else:
					Fo.write(Sp2Script(Flag,Transition,Content,Fs))

			elif Head=='words':
				if ChrName[Flag][0] in ChrNow:
					pass
				else:
					ChrName[Flag][2]=Chr(ChrName[Flag][0],Flag)
					ChrNow.append(ChrName[Flag][0])
				ChrName[Flag][2].rftext(Content,Transition,Mode)
				Fo.write(ChrName[Flag][2].show())

			elif Head=='text':
				Fo.write('    '+Content)
		else:
			pass
	if os.path.exists('../script/test.rpy'):
		os.remove('../script/test.rpy')
	Fo=codecs.open('../script/script.rpy','w')
	Fo.write('label start:\n')
	for File in ListFile:
		Fo.write('    call '+File+'\n')
	Fo.close()
	FileList=open('Gal2Renpy/ListFile','w')
	pickle.dump(ListFile,FileList)
	FileList.close()






