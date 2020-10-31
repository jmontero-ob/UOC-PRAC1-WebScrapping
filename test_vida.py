import pandas
import numpy
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re

from koobin_scrapper_functions import llegeix_vivaticket_sessio

DRIVER_PATH = "d:\\UOC_ML\\chromedriver.exe"
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

#str = "https://proticketing.com/theproject/es_ES/entradas/evento/17775/session/1050399/select?viewCode=Vista_Principal"

#str = "https://shop.vivaticket.com/eng/sell/?cmd=tabellaPrezzi&pcode=7682216&tcode=vt0004330"

str = "https://shop.vivaticket.com/eng/sell/?cmd=tabellaPrezzi&pcode=7606090&tcode=vt0000450"

#str = "https://www.vivaticket.com/it/ticket/spellbound-25/151816"

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(str)
#print(driver.page_source)
#print(type(driver.page_source))
#print(driver.title)

event = driver.find_element_by_xpath("//h2[@class='__title -uppercase']")
print(event.text.split('\n', 1)[0])

venue_session = driver.find_element_by_xpath("//h3[@class='__title -small']")
print(venue_session.text)

#First line is venue
venue = venue_session.text.split('\n', 1)[0]
print('Recinte ',venue)
#Second is session
session = venue_session.text.split('\n', 1)[1]
print('Sessio ',session)

#Zonas
v_zonas = driver.find_elements_by_xpath("//strong[@class='form-control-static vertical-middle']")
for x in v_zonas:
    print(x.text)

#Precios
v_precios = driver.find_elements_by_xpath("//span[@data-role='price']")
for x in v_precios:
    print(x.text)

driver.quit()


## find urls

str = 'https://www.vivaticket.com/it/ticket/la-divina-commedia-opera-musical/148116'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(str)
#print(driver.page_source)

#all_links = driver.find_elements_by_tag_name('a')
#for x in all_links:
#    print(x.g)

elems = driver.find_elements_by_tag_name('a')
for elem in elems:
    href = elem.get_attribute('href')
    result = href.startswith('https://shop.vivaticket.com/ita/sell/?cmd=tabellaPrezzi&pcode=')
    if result == True:
        print(href)

driver.quit()