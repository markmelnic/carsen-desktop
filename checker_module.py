
from bs4_module import getCarPriceChecker
from backup_module import *

import os
import csv
import time
import threading


# existing searches checker
def checker(maindir):
    print("\n\n\n/====================================\\")
    print("Checker initiated")
    os.chdir(maindir)
    os.chdir('./csv files')

    print("Backing up")
    date = backup(maindir)

    os.chdir('./csv files')
    # check for files to be checked
    try:
        with open("csvFilesIndex.txt", mode="r") as cFi:
            files = cFi.readlines()
            cFi.close()

        if len(files) == 1:
            print(len(files), "file found")
        else:
            print(len(files), "files found")
    except:
        os.chdir(maindir)
        print("No files to found")
        print("\====================================/\n\n")
        return

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
                # limit parallel threads number
                '''
                if len(threads) == 10:
                    for thread in threads:
                        thread.join()
                    threads = []
                '''
            for thread in threads:
                thread.join()
            print("All threads are finished")
            changesFile.close()

    # print changes
    with open("changesTemp.csv", mode="r", newline='') as changesFile:
        changesReader = csv.reader(changesFile)
        changes = list(changesReader)
        changesFile.close()
    os.remove("changesTemp.csv")
  
    ind = 0
    if len(changes) == 0:
        print("No changes found")
    else:
        print("Changes found:")
        for i in range(len(changes)):
            try:
                if (int(changes[i][0]) == 0) and (int(changes[i][1]) == 0) and (int(changes[i][2]) == 0):
                    ind += 1
                else:
                    print("In file -", changes[i][0], "- at line ", changes[i][1], " by ", changes[i][2])
            except:
                print("In file -", changes[i][0], "- at line ", changes[i][1], " by ", changes[i][2])

    if not ind == 0:
        print(ind, "ads removed")
    
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

    # read file contents
    with open(file, mode="r", newline='') as csvFile:
        csvReader = csv.reader(csvFile)
        data = list(csvReader)
        csvFile.close()

    # process every link
    with open(file, mode="w", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        links = []
        for i in range(len(data) - 1):
            links.append(data[i + 1][0])

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
                if(firstPrice) == newPrice:
                    continue
                else:
                    changedPrice = firstPrice - newPrice
                    changedPrice = -changedPrice

                    # skip if price hasn't changed, else append the change
                    if not changedPrice == 0:
                        try:
                            if not int(changedPrice) == int(data[i + 1][6]):
                                if not firstPrice == newPrice:
                                    data[i + 1].append(changedPrice)
                                    changesWriter.writerow([file , i + 1, changedPrice])
                        except:
                            if not firstPrice == newPrice:
                                data[i + 1].append(changedPrice)
                                changesWriter.writerow([file , i + 1, changedPrice])
            except:
                try:
                    for temp in range(2):
                        time.sleep(2)
                        newPrice = getCarPriceChecker(link)
                        if(firstPrice) == newPrice:
                            continue
                        else:
                            changedPrice = firstPrice - newPrice
                            changedPrice = -changedPrice

                            # skip if price hasn't changed, else append the change
                            if not changedPrice == 0:
                                try:
                                    if not int(changedPrice) == int(data[i + 1][6]):
                                        if not firstPrice == newPrice:
                                            data[i + 1].append(changedPrice)
                                            changesWriter.writerow([file , i + 1, changedPrice])
                                except:
                                    if not firstPrice == newPrice:
                                        data[i + 1].append(changedPrice)
                                        changesWriter.writerow([file , i + 1, changedPrice])
                except:
                    print("*ad removed*")
                    data.pop(i + 1)
                    i -= 1
                    changesWriter.writerow([0 , 0, 0])

        # write data back to file
        csvWriter.writerows(data)
        csvFile.close()
    print(file, " checked\n")
    print(threadNumber, "executed in", time.time() - time_started)