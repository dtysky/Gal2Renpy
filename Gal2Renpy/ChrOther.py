#-*-coding:utf-8-*- 
from Class import *
from Effect import *
from ChrFace import *

#Chareter Name
#Set the key 'new' value to 'True' if you change this dict !
#Add an 'u' in front of key or value if you use Chinese !
ChrName={
	'new': False ,
	"Saying": None ,
	u"寒苍": ["Dream","#000000",None] ,
	u"晗樱": ["Soul","#000000",None] ,
	u"苓苏": ["Flower","#000000",None] ,
	u"雏末": ["Moon","#000000",None] ,
	u"弗莱士": ["Star","#000000",None] ,
	u"暮": ["Logos","#000000",None] ,
	u"晓": ["Poem","#000000",None] ,
	u"散夜": ["Existent","#000000",None] ,
	u"无名": ["Void","#000001",None] ,
}


#Chareter Clothes
#You must give them a default value at least !
#Set the key 'new' value to 'True' if you change this dict !
#Add an 'u' in front of key or value if you use Chinese !
ChrClothes={
	'new': False ,
	#寒苍
	u'寒苍': {
		u'校服': 'A',
		u'私服': 'B'
	},
}


#Chareter Pose
#You must give them a default value at least !
#Set the key 'new' value to 'True' if you change this dict !
#Add an 'u' in front of key or value if you use Chinese !
ChrPose={
	'new': False ,
	#寒苍
	u'寒苍': {
		u'普通': 'A',
		u'叉腰': 'B'
	},
}

#Chareter Center Position
#Add an 'u' in front of key or value if you use Chinese !
ChrPosition={
	#Size A
	"A1": "Grid(1,7)" ,

	#Size B
	"B1": "Grid(1,5)" ,

	#Size C
	"C1": "Grid(1,2)"
}


#Chareter keywords, don't change !
ChrKeyword={
	"t": Trans,
	"f": ChrFace,
	"c": ChrClothes,
	"p": ChrPose,
	"l": ChrPosition

}
