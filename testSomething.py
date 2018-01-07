import glob
import os
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *

ab=autoBracket(5,2,2)
p=ab.createBracket()
print("POINTS")
print(p)
svFile=open("bracket3.csv","w+")
for points in p:
	pStr=str(points)
	pStr=pStr.replace('[','')
	pStr=pStr.replace(']','')
	pStr=pStr.replace(' ','')
	pStr=pStr.replace('\n','')
	print(pStr)
	svFile.write(pStr)
	svFile.write("\n")
brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
for points in p:
	for point in points:
		print(point)
		cv2.line(brack,(point[0],point[1]),(point[0]+10,point[1]+10),(255,0,0,255),40)
cv2.imwrite("bracket.png",brack)
#root=tk.Tk()
#ets=enterTourneySize(root)
#root.wait_window(ets.top)
#Label(root,text=str(ets.team)+" "+str(ets.partis)+" "+str(ets.rounds)).pack()
