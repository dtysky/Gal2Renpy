#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

"""

Wait for rewriting...
Don't care it now...

"""






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
CgC=Cg(US,Fs)
HPCC=HPC(US,Fs)
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
	if US.HPCSystem:
		Fo.write('    $ HPCMessInit()\n')
	for path in FileNow:
		Fs.open(path,'r')
		ListFile[f]=[]

	Fo.close()


else:

			
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






