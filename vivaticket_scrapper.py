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



# Opera amb Andrea Bocelli

v_url_opera = "https://shop.vivaticket.com/eng/sell/?cmd=tabellaPrezzi&pcode=7682216&tcode=vt0004330"

#Inicialitzo dataframe
v_cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event','Sessio','Zona Preu','Preu','Data Registre']
#cab = ['Ticketera', 'Tipus Event', 'Recinte','Event','Sessio','Zona Preu','Preu','Data Registre']
v_data_viva = pandas.DataFrame(columns=v_cab)

# Opera amb Andrea Bocelli
data_butter = llegeix_vivaticket_sessio(v_url_opera, 'Opera')
v_data_viva = v_data_viva.append(data_butter)

# Teatre amb La Dvina Comedia
# Event amb multiples sesions : primer iterem per las sesions i cridarem a la funció per treure les dades
# de les session, que tenen el mateix format que les de Opera de Bocelli

v_url_teatre = 'https://www.vivaticket.com/it/ticket/la-divina-commedia-opera-musical/148116'

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(v_url_teatre)

# Busquem els links
v_links = driver.find_elements_by_tag_name('a')
for elem in v_links:
    href = elem.get_attribute('href')
    result = href.startswith('https://shop.vivaticket.com/ita/sell/?cmd=tabellaPrezzi&pcode=')
    if result == True:
        #LCrida a la funció per tractar la sessió
        data_butter = llegeix_vivaticket_sessio(href, 'Teatre')
        v_data_viva = v_data_viva.append(data_butter)

driver.quit()

print('Scrapper VivaTicket executat correctament. Volcant les dades a fitxer')

#Escriure dataframe a fitxer
v_data_viva.to_csv('d:\Vivatickets_prices.csv',encoding='utf-8',index=False)
