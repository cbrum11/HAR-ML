import requests
import numpy as np
from bs4 import BeautifulSoup
import proxy
import useragent
import time


# grab_html_pages.py Description 
#-------------------------------
# Grab list of proxies and user-agents from respective websites.  Use priceQueries()
# to loop through smaller subset of primary price query. Use pageQueries()
# to iterate through all pages of a price query subset.  makeRequest() carries
# out the HTML get() request using a random proxy IP address and user-agent.  saveHtmlFile() 
# saves the page as an HTML file in the HTML_FILES directory.  lastPage() checks
# if the current HTML response object is the last page of a sub-price query (allowing
# the script to move forward to the next sub-price query). 
#-------------------------------

# Start Time
t0 = time.time()

# Get response object via proxy and user agent.  Test that response returned OK.  If not, Retry.
# Print proxy used to console...
def makeRequest(baseUrl, payload, proxy_list, agent_list):
    random_proxy = np.random.choice(proxy_list)
    random_agent = np.random.choice(agent_list)
    r = requests.get(baseUrl, params=payload, proxies=random_proxy, headers=random_agent)
    print(f'Proxy Used: {random_proxy} | R Status: {r.status_code} | R OK: {r.ok}' )
    while not r.ok:
        proxy_list[:] = [p for p in proxy_list if p.get('http') != random_proxy.get('http')]
        random_proxy = np.random.choice(proxy_list)
        random_agent = np.random.choice(agent_list)
        r = requests.get(baseUrl, params=payload, proxies=random_proxy, headers=random_agent) 
        print(f'Proxy Used: {random_proxy} | R Status: {r.status_code} | R OK: {r.ok}' )
    return r
    
# Checks if the HTML response contains 'No Results Found'
# to mark that we have reached the last page of a query.
def lastPage(soup):
    try:
        result_check = soup.find('h2').text
        return result_check == 'No Results Found'
    except:
        return False

# Saves a requests response object as an HTML file.  The file is named
# for the specific page and low price query used and the page.  
# For example, the page 3 query for $60,000 - $65,000 would have a filename 
# '60000_3.html'
def saveHtmlFile(response, low_price, page):
    f = open('HTML_FILES/'+str(low_price)+'_'+str(page)+'.html', 'w+')
    f.writelines(response.text)
    f.close()

# Iterate through all pages of a particular high/low sub-query price
# Break out when lastPage(soup) evaluates to TRUE
def pageQueries(low_query_price, high_query_price, proxy_list,agents):
    i = 1
    while i <= 20: # Website limits max of 20 pages on any search results
        baseUrl = 'https://www.har.com/search/dosearch/'
        payload = {
                    'page' : i,
                    'for_sale' : '1',
                    'region_id' : '1',
                    'property_class_id' : '1',
                    'listing_price_min' : low_query_price, 
                    'listing_price_max' : high_query_price,
                    'city' : 'Houston'
                    }
        r = makeRequest(baseUrl, payload,proxy_list,agents)
        soup = BeautifulSoup(r.text, 'html.parser')
        if not lastPage(soup):
            print('PAGE '+ str(i)) # Print Page Number
            saveHtmlFile(r,low_query_price,i)
            i += 1
        else:
            break

# Slice the main query min/max price into smaller steps.
# This ensures less than 20 pages are returned per sub-query.
# No queries are seen to return more than 20 pages for a step
# of 5000.
def priceQueries(min_price, max_price, step, proxy_list, agents):
    for i in range(min_price, max_price, step):
        # Ensure we don't return duplicate results for overlapping price queries
        # by adding $1 to each minimum price query (after the first query)
        if i == min_price:
            new_min = i
        else:
            new_min = i+1
        new_max = i+step
        print(new_min)
        print(new_max)
        pageQueries(new_min,new_max,proxy_list,agents)

#------------- Main Program ----------------------#    

# Note: no protection implemented if priceQueries
# calculates to a float number of steps.
# In other words, (min_price - max_price)/step needs 
# to evaluate to a whole number.
min_price = 0
max_price = 1000000
step = 5000

# Get list of proxies
proxies = proxy.getProxies()
# Get list of user-agents
agents = useragent.getAgents()

#Query all prices
priceQueries(min_price,max_price,step, proxies, agents)

# End time
t1 = time.time()
# Calculate Run Time
total = t1-t0
print('Total Run Time: '+str(total))