import tkinter as tk
from tkinter import *
import sys
import ctypes  # An included library with Python install.
import numpy as np
import cv2
import glob,os
from PIL import Image
from PIL import ImageTk
from math import ceil
from autoBracket import autoBracket
import autoCrop
import random
from popupWindows import *

#POPUPWINDOWS.py contains the classes for most of the tkinter popup windows. These are used to prompt the user to enter information for other programs


#Displays a team and prompts the user to enter in their team name (used by setTeamNames.py)
class enterTeamName(object):
	teamName=""
	def enter(self,event):
		self.teamName=self.tNE.get()
		if self.teamName!="":
			self.top.destroy()
		
	def __init__(self,master,minPics):
		top=self.top=Toplevel(master)
		self.top.attributes('-topmost',1)
		minPicLabels=self.minPicLabels=list()
		i=0
		for pic in minPics:
			minPicLabels.append(Label(top,image=pic))
			minPicLabels[i].grid(row=0,column=i)
			i+=1
		instLabel=self.instLabel=Label(top,text="Enter team name: ")
		instLabel.grid(row=1,column=0)
		teamNameEntry=self.tNE=Entry(top)
		teamNameEntry.grid(row=1,column=1)
		teamNameEntry.bind("<Return>",self.enter)
		teamNameEntry.focus_force()

#Displays all the vermin that faught in the previous match and prompts the user to choose the winner (used by bracketUpdate.py)
class pickWinners(object):
	winnersIndex='-1_-1'
	def choice(self,index):
		print("CHOUCE "+str(index))
		winnersIndex=self.winnersIndex=index
		if winnersIndex!='-1_-1':
			self.top.destroy()

	def __init__(self,master,teamPics,indicies):
		top=self.top=Toplevel(master)
		self.top.attributes('-topmost',1)
		teamLabels=self.teamLabels=list()
		topLabel=self.topLabel=Label(top,text="PICK WINNER")
		topLabel.grid(row=1,column=0)
		i=0
		for pic,index in zip(teamPics,indicies):
			print("popup "+str(indicies[i]))
			teamLabels.append(Button(top))
			teamLabels[i].config(image=pic,text=str(index),command= lambda a=index: self.choice(a))
			teamLabels[i].grid(row=0,column=i)
			i+=1

#Promptz the user to enter in the team size, number of rounds and number of partisipants in the tourney (used by tourneyHelper.py)
class enterTourneySize(object):
	rounds=0
	partis=0
	team=0
	def __init__(self,master):
		top=self.top=Toplevel(master)
		self.top.attributes('-topmost',1)
		rLabel=self.rL=Label(top,text="Enter # rounds")
		pLabel=self.pL=Label(top,text="Enter # teams per round (i.e. 2= x vs x, 3= x vs x vs x, etc.)")
		tLabel=self.tL=Label(top,text="Enter # vermin per team")
		rEntry=self.rEntry=Entry(top)
		pEntry=self.pEntry=Entry(top)
		tEntry=self.tEntry=Entry(top)
		rLabel.grid(row=0,column=0)
		pLabel.grid(row=1,column=0)
		tLabel.grid(row=2,column=0)
		rEntry.grid(row=0,column=1)
		pEntry.grid(row=1,column=1)
		tEntry.grid(row=2,column=1)
		rEntry.bind("<Return>",func= lambda event, a=0: self.enter(event,a))
		pEntry.bind("<Return>",func= lambda event, a=1: self.enter(event,a))
		tEntry.bind("<Return>",func= lambda event, a=2: self.enter(event,a))
		tEntry.bind("<Return>",func= lambda event, a=2: self.enter(event,a))
		rEntry.focus_force()
	
	def enter(self,event,entryID):
		try:
			self.rounds=int(self.rEntry.get())
			self.partis=int(self.pEntry.get())
			self.team=int(self.tEntry.get())
			if self.team>0 and self.partis>0 and self.rounds>0:
				self.top.destroy()
				return
			ctypes.windll.user32.MessageBoxW(0, "Missing Value", "Alert", 1)
			return
		except ValueError:
			ctypes.windll.user32.MessageBoxW(0, "Error: Not a Number", "Alert", 1)
			return

#prompts the user to choose which code to run (used by verminTourneyHelper.py)
class pickCodeToRun(object):
	codeChoice=0
	def pick(self,choice):
		self.codeChoice=choice
		self.top.destroy()

	def __init__(self,master):
		top=self.top=Toplevel(master)
		self.top.attributes('-topmost',1)
		self.top.focus_force()
		#self.instLabel=Label(top,text="Pick code to run")
		#self.instLabel.grid(row=0,column=0)
		self.startButt=Button(top,text="Start Tourney",command=lambda a=0:self.pick(a))
		self.startButt.grid(row=0,column=0)
		self.teamNamesButt=Button(top,text="Add Team Names",command=lambda a=1:self.pick(a))
		self.teamNamesButt.grid(row=1,column=0)
		self.updateButt=Button(top,text="Update Bracket",command=lambda a=2:self.pick(a))
		self.updateButt.grid(row=2,column=0)

