from pybaseball import batting_stats, playerid_reverse_lookup, pitching_stats
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

import json
import pandas as pd
import time

import string

import urllib.request, urllib.parse, urllib.error
import ssl
from requests_html import HTMLSession
import cfscrape

from urllib.request import Request, urlopen

from itertools import chain


hof = None
with open('hof.json') as json_file:
    hof = json.load(json_file)

player_data = {}
with open('player_data.json') as json_file:
    player_data_temp = json.load(json_file)
    for name in player_data_temp:
        player_data[player_data_temp[name]["id"].lower()] = player_data_temp[name]["card"]

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

base_page = "https://www.baseball-almanac.com/players/player.php?p="
base_img = "https://www.baseball-almanac.com"
http = httplib2.Http()
hdr = {'User-Agent': 'Mozilla/5.0'}
    

def save(d,file_name):
    with open(file_name, "w") as outfile:
        json.dump(d, outfile)

def apply_hof(row):
    if row["key_bbref"] in hof:
        return True
    else:
        return False

def apply_active(row):
    if row["mlb_played_last"] == 2023.0:
        return True
    else:
        return False

def apply_war(row):
    if row["WAR"] > 2.5 and row["mlb_played_last"] > 2020.0:
        return True
    elif row["WAR"] > 10.0 and row["mlb_played_last"] > 2010.0:
        return True
    elif row["WAR"] > 40.0:
        return True
    else:
        return False

def get_photo(row):
    if row["photo"] == None:
        url = base_page+row["key_bbref"]
        req = Request(url,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, features="html.parser")
        for img in soup.find_all("img"):
            if img.has_attr('src') and "/players/pics/" in img['src']:
                return base_img+img['src']
        
                
    else:
        return row["photo"]

def manual_photos(row):
    if row["photo"] == None:
        print(row["Name"])
        return input("Enter link: ") 
                
    else:
        return row["photo"]

def apply_photo(row):
    if row["key_bbref"] in player_data:
        return player_data[row["key_bbref"]]
    else:
        return None

def master_script():
    bat_data = batting_stats(1700, 2023, qual=200, ind=0)
    pit_data = pitching_stats(1700, 2023, qual=200, ind=0)

    bat_data = bat_data.rename(columns={'IDfg': 'key_fangraphs'})
    pit_data = pit_data.rename(columns={'IDfg': 'key_fangraphs'})
        
    bat_keys = playerid_reverse_lookup(bat_data['key_fangraphs'].tolist(), key_type='fangraphs')
    pit_keys = playerid_reverse_lookup(pit_data['key_fangraphs'].tolist(), key_type='fangraphs')

    bat_data = pd.merge(bat_data, bat_keys, how="inner", on=["key_fangraphs"])
    pit_data = pd.merge(pit_data, pit_keys, how="inner", on=["key_fangraphs"])

    bat_data['photo'] = bat_data.apply(apply_photo, axis=1)
    bat_data['is_hof'] = bat_data.apply(apply_hof, axis=1)
    bat_data['is_active'] = bat_data.apply(apply_active, axis=1)
    
    pit_data['photo'] = pit_data.apply(apply_photo, axis=1)
    pit_data['is_hof'] = pit_data.apply(apply_hof, axis=1)
    pit_data['is_active'] = pit_data.apply(apply_active, axis=1)
    
    bat_data = bat_data[bat_data.apply(apply_war, axis=1)]
    pit_data = pit_data[pit_data.apply(apply_war, axis=1)]

    bat_data['photo'] = bat_data.apply(get_photo, axis=1)
    pit_data['photo'] = pit_data.apply(get_photo, axis=1)
    
    save_files(bat_data, pit_data)


def load_files():
    bat_data = pd.read_json('bat_data.json', lines=True)
    pit_data = pd.read_json('pit_data.json', lines=True)

    return (bat_data, pit_data)

def save_files(bat_data, pit_data):
    bat_data.to_json('bat_data.json', orient='records', lines=True)
    pit_data.to_json('pit_data.json', orient='records', lines=True)

def update_photos():
    bat_data,pit_data = load_files()
    print("here")
    print(bat_data)
    bat_data['photo'] = bat_data.apply(manual_photos, axis=1)
    save_files(bat_data,pit_data)
                
        
def get_HOF():
    brefIDs = {}
    http = httplib2.Http()
    status, response = http.request('https://www.baseball-reference.com/awards/hof.shtml/')
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href'):
            if 'players/' in link['href'] and 'shtml' in link['href'] and 'pronunciation' not in link['href']:
                brefIDs[link['href'].split('/')[-1].split('.shtml')[0]] = True

    return brefIDs

bat_data,pit_data = load_files()
print(list(pit_data.columns))
