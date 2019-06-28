import requests
from bs4 import BeautifulSoup

# useragent.py Description
#-----------------------------------
# Returns a list of dictionaries of the form [{User-Agent: usr1},{User-Agent: usr2}, ...]
# to be used as the user agent for a requests.get() call.
#----------------------------------

# Get soup object from request
def _getSoup():
    url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# Create a list of dictionaries from a list of user-agents.
# takes the form [{'User-Agent': usr1},{User-Agent: usr2}, ..]'
# to be passed to requests.get( headers= '') argument.
def makeDict(agentList):
    agent_dict_list = []
    for user in agentList:
        agent_dict_list.append({'User-Agent': user})
    return agent_dict_list

# Parse soup to find user-agents...
def getAgents():
    userList = []
    soup = _getSoup()
    td = soup.find_all('td', class_='useragent')
    for each in td:
        user = each.text
        userList.append(user)
    # Create properly formatted user-agent argument for
    # requests.get()
    agent_dict_list = makeDict(userList)
    print('Agents Grab Successful...')
    return agent_dict_list
