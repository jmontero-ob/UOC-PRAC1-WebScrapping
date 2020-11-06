import pandas
import numpy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

from koobin_scrapper_functions import llegeix_janto_sessio

#
# Setting dels headers
#

user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

v_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    */*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": user_agent_desktop}

#
# Main Jaula de las Locas: busquem les urls de les sesions e invokem la funció de manera iterativa
#

# URL del Evento on podrem trobar les urls de les sessions
v_url_evento = "https://www.topgrups.com/es/cartellera/la-jaula-de-las-locas/"

#Inicialitzo dataframe
v_cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event','Sessio','Zona Preu','Preu','Data Registre']
#cab = ['Ticketera', 'Tipus Event', 'Recinte','Event','Sessio','Zona Preu','Preu','Data Registre']
v_data_janto = pandas.DataFrame(columns=v_cab)

#Busco les sesions del evento de locas - es info genérica
data_butter = llegeix_janto_sessio(v_url_evento,'Musical',v_headers)
v_data_janto = v_data_janto.append(data_butter)

print('Scrapper Janto Jaula Locas executat correctament. Volcant les dades a fitxer')

#
# Main Petit Princep: busquem les urls de les sesions del Petit Princep
#
# URL del Evento on podrem trobar les urls de les sessions
v_url_evento = "https://www.topgrups.com/cartellera/el-petit-princep-3/"
data_butter = llegeix_janto_sessio(v_url_evento,'Familiar',v_headers)
v_data_janto = v_data_janto.append(data_butter)

print('Scrapper Janto El Petit Princep executat correctament. Volcant les dades a fitxer')

#
# Main El Mago Pop: busquem les urls de les sesions del Mago Pop
#

# URL del Evento on podrem trobar les urls de les sessions
v_url_evento = "https://www.topgrups.com/cartellera/mago-pop-nada-es-imposible/"
data_butter = llegeix_janto_sessio(v_url_evento,'Magia',v_headers)
v_data_janto = v_data_janto.append(data_butter)

print('Scrapper Janto Mago Pop executat correctament. Volcant les dades a fitxer')


#Escriure dataframe a fitxer
v_data_janto.to_csv('D:\event_prices_janto_musical.csv',encoding='utf-8',index=False)