
from mobile_de_module import *

import os
import io
import csv
import time
import threading

# initiate search
def search(maindir, srcInput):
    print("\n\n\n/====================================\\")
    print("\nSearcher initiated")
    os.chdir(maindir)
    os.chdir('./csv files')
    csvdir = os.getcwd()
    
    # ================== initialization ==================
    # inputs
    firstinput = srcInput

    currentURL = firstURL(maindir, csvdir, firstinput)
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
        currentURL = firstURL(maindir, csvdir, firstinput)
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
        for currentPage in range(1, converted_pagesnr + 1):
            threadNumber = "Thread " + str(currentPage)
            thread = threading.Thread(target = getCarLinksTemp, args = (threadNumber, currentURL, linksFile))
            threads.append(thread)
            thread.start()

            # limit parallel threads number
            if len(threads) == 4:
                for thread in threads:
                    thread.join()
                threads = []
            
            currentURL = nextPage(currentURL, currentPage)

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
        os.chdir(maindir)
        print("\====================================/\n\n")
        return
    elif len(carLink) == 1:
        print(len(carLink), "ad to process\n--------------------")
    else:
        print(len(carLink), "ads to process\n--------------------")

    os.chdir(maindir)
    os.chdir('./csv files')

    # output file name
    fileName = carMake + "_" + carModel + "_" + firstinput[2] + "-" + firstinput[3] + "_" + firstinput[4] + "-" + firstinput[5] + "_" + firstinput[6] + "-" + firstinput[7] + "_" + firstinput[8] + "-" + firstinput[9] + ".csv"

    with open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Score"])
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
                    if len(threads) < 23:
                        threads.pop(thread)
                        break
                threads = []

        # wait for all threads to finish execution
        for thread in threads:
            thread.join()
        print("All threads are finished")
        csvFile.close()

    os.chdir(maindir)
    os.chdir('./csv files')
    print("Giving scores to vehicles")
    score(fileName)
    #except:
    #   print("Can not calculate score, possible error")
    os.chdir(maindir)
    print("Search executed successfully")
    print("\====================================/\n\n")
    return fileName


# initial input function (console)
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
        priceScore.append(1 - ((price - minPrice) / (maxPrice - minPrice)))

    # reg score
    minReg = min(allReg)
    maxReg = max(allReg)
    
    regScore = []
    for reg in allReg:
        regScore.append(1 - (reg - minReg) / (maxReg - minReg))

    # mileage score
    minMiles = min(allMiles)
    maxMiles = max(allMiles)

    milScore = []
    milTempScore = []
    for mil in allMiles:
        milScore.append(1 - (mil - minMiles) / (maxMiles - minMiles))

    '''
    tmax = max(milTempScore)
    tmin = min(milTempScore)
    for sc in milTempScore:
        if sc < 0:
            milScore.append(1 - sc)
        else:
            milScore.append(1 - ((sc - tmin) / (tmax - tmin)))
    '''

    # final score
    fScore = []
    for pricesc, mileagesc, regsc in zip(priceScore, milScore, regScore):
        fScore.append(pricesc + mileagesc + regsc)

    
    with open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Score"])
        for dat, score in zip(data, fScore):
            csvWriter.writerow([dat[0], dat[1], dat[2], dat[3], dat[4], dat[5], score])
        csvFile.close()