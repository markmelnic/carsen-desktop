
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


# to be implemented
def loader():
    print("WIP")


def inputFunct():
    # inputs
    print("The Car Manufacturer input is mandatory, \nelse press ENTER to skip a field.\n")
    carMake = input("Car Manufacturer: ")
    carModel = input("Car Model: ")

    print("\nPrice range:")
    fromPrice = input("from: ")
    toPrice = input("to: ")

    print("\nRegistration years range:")
    fromReg = input("from: ")
    toReg = input("to: ")

    print("\nMileage range:")
    fromMiles = input("from: ")
    toMiles = input("to: ")

    print("\nEngine power range:")
    fromPower = input("from: ")
    toPower = input("to: ")

    return carMake, carModel, fromPrice, toPrice, fromReg, toReg, fromMiles, toMiles, fromPower, toPower

def main():
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

    # get links
    with open("links.txt", mode="w") as linksFile:
        threads = []
        for currentPage in range(converted_pagesnr):
            if currentPage == 0:
                currentURL = curURL(dv)
                killd(dv)
            threadNumber = "Thread " + str(currentPage)
            thread = threading.Thread(target = getCarLinksTemp, args = (threadNumber, currentURL, linksFile))
            threads.append(thread)
            thread.start()
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
    with open("links.txt", mode="r") as linksFile:
        #for line in linksFile:
        #    carLink.append(line)
        carLink = linksFile.readlines()
        linksFile.close()
    os.remove("links.txt")

    if len(carLink) == 0:
        print("No ads to process\n--------------------")
    elif len(carLink) == 1:
        print(len(carLink), "ad to process\n--------------------")
    else:
        print(len(carLink), "ads to process\n--------------------")

    # get data and write to csv
    '''
    try:
        os.remove("cars.csv")
        with io.open('cars.csv', 'w', encoding="utf-8", newline='') as csvFile:
            csvFile.close()
    except:
        None
    '''
    # output file name
    carMake = input[0]
    carModel = input[1]
    carMake = carMake.replace(" ", "-")
    carModel = carModel.replace(" ", "-")
    if carModel == "":
        fileName = carMake + ".csv"
    else:
        fileName = carMake + "_" + carModel + ".csv"

    with io.open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price", "Mileage", "Power (HP)"])
        # start threading for getting data
        threads = []
        for i in range(len(carLink)):
            threadNumber = "Thread " + str(i)
            thread = threading.Thread(target = getData, args = (threadNumber, carLink[i], csvWriter))
            threads.append(thread)
            thread.start()
            if len(threads) == 24:
                for thread in threads:
                    thread.join()
                threads = []

        # wait for all threads to finish execution
        for thread in threads:
            thread.join()
        print("All threads are finished")
        csvFile.close()


if __name__ == '__main__':
    time_started = time.time()
    main()
    print("\n\nTotal execution time = ", time.time() - time_started)