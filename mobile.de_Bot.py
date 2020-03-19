
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
    tmp = getCarData(carLink)
    carTitle = tmp[0]
    carPrice = tmp[1]
    carReg = tmp[2]
    carMiles = tmp[3]
    csvWriter.writerow([carLink ,carReg, carTitle, carPrice, carMiles])
    print(threadNumber, "executed in", time.time() - time_started)
        

def main():
    # ================== initialization ==================
    carMake = input("Car Manufacturer: ")
    carModel = input("Car Model: ")
    dv = boot()
    startSearcher(dv)
    firstSearch(dv, carMake, carModel)

    currentURL = curURL(dv)
    converted_pagesnr = getNr(currentURL)
    if converted_pagesnr == 1:
        print(converted_pagesnr, "page to be scanned")
    else:
        print(converted_pagesnr, "pages to be scanned")

    # get links
    carLink  = []
    for currentPage in range(converted_pagesnr):
        if currentPage == 0:
            currentURL = curURL(dv)
            killd(dv)
        carLinksCurrentPage = getCarLinks(currentURL)
        for i in range(len(carLinksCurrentPage)):
            carLink.append(carLinksCurrentPage[i])
        currentURL = nextPage(dv, currentURL, currentPage)
        if currentPage == 0:
            print(currentPage + 1, "page processed")
        else:
            print(currentPage + 1, "pages processed")

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

    with io.open('cars.csv', 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Reg. Year", "Title", "Price", "Mileage"])
        threads = []
        for i in range(len(carLink)):
            #time.sleep(0.4)
            threadNumber = "Thread " + str(i)
            thread = threading.Thread(target = getData, args = (threadNumber, carLink[i], csvWriter))
            threads.append(thread)
            thread.start()
            if len(threads) == 32:
                for thread in threads:
                    thread.join()
                threads = []

        for thread in threads:
            thread.join()
        print("All threads are finished")
        csvFile.close()


if __name__ == '__main__':
    time_started = time.time()
    main()
    print("\n\nTotal execution time = ", time.time() - time_started)