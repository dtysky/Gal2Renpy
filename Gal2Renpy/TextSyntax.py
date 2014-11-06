#coding:utf-8

#Copyright(c) 2014 dtysky

import re
import sys
import os
import json
import locale
from ctypes import *
import codecs
from Keyword import *
import hashlib

#The text-syntax super class
class TextSyntax():
	#One or two arguments 
	def __init__(self):
		self.attrs={}
	def SetAttrs(self,attrs1,attrs2):
		attrs1=re.findall(r'[a-z]+:.*',attrs1)
		pass
	#Refresh attributes in this charecter
	def rfattrs(self,Attrs):
		for attr in Attrs.replace('，',',').split(','):
			ttmp=attr.replace('：',':').split(':')
			if ttmp[0] not in self.us.ChrKeyword==None:
				self.fs.error("This charecter's attribute does not exist !")
			else:
				if (ttmp[0]=='c') | (ttmp[0]=='p') | (ttmp[0]=='f'):

					if self.us.ChrKeyword[ttmp[0]][self.orgname].get(ttmp[1])==None:
						self.fs.error("This ChrAttribute "+str(self.name+' '+ttmp[0])+" does not exist !")
					else:
						self.attrs[ttmp[0]]=self.us.ChrKeyword[ttmp[0]][self.orgname][ttmp[1]]
				else:

					if self.us.ChrKeyword[ttmp[0]].get(ttmp[1])==None:
						self.fs.error("This ChrAttribute "+str(self.name+' '+ttmp[0])+" does not exist !")
					else:
						self.attrs[ttmp[0]]=self.us.ChrKeyword[ttmp[0]][ttmp[1]]

			self.attrs['new']=True
	#Refresh next word by this charecter
	def rftext(self,Text,Style,Mode):
		self.say['Text']=Text
		self.say['Style']=Style
		self.say['Mode']=Mode
		self.say['new']=True
	#Check whether the attributes completely
	def checkattrs(self):
		if self.attrs['new']:
			if self.complete==False:
				for attr in self.attrs:
					if self.attrs[attr]==None:
						self.fs.error("This charecter's attributes are not complete !")
	#A interface
	def getattrs(self):
		rn=self.attrs
		rn.update({'name':self.name})
		return rn

	#Creat scripts which are related to charecters
	def show(self):
		rn=''
		if self.attrs['new']:
			self.complete==True
			if self.attrs['t']=='hide':
				self.attrs['t']='dissolve'
				rn='    hide '+self.name+'\n'#+' '+self.attrs['c']+self.attrs['p']+self.attrs['f']+self.attrs['d']+'\n'
			else:
				rn+='    show '+self.name+' '+self.attrs['p']+self.attrs['c']+self.attrs['f']+self.attrs['d']+' '
				rn+='at '+self.attrs['l']+'\n'
				rn+='    with '+self.attrs['t']+'\n'
			self.attrs['new']=False
			self.attrs['t']=self.tDefault
			return rn
		elif self.say['new']:
			rn+=self.name+self.say['Mode']+' '
			if self.say['Style']=='Say':
				rn+="'"+self.say['Text']+"'\n"
			else:
				rn+="'（"+self.say['Text']+"）'\n"
			self.say['new']=False
			return '    '+rn
		else:
			self.fs.error('This charecter does not be created !')