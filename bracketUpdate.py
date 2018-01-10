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

def bracketUpdate():
	os.chdir("bracket")
	points,[numTeams,numRounds,numPartis]=metaBracketReader.readBracketMetaData("bracketMetaData.csv")
	print("DSFD "+str(numTeams)+" "+str(numRounds)+" "+str(numPartis))
	print(points)
	
bracketUpdate()