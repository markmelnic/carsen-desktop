
from mobile_de_module import getCarPriceChecker
from search_module import score
from backup_module import *

import os
import csv
import time
import shutil
import threading
from datetime import datetime


# existing searches checker
def checker(maindir):
    print("\n\n\n/====================================\\")
    print("Checker initiated")
    os.chdir(maindir)

    print("Backing up")
    date = backup(maindir)

    # check for files to be checked
    files = []
    os.chdir(maindir)
    try:
        with os.scandir("./csv files") as entries:
            files_to_ignore = ["<DirEntry 'changesTemp.csv'>", "<DirEntry 'changesTimestamp.txt'>", "<DirEntry 'favorites.csv'>", "<DirEntry 'favchangesTimestamp.txt'>", "<DirEntry 'favchangesTemp.csv'>"]
            files = []
            for entry in entries:
                if entry.is_file():
                    if not str(entry) in files_to_ignore:
                                files.append(entry.name)
    except:
        os.chdir(maindir)
        print("No files found")
        print("\====================================/\n\n")
        return

    os.chdir("./csv files")
    if len(files) == 0:
        os.chdir(maindir)
        print("Nothing to check")
        print("\====================================/\n\n")
        return
    else:
        threads = []
        i = 1
        # start processing every file
        with open("changesTemp.csv", mode="w", newline='') as changesFile:
            changesWriter = csv.writer(changesFile)
            for file in files:
                file = file.strip("\n")

                threadNumber = "Thread " + str(i)
                thread = threading.Thread(target = filesThread, args = (threadNumber, file, changesWriter))
                threads.append(thread)
                thread.start()
                i += 1

            # wait for all threads to finish
            for thread in threads:
                thread.join()
            print("All threads are finished")
            changesFile.close()

    # print changes
    with open("changesTemp.csv", mode="r", newline='') as changesFile:
        changesReader = csv.reader(changesFile)
        changes = list(changesReader)
        changesFile.close()

    if len(changes) == 0:
        print("No changes found")
    else:
        print("Changes found:")
        for i in range(len(changes)):
            print("value -", changes[i][0], "- link ", changes[i][1])
   
    with open("changesTimestamp.txt", mode="w", newline='') as timestampFile:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            timestampFile.write(dt_string)
            timestampFile.close()
            
    # remove backup folder if execution was successful
    os.chdir(maindir)
    os.chdir('./backup')
    shutil.rmtree(date)
    os.chdir(maindir)

    print("Checker executed successfully")
    print("\====================================/\n\n")


# threading files
def filesThread(threadNumber, file, changesWriter):
    time_started = time.time()
    print(threadNumber, "started at", time_started)

    try:
        # read file contents
        with open(file, mode="r", newline='') as csvFile:
            csvReader = csv.reader(csvFile)
            data = list(csvReader)
            csvFile.close()

        # get all links
        links = []
        for i in range(len(data) - 1):
            if not data[i + 1][0] in links:
                links.append(data[i + 1][0])
            else:
                print("Duplicate not included")

        # process every link
        with open(file, mode="w", newline='') as csvFile:
            csvWriter = csv.writer(csvFile)

            # check every link
            i = -1
            for link in links:
                i += 1
                if i == 0:
                    print(file, "-", i + 1, "ad checked")
                else:
                    print(file, "-", i + 1, "ads checked")

                # get new price and compare to existing one
                try:
                    newPrice = getCarPriceChecker(link)
                    firstPrice = int(data[i + 1][3])
                    if not firstPrice == newPrice:
                        data[i+1][3] = newPrice
                        changedPrice = firstPrice - newPrice
                        changedPrice = -changedPrice
                        # skip if price hasn't changed, else append the change
                        if not changedPrice == 0:
                            changesWriter.writerow([changedPrice, data[i+1][0], data[i+1][1], data[i+1][2], data[i+1][3], data[i+1][4], data[i+1][5], data[i+1][6]])
                except:
                    for temp in range(2):
                        time.sleep(2)
                        newPrice = getCarPriceChecker(link)
                        if not firstPrice == newPrice:
                            changedPrice = firstPrice - newPrice
                            changedPrice = -changedPrice
                            # skip if price hasn't changed, else append the change
                            if not changedPrice == 0:
                                changesWriter.writerow([changedPrice, data[i+1][0], data[i+1][1], data[i+1][2], data[i+1][3], data[i+1][4], data[i+1][5]])

            # write data back to file
            csvWriter.writerows(data)
            csvFile.close()
            score(file)
        print(file, " checked\n")
        print(threadNumber, "executed in", time.time() - time_started)
    except:
        print(file, " checked\n")
       
       
