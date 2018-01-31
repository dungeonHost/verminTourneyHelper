import numpy as np
import cv2
import glob,os
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from math import ceil
from autoBracket import autoBracket
import autoCrop
import random
from popupWindows import enterTourneySize

numRounds=5
teamSize=1
numPartis=2
firstEvo=list()

def tourneyHelper():
	global csvFile
	global teamSize
	root=tk.Tk()
	os.chdir("..")
	if not os.path.exists("bracket"):
		os.mkdir("bracket")
	csvFile=open("bracket/bracket.csv","w+")
	#if not os.path.exists("vermin"):
	#	os.mkdir("vermin")
	#csvFile=open("b2racket/bracket.csv","w+")
	csvStrList=list()
	totalDone=0
	fileNameList=[f for f in os.walk(".").__next__()[2]if f[-4:]==".png"]
	ets=enterTourneySize(root)
	root.wait_window(ets.top)
	numRounds=ets.rounds
	teamSize=ets.team
	numPartis=ets.partis
	root.destroy()
	
	print(len(fileNameList))
	print((numPartis**numRounds)*teamSize)
	try:
		randList=random.sample(range(len(fileNameList)),(numPartis**numRounds)*teamSize)
		pass
	except ValueError:
		randList=range(0,len(fileNameList))
		pass
	for fileName in fileNameList: #glob.glob("*.png"):
		if(totalDone in randList):
			#if not os.path.exists(fileName[:-4]):
			#	os.mkdir(fileName[:-4])
			im=cv2.imread(fileName,cv2.IMREAD_UNCHANGED)
			crop_imgs=autoCrop.splitImage(fileName,im)
			picToKeep,vermString=autoCrop.pickImage(crop_imgs,im)
			index=0
			csvStr=""
			os.chdir("bracket")
			for pic in picToKeep:
				cv2.imwrite(fileName[:-4]+str(index)+".png",pic)
				if(index<3):
					if(index==0):
						firstEvo.append(pic)
						#cv2.imshow(firstEvo[0])
						#cv2.waitKey(0)
					#r_im=cv2.resize(pic,(50,50))
					print(os.getcwd())
					cv2.imwrite(fileName[:-4]+str(index)+".png",pic)#r_im)
					
					csvStr+=os.getcwd()+"\\"+fileName[:-4]+str(index)+".png,"
					if len(vermString)>index:
						csvStr+=vermString[index]
					#os.chdir("../vermin")#fileName[:-4])
					#cv2.imshow(fileName[:-4],pic)
					cv2.waitKey(0)
				index+=1
			csvStr+="\n"
			csvStrList.append(csvStr.split(","))
			#print(vermString.split(","))
			print(csvStr.split(","))
			print(csvStrList)
			#csvFile.write(csvStr)
			cv2.imwrite(fileName,im)
			#os.chdir("../bracket")
			cv2.imwrite(fileName,im)
			cv2.waitKey(0)

			os.chdir("..")
		totalDone+=1
	#csvFile.close()
	if teamSize>=2:
		createTeams(csvStrList)
	else:
		teamCounter=0
		for csvStrArr in csvStrList:
			line=",".join(csvStrArr)
			csvFile.write(line)
	csvFile.close()
	#crop_imgs=autoCrop.splitImage()
	#autoBracket(number of rounds,team size,number of participants (1v1=2;1v1v1=3;etc.))
	ab=autoBracket(numRounds,teamSize,numPartis)
	p=ab.createBracket()
	svFile=open("bracketMetaData.csv","w+")
	svFile.write(str(teamSize)+","+str(numRounds)+","+str(numPartis)+"\n")
	for points in p:
		if len(points)>0:
			pStr=str(points)
			pStr=pStr.replace('[','')
			pStr=pStr.replace(']','')
			pStr=pStr.replace(' ','')
			pStr=pStr.replace('\n','')
			svFile.write(pStr)
			svFile.write("\n")
	svFile.write("0,")

