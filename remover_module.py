
import os
import time


# existing searches checker
def remover(maindir, items_to_remove):
    print("\n\n\n/====================================\\")
    print("Remover initiated")
    os.chdir(maindir)
    os.chdir("./csv files")

    for file in items_to_remove:
        fileName = file
        print(fileName)
        os.remove(fileName)
        print("File removed successfully")

    os.chdir(maindir)
    print("\====================================/\n\n")