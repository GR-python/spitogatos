import requests, json, re
"""
  Αυτό το πρόγραμμα παίρνει τα σπίτια από το https://www.spitogatos.gr/students
"""
ids = set()

# Η παράμετρος url για όλες τις σχολές
url = 'https://www.spitogatos.gr/students/processPaginationData'

# Αυτή είναι η παράμετρος headers για όλες τις σχολές
headers = {
    'Host': 'www.spitogatos.gr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,el-GR;q=0.8,el;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-NewRelic-ID': 'VQUHWFRUGwcCU1BXBw==',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'}

# Αυτή είναι η παράμετρος data είναι διαφορετική για κάθε σχολή και την παίρνουμε από ένα browser
# με ενεργοποιημένα τα developer tools στην ταπέλα δίκτυο XHR
# Το συγκεκριμένο είναι από το παιδαγωγικό
# πρέπει να βρεθεί τρόπος να παραχθεί αυτόματα από το πρόγραμμα διαφορετικά πρέπει να γίνει database
# με τα params κάθε σχολής.
paidagvgiko = 'fv_universitySelect=8&drawPolygon=&gmapsBounds=&zoomLevel=14&previousZoomLevel=6&fv_priceLow=&fv_priceHigh=&fv_livingAreaLow=&fv_livingAreaHigh=&fv_listingPropertyType=&fv_roomsMin=&fv_roomsHigh=&fv_floorFrom=&fv_floorTo=&fv_yearBuiltMin=&fv_yearBuiltHigh=under+construction&fv_heatCon=&fv_heatMed=&fv_dateModifiedAfter=&fv_dateUploadedAfter=&newDevelopment=&hasMainImage=&furnished=&garage=&storage=&balcony=&secureDoor=&airConditioning=&alarm=&fireplace=&elevator=&view=&garden=&swimmingPool=&solarHeater=&petsAllowed=&page=50&markerCoords%5B0%5D%5B%5D=37.977583087049&markerCoords%5B0%5D%5B%5D=23.740637842566&markerCoords%5B1%5D%5B%5D=37.979056124708&markerCoords%5B1%5D%5B%5D=23.738214682255&markerCoords%5B2%5D%5B%5D=37.981655644253&markerCoords%5B2%5D%5B%5D=23.738085469231&markerCoords%5B3%5D%5B%5D=37.978882477619&markerCoords%5B3%5D%5B%5D=23.739252300002&markerCoords%5B4%5D%5B%5D=37.98172377795&markerCoords%5B4%5D%5B%5D=23.736746979877&markerCoords%5B5%5D%5B%5D=37.980525978841&markerCoords%5B5%5D%5B%5D=23.737926363945&markerCoords%5B6%5D%5B%5D=37.979026179761&markerCoords%5B6%5D%5B%5D=23.740355355665&markerCoords%5B7%5D%5B%5D=37.984627978876&markerCoords%5B7%5D%5B%5D=23.740868316963&markerCoords%5B8%5D%5B%5D=37.984569305554&markerCoords%5B8%5D%5B%5D=23.73956928961&markerCoords%5B9%5D%5B%5D=37.984726983123&markerCoords%5B9%5D%5B%5D=23.735087653622&markerCoords%5B10%5D%5B%5D=37.980034975335&markerCoords%5B10%5D%5B%5D=23.735544942319&markerCoords%5B11%5D%5B%5D=37.977836318314&markerCoords%5B11%5D%5B%5D=23.739282293245&markerCoords%5B12%5D%5B%5D=37.976881647483&markerCoords%5B12%5D%5B%5D=23.740620296448&markerCoords%5B13%5D%5B%5D=37.982825981453&markerCoords%5B13%5D%5B%5D=23.727735998109&markerCoords%5B14%5D%5B%5D=37.983225658536&markerCoords%5B14%5D%5B%5D=23.725163619965&markerCoords%5B15%5D%5B%5D=37.985503999516&markerCoords%5B15%5D%5B%5D=23.741879956797&markerCoords%5B16%5D%5B%5D=37.985965989064&markerCoords%5B16%5D%5B%5D=23.740783981048&markerCoords%5B17%5D%5B%5D=37.988372978289&markerCoords%5B17%5D%5B%5D=23.734550988302&markerCoords%5B18%5D%5B%5D=37.987315978389&markerCoords%5B18%5D%5B%5D=23.735077958554&markerCoords%5B19%5D%5B%5D=37.984752980992&markerCoords%5B19%5D%5B%5D=23.737610424869&markerCoords%5B20%5D%5B%5D=37.984830995556&markerCoords%5B20%5D%5B%5D=23.73682344798&markerCoords%5B21%5D%5B%5D=37.982856470626&markerCoords%5B21%5D%5B%5D=23.736542444676&markerCoords%5B22%5D%5B%5D=37.981759971008&markerCoords%5B22%5D%5B%5D=23.739374983124&markerCoords%5B23%5D%5B%5D=37.982971470337&markerCoords%5B23%5D%5B%5D=23.735667960718&markerCoords%5B24%5D%5B%5D=37.979285968468&markerCoords%5B24%5D%5B%5D=23.736766953953&markerCoords%5B25%5D%5B%5D=37.977672473062&markerCoords%5B25%5D%5B%5D=23.738278462552&markerCoords%5B26%5D%5B%5D=37.988805987407&markerCoords%5B26%5D%5B%5D=23.730064951815&markerCoords%5B27%5D%5B%5D=37.987108484376&markerCoords%5B27%5D%5B%5D=23.728878954425&markerCoords%5B28%5D%5B%5D=37.977386482526&markerCoords%5B28%5D%5B%5D=23.729580980726&markerCoords%5B29%5D%5B%5D=37.990893982351&markerCoords%5B29%5D%5B%5D=23.732839990407&markerCoords%5B30%5D%5B%5D=37.98339498695&markerCoords%5B30%5D%5B%5D=23.741757916287&markerCoords%5B31%5D%5B%5D=37.99002498854&markerCoords%5B31%5D%5B%5D=23.736159978434&markerCoords%5B32%5D%5B%5D=37.988131977618&markerCoords%5B32%5D%5B%5D=23.738597938791&markerCoords%5B33%5D%5B%5D=37.98668697942&markerCoords%5B33%5D%5B%5D=23.738854927942&markerCoords%5B34%5D%5B%5D=37.985660992563&markerCoords%5B34%5D%5B%5D=23.739970978349&markerCoords%5B35%5D%5B%5D=37.98668697942&markerCoords%5B35%5D%5B%5D=23.738044984639&markerCoords%5B36%5D%5B%5D=37.986464984715&markerCoords%5B36%5D%5B%5D=23.738271966577&markerCoords%5B37%5D%5B%5D=37.990245977417&markerCoords%5B37%5D%5B%5D=23.735881950706&markerCoords%5B38%5D%5B%5D=37.988585983403&markerCoords%5B38%5D%5B%5D=23.735167980194&markerCoords%5B39%5D%5B%5D=37.98760198988&markerCoords%5B39%5D%5B%5D=23.73324399814&markerCoords%5B40%5D%5B%5D=37.986628976651&markerCoords%5B40%5D%5B%5D=23.732608985156&markerCoords%5B41%5D%5B%5D=37.980853971094&markerCoords%5B41%5D%5B%5D=23.740870943293&markerCoords%5B42%5D%5B%5D=37.98025097698&markerCoords%5B42%5D%5B%5D=23.739755982533&markerCoords%5B43%5D%5B%5D=37.980857994407&markerCoords%5B43%5D%5B%5D=23.736068950966&markerCoords%5B44%5D%5B%5D=37.98260897398&markerCoords%5B44%5D%5B%5D=23.733834922314&markerCoords%5B45%5D%5B%5D=37.982322983444&markerCoords%5B45%5D%5B%5D=23.735049962997&markerCoords%5B46%5D%5B%5D=37.980452980846&markerCoords%5B46%5D%5B%5D=23.73441696167&markerCoords%5B47%5D%5B%5D=37.980891983025&markerCoords%5B47%5D%5B%5D=23.73314098455&markerCoords%5B48%5D%5B%5D=37.978629958816&markerCoords%5B48%5D%5B%5D=23.735751947388&markerCoords%5B49%5D%5B%5D=37.979266983457&markerCoords%5B49%5D%5B%5D=23.73448192142&markerCoords%5B50%5D%5B%5D=37.989459964447&markerCoords%5B50%5D%5B%5D=23.729909928516&markerCoords%5B51%5D%5B%5D=37.988856970333&markerCoords%5B51%5D%5B%5D=23.728858921677&markerCoords%5B52%5D%5B%5D=37.988036968745&markerCoords%5B52%5D%5B%5D=23.727607922629&markerCoords%5B53%5D%5B%5D=37.986308997497&markerCoords%5B53%5D%5B%5D=23.725444972515&markerCoords%5B54%5D%5B%5D=37.983569959179&markerCoords%5B54%5D%5B%5D=23.727157982066&markerCoords%5B55%5D%5B%5D=37.984343986027&markerCoords%5B55%5D%5B%5D=23.724547941238&markerCoords%5B56%5D%5B%5D=37.979155965149&markerCoords%5B56%5D%5B%5D=23.730397922918&markerCoords%5B57%5D%5B%5D=37.978648985736&markerCoords%5B57%5D%5B%5D=23.727822918445&markerCoords%5B58%5D%5B%5D=37.976973988116&markerCoords%5B58%5D%5B%5D=23.727975971997&spformat=true'

def scrap_all_pages(params):
    """
      Η κύρια συνάρτηση παίρνει τα στοιχεία της σχολής και επιστρέφει όλα τα σπίτια
      και τα ids
    """
    page_regex = re.compile(r'page=(\d+)')
    def first_page_params():
        """
        Αλλάζει τα params για να δείχνουν στην 1η σελίδα μήπως έχουμε λάθος σελίδα
        """
        page0 = 'page=0'
        return page_regex.sub(page0, params)
    params = first_page_params()
    data = []
    while scrap_spitogatos(params):  # όσο επιστρέφονται δεδομένα
        data += scrap_spitogatos(params)  # τα βάζουμε σε μια λίστα
        params = next_page_params(params)  # και αλλάζουμε σελίδα
    return data, ids


def next_page_params(params):
    page_regex = re.compile(r'page=(\d+)')
    next_page = 'page=' + str(int(page_regex.search(params).group(1)) + 50)
    return page_regex.sub(next_page, params)


def scrap_spitogatos(params):
    r = requests.post(url, headers=headers, data=params)
    j = r.json()
    sxoli = j['data']['university']['titleTag']
    data = j['data']['results']
    for spiti in data:
        ids.add(spiti['listing_id'])
    return data
