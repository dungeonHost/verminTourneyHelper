import glob,os
import tkinter as tk
import numpy as np
import cv2
from tkinter import *
import PIL
from math import ceil
import metaBracketReader
from popupWindows import *

def setTeamNames():
	root=tk.Tk()
	os.chdir("../bracket")
	cvFile=open("bracket.csv","r+")
	metaFile=open("bracketMetaData.csv","a")
	picList=list()
	points,[teamSize,numRounds,numPartis],_,_=metaBracketReader.readBracketMetaData("bracketMetaData.csv")
	i=1
	brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
	skipAhead=numPartis+(numRounds-1)
	skipAheadAt=0
	for i in range(0,numRounds):
		skipAheadAt+=numPartis**(i)
	pointsIndex=numRounds-1
	print("SKIPPPPP "+str(skipAheadAt)+" "+str(skipAhead))
	font = 0
	print(teamSize)
	print("HELLLOOOOOOOOO")
	bIndx=0
	pAdj=[-50,20,0,0]
	resizeOffset=[0,0]
	count=0
	linesRead=0
	teamNames=""
	teamImages=list()
	i=1
	index=0
	for line in cvFile:
		if linesRead<teamSize*numPartis**numRounds:
			linesRead+=1
			splitLine=line.split(',')
			print(splitLine[0])
			image1=PIL.Image.open(splitLine[0])
			tkpi = PIL.ImageTk.PhotoImage(image1)
			picList.append(tkpi)
			if i%teamSize==0:
				etn=enterTeamName(root,picList)
				root.wait_window(etn.top)
				#metaFile.write(etn.teamName+"\n")
				teamNames+=etn.teamName+",\n"
				picList=list()
				teamNameSplit,numEndLines,teamNameLen=splitUpName(etn.teamName)
				print("TEAM NAME SPLIT="+str(teamNameSplit)+" "+"PLEN="+str(teamNameLen))
				if teamNameLen>1:
					textLayer=np.zeros((30*numEndLines,teamNameLen*12,4),dtype=np.uint8)
				else:
					textLayer=np.zeros((30,30,4),dtype=np.uint8)
				if pAdj[2]>0:
					textLayer=np.zeros((teamNameLen*10,teamNameLen*10,4),dtype=np.uint8)
				textLayer.fill(255)
				k=0
				for teamName in teamNameSplit:
					cv2.putText(textLayer,teamName,(0,25+20*k), font, .5,(0,0,0,255),1,cv2.LINE_AA)
					k+=1
				(h,w)=textLayer.shape[:2]
				#textLayer[3]=np.zeros((w,1),dtype=np.uint8)
				center=(w/2,h/2)
				rotation=cv2.getRotationMatrix2D(center, pAdj[2], 1.0)
				textLayer=cv2.warpAffine(textLayer,rotation,(w,h))
				if pAdj[2]>0:
					cv2.line(textLayer,(0,0),(h,0),(255,255,255,255),3)
				try:
					if bIndx==0:
						p1=points[bIndx][pointsIndex][0]+pAdj[0]-int(w/2)
					else:
						p1=points[bIndx][pointsIndex][0]+pAdj[0]
					p2=points[bIndx][pointsIndex][1]+pAdj[1]
					(height,width)=brack.shape[:2]
					p2+=resizeOffset[0]
					p1+=resizeOffset[1]

					print("P2 and P1 "+str(p2)+" "+str(p1))
					if w>width-p1 or h>height-p2 or p1<0:
						print("RESIZE")
						background=np.zeros((int(height+h*int(2)),int(width+w*int(2)),4),dtype=np.uint8)
						background.fill(255)
						background[int(h/2):height+int(h/2),int(w/2):width+int(w/2)]=brack
						brack=background
						cv2.imshow("hi",brack)
						cv2.waitKey(0)
						resizeOffset[1]+=int(w/2)
						resizeOffset[0]+=int(h/2)
						p2+=resizeOffset[0]
						p1+=resizeOffset[1]
					print(str(p2)+","+str(p1)+","+str(brack.shape)+","+str((h,w)))
					print(resizeOffset)
					brack[p2:p2+h,p1:p1+w]+=textLayer
					#cv2.imshow("hi",brack)
					#cv2.waitKey(0)
				except IndexError:
					pass
				#cv2.putText(brack,etn.teamName,(points[bIndx][pointsIndex][0]+pAdj[0]-len(etn.teamName)*4,points[bIndx][pointsIndex][1]+pAdj[1]), font, .75,(100,0,95,255),4,cv2.LINE_AA)
				
				pointsIndex+=1
				index+=1
				i=index
				while i%numPartis==0:
					pointsIndex+=1
					i/=numPartis
				# if pointsIndex>=skipAhead:
					# pointsIndex+=numRounds-2
					# skipAhead+=numPartis+numRounds-2
					# print("Skipasdfdsf "+str(skipAhead))
				if pointsIndex>=skipAheadAt:
					pointsIndex=numRounds-1
					skipAhead=numPartis+(numRounds-1)
					bIndx+=1;
					if pAdj[3]==0:
						pAdj=[50,20,0,1]
					elif pAdj[3]==1:
						print("change to 90")
						pAdj=[30,5,90,2]
				i=0
				count+=1
		else:
			break
		i+=1
	cvFile.close()
	cvFile=open("teamNames.csv","w+")
	cvFile.write(teamNames)
	#metaFile.close()
	if resizeOffset[0]>0 or resizeOffset[1]>0:
		metaFile==open("bracketMetaData.csv","w+")
		#for point in points:
		metaFile.write(str(teamSize)+","+str(numRounds)+","+str(numPartis)+",\n")
		#points=list(map(lambda x: [x[0]+resizeOffset[0],x[1]+resizeOffset[1]],points))
		print(points)
		for pointi in points:
			if len(pointi)>0:
				for point in pointi:
					print("point")
					print(point[0])
					point[0]+=resizeOffset[1]
					point[1]+=resizeOffset[0]
					pStr=str(point)
					pStr=pStr.replace('[','')
					pStr=pStr.replace(']','')
					pStr=pStr.replace(' ','')
					pStr=pStr.replace('\n','')
					metaFile.write(pStr)
					if not point==pointi[-1]:
						metaFile.write(",")
				metaFile.write("\n")
		metaFile.write("0,\n")
		#metaFile.write(teamNames)
		metaFile.close()
	cv2.imwrite("bracket.png",brack)

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