import requests
import pandas
from bs4 import BeautifulSoup


# Definim aquesta funció per extreure caracters especials que ens surtinmalament al fitxer que generarem al final
def limpiar_caracteres(text):
    caracteres = {'ª': 'a', 'ó': 'o', '€': 'euros', 'á': 'a', 'í': 'i', '"' : ' '}
    for car in caracteres:
        if car in text:
            text = text.replace(car, caracteres[car])
    return text

###################################################################################################################

# Afegim a la variable url l'adreça web que volem utilitzar
url = "https://teatrodelamaestranza.koobin.es/index.php?action=PU_evento&Ev_id=480"

# Petició a la pàgina web
req  = requests.get (url)

# Passem el codi obtingut a la variable codigo
codigo=req.status_code

# Si el codi ens ha retornat el valor de 200 continuem
if codigo==200:

    # Valors constants
    v_ticketera = 'Koobin'
    v_tipus_event = 'Teatre'

    # Agafem el contingut HTML de la web cap a un objecte BeautifulSoup()
    soup = BeautifulSoup(req.content,"html.parser")

    # Inicialitzo dataframe
    v_cab = ['Ticketera', 'Tipus Event', 'Recinte', 'Event', 'Sessio', 'Zona Preu', 'Preu']
    v_noa = pandas.DataFrame(columns=v_cab)

    # Recinte
    v_venue = soup.find_all("meta", property="og:site_name")
    v_venue_name =v_venue[0]["content"]

    # Event
    v_event = soup.find_all("meta", property="og:title")
    v_event_name = v_event[0]["content"]

    # Sessió
    v_session = soup.find_all("span", class_="eventoTaronja")
    v_session_name = limpiar_caracteres(v_session[0].text)                 # crida a la funció per treure caracters com accents
    v_session_name = v_session_name.strip()                                # eliminem espais en blanc

    # Obtenim preu i els guardem a un array per a després accedir-los amb les zones
    v_temp_preus = []
    for tag in soup.find_all("span"):
        if tag.has_attr('ap'):
            tag.string=limpiar_caracteres(tag.string)
            v_temp_preus.append(tag.string)

    i = 0
    v_preus = []
    for x in v_temp_preus:
        v_preus.append(x.string)
        i = i + 1

    # Iterem per zones de preu
    v_zonas_tmp = []                            #Array on es guarda el nom de les zones trobades a la classe amb atribut 'da'
    for tag in soup.find_all("span"):
        if tag.has_attr('da'):
            tag.string=limpiar_caracteres(tag.string)
            v_zonas_tmp.append(tag.string)

    i = 0
    for x in v_zonas_tmp:
        v_zona = x.string.strip()
        v_preus[i] = limpiar_caracteres(v_preus[i])

        # Row de datos
        row_dat = {'Ticketera': v_ticketera, 'Tipus Event': v_tipus_event, 'Recinte': v_venue_name, 'Event': v_event_name, 'Sessio': v_session_name, 'Zona Preu': v_zona, 'Preu': v_preus[i]}
        v_noa = v_noa.append(row_dat, ignore_index=True)
        i = i + 1

    # Escriure dataframe a fitxer
    v_noa.to_csv('E:\prova.csv', encoding='utf-8', index=False)

# Si no ens retorna el codi de servidor 200 aleshores que ens surti per pantalla el número de codi retornat pel servidor
else:
    print ("Codi d'estat del servidor : ",codigo)
