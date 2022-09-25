import string
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import json
from itertools import chain

def js_list(encoder, data):
    pairs = []
    for v in data:
        pairs.append(js_val(encoder, v))
    return "[" + ", ".join(pairs) + "]"

def js_dict(encoder, data):
    pairs = []
    for k, v in data.items():
        pairs.append(k + ": " + js_val(encoder, v))
    return "{" + ", ".join(pairs) + "}"

def js_val(encoder, data):
    if isinstance(data, dict):
        val = js_dict(encoder, data)
    elif isinstance(data, list):
        val = js_list(encoder, data)
    else:
        val = encoder.encode(data)
    return val

def grab_players_dict(page_links):
    d_players = dict()
    http = httplib2.Http()
    for i,link in enumerate(page_links):
        status, response = http.request('https://www.baseball-reference.com/'+link)
        for img in BeautifulSoup(response, parse_only=SoupStrainer('img'), features="html.parser"):
            if 'Photo of ' in img['alt']:
                player_name = img['alt'].lstrip('Photo of ')
                d_players[player_name] = dict() 
                d_players[player_name]['img'] = img['src']
                break
        table_soup = BeautifulSoup(response, features="html.parser")
        for table in table_soup.find_all('table', recursive=True):
            footers = table.findChildren("tfoot")
            table_name = table['id']  
            if "standard" in  table_name or "Standard" in table_name:
                if table_name not in d_players[player_name]:
                    d_players[player_name][table_name] = dict()
                if len(footers) == 1:
                    rows = footers[0].findChildren("tr")
                    d_players[player_name][table_name]["totals"] = dict()
                    for stat in rows[0].findChildren("td"):
                        if len(list(stat.children)) >0:
                            d_players[player_name][table_name]["totals"][str(stat['data-stat'])] = next(stat.children).string
                    d_players[player_name][table_name]["avg"] = dict()
                    for stat in rows[1].findChildren("td"):
                        if len(list(stat.children)) >0:
                            d_players[player_name][table_name]["avg"][str(stat['data-stat'])] = next(stat.children).string
                        
    return d_players

def get_active_players():
    links = []
    alphabet_list = list(string.ascii_lowercase)
    http = httplib2.Http()
    for letter in alphabet_list:
        status, response = http.request('https://www.baseball-reference.com/players/'+letter+'/')
        for strong_text in BeautifulSoup(response, parse_only=SoupStrainer('strong'), features="html.parser"):
            for link in list(strong_text.children):
                try:
                    if link.has_attr('href'):
                        if 'player' in link['href'] and 'shtml' in link['href'] and 'pronunciation' not in link['href']:
                            links.append(link['href'])
                except:
                    pass
    return links
    
def get_HOF():
    links = []
    http = httplib2.Http()
    status, response = http.request('https://www.baseball-reference.com/awards/hof.shtml/')
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            if 'players/' in link['href'] and 'shtml' in link['href'] and 'pronunciation' not in link['href']:
                links.append(link['href'])
    return links

def get_WAR_leaders():
    links = set()
    http = httplib2.Http()
    status, response = http.request('https://www.baseball-reference.com/leaders/WAR_career.shtml')
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            if 'players/' in link['href'] and 'shtml' in link['href'] and 'pronunciation' not in link['href']:
                links.add(link['href'])
    return links

war_players_set = set(get_WAR_leaders())
hof_players_set = set(get_HOF())
active_players_set = set(get_active_players())
print(len(war_players_set), len(hof_players_set), len(active_players_set))
players_set = set(chain(war_players_set, hof_players_set, active_players_set))
d_players = grab_players_dict(list(players_set))
encoder = json.JSONEncoder(ensure_ascii=False)
js_obj = js_val(encoder, d_players)

file = open('player_data.txt', 'w')
file.write(js_obj)
file.close()