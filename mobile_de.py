
import os
import json
import time
import requests
from bs4 import BeautifulSoup


# ================== generate search url ===================
def firstURL(maindir, curdir, input):
    make = input[0]
    make = make.lower()
    model = input[1]
    minprice = input[2]
    maxprice = input[3]
    minreg = input[4]
    maxreg = input[5]
    minmileage = input[6]
    maxmileage = input[7]
    
    os.chdir(maindir)
    os.chdir("./resources")
    with open("makes.json", 'r', encoding="utf-8", newline='') as mjson:
        data = mjson.read()
        makes_dict = (json.loads(data))
        makes_dict = makes_dict['makes']
        mjson.close()
    
    for i in range(len(makes_dict)):
        dictindex = makes_dict[i]['n']
        if dictindex.lower() == make:
            findindex = i
            make = makes_dict[i]['i']
            print(make)
            break
    
    # make
    if make != '' or 0:
        makeurl = "&makeModelVariant1.makeId=" + str(make)
    else:
        makeurl = ''
    # model
    if model != '' or 0:
        modelurl = "&makeModelVariant1.modelDescription=" + str(model)
    else:
        modelurl = ''
    # price
    if minprice == '' or 0:
        minpriceurl = ''
    else:
        minpriceurl = "&minPrice=" + str(minprice)
    if maxprice == '' or 0:
        maxpriceurl = ''
    else:
        maxpriceurl = "&maxPrice=" + str(maxprice)
    # reg
    if minreg == '' or 0:
        minregurl = ''
    else:
        minregurl = "&minFirstRegistrationDate=" + str(minreg)
    if maxreg == '' or 0:
        maxregurl = ''
    else:
        maxregurl = "&maxFirstRegistrationDate=" + str(maxreg)
    # mileage
    if minmileage == '' or 0:
        minmileageurl = ''
    else:
        minmileageurl = "&minMileage=" + str(minmileage)
    if maxmileage == '' or 0:
        maxmileageurl = ''
    else:
        maxmileageurl = "&maxMileage=" + str(maxmileage)
    
    urlInit = "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&scopeId=C&sfmr=false"
    
    finalurl = urlInit + makeurl + modelurl + minpriceurl + maxpriceurl + minregurl + maxregurl + maxmileageurl + minmileageurl + "&pageNumber=1"
    
    # categories=Cabrio&categories=EstateCar&categories=Limousine&categories=OffRoad&categories=SmallCar&categories=SportsCar&categories=Van
    
    print(finalurl)
    os.chdir(curdir)
    return finalurl


# ================== navigate to next page
def nextPage(currentURL, currentPage):
    tempLink = []

    i = 0
    while i < len(currentURL):
        i = currentURL.find("pageNumber=", i)
        if i == -1:
            break
        tempLink.append(i + len("pageNumber="))
        i += len("pageNumber=")
        i = currentURL.find("&", i)
        tempLink.append(i)

    nextLink = ''
    for i in range(tempLink[0]):
        nextLink += currentURL[i]

    nextLink += str(currentPage + 2)

    for i in range(len(currentURL) - i - tempLink[0] - len(str(currentPage + 2))):
        nextLink += currentURL[i + tempLink[0] + len(str(currentPage + 2))]

    return nextLink


# ================== get number of pages ==================
def getNr(currentURL):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(currentURL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    time.sleep(2)
    try:
        # checker
        checker = soup.find(class_ = "h2 u-text-orange rbt-result-list-headline").get_text()
        checker = checker.split(" ")[0]
        checker = checker.replace('.', '')
        checker = checker.replace(' ', '')
        checker = int(checker)
        # pages number
        pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
        if len(pagesnr) == 0:
            converted_pagesnr = 1
        else:
            converted_pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

        return converted_pagesnr, checker
    except:
        # checker
        print("\nAds checker failed")
        # pages number
        pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
        if len(pagesnr) == 0:
            converted_pagesnr = 1
        else:
            converted_pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

        return converted_pagesnr


# ================== get car links ==================
def getCarLinks(currentURL):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(currentURL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # _classPrivateSeller - cBox-body cBox-body--resultitem fsboAd rbt-reg rbt-no-top
    # _classDealer - cBox-body--resultitem dealerAd rbt-reg rbt-no-top
    carLinks = []
    for link in soup.find_all('a', {'class': 'link--muted no--text--decoration result-item'}):
        try:
            carLinks.append(link['href'])
        except: 
            None

    return carLinks


# ================== get car data ==================
def getCarData(carLinkCurrentPage):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(carLinkCurrentPage, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # title
    try:
        carTitle = soup.find(id = "rbt-ad-title").get_text()
    except:
        carTitle = "No Title"

    # price
    try:
        carPrice = soup.find(class_ = "h3 rbt-prime-price").get_text()
    except:
        carPrice = '0'

    # registration
    try:
        carReg = soup.find(id = "rbt-firstRegistration-v").get_text()
    except:
        try:
            carReg = soup.find(id = "rbt-category-v").get_text()
        except:
            carReg = 0
    # mileage
    try:
        carMiles = soup.find(id = "rbt-mileage-v").get_text()
    except:
        carMiles = 1414
    # power
    try:
        carPower = soup.find(id = "rbt-power-v").get_text()
    except:
        carPower = 0

    # ================== format necessary data
    # car price first
    carPrice = carPrice.replace('.', '')
    if 'Brutto' in carPrice:
        carPrice = carPrice[ : -11]
    else:
        carPrice = carPrice[ : -2]
    carPrice = int(carPrice)

    # registration
    if 'Neufahrzeug' in carReg:
        carReg = 2020
    elif 'Vorführfahrzeug' in carReg:
        carReg = 4
        #carReg = 'Demo Car'
    elif 'Jahreswagen' in carReg:
        carReg = 3
        #carReg = 'Employee Car'
        #Jahreswagen - employee car
    else:
        carReg = carReg[3 : ]
        carReg = int(carReg)

    # mileage
    if carMiles != 1414:
        carMiles = carMiles[ : -3]
        carMiles = carMiles.replace('.', '')
        carMiles = int(carMiles)

    # power
    if carPower != 0:
        carPower = carPower.split("(")[1]
        carPower = carPower[ : -4]
        carMiles = int(carMiles)

    return carTitle, carReg, carPrice, carMiles, carPower


# get car price for checker
def getCarPriceChecker(link):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(link, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # price
    try:
        carPrice = soup.find(class_ = "h3 rbt-prime-price").get_text()
    except Exception as e:
        print(e)
        return 0

    # ================== format data
    # car price first
    try:
        carPrice = carPrice.replace('.', '')
        if 'Brutto' in carPrice:
            carPrice = carPrice[ : -11]
        else:
            carPrice = carPrice[ : -2]
        carPrice = int(carPrice)
    except Exception as e:
        print(e)
        return 0

    return carPrice