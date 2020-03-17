
import requests
from bs4 import BeautifulSoup
import time


# ================== get number of pages ==================
def getNr(currentURL):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(currentURL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
    converted_pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())
    return converted_pagesnr


# ================== get car data ==================
def carsPerPage(currentURL):
    time.sleep(1)
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    page = requests.get(currentURL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    carLink = []
    for link in soup.find_all('a', {'class': 'link--muted no--text--decoration'}):
        try:
            carLink.append(link['href'])
        except: 
            None
    for link in soup.find_all('a', {'class': 'link--muted no--text--decoration result-item'}):
        try:
            carLink.append(link['href'])
        except: 
            None
    for link in soup.find_all('a', {'class': 'link--muted no--text--decoration result-item'}):
        try:
            carLink.append(link['href'])
        except: 
            print("huinea")
    carTitles = soup.find_all(class_ = "h3 u-text-break-word")
    carPrices = soup.find_all(class_ = "h3 u-block")
    carRegDistPow = soup.find_all(class_ = "rbt-regMilPow")

    # ================== filtrating data
    for i in range(len(carTitles)):
        carTitles[i] = carTitles[i].get_text()
        carPrices[i] = carPrices[i].get_text()
        carRegDistPow[i] = carRegDistPow[i].get_text()
        
    # ================== calculating temporary data
    # car registration temp data
    i = 0
    j = 0
    carReg = []
    carRegTemp = []
    for i in range(len(carTitles)):
        tempstr = ''
        for j in range(10):
            tempstr += carRegDistPow[i][j]
        carRegTemp.append(tempstr)

    # car dist temp data
    i = 0
    carDist = []
    carDistTemp = []
    carDistIndexes = []
    for i in range(len(carRegDistPow)):
        tp = 0
        tp = carRegDistPow[i].find(",", tp)
        carDistIndexes.append(tp + len(", "))
        tp = 0
        tp = carRegDistPow[i].find("km", tp)
        carDistIndexes.append(tp - len(" "))

    i = 0
    chk = []
    for i in range(len(carRegDistPow)):
        chk.append(carRegDistPow[i])
        chk.append("4")

    i = 0
    j = 0
    tempstr = ""
    while i != len(chk):
        tempstr = ""
        for j in range(carDistIndexes[i], carDistIndexes[i + 1]):
            tempstr += (chk[i][j])
        carDist.append(tempstr)
        i += 2

    # ================== formatting data for suitable type
    # car price
    carPrice = [sub[ : -2] for sub in carPrices]
    carPrice = [sub.replace('.', '') for sub in carPrice]
    carPrice = [int(i) for i in carPrice]

    # car registration
    carReg = [sub[6 : ] for sub in carRegTemp] 
    for i, en in enumerate(carReg):
        if en == "en, ":
            carReg[i] = "2020"
        if en == "ulas":
            carReg[i] = "4444"
    carReg = [int(i) for i in carReg]

    # car dist
    carDist = [sub.replace('.', '') for sub in carDist]
    for i, en in enumerate(carDist):
        if en == '':
            carDist[i] = '1414'
    carDist = [int(i) for i in carDist]

    # ================== neat print all values
    for i in range(len(carTitles)):
        print(carLink[i])

        print(carTitles[i])

        print(carPrice[i], " €")

        if carReg[i] == 4444:
            print("Demo Car")
        else:
            print(carReg[i])

        if carDist[i] == 1414:
            print("Either not specified or 0\n")
        else:
            print(carDist[i], " km\n")

    return carLink, carTitles, carPrice, carReg, carDist