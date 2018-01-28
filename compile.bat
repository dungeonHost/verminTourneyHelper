@echo off
set TCL_LIBRARY=C:\Users\Jeff\AppData\Local\Programs\Python\Python36\tcl\tcl8.6
set TK_LIBRARY=C:\Users\Jeff\AppData\Local\Programs\Python\Python36\tcl\tk8.6
//cxfreeze "C:\Users\VergilTheHuragok\PythonProjects\Name\main\main.py" --target-dir "C:\Users\VergilTheHuragok\Desktop\CompiledPythonProjects\build" --target-name "launch.exe"
python setup.py build
pause