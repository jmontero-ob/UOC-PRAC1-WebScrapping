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
v_url_evento = 'https://pre.koobin.com/demo/index.php?action=PU_evento&Ev_id=14'

#Inicialitzo dataframe
v_cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event','Sessio','Zona Preu','Preu','Data Registre']
#cab = ['Ticketera', 'Tipus Event', 'Recinte','Event','Sessio','Zona Preu','Preu','Data Registre']
v_data_koobin = pandas.DataFrame(columns=v_cab)

data_butter = llegeix_koobin_sessio(v_url_evento,'Basket')
v_data_koobin = v_data_koobin.append(data_butter)

#print(v_data_koobin)
print('Scrapper de basket executat correctament. Volcant les dades a fitxer')

#Escriure dataframe a fitxer
v_data_koobin.to_csv('d:\event_prices_basket.csv',encoding='utf-8',index=False)