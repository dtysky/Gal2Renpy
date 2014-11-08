#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################

#A class for storing user's source
class UserTag():
	def __init__(self,TagSourcePath):
		Tags={}
		sys.path.add(TagSourcePath)
		
		self.Tags=Tags