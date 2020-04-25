
import os
import sys
import time
import msvcrt
import keyboard

# import modules
from tkinter_module import *

# create folders
def folderStruct(maindir):
    os.mkdir("backup")
    os.mkdir("csv files")
    os.chdir(maindir)

# main function
if __name__ == '__main__':
    maindir = os.getcwd()

    try:
        folderStruct(maindir)
    except:
        None

    root = Interface()
    mainloop()

    sys.exit(0)
