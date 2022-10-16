import requests
import urllib.request
from plotly.subplots import make_subplots
from scipy.signal import argrelextrema
import json
from tqdm import tqdm

from pyAudioAnalysis import ShortTermFeatures as aF
from pyAudioAnalysis import audioBasicIO as aIO 
import numpy as np 
import subprocess
import os
import httplib2
import plotly
import plotly.graph_objs as go 
from bs4 import BeautifulSoup, SoupStrainer

# Example video link
#https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=single%7Cdouble%7Ctriple%7Chome%5C.%5C.run%7C&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=6%7C5%7C&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=team-date&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&type=details&player_id=MIN&ep_game_date=2019-04-20

def gather_hard_hit_videos(hits):

    f = open('hits_data.json')
    data = json.load(f)

    http = httplib2.Http()
    if hits:
        prefix = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=single%7Cdouble%7Ctriple%7Chome%5C.%5C.run%7C&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=6%7C5%7C&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=team-date&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&type=details"#&player_id=MIN&ep_game_date=2019-04-20
        status, response = http.request('https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=single%7Cdouble%7Ctriple%7Chome%5C.%5C.run%7C&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=6%7C5%7C&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=team-date&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc#results')
    else:
        prefix = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=field\.\.out|double\.\.play|force\.\.out|&hfGT=R|&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2022|2021|2020|2019|2018|2017|2016|2015|&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=6|5|&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=team-date&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&type=details"#&player_id=MIN&ep_game_date=2019-04-20
        status, response = http.request('https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=field%5C.%5C.out%7Cdouble%5C.%5C.play%7Cforce%5C.%5C.out%7C&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2022%7C2021%7C2020%7C2019%7C2018%7C2017%7C2016%7C2015%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=6%7C5%7C&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=team-date&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc#results')

    soup = BeautifulSoup(response ,features="html.parser")
    rows = soup.find_all("tr")
    hits_page_links = []
    for i,row in enumerate(rows):
        if row.has_attr('data-game-date'):
            hits_page_links.append(prefix+"&player_id="+row['data-player-id']+"&ep_game_date="+row['data-game-date'])

    print("grabbing links from hit pages now")
    # Grabbed game videos
    hit_links = []
    for j,hits_page_link in enumerate(hits_page_links):
        status, response = http.request(hits_page_link)
        # 300 * 4 = 1200 videos
        if j < 299:
            print(j)
            for i,hit_row in enumerate(BeautifulSoup(response, parse_only=SoupStrainer('tr'), features="html.parser")):
                if i > 0  and i < 5:
                    childern = list(hit_row.findChildren(recursive=True))
                    title = childern[13].get_text()
                    data[title] = dict()
                    data[title]['EV'] = childern[2].get_text()
                    data[title]['pitcher'] = childern[3].get_text()
                    data[title]['batter'] = childern[4].get_text()
                    data[title]['dist'] = childern[5].get_text()
                    if "singles" in title:
                        data[title]["result"] = "single"
                    elif "lines out" in title or "flies out" in title:
                        data[title]["result"] = "out"
                    elif "ground-rule-double" in title:
                        data[title]["result"] = "ground-rule-double"
                    elif "doubles" in title:
                        data[title]["result"] = "double"
                    elif "triples" in title:
                        data[title]["result"] = "triple"
                    else:
                        data[title]["result"] = "homerun"
                    try:
                        data[title]['savant_link'] = "https://baseballsavant.mlb.com"+str(list(childern[14].findChildren())[0]).split('"')[1]
                    except:
                        del data[title]
        else:
            break


    js_obj = json.dumps(data)
    file = open('hits_data.json', 'w')
    print("saving")
    file.write(js_obj)
    file.close()

    print("Grabbing Video SRC")
    i = 0
    for key in data:
        status, response = http.request(data[key]['savant_link'])
        video = BeautifulSoup(response, parse_only=SoupStrainer('source'), features="html.parser")
        video_url = str(video).split('"')[1]
        data[key]["video url"] = video_url
        print(i)
        i+=1

    
    js_obj = json.dumps(data)
    file = open('hits_data.json', 'w')
    print("saving")
    file.write(js_obj)
    file.close()



# Saves a wav file of a random hit and returns a link and title for video
def grab_clip_and_audio(video: False, gen_audio: False) -> list[str]:
    # Need to find a better way to access replays at random
    if not video:
        res = requests.get("https://baseballsavant.mlb.com/player/random-video?playerId=607625&playerType=1&videoType=2b&_=1664542970837").json()
        title = res['title']
        link = res['link']
    else:
        [title, link] = video

    file_name = "temp_input.mp4"
    urllib.request.urlretrieve(link, file_name)
    if gen_audio:
        command = "ffmpeg -i ./temp_input.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
        subprocess.call(command, shell=False)

    return [link, title]

