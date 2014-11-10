#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import sys
from DefineSyntax import *
from GetAllClass import *

#A function for storing user's tags
def DefineCreat(US,FS,DictHash,DefineSyntaxPath='../DefineSyntax'):
	"""
	Creat all definitions
	"""
	Cls=GetAllClass(DefineSyntaxPath,DefineSyntax)
	for c in Cls:
		obj=c()
		DictHash=obj.Creat(obj.GetFlag(),US,FS,DictHash)
	return DictHash