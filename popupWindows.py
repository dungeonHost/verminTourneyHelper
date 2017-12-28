import tkinter as tk
from tkinter import *
import sys
import ctypes  # An included library with Python install.   

class enterStatsNamesWindow(object):
	csvString=""
	def enter(self,event):
		if(self.nameEntry.get()==""):
			self.csvString=""
			ctypes.windll.user32.MessageBoxW(0, "Missing Name", "Alert", 1)
			return
		self.csvString+=self.nameEntry.get()
		for i in range(0,5):
			self.csvString+=","+self.statEntry[i].get()
			if(self.statEntry[i].get()==""):
				self.csvString=""
				ctypes.windll.user32.MessageBoxW(0, "Missing "+self.labelStr[i], "Alert", 1)
				return
			try:
				float(self.statEntry[i].get())
				pass
			except ValueError:
				self.csvString=""
				ctypes.windll.user32.MessageBoxW(0, "Missing "+self.labelStr[i], "Alert", 1)
				return
		self.csvString+=","
		self.top.destroy()
	
	def __init__(self,master):
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
	