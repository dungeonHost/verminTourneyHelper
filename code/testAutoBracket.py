import glob
import os
import PIL
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *

def ImprovedSplit(string):
	bracket=0
	dash=0
	stringList=list()
	splitString=''
	if(string[0]=='['):
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
			if dash==0:
				splitString+=str(char)
			if char=='\\' and dash==0:
				dash+=1
			else:
				dash=0
	stringList.append(splitString)
	return stringList

def StringtoDict(string):
	dictionary=dict()
	dictStrings=splitString=string.split('|')
	for dictString in dictStrings:
		key_values=dictString.split(":")
		try:
			if(len(key_values)>2):
				for value in key_values[2:]:
					key_values[1]+=":"+value
			splitStringList=ImprovedSplit(key_values[1])
			dictionary[key_values[0]]=list()
			RecerseToGetValues(splitStringList,dictionary[key_values[0]])
			if len(dictionary[key_values[0]])==1:
				dictionary[key_values[0]]=dictionary[key_values[0]][0]
		except(IndexError):
			break
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

def dictToString(dictionary,newLine):
	string=""#str(dictionary)
	for key,value in dictionary.items():
		string+=str(key)+":"+str(value)
		if newLine:
			string+='\n'
		else:
			string+='|'
	string=string.replace('{','')
	string=string.replace('}','')
	string=string.replace('\'','')
	string=string.replace(' ','')
	return string
os.chdir('..')
os.chdir('bracket')
fp=open("bracket.csv","r+")
csvDictList=list()
for line in fp:
	csvDictList.append(StringtoDict(line))
print(csvDictList)
os.chdir('..')

ab=autoBracket(2,2,2,csvDictList)
pointDictionary=ab.createBracket()
svFile=open("bracketMetaData.csv","w+")
svFile.write("2,2,2,1_0\n")

pointString=dictToString(pointDictionary,True)
svFile.write(pointString)

print("THIS STILL WORKING?")


