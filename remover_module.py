
import os
import time


# existing searches checker
def remover(maindir, items_to_remove):
    print("\n\n\n/====================================\\")
    print("Remover initiated")
    os.chdir(maindir)
    os.chdir("./csv files")

    try:
        for file in items_to_remove:
            print(file, "is being removed")
            fileName = file
            print(fileName)
            os.remove(fileName)
            print("File removed successfully")
    except:
        print("Error, probably no file provided")

    os.chdir(maindir)
    print("\====================================/\n\n")