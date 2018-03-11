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
from csvToDicts import *
import math

def bracketUpdate():
	os.chdir("../bracket")
	csvDictConverter=csvToDicts()
	root=tk.Tk()
	#points,[teamSize,numRounds,numPartis],picFilenames,index,teamNames,windicies=metaBracketReader.readAllBrackets("bracketMetaData.csv","bracket.csv")
	numRounds,numPartis,teamSize,currentBout,pointDict=csvDictConverter.ReadMetaBracketCSV("bracketMetaData.csv")
	print(pointDict)
	verminDictList=csvDictConverter.ReadBracketCSV("bracket.csv")

	picList,picIndicies=createPicList(currentBout,pointDict,numPartis,teamSize,numRounds,verminDictList)

	# i=0
	# print("index="+str(index))
	# round=0
	# #i=int(index/(numPartis**(numRounds-1)))
	# i=index
	# j=(numPartis**(numRounds-1))
	# k=1
	# while(int(i/j)>0):
		# round+=1
		# i-=j
		# k+=1
		# j=(numPartis**(numRounds-k))
	# if index<numPartis**(numRounds-1):
		# picList,picIndicies=createPicList(index,numPartis,teamSize,round,numRounds,picFilenames)
	# else:
		# picList,picIndicies=createPicListHighRound(index,numPartis,teamSize,round,numRounds,windicies,picFilenames)

	pw=pickWinners(root,picList,picIndicies)
	root.wait_window(pw.top)
	#bIndx=int(math.floor(index/numPartis**(numRounds-(2+round)))%numPartis)
	updateBracket(pointDict,teamSize,numRounds,numPartis,currentBout,verminDictList,pw.winnersIndex)
	# else:
		# winx=updateBracket(index%(numPartis**(numRounds-2-round)),points,picFilenames,pw.winnersIndex,round,[teamSize,numRounds,numPartis],bIndx,windicies)
	# for win in winx:
		# windicies.append(win)
	# print("WINDING")
	# print(windicies)
	metaFile=open("bracketMetaData.csv","w")
	splitString=currentBout.split("_")
	boutNumber=int(splitString[-1])
	try:
		boutRound=int(splitString[0])
	except(ValueError):
		boutRound=-1
	nextRound=""
	if boutRound<0:
		nextRound="FINAL_"+str(boutNumber+numPartis)
	else:
		if boutNumber>=numPartis**(boutRound+1)-numPartis:
			if boutRound==0:
				nextRound+="FINAL_0"
			else:
				nextRound+=str(boutRound-1)+"_0"
		else:
			nextRound=str(boutRound)+"_"+str(boutNumber+numPartis)
	
	pointDictString=dictToString(pointDict,True)
	metaFile.write(str(numRounds)+","+str(numPartis)+","+str(teamSize)+","+nextRound+"\n")
	metaFile.write(pointDictString)
	metaFile.close()

def createPicList(currentBout,pointDict,numPartis,teamSize,numRounds,verminDictList):
	teamPic=PIL.Image.new('RGB',(50*teamSize+10,60))
	offset=0
	picList=list()
	picIndicies=list()
	
	boutRoundString=False
	splitString=currentBout.split("_")
	boutNumber=int(splitString[1])
	vermStage='stage1'
	try:
		boutRound=int(splitString[0])
	except(ValueError):
		boutRound=-1
		vermStage='stage3'
	if boutRound==(numRounds-2):
		vermStage='stage2'
	elif boutRound<numRounds-2:
		vermStage='stage3'
	
	iterateBout=currentBout[:]
	
	for i in range(0,numPartis):
		print(iterateBout)
		if teamSize>=2:
			for index in pointDict[iterateBout][3]:
				image=PIL.Image.open(verminDictList[index][vermStage][0])
				print(verminDictList[index][vermStage][0])
				image=image.resize((60,60))
				teamPic.paste(image,(offset,0))
				offset+=50
				print(index)
			#teamPic=teamPic.resize((60,60*teamSize))
			offset=0
			picList.append(PIL.ImageTk.PhotoImage(teamPic))
		else:
			index=pointDict[iterateBout][3]
			print(index)
			resizePic=PIL.Image.open(verminDictList[index[0]][vermStage][0])
			resizePic=resizePic.resize((60,60))
			picList.append(PIL.ImageTk.PhotoImage(resizePic))
		picIndicies.append(iterateBout)
		iterateBout=""
		for string in splitString[:-1]:
			iterateBout+=string+"_"
		iterateBout+=str(boutNumber+i+1)
	return picList,picIndicies
	
