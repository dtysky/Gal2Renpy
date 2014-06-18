#-*-coding:utf-8-*- 

import numpy
import re
import sys
import os
import codecs
from ctypes import *
from Gal2Renpy.Class import *
from Gal2Renpy.Fun import *
from Gal2Renpy.ChrOther import *

TestMode=True
Begin=None

Mode='A'
sout=None

Fs=MyFS()
Fs.open('Chapter-00.gal')

ChrNow=[]

#特效必须做成label!

#每次读文件之前先判断是否改动过！

if TestMode==True:
	if os.path.exists('../script/script.rpy'):
		os.rename('../script/script.rpy','../script/script.rpyx')
		if os.path.exists('../script/script.rpyc'):
			os.rename('../script/script.rpyc','../script/script.rpycx')
	Fo=codecs.open('../script/test.rpy','w')
	Fo.write('label start:\n')
	#循环读文件
	for i in range(1):
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
					else:
						Begin=False
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
									ChrName[name][1]=Chr(ChrName[name][0],attrs,Fs)
									ChrNow.append(ChrName[name][0])
									ChrName[name][1].rfattrs(attrs,Fs)
							Fo.write(ChrName[name][1].show())

					elif Flag=='sc':
						pass

					else:
						Fo.write(Sp2Script(Flag,Transition,Content,Fs))

				elif Head=='words':
					if Flag[0] in ChrNow:
						pass
					else:
						Flag[1]=Chr(Flag[0])
						ChrNow.append(Flag[0])
					Flag[1].rftext(Content,Transition,Mode)
					Fo.write(Flag[1].show())

				elif Head=='text':
					if Mode=='A':
						Fo.write('    '+Content)
					else:
						Fo.write('    s '+"'"+Content+"'")

				else:
					pass
			else:
				pass
	Fo.close()


else:
	#循环读文件
		while 1:
			
			[Head,Flag,Transition,Content]=RBlock(Fs)
			if Head=='end':
				Fo.write('    return')
				Fs.close()
				Fo.close()
				break

			if Head=='sp':
				
				if Flag=='sc':
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
									ChrName[name][1]=Chr(ChrName[name][0],attrs,Fs)
									ChrNow.append(ChrName[name][0])
									ChrName[name][1].rfattrs(attrs,Fs)
							Fo.write(ChrName[name][1].show())

				else:
					Fo.write(Sp2Script(Flag,Transition,Content,Fs))

			elif Head=='words':
				if Flag[0] in ChrNow:
					pass
				else:
					Flag[1]=Chr(Flag[0])
					ChrNow.append(Flag[0])
				Flag[1].rftext(Content,Transition,Mode)
				Fo.write(Flag[1].show())

			elif Head=='text':
				Fo.write('    '+Content)
		else:
			pass




