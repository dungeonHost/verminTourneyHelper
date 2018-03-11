import numpy as np
import cv2
import glob,os
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from math import ceil

#AUTOBRACKET.py creates the tourney image (bracket.png) and populates it with all first stage vermin

numRounds=3
teamSize=1
numPartis=3
startFlag=True
topFlag=True
horzLineDist=50
vertLineDist=(70*numPartis)
topPoints=list()
bracketPoints=dict()
class autoBracket:
	#initilize bracket by telling it the size of the tourney
	def __init__(self,nr,ts,np,csvDictList):
		global numRounds
		global numPartis
		global teamSize
		global matchNumber
		self.csvDictList=csvDictList
		teamSize=ts
		numRounds=nr
		numPartis=np
		self.matchNumber=[None]*numRounds
		for i in range(0,numRounds):
			self.matchNumber[i]=0

	#creates and populates the bracket, returns a a list of all the points ([x,y]) at the end of each branch in the bracket (useful for updating the bracket later on)
	def createBracket(self):
		global csvFile
		global startFlag
		global topFlag
		global horzLineDist
		global numPartis
		global numRounds
		global topPoints
		matchNumber=self.matchNumber
		if not os.path.exists("bracket"):
			print("none")
			exit()
		os.chdir("bracket")
		prod=1
		#calculate how long each line needs to be so that the 'trees' don't intersect
		horzLineDist=ceil((prod*((numPartis)**(numRounds-2)))*(vertLineDist-1)/2)
		horzLineDist=int(horzLineDist*3/4)
		if horzLineDist<75:
			horzLineDist=75
		hsum=0
		bsum=0
		hld=horzLineDist
		for i in range(0,numRounds):
			bsum+=hld
			hld=hld/1.3
		for j in range(numRounds-1,1,-1):
			hsum+=int(prod*((numPartis)**(j-1))*(vertLineDist))
			print("JFDSF"+str(hsum)+" "+str(prod)+" "+str(j))
		#calculate the heihgt and widht of the bracket
		h=int(hsum+(numPartis-2)*(150*teamSize+2*(horzLineDist)))+vertLineDist+100
		w=int(bsum)*2+150*(teamSize)+200
		#create the bracket image as a numpy array
		brack=np.ones((h,w,3),np.uint8)*255
		#initilize point to be the middle of the image
		point=[int(w/2),int(h/2)]
		bracketPoints["FINAL_0"]=[point[:],"","",list()]
		startFlag=True
		topFlag=True
		#create the tree growing left from root
		self.drawBrackHorz(point[0],point[1],brack,-1,numRounds,horzLineDist)
		startFlag=True
		topFlag=True
		#create the right tree
		self.drawBrackHorz(point[0],point[1],brack,1,numRounds,horzLineDist)
		if numPartis>2:
			topFlag=True
			startFlag=True
			#bottom tree
			self.drawBrackVert(point[0],point[1],brack,1,numRounds,horzLineDist)
		if numPartis>3:
			topFlag=True
			startFlag=True
			#top tree
			self.drawBrackVert(point[0],point[1],brack,-1,numRounds,horzLineDist)
		#make sure that the bracket image has 4 channels (r,g,b,a) same as the cropped out images 
		h,w,_=brack.shape
		a = np.ones((h,w,1), np.uint8)*255
		b,g,r=cv2.split(brack)
		rgba=[b,g,r,a]
		bracket=cv2.merge(rgba,4)
		print(bracket.shape)
		#save the bracket image (useful if bracket.csv is empty and you just want an empty bracket image)
		cv2.imwrite("bracket.png",bracket)
		
		self.matchNumber[numRounds-1]=0
		#populate the right and left trees of the bracket with first stage vermin
		fp=self.populateBracket()
		print(bracketPoints)
		#if numPartis>2:
			#populate the bottom and top trees
		#	self.populateVertBracket(fp)
		return bracketPoints

	#add the first stage vermins to the right and left trees of the bracket
	def populateBracket(self):
		global bracketPoints
		global numRounds
		matchNumber=self.matchNumber
		point=bracketPoints[str(numRounds-1)+"_0"][0][:]
		point[0]-=50*teamSize
		point[1]-=25
		cnt=1
		vrmIndx=0
		bracket=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
		print("StartHorz")
		#fp=open("bracket.csv","r+")
		csvDictList=self.csvDictList
		tempCsvDictList=csvDictList[:]
		pickVermList=list()
		#for csvDict in self.csvDictList:
		while len(tempCsvDictList)>=teamSize:
			#splitString=line.split(',')
			#read in the vermin's first stage image as a numpy array, resize it so it fits
			print(tempCsvDictList)
			csvDict=tempCsvDictList[0]
			
			#this is used for team battles to make sure that teamates are near one another
			print("cnt teamsizee "+str(cnt%teamSize)+" "+str(cnt)+" "+str(teamSize))
			print((numPartis*(numPartis**(numRounds)*teamSize)))
			if teamSize>1:
				for teamMateIndex in csvDict['teamMates']:
					teamMateCsvDict=csvDictList[teamMateIndex]
					self.addVermToBracket(teamMateCsvDict['stage1'][0],point,bracket)
					if (cnt-1)<(numPartis**(numRounds-1))*2:
						point[0]+=50
					else:
						point[1]+=50
				bracketPoints[str(numRounds-1)+"_"+str(cnt-1)][3].extend(csvDict['teamMates'])
				pickVermList.extend(csvDict['teamMates'])
			else:
				pickVermList.append(int(csvDict['index']))
				bracketPoints[str(numRounds-1)+"_"+str(cnt-1)][3].append(int(csvDict['index']))
				self.addVermToBracket(csvDict['stage1'][0],point,bracket)
			tempCsvDictList=list()
			print(pickVermList)
			for tempCsvDict in csvDictList:
				if not(tempCsvDict['index'] in pickVermList):
					print(tempCsvDict['index'])
					print(tempCsvDict)
					tempCsvDictList.append(tempCsvDict)
			cnt+=1
			try:
				point=bracketPoints[str(numRounds-1)+"_"+str(cnt-1)][0][:]
				print("point "+str(point))
				if (cnt-1)<(numPartis**(numRounds-1)):
					point[0]-=50*teamSize
					point[1]-=25
				elif (cnt-1)<(numPartis**(numRounds-1))*2:
					#point[0]=50*teamSize
					point[1]-=25
				elif (cnt-1)<(numPartis**(numRounds-1))*3:
					
					point[0]-=25
			except(KeyError):
				cv2.imwrite("bracket.png",bracket)
				print("EXIT")
				return
			#if cnt%(numPartis*(numPartis**(numRounds-1)*teamSize))==0:
			#	cv2.imwrite("bracket.png",bracket)
			#	print("EXIT")
			#	return
			vrmIndx+=1
		cv2.imwrite("bracket.png",bracket)

	# #populate the top and bottom trees (pretty much the same as with the horozontal version only with different point adjustment values)
	# def populateVertBracket(self,fp):
		# matchNumber=self.matchNumber
		# point=topPoints[2]
		# point[0]-=25
		# cnt=1
		# bracket=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
		# print("StartVERT")
		# if not(fp):
			# return
		# for line in fp:
			# splitString=line.split(',')
			# pic=cv2.imread(splitString[0].rstrip(),cv2.IMREAD_UNCHANGED)
			# print(splitString[0])
			# alphS=pic[:,:,3]/255.0
			# alphL=1.0-alphS
			# for c in range(0,3):
				# bracket[point[1]:point[1]+50, point[0]:point[0]+50,c]=(alphS*pic[:,:,c]+alphL*bracket[point[1]:point[1]+50, point[0]:point[0]+50,c])
			# alphS=0
			# alphL=0
			# if cnt%teamSize==0:
				# point[0]+=int((vertLineDist)/(numPartis-1))
				# point[1]-=(50*(teamSize-1))#*dir)
			# else:
				# point[1]+=50
			# if cnt%(numPartis**(numRounds-1)*teamSize)==0:
				# break
			# cnt+=1
		# cv2.imwrite("bracket.png",bracket)
	
	def addVermToBracket(self,picFileName,point,bracket):
		pic=cv2.imread(picFileName,cv2.IMREAD_UNCHANGED)
		print(picFileName)
		pic=cv2.resize(pic,(50,50))
		alphS=pic[:,:,3]/255.0
		alphL=1.0-alphS
		#copy each channel from  the vermin image into the bracket numpy array (I can't even remember why I did it like this)
		for c in range(0,3):
			bracket[point[1]:point[1]+50, point[0]:point[0]+50,c]=(alphS*pic[:,:,c]+alphL*bracket[point[1]:point[1]+50, point[0]:point[0]+50,c])
	
	#draw the right and left trees of the tourney
	def drawBrackHorz(self,x,y,brack,dir,r,hLD):
		global startFlag
		global numRounds
		global teamSize
		global numPartis
		global topPoints
		global topFlag
		global bracketPoints
		matchNumber=self.matchNumber
		point=[x,y]
		#for the first branch do this
		if startFlag:
			print("start")
			point[0]+=int(hLD*dir/2)
			self.drawLineHorz(point,int(1*hLD),dir,brack)
			hLD=int(hLD/1.3)
			startFlag=False
			#if(dir==-1):
			#	bracketPoints[0].append(point[:])
			#else:
			#	bracketPoints[1].append(point[:])
			bracketPoints["0_"+str(matchNumber[0])]=[point[:],"FINAL_0","Loser_0_"+str(int(matchNumber[0]/numPartis)),list()]
			matchNumber[0]+=1
			r-=1
		prod=1
		for i in range(r,1):
			prod*=i
		#calculate the length of each vertical line drawn for the bracket
		vertDist=int(prod*((numPartis)**(r-1))*(vertLineDist))
		print("VERT="+str(vertDist)+" r="+str(r)+" blocks="+str(ceil(((3*r-1)/2)**(r-1))))
		point[1]+=int(vertDist/2)
		#draw a verticle line
		self.drawLineVert(point,vertDist,-1,brack)
		#addjust horozontal line distance to save on space
		hLD=int(hLD/1.3)
		print("r="+str(r)+" hld="+str(hLD))
		for i in range(0,numPartis):
			#draw a horzontal line
			self.drawLineHorz(point,hLD,dir,brack)
			#if(dir==-1):
			#	bracketPoints[0].append(point[:])
			#else:
			#	bracketPoints[1].append(point[:])
			tempRound=numRounds-r
			bracketPoints[str(tempRound)+"_"+str(matchNumber[tempRound])]=[point[:],(str(tempRound-1)+"_"+str(int(matchNumber[tempRound]/numPartis))),("Loser_"+str(tempRound)+"_"+str(int(matchNumber[tempRound]/numPartis))),list()]
			matchNumber[tempRound]+=1
			if(r>1):
				#recursively call untill an entire branch has been drawn
				self.drawBrackHorz(point[0],point[1],brack,dir,r-1,hLD)
			elif(topFlag):
				topPoints.append(point[:])
				print(topPoints)
				print(point)
				topFlag=False
			point[0]-=hLD*dir
			print("r="+str(r)+" hld="+str(hLD))
			point[1]+=int((vertDist)/(numPartis-1))
		return
	
	#same as draw horoz only with different point adjustment values
	def drawBrackVert(self,x,y,brack,dir,r,hLD):
		global startFlag
		global numRounds
		global teamSize
		global numPartis
		global topPoints
		global topFlag
		point=[x,y]
		matchNumber=self.matchNumber
		if startFlag:
			print("start")
			point[1]+=int(hLD*dir/2)
			self.drawLineVert(point,int(1*hLD),dir,brack)
			hLD=int(hLD/1.3)
			startFlag=False
			bracketPoints["0_"+str(matchNumber[0])]=[point[:],"FINAL_0","Loser_0_"+str(int(matchNumber[0]/numPartis)),list()]
			matchNumber[0]+=1
			r-=1
		prod=1
		for i in range(r,1):
			prod*=i
		vertDist=int(prod*((numPartis)**(r-1))*(vertLineDist))
		print("VERT="+str(vertDist)+" r="+str(r)+" blocks="+str(ceil(((3*r-1)/2)**(r-1))))
		point[0]+=int(vertDist/2)
		self.drawLineHorz(point,vertDist,-1,brack)
		hLD=int(hLD/1.3)
		print("r="+str(r)+" x="+str(point[0]))
		for i in range(0,numPartis):
			self.drawLineVert(point,hLD,dir,brack)
			tempRound=numRounds-r
			bracketPoints[str(tempRound)+"_"+str(matchNumber[tempRound])]=[point[:],(str(tempRound-1)+"_"+str(int(matchNumber[tempRound]/numPartis))),("Loser_"+str(tempRound)+"_"+str(int(matchNumber[tempRound]/numPartis))),list()]
			matchNumber[tempRound]+=1
			if(r>1):
				self.drawBrackVert(point[0],point[1],brack,dir,r-1,hLD)
			elif(i==0 and topFlag):
				print(topPoints)
				print(point)
				topPoints.append(point[:])
				topFlag=False
			point[1]-=hLD*dir
			point[0]+=int((vertDist)/(numPartis-1))
		return
		
	#what do you think it does?
	def drawLineHorz(self,point,dist,dir,brack):
		#cv2.line(image,start point,end point,color,thickness)
		cv2.line(brack,(point[0],point[1]),(point[0]+dist*dir,point[1]),(0,0,0),4)
		#addjust the point
		point[0]+=dist*dir

	#its a mystery
	def drawLineVert(self,point,dist,dir,brack):
		cv2.line(brack,(point[0],point[1]),(point[0],point[1]+dist*dir),(0,0,0),4)
		point[1]+=dist*dir

#if not os.path.exists("bracket"):
#	os.mkdir("bracket")
#y=autoBracket(3,2,3)
#y.createBracket()
#print("hi")
# if not os.path.exists("bracket"):
	# exit()
# os.chdir("bracket")
# csvFile=open("bracket.csv","r+")
# a=autoBracket(numRounds,teamSize,numPartis)
# a.createBracket()