# def createPicListHighRound(index,numPartis,teamSize,round,numRounds,windicies,picFilenames):
	# teamPic=PIL.Image.new('RGB',(50*teamSize+10,60))
	# offset=0
	# count=0
	# j=0
	# picList=list()
	# picIndicies=list()
	# indx=(index-(numPartis**(numRounds-1)))*numPartis*teamSize
	# r=round
	# if round>=3:
		# r=2
	# for i in range(0,numPartis*teamSize):
		# if teamSize<2:
			# image=PIL.Image.open(picFilenames[r][windicies[indx+i]])
			# image=image.resize((60,60))
			# print("INDXII "+str(indx+i)+" "+str(windicies[indx+i]))
			# picList.append(PIL.ImageTk.PhotoImage(image))
			# picIndicies.append(windicies[indx+i])
		# else:
			# print("WJID "+str((windicies[indx]+j,indx,j)))
			# image=PIL.Image.open(picFilenames[r][windicies[indx]+j])
			# teamPic.paste(image,(offset,0))
			# offset+=50
			# count+=1
			# j+=1
			# if count>=teamSize:
				# j=0
				# picIndicies.append(windicies[indx])
				# indx+=1
				# teamPic=teamPic.resize((60,60*teamSize))
				# picList.append(PIL.ImageTk.PhotoImage(teamPic))
				# offset=0
				# count=0
				
def updateBracket(pointDict,teamSize,numRounds,numPartis,currentBout,vermDictList,winner):
	brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
	print(brack.shape)
	splitBout=currentBout.split("_")
	boutNumber=int(splitBout[-1])
	vermStage='stage3'
	try:
		boutRound=int(splitBout[0])
		if boutRound==(numRounds):
			vermStage='stage1'
		elif boutRound==(numRounds-1):
			vermStage='stage2'
	except(ValueError):
		boutRound=-1
	
	offset=[-1,0]
	dir=[-1,0]
	numContestants=numPartis**(boutRound+1)
	print("CONTEsTENTS")
	print(numContestants)

	for i in range(0,numPartis):
		pointIndex=""
		for string in splitBout[:-1]:
			pointIndex+=string+"_"
		pointIndex+=str(boutNumber+i)

		if(pointDict[pointIndex][1][0]=='F' and pointIndex==winner):
			offset=[0,0,-50-50*(teamSize-1),-50]
			dir=[1,0]
		elif(boutNumber+i>=0 and (boutNumber+i)/numContestants<(1/numPartis)):
			offset=[0,30,15,-25]
			dir=[1,0]
		elif((boutNumber+i)/numContestants>=(1/numPartis) and (boutNumber+i)/numContestants<(2/numPartis)):
			offset=[-55,30,-65,-25]
			dir=[-1,0]
		elif((boutNumber+i)/numContestants>=(2/numPartis) and (boutNumber+i)/numContestants<(3/numPartis) ):
			offset=[-30,0,-25,-65]
		elif((boutNumber+i)/numContestants>=(3/numPartis)):
			offset=[0,0,-25,25]
		if pointIndex!=winner:
			point=pointDict[pointIndex][0][:]
			print(point)
			print(offset)
			cv2.putText(brack,"X",(point[0]+offset[0],point[1]+offset[1]), 0, 3,(0,0,255,255),7,cv2.LINE_AA)
		else:
			print(pointDict[pointIndex])
			point=pointDict[pointDict[pointIndex][1]][0][:]
			pointDict[pointDict[pointIndex][1]][-1]=pointDict[pointIndex][-1]
			point=[point[0]+offset[2],point[1]+offset[3]]
			for vermIndex,i in zip(pointDict[pointIndex][-1],range(0,len(pointDict[pointIndex][-1]))):
				vermFileName=vermDictList[vermIndex][vermStage][0]
				pic=cv2.imread(vermFileName,cv2.IMREAD_UNCHANGED)
				if pointDict[pointIndex][1][0]!='F':
					pic=cv2.resize(pic,(50,50))
					alphS=pic[:,:,3]/255.0
					alphL=1.0-alphS
					print(point)
					print(brack.shape)
					for c in range(0,3):
						brack[point[1]:point[1]+50, point[0]:point[0]+50,c]=(alphS*pic[:,:,c]+alphL*brack[point[1]:point[1]+50, point[0]:point[0]+50,c])
					point=[point[0]+50*dir[0],point[1]+50*dir[1]]
				else:
					pic=cv2.resize(pic,(100,100))
					print(point)
					print(brack.shape)
					alphS=pic[:,:,3]/255.0
					alphL=1.0-alphS
					for c in range(0,3):
						brack[point[1]:point[1]+100, point[0]:point[0]+100,c]=(alphS*pic[:,:,c]+alphL*brack[point[1]:point[1]+50, point[0]:point[0]+50,c])
					point=[point[0]+100*dir[0],point[1]+100*dir[1]]
				
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

