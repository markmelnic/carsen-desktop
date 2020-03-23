
import keyboard

from search_module import *
from checker_module import *
from remover_module import *


# main function
if __name__ == '__main__':
    while True:
        #time_started = time.time()
        #print("\n\nTotal execution time = ", time.time() - time_started)
        print("\n\n==================================")
        print("Press 1 for initiating a new search")
        print("      2 for checking existing ones")
        print("      3 for removing a search")
        print("      X to exit")
        #print("     4 for stopping the program")
        while True:
            # searcher
            if keyboard.is_pressed('F1'):
                search()
                break
            # checker
            if keyboard.is_pressed('F2'):
                checker()
                break
            # remover
            if keyboard.is_pressed('F3'):
                remover()
                break
            '''
            # exit
            if keyboard.is_pressed('x'):
                break
            '''