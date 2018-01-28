import tkinter as tk
from tkinter import *
import bracketUpdate
import tourneyHelper
import setTeamNames
from popupWindows import pickCodeToRun


root=tk.Tk()
pctr=pickCodeToRun(root)
root.wait_window(pctr.top)
choice=pctr.codeChoice
root.destroy()
if choice==0:
	tourneyHelper.tourneyHelper()
elif choice==1:
	setTeamNames.setTeamNames()
elif choice==2:
	bracketUpdate.bracketUpdate()