# Read audio for energy features and return timestamps for video to show only the hit
def grab_time_stamp(plot=False, title="")-> list[int]:
    # read audio data from file 
    # (returns sampling freq and signal as a numpy array)
    fs, s = aIO.read_audio_file("./audio.wav")
    s = aIO.stereo_to_mono(s)
    duration = len(s) / float(fs)

    # extract short-term features using a 50msec non-overlapping windows
    # can adjust these vars for more accurate timestamps
    win, step = 0.010, 0.010

    [f, fn] = aF.feature_extraction(s, fs, int(fs * win), int(fs * step))

    # Find energy which will be used to detect contact
    time = np.arange(0, duration - step, win) 
    energy = f[fn.index('energy'), (int(2/win)):]
    delta_energy = f[fn.index('delta energy'), (int(2/win)):]
    energy_entropy = f[fn.index('energy_entropy'), (int(2/win)):]
    spectral_spread = f[fn.index('spectral_spread'), (int(2/win)):]
    spectral_centroid = f[fn.index('spectral_centroid'), (int(2/win)):]
    delta_sprectral_centroid = f[fn.index('delta spectral_centroid'), (int(2/win)):]
    # print('Feature names:')
    # for i, nam in enumerate(fn):
    #     print(f'{i}:{nam}')

    # Find the window with the most energy
    index = np.argmin(energy_entropy)

    local_max_energy = argrelextrema(energy, np.greater)
    start = 0
    end = time[index]+.05
    if time[index] > 2:
        start = 1
    
    if plot:
        fig = make_subplots(rows=2, cols=3)

        fig.add_trace(
            go.Scatter(x=time, y=energy),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=time, y=energy_entropy),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=time, y=delta_energy),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(x=time, y=spectral_spread),
            row=2, col=2
        )

        fig.add_trace(
            go.Scatter(x=time, y=spectral_centroid),
            row=2, col=3
        )

        fig.add_trace(
            go.Scatter(x=time, y=delta_sprectral_centroid),
            row=1, col=3
        )

        fig.update_layout(height=600, width=1000, title_text="Side By Side Subplots")
        fig.show()

    os.remove('./audio.wav')

    return [start, end]

def get_data_for_q():
    [link, title] = grab_clip_and_audio()
    [timestamp_start, timestamp_end] = grab_time_stamp(True)
    print(link, title)
    print(timestamp_start, timestamp_end)
    return [link, title, timestamp_start, timestamp_end]


def label_data():
    # f = open('labled_hits.json')
    # data = json.load(f)
    # f.close()
    f = open('hits_data.json')
    data_to_be_labled = json.load(f)
    keys = list(data_to_be_labled.keys())
    for i in tqdm (range (len(keys)), 
               desc="Predicting Audio Times", 
               ascii=False, ncols=75):
        key = keys[i]
        try:
            if "predicted_end_time" in  data_to_be_labled[key] and "validated" not in data_to_be_labled[key]:
                continue
            elif "validated" in data_to_be_labled[key]:
                data_to_be_labled[key]["validated_time"] = data_to_be_labled[key]["predicted_end_time"]
            try:
                urllib.request.urlretrieve(data_to_be_labled[key]["video url"], "temp.mp4")
            except:
                print("request error")
                continue
            command = "ffmpeg -i ./temp.mp4 -ab 160k -ac 2 -ar 44100 -vn temp.wav"
            subprocess.call(command, shell=False, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            fs, s = aIO.read_audio_file("./temp.wav")
            s = aIO.stereo_to_mono(s)
            duration = len(s) / float(fs)
            # extract short-term features using a 50msec non-overlapping windows
            # can adjust these vars for more accurate timestamps
            win, step = 0.01, 0.01
            [f, fn] = aF.feature_extraction(s, fs, int(fs * win), int(fs * step))
            # Find energy which will be used to detect contact
            time = np.arange(win*10, duration/2 - step, win) 
            energy = f[fn.index('energy'), 10:int(duration/2/win)]
            # delta_energy = f[fn.index('delta energy'), :]
            energy_entropy = f[fn.index('energy_entropy'), 10:int(duration/2/win)]
            # spectral_spread = f[fn.index('spectral_spread'), :]
            # spectral_centroid = f[fn.index('spectral_centroid'), :]
            # delta_sprectral_centroid = f[fn.index('delta spectral_centroid'), :]

            # Find the targeted window
            index = np.argmin(energy_entropy)

            local_max_energy = argrelextrema(energy, np.greater)
            start = 0
            end = time[index]-win*10

            # print("predicted time " + str(end))
            
            # fig = make_subplots(rows=2, cols=3)

            # fig.add_trace(
            #     go.Scatter(x=time, y=energy),
            #     row=1, col=1
            # )

            # fig.add_trace(
            #     go.Scatter(x=time, y=energy_entropy),
            #     row=1, col=2
            # )
                
            # fig.add_trace(
            #     go.Scatter(x=time, y=delta_energy),
            #     row=2, col=1
            # )

            # fig.add_trace(
            #     go.Scatter(x=time, y=spectral_spread),
            #     row=2, col=2
            # )

            # fig.add_trace(
            #     go.Scatter(x=time, y=spectral_centroid),
            #     row=2, col=3
            # )

            # fig.add_trace(
            #     go.Scatter(x=time, y=delta_sprectral_centroid),
            #     row=1, col=3
            # )

            # fig.update_layout(height=600, width=1000, title_text="Side By Side Subplots")
            # fig.show()
            data_to_be_labled[key]["predicted_end_time"] = end+.25
            os.remove('./temp.wav')

        except KeyboardInterrupt:
            os.remove('./temp.wav')
            break

    
    js_obj = json.dumps(data_to_be_labled)
    file = open('hits_data.json', 'w')
    print("saving")
    file.write(js_obj)
    file.close()


label_data()
#get_data_for_q()
#gather_hard_hit_videos(False)

# IDEA:
# Use a request to get a random video of mlb player getting a hit IE:

# https://baseballsavant.mlb.com/player/random-video?playerId=607625&playerType=1&videoType=hit&_=1664542970837

# Possibly only download moov atom

# Extract audio from video @ link on server side flask and find noise of contact to clip video
# This could involve tuning certain filters on the audio to find a fairly accurate measure of when the ball is hit

# Pass timestamp of contact, link to video, and outcome to front end application for game

# What's next...
# Set up server and basic page to display clips and make sure everything works logically
# Re use the old gauntlet page or ammend it to have a new play option
# Add buttons and game mechanics to page such as a count down timer after video finishes and buttons to select result of at bat
# When selecting clips select all kinds of plays but with a higher proportion of hits than outs
# Profit?