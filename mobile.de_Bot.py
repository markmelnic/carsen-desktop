
#from main import *
from bs4_module import *
from selenium_module import *

import os
import io
import csv
import time
import threading


def getData(threadNumber, carLink, csvWriter):
    time_started = time.time()
    print(threadNumber, "started at", time_started)
    data = getCarData(carLink)
    csvWriter.writerow([carLink , data[0], data[1], data[2], data[3], data[4]])
    print(threadNumber, "executed in", time.time() - time_started)
        

def getCarLinksTemp(threadNumber, currentURL, linksFile):
    time_started = time.time()
    print(threadNumber, "started at", time_started)
    carLinks = getCarLinks(currentURL)
    for item in carLinks:
        linksFile.write("%s\n" % item)
    print(threadNumber, "executed in", time.time() - time_started)

'''
# to be implemented
def loader():
'''

def inputFunct():
    # inputs
    print("\nThe Car Manufacturer input is mandatory,")
    print("else press ENTER to skip a field.")
    print("For maximal efficiency try to filter the search enough to get less than 1000 results\n")
    
    carMake = input("Car Manufacturer: ")
    carModel = input("Car Model: ")

    print("\nPrice range:")
    fromPrice = input("from - ")
    toPrice = input("to - ")

    print("\nRegistration years range:")
    fromReg = input("from - ")
    toReg = input("to - ")

    print("\nMileage range:")
    fromMiles = input("from - ")
    toMiles = input("to - ")

    print("\nEngine power range:")
    fromPower = input("from - ")
    toPower = input("to - ")

    return carMake, carModel, fromPrice, toPrice, fromReg, toReg, fromMiles, toMiles, fromPower, toPower


def searcher():
    print("\nSearcher initiated")
    # ================== initialization ==================
    # inputs
    input = inputFunct()

    # program start
    dv = boot()
    startSearcher(dv)
    firstSearch(dv, input)

    currentURL = curURL(dv)
    getNumber = getNr(currentURL)
    try:
        converted_pagesnr = getNumber[0]
        adsCheck = getNumber[1]
    except:
        converted_pagesnr = getNumber
        adsCheck = 21

    if (converted_pagesnr == 1) and (adsCheck > 20):
        print("Possible error, trying again...")
        # retry
        dv = boot()
        startSearcher(dv)
        firstSearch(dv, input)
        currentURL = curURL(dv)
        getNumber = getNr(currentURL)
        try:
            converted_pagesnr = getNumber[0]
            adsCheck = getNumber[1]
        except:
            None

    if converted_pagesnr == 1:
        print("\n", converted_pagesnr, "page to process")
    else:
        print("\n", converted_pagesnr, "pages to process")

    # create file name
    carMake = input[0]
    carModel = input[1]
    carMake = carMake.replace(" ", "-")
    carModel = carModel.replace(" ", "-")
    if carModel == "":
        linksFileName = carMake + ".txt"
    else:
        linksFileName = carMake + "_" + carModel + ".txt"

    # get links
    with open(linksFileName, mode="w") as linksFile:
        threads = []
        for currentPage in range(converted_pagesnr):
            if currentPage == 0:
                currentURL = curURL(dv)
                killd(dv)
            threadNumber = "Thread " + str(currentPage)
            thread = threading.Thread(target = getCarLinksTemp, args = (threadNumber, currentURL, linksFile))
            threads.append(thread)
            thread.start()

            # limit parallel threads number
            if len(threads) == 4:
                for thread in threads:
                    thread.join()
                threads = []
            currentURL = nextPage(dv, currentURL, currentPage)

        # wait for all threads to finish execution
        for thread in threads:
            thread.join()
        print("All threads are finished")
        linksFile.close()

    # get links to variable
    carLink = []
    with open(linksFileName, mode="r") as linksFile:
        #for line in linksFile:
        #    carLink.append(line)
        carLink = linksFile.readlines()
        linksFile.close()
    os.remove(linksFileName)
    #os.remove("links.txt")

    if len(carLink) == 0:
        print("No ads to process\n--------------------")
    elif len(carLink) == 1:
        print(len(carLink), "ad to process\n--------------------")
    else:
        print(len(carLink), "ads to process\n--------------------")

    # output file name
    if carModel == "":
        fileName = carMake + ".csv"
    else:
        fileName = carMake + "_" + carModel + ".csv"
    
    # add filename to files index
    with open("csvFilesIndex.txt", mode="a+") as cFi:
        cFi.write("%s\n" % fileName)
        cFi.close()

    with io.open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Price change since first search"])
        # start threading for getting data
        threads = []
        for i in range(len(carLink)):
            threadNumber = "Thread " + str(i)
            thread = threading.Thread(target = getData, args = (threadNumber, carLink[i], csvWriter))
            threads.append(thread)
            thread.start()

            # limit parallel threads number
            if len(threads) == 24:
                for thread in threads:
                    thread.join()
                threads = []

        # wait for all threads to finish execution
        for thread in threads:
            thread.join()
        print("All threads are finished")
        csvFile.close()

# existing searches checker
def checker():
    print("\nChecker initiated")
    # check for files to be checked
    with open("csvFilesIndex.txt", mode="r") as cFi:
        files = cFi.readlines()
        cFi.close()

    for file in files:
        file = file.strip("\n")

        with open(file, mode="r", newline='') as csvFile:
            csvReader = csv.reader(csvFile)
            data = list(csvReader)
            csvFile.close()

        with open(file, mode="w", newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            links = []
            for i in range(len(data) - 1):
                links.append(data[i + 1][0])

            i = -1
            for link in links:
                i += 1
                if i == 0:
                    print(i + 1, "ad checked")
                else:
                    print(i + 1, "ads checked")
                newPrice = getCarPriceChecker(link)

                if(data[i + 1][3]) == newPrice:
                    continue
                else:
                    changedPrice = int(data[i + 1][3]) - newPrice
                    data[i + 1].pop(6)
                    if changedPrice > 0:
                        changedPrice = -changedPrice
                        data[i + 1].append(changedPrice)
                    else:
                        data[i + 1].append("+" + str(changedPrice))
             
            csvWriter.writerows(data)
            csvFile.close()
    print("Checker executed successfully")


# existing searches checker
def remover():
    print("\nRemover initiated")
    print("\nWhich search would you like to remove?")
    fileName = input("File Name (without .csv extension): ")
    fileName = fileName + ".csv"

    # open file to read lines
    with open("csvFilesIndex.txt", mode="r") as cFi:
        lines = cFi.readlines()
        cFi.close()

    # rewrite file without removed filename
    with open("csvFilesIndex.txt", "w") as cFi:
        for line in lines:
            if line.strip("\n") != fileName:
                cFi.write(line)
    try:
        os.remove(fileName)
        print("File removed successfully")
    except:
        print("File inexistent")


if __name__ == '__main__':
    #time_started = time.time()
    #print("\n\nTotal execution time = ", time.time() - time_started)
    print("\n\n==================================")
    print("Type 1 for initiating a new search")
    print("     2 for checking existing ones")
    print("     3 for removing a search")
    #print("     4 for stopping the program")
    inp = input("Input: ")
    prompter = int(inp)
    if prompter == 1:
        searcher()
    elif prompter == 2:
        checker()
    elif prompter == 3:
        remover()
    else:
        print("Incorrect input")