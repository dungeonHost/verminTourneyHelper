import glob
import os
import PIL
import cv2
import numpy as np
file_name = "test.png"
import tkinter as tk
from autoBracket import autoBracket
from popupWindows import *
from csvToDicts import *

p=dict()
p['hi']='hi'
p['bye']=['bye',25]
for i in p:
	print(i)