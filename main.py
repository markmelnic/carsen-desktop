
import time
import msvcrt
import keyboard

from backup_module import *
from search_module import *
from checker_module import *
from remover_module import *


# main function
if __name__ == '__main__':
    maindir = os.getcwd()
    x = 0
    while True:
        if x == 1:
            break
        #time_started = time.time()
        #print("\n\nTotal execution time = ", time.time() - time_started)
        print("\n\n/====================================\\")
        print("|Press F1 to initiate a new search   |")
        print("|      F2 to check existing searches |")
        print("|      F3 to remove a search         |")
        print("|      F4 to backup (recommended)    |")
        print("|      X to exit                     |")
        print("\====================================/", end = '')
        #print("     4 for stopping the program")
        while True:
            msvcrt.getch()
            # searcher
            if keyboard.is_pressed('F1'):
                search(maindir)
                break
            # checker
            elif keyboard.is_pressed('F2'):
                checker(maindir)
                break
            # remover
            elif keyboard.is_pressed('F3'):
                remover(maindir)
                break
            # remover
            elif keyboard.is_pressed('F4'):
                backup(maindir)
                break
            # exit
            elif keyboard.is_pressed('x'):
                x = 1
                break