import pandas
#import numpy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


# Funció per extreure/reemplaçar caracters especials del fitxer d'extracció que generarem
def limpiar_caracteres(text):
    caracteres = {'ª': 'a', 'ó': 'o', 'Ó': 'O', 'É': 'E', 'Ú': 'U', 'é': 'e', 'á': 'a', 'í': 'i',
                  ' €': ' euros','€': ' euros', '"': ' ', ', ': '-', '|': ' ', '*': ''}
    for car in caracteres:
        if car in text:
            text = text.replace(car, caracteres[car])
    return text


def llegeix_koobin_sessio(p_url,p_tipus_event,p_headers):

    #Capçalera del Dataset, inci

    cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event', 'Sessio', 'Zona Preu', 'Preu', 'Data Registre']
    data = pandas.DataFrame(columns=cab)

    #Valors constants
    v_ticketera = 'Koobin'
    v_tipus_event = p_tipus_event

    #get the page
    page = requests.get(p_url,headers = p_headers)
    #get the soup
    soup = BeautifulSoup(page.content,features="html.parser")

    #
    # Obtenim Event, Sessió i Recinte
    #

    #Recinte
    v_venue = soup.find_all("meta", property="og:site_name")
    v_venue_name = v_venue[0]["content"]
    v_venue_name = limpiar_caracteres(v_venue_name)
    v_venue_name = v_venue_name.title()

    #Event
    v_event = soup.find_all("meta", property="og:title")
    v_event_name = v_event[0]["content"]
    v_event_name = limpiar_caracteres(v_event_name)
    v_event_name = v_event_name.strip()
    v_event_name = v_event_name.title()

    #Sessió
    v_session = soup.find_all("span", class_="eventoTaronja")

    if p_tipus_event == 'Opera':
        v_session_name = v_session[0].string.strip()
        v_session_name = limpiar_caracteres(v_session_name)
    elif p_tipus_event == 'Teatre':
        v_session_name = v_session[0].text
    elif p_tipus_event == 'Basket':
        v_session_name = 'Baskonia - Zalguiris'
    elif p_tipus_event == 'Musica':
        v_session = soup.find_all("span", class_="eventoTaronja")
        v_session_name = limpiar_caracteres(v_session[0].text)
        v_session_name = v_session_name.strip()
        if v_event_name == 'Jose Merce':
           v_session_name = v_session_name[33:]             # agafem només una part del nom de l'event del que interessa

    #
    # Obtenim preu i els guardem a un array per a després accedir-los amb les zones
    #

    if p_tipus_event  == 'Teatre' or p_tipus_event == 'Musica':
        v_tmp_preus = []
        for tag in soup.find_all("span"):
            if tag.has_attr('ap'):
                tag.string = limpiar_caracteres(tag.string)
                v_tmp_preus.append(tag.string)
    else:
        v_tmp_preus = soup.find_all("strong", class_="Taronja nowrap")

    i=0
    v_preus = []
    for x in v_tmp_preus:
        v_preus.append(x.string)
        i= i +1

    #
    # Iterem per zones de preu
    #

    v_zonas_tmp = []
    if p_tipus_event  != 'Teatre' and p_tipus_event != 'Musica':
        v_zonas_tmp = soup.find_all("div", class_="areaNom")
        v_zonas_tmp = limpiar_caracteres(v_zonas_tmp)
    else:
        for tag in soup.find_all("span"):
            if tag.has_attr('da'):
                tag.string = limpiar_caracteres(tag.string)
                v_zonas_tmp.append(tag.string)

    i=0
    for x in v_zonas_tmp:
        v_nombre_zona = limpiar_caracteres(x.string)
        v_preus[i] = limpiar_caracteres(v_preus[i])
        # Row de datos
        row_dat = {'Ticketera': v_ticketera, 'Tipus Event': v_tipus_event, 'Recinte': v_venue_name, 'Event': v_event_name,
                   'Sessio': v_session_name, 'Zona Preu' : v_nombre_zona, 'Preu' : v_preus[i],
                   'Data Registre' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        data = data.append(row_dat, ignore_index=True)
        i= i +1

    return data


### Funció per extreure les dades de la pàgina JANTO ###
def llegeix_janto_sessio(p_url,p_tipus_event,p_headers):

    #Capçalera del Dataset, inci

    cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event','Sessio','Zona Preu','Preu','Data Registre']
    data = pandas.DataFrame(columns=cab)

    #Valors constants
    v_ticketera = 'Janto'
    v_tipus_event = p_tipus_event

    #get the page
    page = requests.get(p_url,headers = p_headers)
    #get the soup
    soup = BeautifulSoup(page.content,features="html.parser")

       #
    # Obtenim Event, Sessió i Recinte
    #

    # Event
    v_event = soup.find("div", id="nom-espectacle")
    v_event_name = v_event['data-value']
    v_event_name = limpiar_caracteres(v_event_name)
    if v_event_name == 'Magia':
        v_event_name=v_event_name[:9]


    v_session = soup.find("div", class_="programacio")
    # Sessió
    v_spans_ses = v_session.find_all("span")
    v_session_name = v_spans_ses[0].text
    v_session_name=limpiar_caracteres(v_session_name)

    #treiem , per -
   # v_session_name = v_session_name.replace(",","-")

    #Recinte
    v_venue_name =  v_spans_ses[1].text
    if v_tipus_event == 'Familiar':
        v_venue_name=v_venue_name[:13]
    elif v_tipus_event == 'Magia':
        v_venue_name=v_venue_name[:16]
    #
    # Obtenim preu i els guardem a un array per a després accedir-los amb les zones
    #

    v_tmp_preus = []
    v_tmp_preus = soup.find_all("td", class_="individualls__row")

    i=0
    v_preus = []
    for x in v_tmp_preus:
        v_preus.append(x.string)
        i= i +1

    #eliminem euro dels preus i comes per punts
   # v_preus_final = [x.replace(' €','') for x in v_preus]
   # v_preus_final = [x.replace('€', '') for x in v_preus_final]
   # v_preus_final = [x.replace(',','.') for x in v_preus_final]

    #
    # Iterem per zones de preu
    #

    v_zonas_tmp = []
    v_zonas_tmp = soup.find_all("td", class_="zona")

    i=0
    for x in v_zonas_tmp:
        v_nombre_zona = x.string
        v_preus[i]=limpiar_caracteres(v_preus[i])
        if v_nombre_zona is not None:
            # Row de datos
            row_dat = {'Ticketera': v_ticketera, 'Tipus Event': v_tipus_event, 'Recinte': v_venue_name, 'Event': v_event_name,
                   'Sessio': v_session_name, 'Zona Preu' : v_nombre_zona, 'Preu' : v_preus[i],
                   'Data Registre' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            data = data.append(row_dat, ignore_index=True)
            i= i +1

    return data


def llegeix_vivaticket_sessio(p_url,p_tipus_event):

    #Necessitem treballar amb Selenium per extreure d'aquest portal
    DRIVER_PATH = "d:\\UOC_ML\\chromedriver.exe"
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")


    #Capçalera del Dataset, inci

    cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event','Sessio','Zona Preu','Preu','Data Registre']
    data = pandas.DataFrame(columns=cab)

    #Valors constants
    v_ticketera = 'VivaTicket'
    v_tipus_event = p_tipus_event

    #invoquem el driver per obtenir el html
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    soup = driver.get(p_url)

    #
    # Obtenim Event, Sessió i Recinte
    #

    #Event
    try:
        v_event = driver.find_element_by_xpath("//h2[@class='__title -uppercase']")
        v_event_name = v_event.text.split('\n', 1)[0]
    except NoSuchElementException:
        v_event_name = 'Event'

    # v_session = soup.find_all("span", class_="eventoTaronja")
    # if p_tipus_event == 'Opera':
    #    v_session_name = v_session[0].string.strip()
    # elif p_tipus_event == 'Teatre':
    #    v_session_name = v_session[0].text
    # elif p_tipus_event == 'Basket':
    #    v_session_name = 'Baskonia - Zalguiris'
    # v_session_name = 'Sessió'

    #Sessió i recinte
    try:
        v_venue_session = driver.find_element_by_xpath("//h3[@class='__title -small']")
        # First line is venue
        v_venue_name = v_venue_session.text.split('\n', 1)[0]
        # Second is session
        v_session_name = v_venue_session.text.split('\n', 1)[1]
        #treiem , per -
        v_session_name = v_session_name.replace(",","-")
    except NoSuchElementException:
        v_venue_name = 'Recinte'
        v_session_name = 'Sessio'

    #
    # Obtenim preu i els guardem a un array per a després accedir-los amb les zones
    #

    v_tmp_preus = driver.find_elements_by_xpath("//span[@data-role='price']")

    i=0
    v_preus = []
    for x in v_tmp_preus:
        v_preus.append(x.text)
        i= i +1

    #eliminem euro dels preus i comes per punts
    v_preus_final = [x.replace(' €','') for x in v_preus]
    v_preus_final = [x.replace('€', '') for x in v_preus_final]
    v_preus_final = [x.replace(',','.') for x in v_preus_final]

    #
    # Iterem per zones de preu
    #

    v_zonas_tmp = []
    v_zonas_tmp = driver.find_elements_by_xpath("//strong[@class='form-control-static vertical-middle']")

    i=0
    for x in v_zonas_tmp:
        v_nombre_zona = x.text
        # Row de datos
        row_dat = {'Ticketera': v_ticketera, 'Tipus Event': v_tipus_event, 'Recinte': v_venue_name, 'Event': v_event_name,
                   'Sessio': v_session_name, 'Zona Preu' : v_nombre_zona, 'Preu' : v_preus_final[i],
                   'Data Registre' : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        data = data.append(row_dat, ignore_index=True)
        i= i +1

    #Alliberem sessió driver
    driver.quit()

    return data