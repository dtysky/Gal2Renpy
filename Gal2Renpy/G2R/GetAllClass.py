#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import sys,os

#A function for getting all class from a dir depend on path
def GetAllClass(Path,ParentClass):
	"""
	Return a list contents all class
	"""
	def IsClass(d):
		return type(d)==type(ParentClass)
	def IsSubOfTag(d):
		return issubclass(d,ParentClass)
	sys.path.append(Path)
	Mds=[]
	Cls=[]
	#Import all modules from TagSorce dir
	for root,dirs,files in os.walk(Path):
		for f in files:
			n,e=os.path.splitext(f)
			if e=='.py':
				Mds.append(__import__(n))
	#Get all classes which are children of Path
	for m in Mds:
		for d in dir(m):
			d=getattr(m,d)
			if not IsClass(d):
				continue
			if not IsSubOfTag(d):
				continue
			Cls.append(d)
	return Cls