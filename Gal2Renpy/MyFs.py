#coding:utf-8

#Copyright(c) 2014 dtysky

import re
import sys
import os
from ctypes import *
import codecs
import hashlib
user32 = windll.LoadLibrary('user32.dll')
MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

class MyFS():

	def __init__(self):
		pass
	def Open(self,path,mode):
		self.path=path
		self.linepos=0
		if not os.path.exists(path):
			self.Error('The file '+path+' does not exist !')
		self.fs=codecs.open(path,mode,'utf-8').read().splitlines()
	def FromText(self,s):
		self.linepos=0
		self.fs=s.splitlines()
	def ReadLine(self):
		self.linepos+=1
		return self.fs[self.linepos-1]
	def IsEnd(self):
		if self.linepos==len(self.fs):
			return True
		return False
	def Error(self,e,exit=True):
		MessageBox(e.encode(locale.getdefaultlocale()[1])+'\r\n'+'file : '+self.path.encode(locale.getdefaultlocale()[1])+'\r\n'+'line : '+str(self.linepos))
		if exit:
			sys.exit(0)
	def hash(self):
		md5obj=hashlib.md5()
		while 1:
			f=self.fs.read(8096)
			if not f:
				break
			else:
				md5obj.update(f.encode('utf-8'))
		hash=md5obj.hexdigest() 
		self.fs.seek(0)
		return hash
	def Close(self):
		self.fs.close()