def createTeams(csvStrList):
	global teamSize
	global csvFile
	root=tk.Tk()
	teamLabels=list()
	butts=list()
	
	team=list()
	images=list()
	
	os.chdir("bracket")
	for fileName in glob.glob("*.png"):
		print(repr(fileName))
	instruction=Label(root,justify=LEFT,text="pick "+str(teamSize-1)+" teamates")
	instruction.grid(row=0,column=0)
	
	teamLabels.append(Label(root,justify=LEFT,text="hi"))
	#image=tk.PhotoImage(file=csvStrList[0][0])
	#zoom=[60/image.width(),60/image.height()]
	images.append(tk.PhotoImage(file=csvStrList[0][0]))
	line=",".join(csvStrList[0])
	csvFile.write(line)
	teamLabels[0].config(image=images[0])
	teamLabels[0].grid(row=1,column=0)
	print(csvStrList)
	csvStrList.remove(csvStrList[0])
	print("\n")
	print(csvStrList)
	setUpButts(images,root,teamLabels,instruction,team,csvStrList,butts)
	root.mainloop()
	cv2.destroyAllWindows()
	os.chdir("..")

def setUpButts(images,root,teamLabels,instruction,team,csvStrList,butts):
	index=0
	for pic in csvStrList:
		#img=cv2.resize(firstEvo[index],(60,60))
		#fs=Image.fromarray(img)
		print("PIC")
		print(pic)
		pic=cv2.imread(pic[0],cv2.IMREAD_UNCHANGED)
		pic=cv2.resize(pic,(60,60))
		im=Image.fromarray(pic)
		images.append(ImageTk.PhotoImage(im))#ImageTk.PhotoImage(im)
		butts.append(Button(root,justify=LEFT))
		butts[index].config(image=images[index+1],width="60",height="60",command=lambda a=index: teamSelect(a,images,root,teamLabels,instruction,team,csvStrList,butts))
		butts[index].grid(row=2+int(index/12),column=int(index%12))
		index+=1

def teamSelect(index,images,root,teamLabels,inst,team,csvStrList,butts):
	global teamSize
	global csvFile
	teamLabels.append(Label(root,justify=LEFT))
	teamLabels[len(teamLabels)-1].config(image=images[index+1])
	teamLabels[len(teamLabels)-1].grid(row=1,column=len(teamLabels)-1)
	inst.config(text="pick "+str(teamSize-len(team))+" teamates")
	team.append(csvStrList[index])
	print("teamsize,TEAM LENGTH,index\n"+str((teamSize,len(team),index)))
	print(len(csvStrList))
	print(team)
	if len(team)>=(teamSize-1):
		index=0
		for csvStrArr in team:
			line=",".join(csvStrArr)
			csvFile.write(line)
			csvIndex=csvStrList.index(csvStrArr)
			csvStrList.remove(csvStrArr)
			# del images[csvIndex]
			# del butts[csvIndex]
			# del teamLabels[index]
			# index+=1
		print(len(csvStrList))
		root.destroy()
		if len(csvStrList)<teamSize:
			return
		root=tk.Tk()
		images=list()
		butts=list()
		teamLabels=list()
		team=list()
		
		print(csvStrList)
		#image=tk.PhotoImage(file=csvStrList[0][0])
		#zoom=[60/image.width(),60/image.height()]
		images.append(tk.PhotoImage(file=csvStrList[0][0]))
		instruction=Label(root,justify=LEFT,text="pick "+str(teamSize-1)+" teamates")
		instruction.grid(row=0,column=0)
		teamLabels.append(Label(root,justify=LEFT,text="hi"))
		teamLabels[0].config(image=images[0])
		teamLabels[0].grid(row=1,column=0)
		line=",".join(csvStrList[0])
		csvFile.write(line)
		csvStrList.remove(csvStrList[0])
		
		teamLabels[0].grid(row=1,column=0)
		setUpButts(images,root,teamLabels,instruction,team,csvStrList,butts)
		#csvFile.write("\n")
		print("done")
	print("hi")


#tourneyHelper()
# csvFile2=open("bracket/bracket2.csv","r+")
# csvStrList=list()
# for line in csvFile2:
	# csvStrList.append(line.split(","))
# createTeams(csvStrList)