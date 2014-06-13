#-*-coding:utf-8-*- 

from Gal2Renpy.Keyword import *
from Gal2Renpy.Fun import *
import numpy

BgmPath='./data/bgm/'

TestMode=True

Mode='ADV'
sout=None

ChrState=[n,e,f,c,p,l]=['','','','','','']

Fs=MyFS()
Fs.open('Chapter-00.gal')
Fo=None


#不允许空行

#人物信息识别时需要补全

#特效必须做成label!

#每次读文件之前先判断是否改动过！

if TestMode==True:
	Fo.open('./script/test.rpy')
	#循环读文件
		Begin=False
		while 1:
			[Head,Flag,Transition,Content]=RBlock(Fs)
			if (Head=='sp') & (Flag=='Begin'):
				Begin=True
			elif (Head=='sp') & (Flag=='End'):
				Begin=False
				break
			else:
				if Begin==True:
					if Head=='sp':
						if Flag=='ch':
							

						Fo.write(Sp2Script(Flag,Transition,Content,Mode,FS))





[head,flag,transition,content]=fs.reanline()

else:

	if head=='sp':

		if flag=='mode':
			if content=='None':
				sout='\thide window\n'
			elif content=='Re':
				sout='\tshow window\n'
			elif content=='ADV':
				Mode='A'
			elif content=='NVL':
				Mode='N'
			else:
				Fs.error('This mode does not exist ！')

		elif flag==


