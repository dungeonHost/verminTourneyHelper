import glob
import os
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *

#ab=autoBracket(5,1,2)
#ab.createBracket()
root=tk.Tk()
ets=enterTourneySize(root)
root.wait_window(ets.top)
Label(root,text=str(ets.team)+" "+str(ets.partis)+" "+str(ets.rounds)).pack()
root.mainloop()