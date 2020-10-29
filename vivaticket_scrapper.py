import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re

DRIVER_PATH = "d:\\UOC_ML\\chromedriver.exe"
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

str = "https://shop.vivaticket.com/eng/sell/?cmd=tabellaPrezzi&pcode=7608000&tcode=vt0000450&qubsq=de8bf77b-8a28-4a83-853c-54438166ea3b&qubsp=5e498339-9e96-4fe7-a92b-b3954796defa&qubsts=1603987983&qubsc=bestunion&qubse=vivaticketserver&qubsrt=Safetynet&qubsh=e24a55649dbb85a77564e7248e96223f"

#str = "https://www.vivaticket.com/it/ticket/spellbound-25/151816"

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(str)
print(driver.page_source)
print(type(driver.page_source))
print(driver.title)

driver.quit()

#user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
#'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
#'Safari/537.36'

#v_headers = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
#    */*;q=0.8",
#    "Accept-Encoding": "gzip, deflate, sdch, br",
#    "Accept-Language": "en-US,en;q=0.8",
#    "Cache-Control": "no-cache",
#    "dnt": "1",
#    "Pragma": "no-cache",
#    "Upgrade-Insecure-Requests": "1",
#    "User-Agent": user_agent_desktop}

#get the page
#page = requests.get(str, headers=v_headers)
#get the soup
#soup = BeautifulSoup(page.content,features="html.parser")

#print(soup)