
import os
import time


# existing searches checker
def remover(maindir):
    print("\n\n\n/====================================\\")
    print("Remover initiated")
    os.chdir(maindir)

    files = []
    with os.scandir("./csv files") as entries:
        for entry in entries:
            if entry.is_file():
                files.append(entry.name)

    if len(files) != 0:
        print("Currently active files:")
        i = 1
        for entry in files:
            print(str(i) + ".", entry.strip("\n"))
            i += 1

        print("\nWhich search would you like to remove?")
        i = input("File number as appears in the list above: ")
        try:
            i = int(i) - 1
            fileName = files[i]

            try:
                print(fileName)
                os.chdir("./csv files")
                os.remove(fileName)
                print("File removed successfully")
            except:
                print("File inexistent")
        except:
            print("Execution canceled")

    else:
        print("No files to remove")

    os.chdir(maindir)
    print("\====================================/\n\n")