# favorites checker 
def favoritesChecker(maindir):
    print("\n\n\n/====================================\\")
    print("Checker initiated")
    os.chdir(maindir)

    print("Backing up")
    date = backup(maindir)
    
    os.chdir("./csv files")
    with open("favchangesTemp.csv", mode="w", newline='') as changesFile:
        changesWriter = csv.writer(changesFile)

        # read file contents
        with open("favorites.csv", mode="r", newline='') as csvFile:
            csvReader = csv.reader(csvFile)
            data = list(csvReader)
            csvFile.close()

        # get all links
        links = []
        for i in range(len(data) - 1):
            if not data[i + 1][0] in links:
                links.append(data[i + 1][0])
            else:
                print("Duplicate not included")

        # process every link
        with open("favorites.csv", mode="w", newline='') as csvFile:
            csvWriter = csv.writer(csvFile)

            # check every link
            i = -1
            for link in links:
                i += 1
                if i == 0:
                    print("favorites.csv", "-", i + 1, "ad checked")
                else:
                    print("favorites.csv", "-", i + 1, "ads checked")

                # get new price and compare to existing one
                try:
                    newPrice = getCarPriceChecker(link)
                    firstPrice = int(data[i + 1][3])
                    if not firstPrice == newPrice:
                        data[i+1][3] = newPrice
                        changedPrice = firstPrice - newPrice
                        changedPrice = -changedPrice
                        # skip if price hasn't changed, else append the change
                        if not changedPrice == 0:
                            changesWriter.writerow([changedPrice, data[i+1][0], data[i+1][1], data[i+1][2], data[i+1][3], data[i+1][4], data[i+1][5], data[i+1][6]])
                except:
                    for temp in range(2):
                        time.sleep(2)
                        newPrice = getCarPriceChecker(link)
                        if not firstPrice == newPrice:
                            changedPrice = firstPrice - newPrice
                            changedPrice = -changedPrice
                            # skip if price hasn't changed, else append the change
                            if not changedPrice == 0:
                                changesWriter.writerow([changedPrice, data[i+1][0], data[i+1][1], data[i+1][2], data[i+1][3], data[i+1][4], data[i+1][5]])

            # write data back to file
            csvWriter.writerows(data)
            csvFile.close()
            score("favorites.csv")
        print("favorites.csv", " checked\n")
            
    os.chdir(maindir)
    changesFile.close()
    
    os.chdir("./csv files")
    # print changes
    with open("favchangesTemp.csv", mode="r", newline='') as changesFile:
        changesReader = csv.reader(changesFile)
        changes = list(changesReader)
        changesFile.close()

    if len(changes) == 0:
        print("No changes found")
    else:
        print("Changes found:")
        for i in range(len(changes)):
            print("value -", changes[i][0], "- link ", changes[i][1])
   
    with open("favchangesTimestamp.txt", mode="w", newline='') as timestampFile:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            timestampFile.write(dt_string)
            timestampFile.close()
            
    # remove backup folder if execution was successful
    os.chdir(maindir)
    os.chdir('./backup')
    shutil.rmtree(date)
    os.chdir(maindir)

    print("Checker executed successfully")
    print("\====================================/\n\n")