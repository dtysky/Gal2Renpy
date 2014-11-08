#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import sys
import G2R

#A class for storing user's tags
class UserTag():
	def __init__(self,TagSourcePath=''):
		def IsMyDefine(d):
			if len(d)>1:
					if d[0:1]=='__':
						return False
			return True
		def IsSubOfTag(d):
			return issubclass(d,G2R.TagSource)
		path=TagSourcePath+'/TagSource'
		Tags={}
		sys.path.add(TagSourcePath)
		Mds=[]
		Cls=[]
		#Import all modules from TagSorce dir
		for root,dirs,files in os.walk(TagSourcePath):
			for f in files:
				n,e=os.path.splitext(f)
				if e=='.py':
					Mds.append(__import__(n))
		#Get all classes which are children of TagSource
		for m in Mds:
			for d in dir(m):
				if not IsMyDefine(d):
					continue
				d=getattr(m,d)
				if not IsSubOfTag(d):
					continue
				Mds.append(d)
		for c in Cls:
			

		self.Tags=Tags