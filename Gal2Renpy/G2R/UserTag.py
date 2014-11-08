#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import sys
from TagSource import *
from GetAllClass import *


#A class for storing user's tags
class UserTag():
	"""
	A class for storing all tags
	"""
	def __init__(self,US,TagSourcePath='../TagSource'):
		Tags={}
		Cls=GetAllClass(TagSourcePath,TagSource)
		for c in Cls:
			obj=c()
			Tags[obj.GetFlag()]=obj.Get(obj.GetFlag(),US)
		self.Tags=Tags