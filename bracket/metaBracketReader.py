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
	for line in cvFile:
		line=line.replace('\n','')
		splitLine=line.split(',')
		try:
			if count==0:
				print(splitLine)
				numRounds=int(splitLine[0])
				teamSize=int(splitLine[1])
				numPartis=int(splitLine[2])
			else:
				coCount=1
				point=[0,0]
				for coord in splitLine:
					print(point)
					print("CC="+str(coCount))
					if coCount%2==0:
						coCount=0
						point[1]=int(coord)
						points[count-1].append(point)
						print(point)
						point=[0,0]
					else:
						point[0]=int(coord)
					coCount+=1
			count+=1
		except ValueError:
			print("VALUE ERROR")
			pass
	print("\n")
	print(points)
	return points

def openAndModifyImage(p):
	brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
	for points in p:
		for point in points:
			print(point)
			cv2.line(brack,(point[0],point[1]),(point[0]+10,point[1]+10),(255,0,255,255),50)
	cv2.imwrite("bracket.png",brack)

points=readBracketMetaData("bracket3.csv")
openAndModifyImage(points)