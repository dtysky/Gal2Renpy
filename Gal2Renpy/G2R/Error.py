#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

from ctypes import *
import codecs,locale
user32 = windll.LoadLibrary('user32.dll')
MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 


def SourceError(e,exit=True):
	MessageBox('Source error!\r\n'+e.encode(locale.getdefaultlocale()[1]))
	if exit:
		sys.exit(0)

def TagError(e,exit=True):
	MessageBox('Tag error!\r\n'+e.encode(locale.getdefaultlocale()[1]))
	if exit:
		sys.exit(0)