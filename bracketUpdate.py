import glob
import os
import PIL
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *
import metaBracketReader
import math

def bracketUpdate():
	os.chdir("../bracket")
	points,[teamSize,numRounds,numPartis],picFilenames,index,teamNames,windicies=metaBracketReader.readAllBrackets("bracketMetaData.csv","bracket.csv")
	i=0
	print("index="+str(index))
	picList=list()
	root=tk.Tk()
	round=0
	#i=int(index/(numPartis**(numRounds-1)))
	i=index
	j=(numPartis**(numRounds-1))
	k=1
	while(int(i/j)>0):
		round+=1
		i-=j
		k+=1
		j=(numPartis**(numRounds-k))
	print("ROUND="+str(round))
	picIndicies=list()
	if index<numPartis**(numRounds-1):
		teamPic=PIL.Image.new('RGB',(50*teamSize+10,60))
		offset=0
		i=0
		j=0
		indx=index*numPartis*teamSize
		print("INDX="+str(indx))
		for picFile in picFilenames[0][indx:indx+numPartis*teamSize]:
			if teamSize<2:
				picList.append(PIL.ImageTk.PhotoImage(PIL.Image.open(picFile)))
				picIndicies.append(indx+i)
				i+=1
			else:
				teamPic.paste(PIL.Image.open(picFile),(offset,0))
				offset+=50
				i+=1
				if i>=teamSize:
					picList.append(PIL.ImageTk.PhotoImage(teamPic))
					offset=0
					picIndicies.append(indx+j)
					j+=teamSize
					i=0
	else:
		teamPic=PIL.Image.new('RGB',(50*teamSize+10,60))
		offset=0
		#indx=(index-(numPartis**(numRounds-1))*(round))*(numPartis+teamSize)
		indx=(index-(numPartis**(numRounds-1)))*numPartis*teamSize
		print("INDX="+str(indx))
		count=0
		j=0
		r=round
		if round>=3:
			r=2
		for i in range(0,numPartis*teamSize):
			if teamSize<2:
				image=PIL.Image.open(picFilenames[r][windicies[indx+i]])
				print("INDXII "+str(indx+i)+" "+str(windicies[indx+i]))
				picList.append(PIL.ImageTk.PhotoImage(image))
				picIndicies.append(windicies[indx+i])
			else:
				print("WJID "+str((windicies[indx]+j,indx,j)))
				image=PIL.Image.open(picFilenames[r][windicies[indx]+j])
				teamPic.paste(image,(offset,0))
				offset+=50
				count+=1
				j+=1
				if count>=teamSize:
					j=0
					picIndicies.append(windicies[indx])
					indx+=1
					picList.append(PIL.ImageTk.PhotoImage(teamPic))
					offset=0
					count=0
	pw=pickWinners(root,picList,picIndicies)
	root.wait_window(pw.top)
	print("WINNER="+str(pw.winnersIndex))
	print(teamSize)
	bIndx=int(math.floor(index/numPartis**(numRounds-(2+round)))%numPartis)
	print(numPartis**(round+1))
	print(windicies)
	print(bIndx)
	print("PICIND="+str(picIndicies))
	if round==0:
		winx=updateBracket(index%(numPartis**(numRounds-2)),points,picFilenames,pw.winnersIndex,round,[teamSize,numRounds,numPartis],bIndx,windicies)
	else:
		winx=updateBracket(index%(numPartis**(numRounds-2-round)),points,picFilenames,pw.winnersIndex,round,[teamSize,numRounds,numPartis],bIndx,windicies)
	for win in winx:
		windicies.append(win)
	print("WINDING")
	print(windicies)
	updateIndex("bracketMetaData.csv",index+1,windicies)

def updateBracket(index,points,picList,winner,round,tRP,bIndx,windex):
	windicies=list()
	print("Indx,winer,round,trp,bindx "+str((index,winner,round,tRP,bIndx)))
	print("winner= "+str(winner))
	brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
	(teamSize,numRounds,numPartis)=tRP
	if round==0:
		picIndex=winner[0]#index*(numPartis+(teamSize-1))+winner
	else:
		picIndex=winner[0]#windex[index-numPartis**(numRounds-1)]
	f=0
	for i in range(0,round+2):
		f+=(numPartis**(i))
	print("F+"+str((f)))
	pointIndex=(numRounds-(round+2))+(index*(f))
	print(str((pointIndex,index*(numPartis**(2+round)-1),(numPartis**(2+round)-1))))
	k=numPartis#*(round+1)
	#if index==0:
#		pointIndex+=1
	i=1
	while(int(index/k)>0):
		pointIndex+=1
		k+=numPartis
		print("kkkkkkkkk-"+str((k,pointIndex)))
	print("pic,point "+str((picIndex,pointIndex)))
	if round>=2:
		round=1
	if round<=0:
		dir=[1,1,1,10,-20]
		if bIndx==1:
			dir=[-3,1,-1,10,0]
		elif bIndx==2:
			dir=[-1,3,-1,25,-10]
	else:
		dir=[1,1,1,10,50]
		if bIndx==1:
			dir=[-3,1,-1,10,-50]
		elif bIndx==2:
			dir=[-1,3,-1,-50,-10]
	print("PI,bIndx "+str((pointIndex,bIndx)))
	p1=points[bIndx][pointIndex][0]+25*dir[0]
	p2=points[bIndx][pointIndex][1]-25*dir[1]
	if teamSize>1:
		j=0
		for picFileName in picList[round+1][picIndex:picIndex+teamSize]:
			print(picFileName)
			pic=cv2.imread(picFileName,cv2.IMREAD_UNCHANGED)
			brack[p2:p2+50,p1:p1+50]=pic
			if bIndx<2:
				p1+=50*dir[2]
			else:
				p2+=50*dir[2]
			j+=1
		windicies.append(picIndex)
	else:
		print(picList[round+1][picIndex])
		pic=cv2.imread(picList[round+1][picIndex],cv2.IMREAD_UNCHANGED)
		print(str((p1,p2,brack.shape)))
		brack[p2:p2+50,p1:p1+50]=pic
		windicies.append(picIndex)
	for i in range(1,(numPartis)**(round+1)+1,(numPartis*round)+1):
		print("HELLO "+str(i)+" "+str((numPartis+1)**(round+1))+" "+str(winner[1]*((numPartis*round)+1)))
		if not i==(winner[1]*((numPartis*round)+1)+1):
			cv2.putText(brack,"X",(points[bIndx][pointIndex+i][0]+dir[4],points[bIndx][pointIndex+i][1]+dir[3]), 0, 1,(0,0,255,255),4,cv2.LINE_AA)
	cv2.imwrite("bracket.png",brack)
	print(windicies)
	return windicies

def updateIndex(fileName,index,windicies):
	lines=open(fileName,"r+").read().splitlines()
	print(lines[-1])
	oldLine=lines[-1].splitlines()
	oldLine=oldLine[1:len(oldLine)]
	lines[-1]=str(index)+','.join(oldLine)
	for windex in windicies:
		lines[-1]+=","+str(windex)
	lines[-1]+=",\n"
	open(fileName,"w").write('\n'.join(lines))

#bracketUpdate()