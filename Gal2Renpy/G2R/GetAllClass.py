#coding:utf-8
#################################
#Copyright(c) 2014 dtysky
#################################
import sys

#A function for getting all class from a dir depend on path
def GetAllClass(Path,ParentClass):
	"""
	Return a list contents all class
	"""
	def IsMyDefine(d):
		if len(d)>1:
				if d[0:1]=='__':
					return False
		return True
	def IsSubOfTag(d):
		return issubclass(d,ParentClass)
	sys.path.add(Path)
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
			if not IsMyDefine(d):
				continue
			d=getattr(m,d)
			if not IsSubOfTag(d):
				continue
			Cls.append(d)
	return Cls