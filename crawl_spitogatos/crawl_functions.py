import requests
from bs4 import BeautifulSoup
import re, json
from post_requests import *

def get_sxoles_spitogatos():
    sxoles = []
    url = "https://www.spitogatos.gr/students/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        try:
            st = link.get('href')
            if st[0:35] == url:
                sxoles.append((link.get_text().strip(), st))
        except:
            pass
    return sxoles

def get_details_per_house(url_spitiou):  # briskei leptomereiew gia to kaue spiti
    r = requests.get(url_spitiou)
    soup = BeautifulSoup(r.text, 'html.parser')
    if r.status_code != 200:
        print('\n ----den brhka selida---')
        spitia = []
    link = soup.find('div', {'class': "bck light_grey hide-print"})
    lek = ' '.join(link.text.split())
    lak = soup.find('div', {'itemprop': "description"})
    lak = ' '.join(lak.text.split())
    lek = lek + lak
    lek = ' '.join(lek.split())
    return lek

#var listingResultsJasonEncoded=
def get_spitia_sxolis(url_sxolis):
    data =requests.get(url_sxolis).content
    soup = BeautifulSoup(data, 'lxml')
    house_counter = soup.find(id='listingsSection').find(attrs={'class': 'paginationText'})
    patt = r"var listingsResultsJsonEncoded ?= ?(\[[^]]+])"
    return house_counter.text, json.loads(re.search(patt, str(data)).group(1).encode('utf-8').decode('unicode-escape'))

