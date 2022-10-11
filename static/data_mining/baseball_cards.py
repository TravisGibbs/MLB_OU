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

def correct_questions():
    f = open('player_data.json')
    data = json.load(f)
    for player_name in data:
        if "pitching_standard" in data[player_name]:
            pitching_data = data[player_name]["pitching_standard"]["totals"]
            if "more Saves" in pitching_data:
                if pitching_data["more Saves"] == '0':
                    del data[player_name]["pitching_standard"]["totals"]["more Saves"]
            if "more Hits" in pitching_data:
                data[player_name]["pitching_standard"]["totals"]["more Hits conceded"] = pitching_data["more Hits"]
                del data[player_name]["pitching_standard"]["totals"]["more Hits"]
            if "more Runs" in pitching_data:
                data[player_name]["pitching_standard"]["totals"]["more Runs conceded"] = pitching_data["more Runs"]
                del data[player_name]["pitching_standard"]["totals"]["more Runs"]
            if "more Home Runs" in pitching_data:
                data[player_name]["pitching_standard"]["totals"]["more Home Runs conceded"] = pitching_data["more Home Runs"]
                del data[player_name]["pitching_standard"]["totals"]["more Home Runs"]
            if "more BB" in pitching_data:
                data[player_name]["pitching_standard"]["totals"]["more BB conceded"] = pitching_data["more BB"]
                del data[player_name]["pitching_standard"]["totals"]["more BB"]
            if "more SO" in pitching_data:
                data[player_name]["pitching_standard"]["totals"]["more Strikeouts"] = pitching_data["more SO"]
                del data[player_name]["pitching_standard"]["totals"]["more SO"]
        else:
            if "more SO" in  data[player_name]['batting_standard']['totals']:
                data[player_name]['batting_standard']['totals']['more Strikeouts'] = data[player_name]['batting_standard']['totals']["more SO"]
                del  data[player_name]['batting_standard']['totals']["more SO"]
    f.close()
    js_obj = json.dumps(data)
    file = open('player_data.json', 'w')
    print("saving")
    file.write(js_obj)
    file.close()

correct_questions()
#round_two()