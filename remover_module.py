
import os
import time


# existing searches checker
def remover(maindir, file_to_remove):
    print("\n\n\n/====================================\\")
    print("Remover initiated")
    os.chdir(maindir)
    os.chdir("./csv files")

    try:
        print(file_to_remove, "is being removed")
        fileName = file_to_remove
        print(fileName)
        os.remove(fileName)
        print("File removed successfully")
    except:
        print("Error, probably no file provided")

    os.chdir(maindir)
    print("\====================================/\n\n")