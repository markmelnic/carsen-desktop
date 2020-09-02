
import os, json, time, requests
from random import choice
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

# ================== get random proxy ====================
def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, 
    soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
    return proxy


# ================== generate search url ===================
def first_search_url(maindir, curdir, inp : list) -> str:
    # what each input is
    # 0 - make
    # 1 - model
    # 2 - minprice
    # 3 - maxprice
    # 4 - minreg
    # 5 - maxreg
    # 6 - minmileage
    # 7 - maxmileage

    os.chdir(maindir)
    with open("./resources/makes.json", 'r', encoding="utf-8", newline='') as mjson:
        makes_dict = json.load(mjson)
        makes_dict = makes_dict['makes']

    if inp[0].lower() == 'any':
        make = ''
    else:
        for make in makes_dict:
            if make['n'].lower() == inp[0].lower():
                make = make['i']
                break

    url_params = ''

    # make
    if make == '' or make == 0 or make == "any":
        url_params += ''
    else:
        url_params += "&makeModelVariant1.makeId=" + str(make)

    # model
    if inp[1] == '' or inp[1] == 0:
        url_params += ''
    else:
        url_params += "&makeModelVariant1.modelDescription=" + str(inp[1])

    # price
    if inp[2] == '' or inp[2] == 0:
        url_params += ''
    else:
        url_params += "&minPrice=" + str(inp[2])
    if inp[3] == '' or inp[3] == 0:
        url_params += ''
    else:
        url_params += "&maxPrice=" + str(inp[3])

    # reg
    if inp[4] == '' or inp[4] == 0:
        url_params += ''
    else:
        url_params += "&minFirstRegistrationDate=" + str(inp[4])
    if inp[5] == '' or inp[5] == 0:
        url_params += ''
    else:
        url_params += "&maxFirstRegistrationDate=" + str(inp[5])

    # mileage
    if inp[6] == '' or inp[6] == 0:
        url_params += ''
    else:
        url_params += "&minMileage=" + str(inp[6])
    if inp[7] == '' or inp[7] == 0:
        url_params += ''
    else:
        url_params += "&maxMileage=" + str(inp[7])

    # categories=Cabrio&categories=EstateCar&categories=Limousine&categories=OffRoad&categories=SmallCar&categories=SportsCar&categories=Van

    url = "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&scopeId=C&sfmr=false"

    os.chdir(curdir)
    return url + url_params + "&pageNumber=1"


# ================== navigate to next page
def next_page(current_url, current_page):
    if current_page < 10:
        print(current_url[:-1] + str(current_page + 2))
        return current_url[:-1] + str(current_page + 2)
    elif current_page >= 10:
        print(current_url[:-2] + str(current_page + 2))
        return current_url[:-2] + str(current_page + 2)


# ================== get number of pages ==================
def get_pages_count(current_url):
    response = requests.get(current_url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # checker
        checker = soup.find(class_ = "h2 u-text-orange rbt-result-list-headline").get_text()
        checker = int(checker.split(" ")[0].replace(' ', '').replace('.', ''))
        # pages number
        pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
        if len(pagesnr) == 0:
            converted_pagesnr = 1
        else:
            converted_pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

        return converted_pagesnr, checker
    except:
        failed_get_pages_count(current_url, soup)

def failed_get_pages_count(current_url, soup):
    # pages number
    pagesnr = soup.find_all(class_ = "btn btn--muted btn--s")
    if len(pagesnr) == 0:
        converted_pagesnr = 1
    else:
        converted_pagesnr = int(pagesnr[(len(pagesnr) - 1)].get_text())

    return converted_pagesnr

# ================== get car links ==================
def get_car_links(current_url):
    page = requests.get(current_url, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    # _classPrivateSeller - cBox-body cBox-body--resultitem fsboAd rbt-reg rbt-no-top
    # _classDealer - cBox-body--resultitem dealerAd rbt-reg rbt-no-top
    return [link['href'] for link in soup.find_all('a', {'class': 'link--muted no--text--decoration result-item'})]


# ================== get car data ==================
def get_car_data(carLinkCurrentPage):
    page = requests.get(carLinkCurrentPage, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    # title
    try:
        car_title = soup.find(id = "rbt-ad-title").get_text()
    except:
        car_title = "N/A"

    # price
    try:
        car_price = soup.find(class_ = "h3 rbt-prime-price").get_text()
    except:
        car_price = "N/A"

    # registration
    try:
        car_reg = soup.find(id = "rbt-firstRegistration-v").get_text()
    except:
        try:
            car_reg = soup.find(id = "rbt-category-v").get_text()
        except:
            car_reg = "N/A"
    # mileage
    try:
        car_mileage = soup.find(id = "rbt-mileage-v").get_text()
    except:
        car_mileage = "N/A"
    # power
    try:
        car_power = soup.find(id = "rbt-power-v").get_text()
    except:
        car_power = "N/A"

    # ================== format necessary data
    # car price first
    car_price = car_price.replace('.', '')
    if 'Brutto' in car_price:
        car_price = int(car_price[ : -11])
    else:
        car_price = int(car_price[ : -2])

    # registration
    try:
        if 'Neufahrzeug' in car_reg:
            car_reg = 2020
        #elif 'Vorführfahrzeug' in car_reg:
        #    car_reg = 4
        #    #carReg = 'Demo Car'
        #elif 'Jahreswagen' in car_reg:
        #    car_reg = 3
        #    #carReg = 'Employee Car'
        #    #Jahreswagen - employee car
        else:
            car_reg = int(car_reg[3 : ])
    except:
        car_reg = 'N/A'


    # power
    if car_power != 0:
        car_power = int(car_power.split("(")[1][ : -4])

    return car_title, car_reg, car_price, car_mileage, car_power


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