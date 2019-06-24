import requests
from bs4 import BeautifulSoup

# proxy.py Description
#-----------------------------------
# Returns a list of dictionaries of the form [{http: proxy1},{http: proxy2}, ..]
# to be used as an IP mask for a requests.get() call.
#----------------------------------

# Get soup object from request
def _getSoup():
    url = 'https://free-proxy-list.net/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# Create a list of dictionaries from a list of proxies.
# takes the form '[{http: proxy1},{http: proxy2}, ..]'
# to be passed to requests.get( proxies= '') argument.
def makeDict(proxyList):
    proxy_dict_list = []
    for proxy in proxyList:
        proxy_dict_list.append({'http': proxy})
    return proxy_dict_list

# Parse soup to find proxies...
def getProxies():
    proxyList = []
    soup = _getSoup()
    tr = soup.find('tbody').find_all('tr')
    for each in tr:
        ipAddress = each.td.get_text()
        proxyList.append(ipAddress)
    # Create properly formatted proxy argument for
    # requests.get()
    proxy_dict_list = makeDict(proxyList)
    print('Proxies Grab Successful...')
    return proxy_dict_list