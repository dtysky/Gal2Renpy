#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
from SpSyntax import *
from GetAllClass import *

#A function for storing user's tags
def SpCreat(SpSyntaxPath='../SpSyntax'):
	"""
	Return a dict which content all script-creater objects 
	"""
	Cls=GetAllClass(SpSyntaxPath,SpSyntax)
	Objs={}
	for c in Cls:
		obj=c()
		Objs[obj.GetFlag()]=obj
	return Objs