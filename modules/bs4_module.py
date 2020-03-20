
import requests
from bs4 import BeautifulSoup
import time


# ================== get number of pages ==================
def getNr(currentURL):
    time.sleep(1)
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(currentURL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
    for i in range(5):
        pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
        if len(pagesnr) == 0:
            converted_pagesnr = 1
        elif int(pagesnr[(len(pagesnr) - 1)].get_text()) == (0 or -1):
            converted_pagesnr = 1
        else:
            converted_pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

    return converted_pagesnr


# ================== get car links ==================
def getCarLinks(currentURL):
    time.sleep(0.5)
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
    carTitle = soup.find(id = "rbt-ad-title").get_text()

    # price
    carPrice = soup.find(class_ = "h3 rbt-prime-price").get_text()

    # registration
    try:
        carReg = soup.find(id = "rbt-firstRegistration-v").get_text()
    except:
        carReg = soup.find(id = "rbt-category-v").get_text()
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
        carReg = 4444
    elif 'Jahreswagen' in carReg:
        carReg = 3333
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
    if carPower == 0:
        pass
    else:
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
        print("Either not specified or 0 km")
    else:
        print(carMiles, "km")
    '''

    return carTitle, carReg, carPrice, carMiles, carPower