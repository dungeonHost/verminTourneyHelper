import glob,os
import tkinter as tk
import numpy as np
import cv2
from tkinter import *
import PIL
from math import ceil
from csvToDicts import *
from popupWindows import *

def setTeamNames():
	root=tk.Tk()
	os.chdir("../bracket")
	#cvFile=open("bracket.csv","r+")
	#metaFile=open("bracketMetaData.csv","a")
	picList=list()
	csvDictConverter=csvToDicts()
	numRounds,numPartis,teamSize,currentBout,pointDict=csvDictConverter.ReadMetaBracketCSV("bracketMetaData.csv")
	verminDictList=csvDictConverter.ReadBracketCSV("bracket.csv")
	brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
	font = 0
	teamNames=""
	index=0
	print(pointDict.items())
	print(pointDict['FINAL_0'])
	print(pointDict['0_0'])
	for pointIndex in pointDict:
		pointList=pointDict[pointIndex]
		print(pointIndex)
		print(pointList)
		if len(pointList[-1])>0:
			for vermIndex in pointList[-1]:
				image1=PIL.Image.open(verminDictList[vermIndex]['stage1'][0])
				image1=image1.resize((60,60))
				picList.append(PIL.ImageTk.PhotoImage(image1))
				image1=PIL.Image.open(verminDictList[vermIndex]['stage2'][0])
				image1=image1.resize((60,60))
				picList.append(PIL.ImageTk.PhotoImage(image1))
				image1=PIL.Image.open(verminDictList[vermIndex]['stage3'][0])
				image1=image1.resize((60,60))
				picList.append(PIL.ImageTk.PhotoImage(image1))
			etn=enterTeamName(root,picList)
			root.wait_window(etn.top)
			for vermIndex in pointList[-1]:
				verminDictList[vermIndex]['teamName']=etn.teamName.replace(" ","_")
			picList=list()
			teamNameSplit,numEndLines,teamNameLen=splitUpName(etn.teamName)
			print("TEAM NAME SPLIT="+str(teamNameSplit)+" "+"PLEN="+str(teamNameLen))
			
			offset,rotation=calculateOffset(teamNameLen,numEndLines,pointIndex,numPartis,numRounds)
			textLayer=createTextLayer(teamNameSplit,numEndLines,teamNameLen,rotation,font)
			point=pointList[0]
			try:
				(textH,textW)=textLayer.shape[:2]
				(brackH,brackW)=brack.shape[:2]
				textPoint=point[:]
				#left,down = [-,+]
				textPoint[0]+=offset[0]
				textPoint[1]+=offset[1]
				if textW>brackW-textPoint[0] or textH>brackH-textPoint[1] or textPoint[0]<0 or textPoint[1]<0:
					print("RESIZE")
					background=np.zeros((int(brackH*2),int(brackW*2),4),dtype=np.uint8)
					background.fill(255)
					background[int(brackH/2):brackH+int(brackH/2),int(brackW/2):brackW+int(brackW/2)]=brack
					brack=background
					cv2.imshow("hi",brack)
					cv2.waitKey(0)
					textPoint[0]+=int(brackW/2)
					textPoint[1]+=int(brackH/2)
					for changeIndex in pointDict:
						changePoint=changeIndex[0]
						changePoint[0]+=int(brackW/2)
						changePoint[1]+=int(brackH/2)
				(textH,textW)=textLayer.shape[:2]
				brack[textPoint[1]:textPoint[1]+textH,textPoint[0]:textPoint[0]+textW]+=textLayer
			except IndexError:
				pass
	for i in range(0,2):
		print(i)
	csvFile=open("bracket.csv","w+")
	metaFile=open("bracketMetaData.csv","w+")
	for vermDict in verminDictList:
		csvFile.write(dictToString(vermDict,False))
		csvFile.write("\n")
	csvFile.close()
	metaFile.write(str(numRounds)+","+str(numPartis)+","+str(teamSize)+","+currentBout+"\n")
	pointString=dictToString(pointDict,True)
	metaFile.write(pointString)
	
	cv2.imwrite("bracket.png",brack)

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

def calculateOffset(nameLength,numberNewLines,pointIndex,numPartis,numRounds):
	splitBout=pointIndex.split("_")
	boutNumber=int(splitBout[-1])
	numContestants=numPartis**(numRounds)
	offset=[0,0]
	rotation=0
	if(boutNumber>=0 and (boutNumber)/numContestants<(1/numPartis)):
		#offset=[-10*nameLength,15+numberNewLines*10]
		offset=[-8*nameLength,15]
	elif((boutNumber)/numContestants>=(1/numPartis) and (boutNumber)/numContestants<(2/numPartis)):
		#offset=[60+10*nameLength,85+numberNewLines*10]
		offset=[0,15]
	elif((boutNumber)/numContestants>=(2/numPartis) and (boutNumber)/numContestants<(3/numPartis) ):
		offset=[15,0]
		rotation=90
	elif((boutNumber)/numContestants>=(3/numPartis)):
		offset=[0,0]
		rotation=90
	return offset,rotation

def createTextLayer(teamNameSplit,numEndLines,teamNameLen,rotate,font):
	textLayer=np.zeros((30*numEndLines,teamNameLen*12,4),dtype=np.uint8)
	if teamNameLen<=1:
		textLayer=np.zeros((30,30,4),dtype=np.uint8)
	if rotate>0:
		textLayer=np.zeros((teamNameLen*12+30,teamNameLen*12+30,4),dtype=np.uint8)
	#if pAdj[2]>0:
	#	textLayer=np.zeros((teamNameLen*10,teamNameLen*10,4),dtype=np.uint8)
	textLayer.fill(255)
	k=0
	for teamName in teamNameSplit:
		cv2.putText(textLayer,teamName,(0,25+20*k), font, .5,(0,0,0,255),1,cv2.LINE_AA)
		k+=1
	(h,w)=textLayer.shape[:2]
	#textLayer[3]=np.zeros((w,1),dtype=np.uint8)
	center=(w/2,h/2)
	rotation=cv2.getRotationMatrix2D(center, rotate, 1.0)
	textLayer=cv2.warpAffine(textLayer,rotation,(w,h))
	if rotate>0:
		textLayer=textLayer[0:teamNameLen*12,0:30*numEndLines]
	#if pAdj[2]>0:
	#	cv2.line(textLayer,(0,0),(h,0),(255,255,255,255),3)
	return textLayer

def splitUpName(teamName):
	endLines=1
	teamNameSplit=list()
	physicalLength=len(teamName)
	if len(teamName)>14:
		split=teamName.split(' ');
		count=0
		teamName=""
		for word in split:
			count+=len(word)
			print(str(count)+","+word)
			if count>14:
				physicalLength=count
				count=0
				teamNameSplit.append(teamName)
				teamName=word+" "
				endLines+=1
			else:
				teamName+=word+" "
	teamNameSplit.append(teamName)
	print("PLEN="+str(physicalLength))
	return teamNameSplit,endLines,physicalLength
#setTeamNames()