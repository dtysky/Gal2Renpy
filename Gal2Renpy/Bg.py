#-*-coding:utf-8-*- 

#Main Scence
#Set the key 'new' value to 'True' if you change this dict !
#Add an 'u' in front of key or value if you use Chinese !
BgMain={
	'new': False ,
	u"白": 'White',
	u"家": "Home" ,
}


#Sub Scence
#You must give them a default value at least !
#Set the key 'new' value to 'True' if you change this dict !
#Add an 'u' in front of key or value if you use Chinese !
BgSub={
	'new': False ,
	#家
	u'家':{
		u"房间": "01" ,
		u"大厅": '02' ,
	},

	#白
	u'白':{
		'default': '01',
	}
}

#Weather
#You must give them a default value at least !
#Set the key 'new' value to 'True' if you change this dict !#Set the key 'new' value to 'True' if you change this dict !#Set the key 'new' value to 'True' if you change this dict !#Set the key 'new' value to 'True' if you change this dict !
#Add an 'u' in front of key or value if you use Chinese !
BgWeather={
	'new': False ,
	#家
	u'家':{
		u"晴": "A" ,
	},

	#白
	u'白':{
		'default': 'A',
	}
}