import pandas
import numpy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def llegeix_koobin_sessio(p_url,p_tipus_event):

    #Capçalera del Dataset, inci

    cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event','Sessio','Zona Preu','Preu','Data Registre']
    data = pandas.DataFrame(columns=cab)

    #Valors constants
    v_ticketera = 'Koobin'
    v_tipus_event = p_tipus_event

    #get the page
    page = requests.get(p_url)
    #get the soup
    soup = BeautifulSoup(page.content,features="html.parser")

    #
    # Obtenim Event, Sessió i Recinte
    #

    #Recinte
    v_venue = soup.find_all("meta", property="og:site_name")
    v_venue_name = v_venue[0]["content"]

    #Event
    v_event = soup.find_all("meta", property="og:title")
    v_event_name = v_event[0]["content"]

    #Sessió
    v_session = soup.find_all("span", class_="eventoTaronja")
    if p_tipus_event == 'Opera':
        v_session_name = v_session[0].string.strip()
    elif p_tipus_event == 'Teatre':
        v_session_name = v_session[0].text
    elif p_tipus_event == 'Basket':
        v_session_name = 'Baskonia - Zalguiris'

    #treiem , per -
    v_session_name = v_session_name.replace(",","-")

    #
    # Obtenim preu i els guardem a un array per a després accedir-los amb les zones
    #

    if p_tipus_event  == 'Teatre':
        v_tmp_preus = []
        for tag in soup.find_all("span"):
            if tag.has_attr('ap'):
                v_tmp_preus.append(tag.string)
    else:
        v_tmp_preus = soup.find_all("strong", class_="Taronja nowrap")

    i=0
    v_preus = []
    for x in v_tmp_preus:
        v_preus.append(x.string)
        i= i +1

    #eliminem euro dels preus i comes per punts
    v_preus_final = [x.replace(' €','') for x in v_preus]
    v_preus_final = [x.replace(',','.') for x in v_preus_final]

    #
    # Iterem per zones de preu
    #

    v_zonas_tmp = []
    if p_tipus_event  != 'Teatre':
        v_zonas_tmp = soup.find_all("div", class_="areaNom")
    else:
        for tag in soup.find_all("span"):
            if tag.has_attr('da'):
                v_zonas_tmp.append(tag.string)

    i=0
    for x in v_zonas_tmp:
        v_nombre_zona = x.string.strip()
        # Row de datos
        row_dat = {'Ticketera': v_ticketera, 'Tipus Event': v_tipus_event, 'Recinte': v_venue_name, 'Event': v_event_name,
                   'Sessio': v_session_name, 'Zona Preu' : v_nombre_zona, 'Preu' : v_preus_final[i],
                   'Data Registre' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        data = data.append(row_dat, ignore_index=True)
        i= i +1

    return data