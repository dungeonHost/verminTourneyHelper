from cx_Freeze import setup,Executable
import os
import sys

os.environ['TCL_LIBRARY'] = r'C:\Users\Jeff\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Jeff\AppData\Local\Programs\Python\Python36\tcl\tk8.6'
base=None

executabls=[Executable("verminTourneyHelper.py",base=base)]
build_exe_options={"packages":["os","tkinter","PIL","numpy"],"include_files":[r"C:\Users\Jeff\AppData\Local\Programs\Python\Python36\DLLs\tcl86t.dll", r"C:\Users\Jeff\AppData\Local\Programs\Python\Python36\DLLs\tk86t.dll"]}
print(executabls)

packages=["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "<any name>",
    options = {"build_exe":build_exe_options},
    version = "<any number>",
    description = '<any description>',
    executables = executabls
)