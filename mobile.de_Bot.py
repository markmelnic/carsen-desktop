
from bs4_module import *
from selenium_module import *

import io
import csv

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

if len(carLink) == 0:
    print(len(carLink), "ad to process\n--------------------")
else:
    print(len(carLink), "ads to process\n--------------------")

# get data
carTitle = []
carPrice = []
carReg   = []
carMiles = []
for i in range(len(carLink)):
        tmp = getCarData(carLink[i])
        carTitle.append(tmp[0])
        carPrice.append(tmp[1])
        carReg.append(tmp[2])
        carMiles.append(tmp[3])
        if i == 0:
            print(i + 1, "ad processed\n")
        else:
            print(i + 1, "ads processed\n")

# writing to csv file
print("Writing to csv")
with io.open('cars.csv', 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Ad Link", "Reg. Year", "Title", "Price", "Mileage"])
    for i in range(len(carLink)):
        writer.writerow([carLink[i] ,carReg[i], carTitle[i], carPrice[i], carMiles[i]])
file.close()

print("=== END ===")