# def updateBracket(index,points,picList,winner,round,tRP,bIndx,windex):
	# windicies=list()
	# print("Indx,winer,round,trp,bindx "+str((index,winner,round,tRP,bIndx)))
	# print("winner= "+str(winner))
	# brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
	# (teamSize,numRounds,numPartis)=tRP
	# if round==0:
		# picIndex=winner[0]#index*(numPartis+(teamSize-1))+winner
	# else:
		# picIndex=winner[0]#windex[index-numPartis**(numRounds-1)]
	# f=0
	# for i in range(0,round+2):
		# f+=(numPartis**(i))
	# print("F+"+str((f)))
	# pointIndex=(numRounds-(round+2))+(index*(f))
	# print(str((pointIndex,index*(numPartis**(2+round)-1),(numPartis**(2+round)-1))))
	# k=numPartis#*(round+1)
	# #if index==0:
# #		pointIndex+=1
	# i=1
	# while(int(index/k)>0):
		# pointIndex+=1
		# k+=numPartis
		# print("kkkkkkkkk-"+str((k,pointIndex)))
	# print("pic,point "+str((picIndex,pointIndex)))
	# if round>=2:
		# round=1
	# if round<=0:
		# dir=[1,1,1,10,-20]
		# if bIndx==1:
			# dir=[-3,1,-1,10,0]
		# elif bIndx==2:
			# dir=[-1,3,-1,25,-10]
	# else:
		# dir=[1,1,1,10,50]
		# if bIndx==1:
			# dir=[-3,1,-1,10,-50]
		# elif bIndx==2:
			# dir=[-1,3,-1,-50,-10]
	# print("PI,bIndx "+str((pointIndex,bIndx)))
	# p1=points[bIndx][pointIndex][0]+25*dir[0]
	# p2=points[bIndx][pointIndex][1]-25*dir[1]
	# if teamSize>1:
		# j=0
		# for picFileName in picList[round+1][picIndex:picIndex+teamSize]:
			# print(picFileName)
			# pic=cv2.imread(picFileName,cv2.IMREAD_UNCHANGED)
			# brack[p2:p2+50,p1:p1+50]=pic
			# if bIndx<2:
				# p1+=50*dir[2]
			# else:
				# p2+=50*dir[2]
			# j+=1
		# windicies.append(picIndex)
	# else:
		# print(picList[round+1][picIndex])
		# pic=cv2.imread(picList[round+1][picIndex],cv2.IMREAD_UNCHANGED)
		# pic=cv2.resize(pic,(50,50))
		# print(str((p1,p2,brack.shape)))
		# brack[p2:p2+50,p1:p1+50]=pic
		# windicies.append(picIndex)
	# for i in range(1,(numPartis)**(round+1)+1,(numPartis*round)+1):
		# print("HELLO "+str(i)+" "+str((numPartis+1)**(round+1))+" "+str(winner[1]*((numPartis*round)+1)))
		# if not i==(winner[1]*((numPartis*round)+1)+1):
			# cv2.putText(brack,"X",(points[bIndx][pointIndex+i][0]+dir[4],points[bIndx][pointIndex+i][1]+dir[3]), 0, 1,(0,0,255,255),4,cv2.LINE_AA)
	# cv2.imwrite("bracket.png",brack)
	# print(windicies)
	# return windicies

# def updateIndex(fileName,index,windicies):
	# lines=open(fileName,"r+").read().splitlines()
	# print(lines[-1])
	# oldLine=lines[-1].splitlines()
	# oldLine=oldLine[1:len(oldLine)]
	# lines[-1]=str(index)+','.join(oldLine)
	# for windex in windicies:
		# lines[-1]+=","+str(windex)
	# lines[-1]+=",\n"
	# open(fileName,"w").write('\n'.join(lines))

#bracketUpdate()