
from bs4_module import getCarPriceChecker

import os
import csv
import time
import threading


# existing searches checker
def checker():
    print("\n\n\n/====================================\\")
    print("Checker initiated")

    # check for files to be checked
    with open("csvFilesIndex.txt", mode="r") as cFi:
        files = cFi.readlines()
        cFi.close()
    print(len(files), "files found")

    if len(files) == 0:
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
  
    print("Changes found:")
    for i in range(len(changes)):
        print("In file -", changes[i][0], "- at line ", changes[i][1], " by ", changes[i][2])
    
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
            newPrice = getCarPriceChecker(link)
            if(data[i + 1][3]) == newPrice:
                continue
            else:
                changedPrice = int(data[i + 1][3]) - newPrice
                changedPrice = -changedPrice

                # skip if price hasn't changed, else append the change
                if changedPrice == 0:
                    continue
                else:
                    dt = data[i + 1][-1]
                    if not int(changedPrice) == int(dt):
                        data[i + 1].append(changedPrice)
                        changesWriter.writerow([file , i + 1, changedPrice])

        # write data back to file
        csvWriter.writerows(data)
        csvFile.close()
    print(file, " checked\n")
    print(threadNumber, "executed in", time.time() - time_started)