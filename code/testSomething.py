import glob
import os
import PIL
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *

#ab=autoBracket(5,2,2)
#p=ab.createBracket()
print("POINTS")
os.chdir("bracket")
root=tk.Tk()
#Label(root,text=str("fds"+etn.teamName)).pack()
# cvFile=open("bracket.csv","r+")
# cvString=""
# picList=list()
# for line in cvFile:
	# print(line+"\n")
	# if line=="\n":
		# print("nothing")
		# etn=enterTeamName(root,picList)
		# root.wait_window(etn.top)
		# cvString+=etn.teamName+",\n"
		# picList=list()
	# else:
		# splitLine=line.split(',')
		# print(splitLine[0])
		# image1 = PIL.Image.open(splitLine[0])
		# tkpi = PIL.ImageTk.PhotoImage(image1)
		# picList.append(tkpi)
		# cvString+=line
# print(cvString)
# cvFile=open("bracket2.csv","w+")
# cvFile.write(cvString)
# cvFile.close()
# root.mainloop()
# print("hi")
#print(p)
svFile=open("test.csv","w+")
svFile.write("\n")
svFile.write("HELLO,HELLO\n")
svFile.write("\n")
svFile.write("HELLO,HELLO\n")
svFile.close()
# for points in p:
	# pStr=str(points)
	# pStr=pStr.replace('[','')
	# pStr=pStr.replace(']','')
	# pStr=pStr.replace(' ','')
	# pStr=pStr.replace('\n','')
	# print(pStr)
	# svFile.write(pStr)
	# svFile.write("\n")
# brack=cv2.imread("bracket.png",cv2.IMREAD_UNCHANGED)
# for points in p:
	# for point in points:
		# print(point)
		# cv2.line(brack,(point[0],point[1]),(point[0]+10,point[1]+10),(255,0,0,255),40)
# cv2.imwrite("bracket.png",brack)
#root=tk.Tk()
#ets=enterTourneySize(root)
#root.wait_window(ets.top)
#Label(root,text=str(ets.team)+" "+str(ets.partis)+" "+str(ets.rounds)).pack()
