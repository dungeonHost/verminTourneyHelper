import glob
import os
import PIL
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *

class csvToDicts(object):

	def ReadBracketCSV(self,fileName):
		fp=open(fileName,"r+")
		csvDictList=list()
		for line in fp:
			csvDictList.append(self.StringtoDict(line,'|'))
		return csvDictList
	
	def ReadMetaBracketCSV(self,fileName):
		fp=open(fileName,"r+")
		csvDict=dict()
		csvString=''
		firstSplit=fp.readline().split(',')
		rounds=int(firstSplit[0])
		partis=int(firstSplit[1])
		teamSize=int(firstSplit[2])
		currentBout=firstSplit[3].replace('\n','')
		for line in fp:
			csvString+=line
		print(csvString)
		csvDict=self.StringtoDict(csvString,'\n')
		return rounds,partis,teamSize,currentBout,csvDict

	def ImprovedSplit(self,string):
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

	def StringtoDict(self,string,splitChar):
		dictionary=dict()
		dictStrings=splitString=string.split(splitChar)
		for dictString in dictStrings:
			key_values=dictString.split(":")
			try:
				if(len(key_values)>2):
					for value in key_values[2:]:
						key_values[1]+=":"+value
				splitStringList=self.ImprovedSplit(key_values[1])
				dictionary[key_values[0]]=list()
				self.RecerseToGetValues(splitStringList,dictionary[key_values[0]])
				if len(dictionary[key_values[0]])==1:
					dictionary[key_values[0]]=dictionary[key_values[0]][0]
			except(IndexError):
				break
		return dictionary
		
	def RecerseToGetValues(self,values,dictionaryList):
		for value in values:
			if value.find('[')!=-1 and value.find(']')!=-1:
				splitValues=self.ImprovedSplit(value)
				dictionaryList.append(list())
				self.RecerseToGetValues(splitValues,dictionaryList[-1])
			else:
				try:
					if value.find('_')>=1:
						dictionaryList.append(value)
					else:
						dictionaryList.append(int(value))
				except(ValueError):
					if(value!=''):
						dictionaryList.append(value)