import glob
import os
import PIL
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *

def dictToStrings(dictionary):
	string=""#str(dictionary)
	for key,value in dictionary.items():
		string+=str(key)+":"+str(value)+"\n"
	string=string.replace('{','')
	string=string.replace('}','')
	string=string.replace('\'','')
	string=string.replace(' ','')
	return string

def StringtoDict(string):
	dictionary=dict()
	dictStrings=splitString=string.split('\n')
	for dictString in dictStrings:
		key_values=dictString.split(":")
		splitStringList=ImprovedSplit(key_values[1])
		dictionary[key_values[0]]=list()
		RecerseToGetValues(splitStringList,dictionary[key_values[0]])
	return dictionary
			
def RecerseToGetValues(values,dictionaryList):
	for value in values:
		if value.find('[')!=-1 and value.find(']')!=-1:
			splitValues=ImprovedSplit(value)
			dictionaryList.append(list())
			RecerseToGetValues(splitValues,dictionaryList[-1])
		else:
			try:
				dictionaryList.append(int(value))
			except(ValueError):
				if(value!=''):
					dictionaryList.append(value)

def ImprovedSplit(string):
	bracket=0
	stringList=list()
	splitString=''
	string=string[1:-1]
	for char in string:
		if char==',' and bracket==0:
			stringList.append(splitString)
			splitString=''
		else:
			if char=='[':
				bracket+=1
			elif char==']':
				bracket-=1
			splitString+=str(char)
	stringList.append(splitString)
	return stringList

class fuck:
	#arrayTest=[]
	def __init__(self,whatever):
		self.arrayTest=[None]*10
		for i in range(0,10):
			self.arrayTest[i]=whatever
	
	def printArray(self):
		print(self.arrayTest)

dictionary={'top':list(),'bottom':list()}
numbers=["zero","one","two","three","four","five","six","seven","eight","nine","ten"]
topList=dictionary['top']
topList.append("HI")
topList.append("BYE")
listList=list()
for i in range(0,10):
	dictionary[numbers[i]]=list()
	listList.append(list())
dictionary['NONO']=["hi",[1,2],"WHAT",9,list()]
dictionary['zero'].append([0,1])
dictionary['zero'].append([2,3])
dictionary['zero'].append(["HI FUCKER",[1,2],"pop",.9999,list()])
dictionary['NONO'][4].append("HELLO")
dictionary['NONO'][4].append("GGOOFS")
dictionary['NONO']+=[8]
listList[0].append([0,1])
print(dictionary)
string=dictToStrings(dictionary)
dictionary=StringtoDict(string[0:-1])
print(dictionary)

fuc=fuck(10)
fuc.printArray()