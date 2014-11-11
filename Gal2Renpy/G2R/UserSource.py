#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

import re
import sys
import os
import json
import codecs

#A class for storing user's source
class UserSource():
	def __init__(self,Path=''):
		Args={}
		Keywords=None
		path=Path+'User'
		def GetFileList():
			fps=[]
			for root,dirs,files in os.walk(Path):
				for f in files:
					fps.append(root+'/'+f)
			return fps
		def ReadJson(FileName):
			return json.load(codecs.open(FileName,'r','utf-8'))
		tags={}
		fps=GetFileList()
		for fp in fps:
			ji=ReadJson(fp)
			for flag in ji:
				if flag=='Keywords':
					Keywords=ji[flag]
					continue
				if flag not in Args:
					Args[flag]={}
				for t in ji[flag]:
					if t=='Tag':
						tags[flag]=ji[flag][t]
					elif t=='Common':
						if t not in Args[flag]:
							Args[flag][t]={}
						Args[flag][t].update(ji[flag][t])
					else:
						Args[flag].update(ji[flag])
				if 'Tag' in ji[flag]:
					del ji[flag]['Tag']
		for flag in Args:
			if 'Common' in Args[flag]:
				for arg in Args[flag]:
					Args[flag][arg].update(Args[flag]['Common'])
				del Args[flag]['Common']
		for flag in tags:
			Args[flag]['Tag']=tags[flag]
		self.Args=Args
		self.Keywords=Keywords