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
		path=Path+'User'
		def GetFileList():
			fps=[]
			for root,dirs,files in os.walk(US.TextPath):
    			for f in files:
    				fps.append(root+'/'+f)
    		return fps
		def ReadJson(FileName):
			return json.load(codecs.open(FileName,'r','utf-8'))
		tags={}
		for fp in fps:
			ji=ReadJson(fp)
			for flag in ji:
				if flag not in Args:
					Args[flag]={}
				for t in ji[flag]:
					if ji[flag][t]=='Tag':
						tag[flag]=ji[flag][t]
						del ji[flag][t]
				Args[flag].update(ji[flag])
		for flag in Args:
			if 'Common' in Args[flag]:
				for arg in Args[flag]:
					Args[flag][arg].append(Args[flag]['Common'])
				del Args[flag]['Common']
		for flag in tags:
			Args[flag]['Tag']=tags[flag]
		self.Args=Args
		
		#Keywords
		jtmp=json.load(codecs.open(path+'User/KeyWord.json','r','utf-8'))['KeyWord']
		self.KeyWord={}
		for k in jtmp:
			self.KeyWord[k]={'l':[]}
			for l in jtmp[k]:
				self.KeyWord[k]['l'].append(l[0])
				self.KeyWord[k][l[0]]=l[1:]


		self.Date='None'