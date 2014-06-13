MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

class MyFS():

	def __init__(self):
		pass
	def open(self,path):
		self.fs=codecs.open(path,'r','utf-8')
		self.path=path
		self.linepos=0
	def readline(self):
		self.linepos+=1
		return self.fs.readline()
	def error(self,e):
		MessageBox(e+'\n'+'file : '+self.path+'\n'+'line : '+str(self.linepos))
		sys.exit(0)


#A class for charecter
class Chr():
	#One or two arguments 
	def __init__(self,*Text):
		if len(Text)==1:
			self.name=Name
			#'new' will be true if the attributes has been changed
			self.attrs={'e':None,'f':None,'c':None,'p':None,'l':None,'new':False}
		elif len(Text)==2:
			self.name=Text[0]
			self.attrs={'e':None,'f':None,'c':None,'p':None,'l':None,'new':False}
			self.rfattrs(Text[1],Fs)
		#Text,Say or Think,Mode,Is refreshed
		self.say={'Text':None,'Style':None,'Mode':None,'new':False}
	#Refresh attributes in this charecter
	def rfattrs(self,Attrs,Fs):
		for attr in Attrs.replace('，',',').split(','):
			ttmp=attr.replace('：',':')split(':')
			if ChrKeyword.get(ttmp[0])==None:
				Fs.error("This charecter's attribute does not exist !")
			else:
				if eval(ChrKeyword[ttmp[0]]+'get('+ttmp[1]+')')==None:
					Fs.error("This "+ChrKeyword[ttmp[0]]+" does not exist !")
				else:
					eval('self.attrs(ttmp[0])='ChrKeyword[ttmp[0]]+'['ttmp[1]+']')
			self.attrs['new']=True
	#Refresh next word by this charecter
	def rftext(self,Text,Style,Mode):
		self.say['Text']=Text
		self.say['Style']=Style
		self.say['Mode']=Mode
	#Creat scripts which are related to charecters
	def show():
		rn=''
		if self.attrs['new']:
			rn+='\tshow '+self.name+self.attrs['c']+self.attrs['p']+self.attrs['f']
			rn+=' at '+self.attrs['l']+'\n'
			rn+='\twith '+self.attrs['e']+'\n'
			self.attrs['new']=False
			return rn
		elif self.say['new']:
			rn+=self.name+self['Mode']+' '
			if self.say['Style']=='Say':
				rn+="'（"+self.say['Text']+"）'"+'\n'
			else:
				rn+="'"+self.say['Text']+"'"+'\n'
			self.say['new']=False
			return rn
		else:
			MessageBox('This charecter does not be created !')
			sys.exit(0)




