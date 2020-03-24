
import os
import time
import shutil
import datetime


def backup():
    #print("\n\n\n/====================================\\")
    print("\nBackup initiated")
    time.sleep(2)
    maindir = os.getcwd()
    os.chdir('./csv files')

    # check for files to be backed up
    with open("csvFilesIndex.txt", mode="r") as cFi:
        files = cFi.readlines()
        cFi.close()
    print(len(files), "files found")

    # change working directory and get the new one
    os.chdir(maindir)
    os.chdir('./backup')
    date = datetime.datetime.now()
    date = str(date)
    date = date.replace(':', '.')
    os.mkdir(str(date))

    if len(files) == 0:
        print("Nothing to backup")
        print("\====================================/\n\n")
        return
    else:
        os.chdir(maindir)
        os.chdir('./csv files')
        path = "../backup/" + date
        backup = shutil.copy("csvFilesIndex.txt", path)
        for file in files:
            file = file.strip("\n")
            backup = shutil.copy(file, path)

    os.chdir(maindir)
    time.sleep(2)
    print("Backed up successfully\n")
    #print("\====================================/\n\n")