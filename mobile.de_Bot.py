
from bf4Requests import *
from seleniumInter import *

# ================== initialization ==================
carMake = input("Car Manufacturer: ")
carModel = input("Car Model: ")
dv = boot()
startSearcher(dv)
firstSearch(dv, carMake, carModel)

currentURL = curURL(dv)
converted_pagesnr = getNr(currentURL)

carLink  = []
carTitle = []
carPrice = []
carReg   = []
carMiles = []

for currentPage in range(converted_pagesnr):
    currentURL = curURL(dv)
    carLinksCurrentPage = getCarLinks(currentURL)
    for i in range(len(carLinksCurrentPage)):
        tmp = getCarData(carLinksCurrentPage[i])
        carLink.append(carLinksCurrentPage[i])
        carTitle.append(tmp[0])
        carPrice.append(tmp[1])
        carReg.append(tmp[2])
        carMiles.append(tmp[3])
    nextPage(dv, currentURL, currentPage)
    print("===== results for page ", currentPage + 1, "are above ↑\n\n")

killd(dv)