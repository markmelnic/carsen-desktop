
import time
import requests
from bs4 import BeautifulSoup


# ================== get number of pages ==================
def getNr(currentURL):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(currentURL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    '''
    for i in range(5):
        time.sleep(0.8)
    '''
    time.sleep(2)
    try:
        # checker
        checker = soup.find(class_ = "h2 u-text-orange rbt-result-list-headline").get_text()
        checker = checker.split(" ")[0]
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
        print("\nAds checker failer")
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
    '''
    else:
        carMiles = 'Either not specified or 0'
    '''

    # power
    if carPower != 0:
        carPower = carPower.split("(")[1]
        carPower = carPower[ : -4]
        carMiles = int(carMiles)

    '''
    # ================== neat print all values
    print(carTitle)
    print(carPrice, "€")
    if carReg == 4444:
        print("Demo Car")
    elif carReg == 3333:
        print("Employee Car")
    else:
        print(carReg)
    if carMiles == 1414:
        print("Either not specified or 0")
    else:
        print(carMiles, "km")
    '''

    return carTitle, carReg, carPrice, carMiles, carPower


# get car price for checker
def getCarPriceChecker(link):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(link, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # price
    try:
        carPrice = soup.find(class_ = "h3 rbt-prime-price").get_text()
    except:
        carPrice = '0'

    # ================== format data
    # car price first
    carPrice = carPrice.replace('.', '')
    if 'Brutto' in carPrice:
        carPrice = carPrice[ : -11]
    else:
        carPrice = carPrice[ : -2]
    carPrice = int(carPrice)

    return carPrice