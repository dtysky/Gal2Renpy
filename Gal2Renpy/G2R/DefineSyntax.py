#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
from DHash import *

#The define-creat-syntax super class
class DefineSyntax():
	"""
	Creat definitions for ren'py script from user's source
	"""
	def __init__(self):
		pass
	def GetFlag(self):
		s=self.__class__.__name__.replace('Define','')
		tmp=''
		for _s_ in s:
			tmp+=_s_ if _s_.islower() else '_'+_s_.lower()
		return tmp[1:]
	def Creat(self,Flag,US,FS,DictHash):
		if Flag not in DictHash:
			DictHash[Flag]=0
		return DictHash