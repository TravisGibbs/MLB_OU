import json
from baseball_scraper import playerid_lookup
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
import pandas as pd

# Opening JSON file
def grab_card_images():
    f = open('player_data.json')
    data = json.load(f)
    count = 0 
    for key in data:
        key_split = key.split(" ")
        first, last = key_split[0], key_split[1:]
        id = last[0][:5]+first[:2]+"01"
        first_char = id[0]
        data[key]['id'] = id
        site = 'https://www.baseball-almanac.com/players/player.php?p='+id
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        try:
            page = urlopen(req)
        except:
            print("failed to open url " + key)
            continue
        soup = BeautifulSoup(page, features="lxml")
        header = soup.find('td',  {"class": "header"})
        if header:
            children = header.findChildren("img" , recursive=False)
            for child in children:
                if child.has_attr('src'):
                    data[key]['card'] =  "https://www.baseball-almanac.com"+child['src']
                    count += 1
                    break
        
        if "card" in data[key]:
            print("success" + key)
        else:
            print("failed to find pic " + key)
    print(count/len(data))
    # Closing file
    f.close()
    js_obj = json.dumps(data)
    file = open('player_data.txt', 'w')
    file.write(js_obj)
    file.close()



def round_two():
    f = open('player_data.json')
    data = json.load(f)
    players_who_need_cards = [x for x in data if 'card' not in data[x]]
    print(len(players_who_need_cards))
    try:
        for key in data:
            if 'card' not in data[key]:
                print(key)
                data[key]['card'] = input("input card:")
    except KeyboardInterrupt:
        pass
                
    f.close()
    js_obj = json.dumps(data)
    file = open('player_data.json', 'w')
    print("saving")
    file.write(js_obj)
    file.close()
    
round_two()