import string
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import json
import urllib.request, urllib.parse, urllib.error
import ssl
from urllib.request import Request, urlopen

from itertools import chain

stat_translator = {
        "W": "more Wins",
        "L": "more Losses",
        "win_loss_perc": "a higher Win Loss Percentage",
        "earned_run_average": "a higher ERA",
        "G": "more Games Played",
        "IP": "more Innings Pitched",
        "SV": "more Saves",
        "SHO": "more Shoutouts",
        "CG": "more Complete Games",
        "HR": "more Home Runs Allowed",
        "SO": "more Strike Outs",
        "earned_run_avg_plus": "a higher ERA+",
        "fip": "a higher FIP",
        "whip": "a higher WHIP",
        "hits_per_nine": "a higher H/9",
        "home_runs_per_nine": "a higher HR/9",
        "AB": "more At Bats",
        "R": "more Runs",
        "RBI": "more RBIs",
        "H": "more Hits",
        "HR": "more Home Runs",
        "SB": "more Stolen Bases",
        "BB": "more BB",
        "SO": "more SO",
        "batting_avg": "a higher batting avg",
        "onbase_perc": "a higher on base percentage",
        "slugging_perc": "a higher slugging percentage",
        "onbase_plus_slugging": "a higher ops",
        "onbase_plus_slugging_plus": "a higher ops+",
        "TB": "more total bases"
}

def grab_players_dict(page_links):
    d_players = dict()
    http = httplib2.Http()
    count = 0
    for i,link in enumerate(page_links):
        status, response = http.request('https://www.baseball-reference.com/'+link)
        for img in BeautifulSoup(response, parse_only=SoupStrainer('img'), features="html.parser"):
            if 'Photo of ' in img['alt']:
                player_name = img['alt'].split('Photo of ')[1]
                d_players[player_name] = dict() 
                d_players[player_name]['img'] = img['src']
                break
        player_short_name = (link.split('.shtml')[0]).split('/players/')[1][2:]
        d_players[player_name]['shortname'] = player_short_name
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
                            stat_name = str(stat['data-stat'])
                            if stat_name in stat_translator:
                                d_players[player_name][table_name]["totals"][stat_translator[stat_name]] = next(stat.children).string
        site= 'https://www.baseball-almanac.com/players/cards.php?p='+player_short_name
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, features="lxml")
        headers = soup.find_all('td',  {"class": "header"})
        for header in headers:
            children = header.findChildren("img" , recursive=False)
            for child in children:
                if child.has_attr('src'):
                    d_players[player_name]['card'] =  "https://www.baseball-almanac.com/"+child['src']
                    count += 1
                    break
    print(count/len(d_players))
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
print(str(len(d_players.keys()))+ " players wrote to file!")
js_obj = json.dumps(d_players)

file = open('player_data.txt', 'w')
file.write(js_obj)
file.close()