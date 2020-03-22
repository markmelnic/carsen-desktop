
from search_module import *
from checker_module import *
from remover_module import *


# main function
if __name__ == '__main__':
    #time_started = time.time()
    #print("\n\nTotal execution time = ", time.time() - time_started)
    print("\n\n==================================")
    print("Type 1 for initiating a new search")
    print("     2 for checking existing ones")
    print("     3 for removing a search")
    #print("     4 for stopping the program")
    inp = input("Input: ")
    prompter = int(inp)
    if prompter == 1:
        search()
    elif prompter == 2:
        checker()
    elif prompter == 3:
        remover()
    else:
        print("Incorrect input")
