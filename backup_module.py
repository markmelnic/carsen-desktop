
import os
import time
import shutil
import datetime


def backup(maindir):
    print("\nBackup initiated")
    os.chdir(maindir)

    # check for files to be backed up
    files = []
    with os.scandir("./csv files") as entries:
        for entry in entries:
            if entry.is_file():
                files.append(entry.name)

    # change working directory and get the new one
    try:
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
            return
        else:
            os.chdir(maindir)
            os.chdir('./csv files')
            path = "../backup/" + date
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
    print("Backed up successfully\n")
    return date
