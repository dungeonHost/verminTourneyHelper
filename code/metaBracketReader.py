import numpy as np
import cv2
import glob,os
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from math import ceil
# from autoBracket import autoBracket
# import autoCrop
# import random
# from popupWindows import enterTourneySize
def readBracketMetaData(filename):
	cvFile=open(filename,"r+")
	points=[list(),list(),list(),list()]
	count=0
	teamSize=0
	numRounds=0
	numPartis=0
	tRP=[0,0,0]
	lastmatchIndex=0
	numPoints=0
	windex=[]
	for line in cvFile:
		line=line.replace('\n','')
		splitLine=line.split(',')
		try:
			if count==0:
				tRP[0]=int(splitLine[0])
				tRP[1]=int(splitLine[1])
				tRP[2]=int(splitLine[2])
				for i in range(tRP[1],0,-1):
					numPoints=tRP[2]**i
			elif count<=numPoints:
				coCount=1
				point=[0,0]
				for coord in splitLine:
					if coCount%2==0:
						coCount=0
						point[1]=int(coord)
						points[count-1].append(point)
						point=[0,0]
					else:
						point[0]=int(coord)
					coCount+=1
			else:
				print(line+" dddd")
				line.replace('\n','')
				lastmatchIndex=int(splitLine[0])
				print(splitLine)
				#windex=[int(x) for x in splitLine[1:len(splitLine)]]
				for x in splitLine[1:len(splitLine)]:
					try:
						windex.append(int(x))
					except ValueError:
						pass
				print(windex)
			count+=1
		except ValueError:
			print("VALUE ERROR")
			pass
	return points,tRP,lastmatchIndex,windex

def readBracket(filename,tRP):
	cvFile=open(filename,"r+")
	picFilenames=[list(),list(),list()]
	indexMatch=0
	lastWin=""
	[teamSize,numRounds,numPartis]=tRP
	i=0
	teamNames=list()
	for line in cvFile:
		if i<=(numPartis**numRounds)*teamSize:
			strArr=line.split(',')
			try:
				picFilenames[0].append(strArr[0])
				picFilenames[1].append(strArr[7])
				picFilenames[2].append(strArr[14])
				i+=1
			except IndexError:
				break
		else:
			teamNames.append(strArr[0])
	if indexMatch>=((numPartis**numRounds)*teamSize):
		indexMatch=0
	return picFilenames,teamNames

def openAndModifyImage(p):
	brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
	for points in p:
		for point in points:
			print(point)
			cv2.line(brack,(point[0],point[1]),(point[0]+10,point[1]+10),(255,0,255,255),50)
	cv2.imwrite("bracket.png",brack)
	
def readAllBrackets(metaFilename,brackFilename):
	points,tRP,index,windex=readBracketMetaData(metaFilename)
	picFilenames,teamNames=readBracket(brackFilename,tRP)
	return points,tRP,picFilenames,index,teamNames,windex

#points=readBracketMetaData("bracket3.csv")
#openAndModifyImage(points)