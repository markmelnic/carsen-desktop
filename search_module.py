
from mobile_de import *
from popups_module import *

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
    if carMake.lower() == 'any':
        carMake = ''
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
        for currentPage in range(20):
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
    car_links = []
    with open(linksFileName, mode="r") as linksFile:
        #for line in linksFile:
        #    carLink.append(line)
        car_links = linksFile.readlines()
        linksFile.close()
    os.remove(linksFileName)

    if len(car_links) == 0:
        print("No ads to process")
        Warnings.noadsfound()
        os.chdir(maindir)
        print("\====================================/\n\n")
        return
    elif len(car_links) == 1:
        print(len(car_links), "ad to process\n--------------------")
    else:
        print(len(car_links), "ads to process\n--------------------")

    os.chdir(maindir)
    os.chdir('./csv files')

    # output file name
    fileName = carMake + "_" + carModel + "_" + firstinput[2] + "-" + firstinput[3] + "_" + firstinput[4] + "-" + firstinput[5] + "_" + firstinput[6] + "-" + firstinput[7] + "_" + firstinput[8] + "-" + firstinput[9] + ".csv"

    with open(fileName, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Score"])
        # start threading for getting data
        threads = []
        for link in car_links:
            threadNumber = "Thread " + str(car_links.index(link))
            thread = threading.Thread(target = getData, args = (threadNumber, link, csvWriter))
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
def getCarLinksTemp(thread_number, current_url, links_file):
    time_started = time.time()
    print(thread_number, "started at", time_started)
    carLinks = getCarLinks(current_url)
    for item in carLinks:
        links_file.write("%s\n" % item)
    print(thread_number, "executed in", time.time() - time_started)


# get data from links
def getData(thread_number, car_link, csv_writer):
    time_started = time.time()
    print(thread_number, "started at", time_started)
    data = getCarData(car_link)
    csv_writer.writerow([car_link , data[0], data[1], data[2], data[3], data[4]])
    print(thread_number, "executed in", time.time() - time_started)


# give scores
def score(file_name):
    # read file contents
    with open(file_name, mode="r", newline='') as csvFile:
        csvReader = csv.reader(csvFile)
        data = list(csvReader)
        data.pop(0)
        csvFile.close()

    # getting data
    regs_list = []
    prices_list = []
    miles_list = []
    for dat in data:
        regs_list.append(int(dat[2]))
        prices_list.append(int(dat[3]))
        miles_list.append(int(dat[4]))

    # calculating price score
    min_price = min(prices_list)
    max_price = max(prices_list)

    #multiplier = 3.333
    multiplier = 1
    
    price_scores = []
    for price in prices_list:
        try:
            price_scores.append((1 - ((price - min_price) / (max_price - min_price))) * multiplier)
        except:
            price_scores.append(1)

    # reg score
    min_reg = min(regs_list)
    max_price = max(regs_list)
    
    reg_scores = []
    for reg in regs_list:
        try:
            reg_scores.append(((reg - min_reg) / (max_price - min_reg)) * multiplier)
        except Exception as e:
            reg_scores.append(0)

    # mileage score
    min_miles = min(miles_list)
    max_miles = max(miles_list)

    miles_scores = []
    milTempScore = []
    for mil in miles_list:
        try:
            miles_scores.append((1 - (mil - min_miles) / (max_miles - min_miles)) * multiplier)
        except:
            miles_scores.append(1)

    # final score
    final_score = []
    for pricesc, mileagesc, regsc in zip(price_scores, miles_scores, reg_scores):
        final_score.append(pricesc + mileagesc + regsc)

    
    with open(file_name, 'w', encoding="utf-8", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Ad Link", "Title", "Reg. Year", "Price (EUR)", "Mileage (km)", "Power (HP)", "Score"])
        for dat, score in zip(data, final_score):
            csvWriter.writerow([dat[0], dat[1], dat[2], dat[3], dat[4], dat[5], score])
        csvFile.close()