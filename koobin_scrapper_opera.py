import pandas
import numpy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

from koobin_scrapper_functions import llegeix_koobin_sessio

#
# Main : busquem les urls de les sesions e invokem la funció de manera iterativa
#

# URL del Evento on podrem trobar les urls de les sessions
v_url_evento = 'https://operaoviedo.koobin.com/butterfly'

#get the page
v_page_evento = requests.get(v_url_evento)
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
        data_butter = llegeix_koobin_sessio(link.get('href'),'Opera')
        v_data_koobin = v_data_koobin.append(data_butter)

#print(v_data_koobin)

#
# Teatre El Liceo
#


print('Scrapper executat correctament. Volcant les dades a fitxer')

#Escriure dataframe a fitxer
v_data_koobin.to_csv('d:\event_prices_butter.csv',encoding='utf-8',index=False)