
from bf4Requests import *
from seleniumInter import *

# ================== initialization ==================
carMake = input("Car Manufacturer: ")
carModel = input("Car Model: ")
dv = boot()
startSearcher(dv)
firstSearch(dv, carMake, carModel)

currentURL = curURL(dv)
getNr(currentURL)

for currentPage in range(getNr(currentURL)):
    currentURL = curURL(dv)
    carsPerPage(currentURL)
    nextPage(dv, currentURL, currentPage)
    print("\n\n=== results for page ", currentPage + 1, "are above _|\n\n")
    if currentPage == getNr(currentURL) - 1:
        break

killd(dv)