#Prompts the user to enter in a vermins name and stats after they pick their image from a big list of images (used in autoCrop.py)
#csvString on return = "name,Lifes,muscle, blast, gaurd, fast"
class enterStatsNamesWindow(object):
	statList=list()
	def enter(self,event):
		if(self.nameEntry.get()==""):
			self.statList=list()
			ctypes.windll.user32.MessageBoxW(0, "Missing Name", "Alert", 1)
			return
		self.statList.append(self.nameEntry.get())
		for i in range(0,5):
			self.statList.append(self.statEntry[i].get())
			try:
				float(self.statEntry[i].get())
				pass
			except ValueError:
				self.statList=list()
				ctypes.windll.user32.MessageBoxW(0, "Missing "+self.labelStr[i], "Alert", 1)
				return
		self.top.destroy()
	
	def __init__(self,master):
		self.statList=list()
		top=self.top=Toplevel(master)
		self.top.attributes('-topmost',1)
		self.top.focus_force()
		self.nameLabel=Label(top,text="Name: ")
		self.nameLabel.grid(row=0,column=0)
		self.nameEntry=Entry(top)
		self.nameEntry.focus_force()
		self.nameEntry.config(takefocus="0")
		self.nameEntry.bind("<Return>",self.enter)
		self.nameEntry.grid(row=0,column=1)
		self.labelStr=["Life: ","Musl: ","Blst: ","Gurd: ","Fast: "]
		self.statLabels=dict()
		self.statEntry=dict()
		for i in range(0,5):
			self.statLabels[i]=Label(top,text=self.labelStr[i])
			self.statLabels[i].grid(row=1,column=i*2)
			self.statEntry[i]=Entry(top)
			self.statEntry[i].bind("<Return>",self.enter)
			self.statEntry[i].grid(row=1,column=i*2+1)
	
class createTeamsWindow(object):
	def teamSelect(self,index):
		print(index)
		teamLabels=self.teamLabels
		teamLabels.append(Label(self.top,justify=LEFT))
		teamLabels[len(teamLabels)-1].config(image=self.images[index])
		teamLabels[len(teamLabels)-1].grid(row=1,column=len(teamLabels)-1)
		try:
			self.teamIndexList.append(int(self.csvDictList[index]['index']))
		except(ValueError):
			print("BAD TIMES ARE ABOUND")
		self.instruction.config(text="pick "+str(self.teamSize-len(self.teamIndexList))+" teamates")
		print("teamsize,TEAM LENGTH,index\n"+str((self.teamSize,len(self.teamIndexList),index)))
		if len(self.teamIndexList)>=self.teamSize:
			self.top.destroy()

	def __init__(self,master,csvDictList,teamSize):
		top=self.top=Toplevel(master)
		self.top.attributes('-topmost',1)
		self.top.focus_force()
		root=top
		self.csvDictList=csvDictList
		teamIndexList=self.teamIndexList=list()
		self.teamSize=teamSize
		teamLabels=self.teamLabels=list()
		butts=self.butts=list()
		images=self.images=list()
	
		instruction=self.instruction=Label(root,justify=LEFT,text="pick "+str(teamSize-1)+" teamates")
		self.instruction.grid(row=0,column=0)
		
		print(csvDictList[0]['stage1'][0])
		pic=cv2.imread(csvDictList[0]['stage1'][0],cv2.IMREAD_UNCHANGED)
		pic=cv2.resize(pic,(60,60))
		im=Image.fromarray(pic)
		self.images.append(ImageTk.PhotoImage(im))
		teamLabels.append(Label(root,justify=LEFT,text="hi"))
		teamLabels[0].config(image=images[0])
		teamLabels[0].grid(row=1,column=0)
		self.teamIndexList.append(int(csvDictList[0]['index']))
		index=1
		print(csvDictList[1:])
		print(len(images))
		for csvDict in csvDictList[1:]:
			print(index)
			print(csvDict)
			pic=cv2.imread(csvDict['stage1'][0],cv2.IMREAD_UNCHANGED)
			pic=cv2.resize(pic,(60,60))
			im=Image.fromarray(pic)
			self.images.append(ImageTk.PhotoImage(im))#ImageTk.PhotoImage(im)
			butts.append(Button(root,justify=LEFT))
			butts[index-1].config(image=self.images[index],width="60",height="60",command=lambda a=index: self.teamSelect(a))
			butts[index-1].grid(row=2+int(index/12),column=int(index%12))
			index+=1
		
