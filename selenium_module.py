
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import time


#GENERIC_URL = 'https://www.mobile.de/'
GENERIC_URL = 'https://suchen.mobile.de/fahrzeuge/search.html?vc=Car&dam=0&lang=en'


# ================== driver procedures ===================
# ================== driver boot procedure
def boot():
    # manage notifications
    opts = Options() 
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    opts.add_experimental_option("prefs", prefs)
    opts.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2})
    #opts.add_argument("--window-size=1920,1080")
    #opts.add_argument("--start-maximized")
    #opts.set_headless(headless=True)


    # driver itself
    dv = webdriver.Chrome(chrome_options = opts, executable_path = r"../drivers/chromedriver81.exe")
    return dv


# ================== kill the driver
def killd(dv):
    dv.quit()

# ================== first dv.get
def startSearcher(dv):
    dv.get(GENERIC_URL)


# ================== website processes ===================
def firstSearch(dv, input):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    # ================== accept cookies
    time.sleep(3)
    try:
        cookiesAccept = dv.find_element_by_id("gdpr-consent-accept-button")
        cookiesAccept.click()
    except:
        try:
            cookiesAccept = dv.find_element_by_css_selector(".consent-btn.orange")
            cookiesAccept.click()
        except:
            None

    # ================== selectors
    # select any
    time.sleep(1)
    any = "any"
    makeSelector = dv.find_element_by_id("selectMake1-ds")
    for i in range(len(any)):
        makeSelector.send_keys(any[i])
    time.sleep(0.2)
    makeSelector.send_keys(Keys.ENTER)
    # manufacturer selector
    time.sleep(0.5)
    makeSelector = dv.find_element_by_id("selectMake1-ds")
    for i in range(len(input[0])):
        makeSelector.send_keys(input[0][i])
    time.sleep(0.2)
    makeSelector.send_keys(Keys.ENTER)

    # model selector
    time.sleep(0.7)
    modelSelector = dv.find_element_by_id("selectModel1-ds")
    for i in range(len(input[1])):
        modelSelector.send_keys(input[1][i])
    time.sleep(0.2)
    modelSelector.send_keys(Keys.ENTER)

    # price range selector
    modelSelector = dv.find_element_by_id("minPrice")
    for i in range(len(input[2])):
        modelSelector.send_keys(input[2][i])

    modelSelector = dv.find_element_by_id("maxPrice")
    for i in range(len(input[3])):
        modelSelector.send_keys(input[3][i])

    # registration years range selector
    modelSelector = dv.find_element_by_id("minFirstRegistrationDate")
    for i in range(len(input[4])):
        modelSelector.send_keys(input[4][i])

    modelSelector = dv.find_element_by_id("maxFirstRegistrationDate")
    for i in range(len(input[5])):
        modelSelector.send_keys(input[5][i])

    # mileage range selector
    modelSelector = dv.find_element_by_id("minMileage")
    for i in range(len(input[6])):
        modelSelector.send_keys(input[6][i])

    modelSelector = dv.find_element_by_id("maxMileage")
    for i in range(len(input[7])):
        modelSelector.send_keys(input[7][i])

    # power range selector
    modelSelector = dv.find_element_by_id("minPowerAsArray")
    for i in range(len(input[8])):
        modelSelector.send_keys(input[8][i])

    modelSelector = dv.find_element_by_id("maxPowerAsArray")
    for i in range(len(input[9])):
        modelSelector.send_keys(input[9][i])

    # cubic capacity selector (in cm^3)
    # WIP

    # click search button
    time.sleep(0.1)
    searchButton = dv.find_element_by_id("dsp-upper-search-btn")
    searchButton.click()


# ================== see current URL
def curURL(dv):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(1)
    currentURL = dv.current_url
    return currentURL


# ================== navigate to next page
def nextPage(dv, currentURL, currentPage):
    tempLink = []
    
    if currentPage + 1 == 1:
        nextLink = currentURL
        nextLink += "&pageNumber=2"
    else:
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