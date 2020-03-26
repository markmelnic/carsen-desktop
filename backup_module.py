
import os
import time
import shutil
import datetime


def backup(maindir):
    #print("\n\n\n/====================================\\")
    print("\nBackup initiated")
    time.sleep(2)
    os.chdir(maindir)
    os.chdir('./csv files')

    # check for files to be backed up
    try:
        with open("csvFilesIndex.txt", mode="r") as cFi:
            files = cFi.readlines()
            cFi.close()

        if len(files) == 1:
            print(len(files), "file found")
        else:
            print(len(files), "files found")

        # change working directory and get the new one
        os.chdir(maindir)
        os.chdir('./backup')
        date = datetime.datetime.now()
        date = str(date)
        date = date.replace(':', '.')
        os.mkdir(str(date))

        if len(files) == 0:
            os.chdir(maindir)
            os.chdir('./backup')
            shutil.rmtree(date)
            os.chdir(maindir)
            print("Nothing to backup\n")
            #print("\====================================/\n\n")
            return
        else:
            os.chdir(maindir)
            os.chdir('./csv files')
            path = "../backup/" + date
            backup = shutil.copy("csvFilesIndex.txt", path)
            for file in files:
                file = file.strip("\n")
                try:
                    backup = shutil.copy(file, path)
                except:
                    print("File not found")

    except:
        print("Nothing to backup\n")
        os.chdir(maindir)
        return
    
    os.chdir(maindir)
    time.sleep(2)
    print("Backed up successfully\n")
    return date
    #print("\====================================/\n\n")