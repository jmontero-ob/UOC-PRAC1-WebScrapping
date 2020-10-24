import pandas
import numpy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

from koobin_scrapper_functions import llegeix_koobin_sessio


user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

v_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    */*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "es-es,en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": user_agent_desktop}

#
# Main : Opera amb Madame Buttefly
#

# URL del Evento on podrem trobar les urls de les sessions
v_url_evento = 'https://operaoviedo.koobin.com/butterfly'

#get the page
v_page_evento = requests.get(v_url_evento,v_headers)
#get the soup
v_soup_evento = BeautifulSoup(v_page_evento.content,features="html.parser")

#Inicialitzo dataframe
v_cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event','Sessio','Zona Preu','Preu','Data Registre']
#cab = ['Ticketera', 'Tipus Event', 'Recinte','Event','Sessio','Zona Preu','Preu','Data Registre']
v_data_koobin = pandas.DataFrame(columns=v_cab)

#Busco les sesions del evento de butterfly
for link in v_soup_evento.find_all('a'):
    if link.get('href').find('https://operaoviedo.koobin.com/index.php?action=PU_evento') != -1:
        #print(link.get('href'))
        data_butter = llegeix_koobin_sessio(link.get('href'),'Opera',v_headers)
        v_data_koobin = v_data_koobin.append(data_butter)


#
# Main : Teatre al Liceu
#

# URL del Evento on podrem trobar les urls de les sessions
v_url_evento = 'https://liceubarcelona.koobin.com/index.php?action=PU_evento&Ev_id=44968&_ga=2.220438040.1256762823.1603307756-484716721.1603307756'

v_url_sesion = 'https://liceubarcelona.koobin.com/index.php?action=PU_evento&Ev_id=44969&_ga=2.42270501.1256762823.1603307756-484716721.1603307756'

#get the page
v_page_evento = requests.get(v_url_evento,headers = v_headers)
#get the soup
v_soup_evento = BeautifulSoup(v_page_evento.content,features="html.parser")

#Busco les sesions del evento de butterfly
for link in v_soup_evento.find_all('a'):
    if link.get('href').find('https://liceubarcelona.koobin.com/index.php?action=PU_evento') != -1:
        #print(link.get('href'))
        data_butter = llegeix_koobin_sessio(link.get('href'),'Teatre',v_headers)
        v_data_koobin = v_data_koobin.append(data_butter)


#
# Main : Basket - Zalguiris vs Baskonia
#


# URL del Evento on podrem trobar les urls de les sessions
v_url_evento = 'https://pre.koobin.com/demo/index.php?action=PU_evento&Ev_id=14'

data_butter = llegeix_koobin_sessio(v_url_evento,'Basket',v_headers)
v_data_koobin = v_data_koobin.append(data_butter)


print('Scrapper Koobin executat correctament. Volcant les dades a fitxer')

#Escriure dataframe a fitxer
v_data_koobin.to_csv('d:\koobin_prices.csv',encoding='utf-8',index=False)