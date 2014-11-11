#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import re
import sys
import os
from ctypes import *
import codecs
import hashlib
import locale
user32 = windll.LoadLibrary('user32.dll')
MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

class MyFS():

	def __init__(self):
		pass
	def Open(self,path,mode):
		self.path=path
		self.linepos=0
		self.end=False
		if mode=='r':
			if not os.path.exists(path):
				self.Error('The file '+path+' does not exist !')
		self.fs=codecs.open(path,mode,'utf-8')
	def ReadLine(self):
		self.linepos+=1
		tmp=self.fs.readline()
		if tmp=='':
			self.end=True
		return tmp.strip()
	def Error(self,e,exit=True):
		MessageBox(e.encode(locale.getdefaultlocale()[1])+'\r\n'+'Path : '+self.path.encode(locale.getdefaultlocale()[1])+'\r\n'+'Line : '+str(self.linepos))
		if exit:
			sys.exit(0)
	def IsEnd(self):
		return self.end
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
	def Write(self,s):
		self.fs.write(s)
		self.fs.flush()
	def Close(self):
		self.fs.close()