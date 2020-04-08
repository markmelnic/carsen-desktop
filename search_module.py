
from bs4_module import *
from selenium_module import *

import os
import io
import csv
import time
import threading


def search(maindir, srcInput):
    print("\n\n\n/====================================\\")
    print("\nSearcher initiated")
    os.chdir(maindir)
    os.chdir('./csv files')

    # ================== initialization ==================
    # inputs
    #firstinput = inputFunct()
    firstinput = srcInput

    # program start
    dv = boot()
    startSearcher(dv)
    firstSearch(dv, firstinput)

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
        firstSearch(dv, firstinput)
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
    carMake = firstinput[0]
    carModel = firstinput[1]
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

    if len(carLink) == 0:
        print("No ads to process")
        print("\====================================/\n\n")
        return
    elif len(carLink) == 1:
        print(len(carLink), "ad to process\n--------------------")
    else:
        print(len(carLink), "ads to process\n--------------------")

    # search parameters file
    os.chdir('./search parameters')

    if carModel == "":
        paramsFileName = "params_" + carMake + ".txt"
    else:
        paramsFileName = "params_" + carMake + "_" + carModel + ".txt"

    with open(paramsFileName, mode="w") as paramsFile:
        paramsFile.write("%s\n" % firstinput[0])
        paramsFile.write("%s\n" % firstinput[1])
        paramsFile.write(firstinput[2] + "-" + firstinput[3] + "\n")
        paramsFile.write(firstinput[4] + "-" + firstinput[5] + "\n")
        paramsFile.write(firstinput[6] + "-" + firstinput[7] + "\n")
        paramsFile.write(firstinput[8] + "-" + firstinput[9] + "\n")
        paramsFile.close()

    os.chdir(maindir)
    os.chdir('./csv files')
    # output file name
    if carModel == "":
        fileName = carMake + ".csv"
    else:
        fileName = carMake + "_" + carModel + ".csv"

    with open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Score", "Price change since first search"])
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

    print("Giving scores to vehicles")
    score(fileName)
    #except:
    #   print("Can not calculate score, possible error")

    os.chdir(maindir)
    print("Search executed successfully")
    print("\====================================/\n\n")


# initial input function
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


# get temporary car links
def getCarLinksTemp(threadNumber, currentURL, linksFile):
    time_started = time.time()
    print(threadNumber, "started at", time_started)
    carLinks = getCarLinks(currentURL)
    for item in carLinks:
        linksFile.write("%s\n" % item)
    print(threadNumber, "executed in", time.time() - time_started)


# get data from links
def getData(threadNumber, carLink, csvWriter):
    time_started = time.time()
    print(threadNumber, "started at", time_started)
    data = getCarData(carLink)
    csvWriter.writerow([carLink , data[0], data[1], data[2], data[3], data[4]])
    print(threadNumber, "executed in", time.time() - time_started)

# give scores
def score(fileName):
    # read file contents
    with open(fileName, mode="r", newline='') as csvFile:
        csvReader = csv.reader(csvFile)
        data = list(csvReader)
        data.pop(0)
        csvFile.close()

    # getting data
    allReg = []
    allPrices = []
    allMiles = []
    for dat in data:
        allReg.append(int(dat[2]))
        allPrices.append(int(dat[3]))
        allMiles.append(int(dat[4]))

    # calculating price score
    minPrice = min(allPrices)
    maxPrice = max(allPrices)

    priceScore = []
    for price in allPrices:
        priceScore.append((1 - ((price - minPrice) / (maxPrice - minPrice))) / 1.5)

    # reg score
    minReg = min(allReg)
    maxReg = max(allReg)
    
    regScore = []
    for reg in allReg:
        regScore.append(((reg - minReg) / (maxReg - minReg)) / 4)

    # mileage score
    minMiles = min(allMiles)
    maxMiles = max(allMiles)

    milScore = []
    milTempScore = []
    for mil, reg in zip(allMiles, allReg):
        milTempScore.append((mil / 13500) - (2020 - reg))

    tmax = max(milTempScore)
    tmin = min(milTempScore)
    for sc in milTempScore:
        if sc < 0:
            milScore.append(1 - sc)
        else:
            milScore.append(1 - ((sc - tmin) / (tmax - tmin)))

    # final score
    fScore = []
    for pricesc, mileagesc, regsc in zip(priceScore, milScore, regScore):
        fScore.append(pricesc + mileagesc + regsc)

    
    with open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Score", "Price change since first search"])
        for dat, score in zip(data, fScore):
            csvWriter.writerow([dat[0], dat[1], dat[2], dat[3], dat[4], dat[5], score])
        csvFile.close()