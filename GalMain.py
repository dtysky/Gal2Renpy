#-*-coding:utf-8-*- 

from Gal2Renpy.Keyword import *
from Gal2Renpy.Fun import *
import numpy

BgmPath='./data/bgm/'

TestMode=True

Mode='A'
sout=None

Fs=MyFS()
Fs.open('Chapter-00.gal')
Fo=None

ChrNow=[]


#不允许空行

#人物信息识别时需要补全

#特效必须做成label!

#每次读文件之前先判断是否改动过！

if TestMode==True:
	Fo.open('./script/test.rpy')
	Fo.write('label test:')
	#循环读文件
		Begin=False
		while 1:
			[Head,Flag,Transition,Content]=RBlock(Fs)
			if Head=='end':
				break
			if (Head=='sp') & (Flag=='Begin'):
				if Begin==True:
					Fs.error('A file can only contains one test module !')
				else:
					Begin=True
			elif (Head=='sp') & (Flag=='End'):
				if Begin==False:
					Fs.error('Your test module does not been created !')
				else:
					Begin=False
				break
			elif Begin==True:
				if Head=='sp':
					
					if Flag=='mode':
						if Content=='None':
							sout='\thide window\n'
						elif Content=='Re':
							sout='\tshow window\n'
						elif Content=='ADV':
							Mode='A'
						elif Content=='NVL':
							Mode='N'
						else:
							Fs.error('This mode does not exist ！')

					if Flag=='ch':
						for ch in Content.splitlines():
							name=re.match(r'(\S+)s+(\S+)',ch).group(1)
							attrs=re.match(r'(\S+)s+(\S+)',ch).group(2)
							if ChrName.get(name)==None:
								Fs.error('This charecter does not exist !')
							else:
								if ChrName[name] in ChrNow:
									eval('Chr'+ChrName[name]+'.rfattrs(attrs,Fs)')
								else:
									eval('Chr'+ChrName[name]+'=Chr('+ChrName[name]+','+attrs+',Fs)')
									ChrNow.append(ChrName[name])
							Fo.write(eval('Chr'+ChrName[name]+'.show()'))

					elif Flag=='sc':
						pass

					else:
						Fo.write(Sp2Script(Flag,Transition,Content,Fs))

				elif Head=='words':
					eval('Chr'+ChrName[name]+'.rftext(Content,Transition,Mode)')
					Fo.write(eval('Chr'+ChrName[name]+'.show()'))

				elif Head=='text':
					Fo.write(Content)
			else:
				pass









else:
	pass



