
# configure whether the console window will display
import pywintypes
import win32gui
import win32con
with open('./resources/settings.txt', mode='r') as st:
    settings = st.readlines()
    window_show = int(settings[1])
    st.close()
    if window_show == 0:
        tpth = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(tpth, win32con.SW_HIDE)

import os
import sys
import time
import msvcrt
import keyboard

from backup_module import *
from search_module import *
from tkinter_module import *
from checker_module import *
from remover_module import *


# create folders
def folderStruct(maindir):
    os.mkdir("backup")
    os.mkdir("csv files")
    os.chdir('./csv files')
    #os.mkdir("search parameters")
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
