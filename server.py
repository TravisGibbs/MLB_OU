import os
from random import random, sample, choice
from flask import Flask, render_template, url_for, json, request
from flask_socketio import SocketIO
import pandas as pd
from decimal import *

def apply_war(row):
    if row["mlb_played_last"] > 1930.0:
        return True
    else:
        return False


gif_dict = {"zero":["https://i.pinimg.com/originals/05/88/a0/0588a024b5ba9a1310c2adbd03ae3a2d.gif","https://media1.giphy.com/media/ZIIeLTjVC119j0gKxf/giphy.gif", "https://i.gifer.com/76co.gif", "https://i.pinimg.com/originals/dc/bb/11/dcbb11b1e36e709d309e89a4b123e272.gif", "https://media4.giphy.com/media/3oEduEy55omiUyJWRa/200.gif", "https://1.bp.blogspot.com/-HxtpTBp3PEE/XxhSFxNRRRI/AAAAAAAAuw0/q0Vm-s1QspESuUOkupp7IlKbCxov1WqPwCLcBGAsYHQ/s1600/200.gif", "https://media4.giphy.com/media/3o6Zt1TrXW8uW2lE2I/giphy.gif"], 
    "bad":["https://media3.giphy.com/media/QXg3OUQ5hV74CkYJSa/giphy.gif","https://media3.giphy.com/media/XNDjiA7dGilsm3lX5v/giphy.gif?cid=ecf05e47jg0q1bxknagjo9qht5cyqosfpf8l6o115e6x3ikw&rid=giphy.gif&ct=g", "https://1.bp.blogspot.com/-ocdhldZmvAU/XxhSYhgFeUI/AAAAAAAAuxQ/fwAK5vtuLeM7-ZAwsNBl6mbmdkFVIG7aQCLcBGAsYHQ/s1600/tumblr_mm38p7bIiO1qz5922o1_400.gif", "https://1.bp.blogspot.com/-Kq98uMU_4k4/XxhSVTIsVXI/AAAAAAAAuxE/lZCyH92BRr0-m7lfvGlcnFW567J2xSQ5wCLcBGAsYHQ/s1600/giphy-2.gif", "https://c.tenor.com/xD_c_ZJD6IgAAAAC/strike-ponche.gif"], 
    "okay":["https://media3.giphy.com/media/MfHEgWjIL7mCtYt17w/giphy.gif?cid=ecf05e47jg0q1bxknagjo9qht5cyqosfpf8l6o115e6x3ikw&rid=giphy.gif&ct=g", "https://media0.giphy.com/media/VlMUdPvZ360m6aoi7N/giphy.gif", "https://media3.giphy.com/media/dcj2SyXR36vuw/giphy.gif", "https://i.pinimg.com/originals/b8/bd/29/b8bd293d8235355159e6c5d6553f681c.gif"], 
    "great":["https://media1.giphy.com/media/RbaNKznn9mnJ5UgW56/giphy.gif?cid=6c09b9524169ed8d773be82f3a13657cf2d54c5dbbef2f1e&rid=giphy.gif&ct=g","http://cdn3.vox-cdn.com/assets/4420793/bonds-piro.gif", "https://media2.giphy.com/media/7T5sCHY5Wo8tO5ElNb/giphy.gif?cid=ecf05e47dp7xa0nzorggyrtydqfd3namsvcrf2vowsrpqsbn&rid=giphy.gif&ct=g", "https://media3.giphy.com/media/l2SpUepuM4qgdzbeU/giphy.gif?cid=ecf05e47a1q6aqu3dhx7dbilusm3u4968ip1jz21x8vgnql6&rid=giphy.gif&ct=g", 'https://media3.giphy.com/media/1rMYYnUiubloSDL2yr/giphy.gif?cid=ecf05e47rgit1gaozn0q9s41qdh4dvcuu4sdajreafrvoww5&rid=giphy.gif&ct=g']}


stat_translator_bat = {
    "H": "more Hits",
    "2B": "more doubles",
    "HR": "more Home Runs",
    "R": "more Runs",
    "AB": "more At Bats",
    "RBI": "more RBIs",
    "SB": "more Stolen Bases",
    "BB": "more BB",
    "SO": "more SO",
    "AVG": "a higher batting avg",
    "OPS": "a higher ops",
    "OBP": "a higher on base percentage",
    "SLG": "higher slugging",  
    "WAR": "more bWAR"
}

dehex_d = {
    "0":"0",
    "1":"1",
    "2":"2",
    "3":"3",
    "4":"4",
    "5":"5",
    "6":"6",
    "7":"7",
    "8":"8",
    "9":"9",
    "A":"10",
    "B":"11",
    "C":"12",
    "D":"13",
    "E":"14",
    "F":"15",
}

rehex_d = {
    "0":"0",
    "1":"1",
    "2":"2",
    "3":"3",
    "4":"4",
    "5":"5",
    "6":"6",
    "7":"7",
    "8":"8",
    "9":"9",
    "10":"A",
    "11":"B",
    "12":"C",
    "13":"D",
    "14":"E",
    "15":"F",
}

stat_translator_pit = {
    "W": "more Wins",
    "L": "more Losses",
    "ERA": "a higher ERA",
    "G": "more Games Played",
    "IP": "more Innings Pitched",
    "SV": "more Saves",
    "ShO": "more Shoutouts",
    "CG": "more Complete Games",
    "HR": "more Home Runs Allowed",
    "SO": "more Strike Outs",
    "FIP": "a higher FIP",
    "WHIP": "a higher WHIP",
    "H/9": "a higher H/9",
    "HR/9": "a higher HR/9",
    "K/9": "a higher K/9",   
    "WAR": "more bWAR"
}

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
bat_data_json_url = os.path.join(SITE_ROOT, "static/data_mining", "bat_data.json")
pit_data_json_url = os.path.join(SITE_ROOT, "static/data_mining", "pit_data.json")
translation_json_url = os.path.join(SITE_ROOT, "static/data_mining", "translation.json")

batted_ball_data_json_url = os.path.join(SITE_ROOT, "static/data_mining", "hits_data.json")

batted_ball_data =json.load(open(batted_ball_data_json_url))

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")

tranlator = json.load(open(translation_json_url))

def load_files():
    bat_data = pd.read_json(bat_data_json_url, lines=True)
    pit_data = pd.read_json(pit_data_json_url, lines=True)

    return (bat_data, pit_data)

batters, pitchers = load_files()

batters = batters[batters.apply(apply_war, axis=1)]
pitchers = pitchers[pitchers.apply(apply_war, axis=1)]

def pad(unpadded_str):
    padded_str = unpadded_str
    if len(unpadded_str) < 4096:
        padded_str = "0"*(4096-len(unpadded_str)) + unpadded_str

    return padded_str

def scramble(str_arr):
    new_arr = []
    for i,str in enumerate(str_arr):
        new_arr.append(rehex_d[tranlator[i][dehex_d[str]]])
    return new_arr

@app.route("/again", methods=["GET"])
def again():
    return render_template("elevator.html", message="again?")

@app.route("/elevator", methods=["GET"])
def elevator():
    return render_template("elevator.html", message="welcome")

@app.route("/iot",  methods=['POST'])
def iot():
    record = json.loads(request.data)
    with open('/data.txt', 'w') as f:
        f.write(json.dumps(record, indent=2))
    print(record)
    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/image/<image_str>", methods=["GET"])
def image(image_str):
    if image_str == "empty":
        image_str = ""
    elif image_str == "random":
        image_str = ""
        hexValues = list(dehex_d.keys())
        for _i in range(4096):
            image_str += choice(hexValues)
    padded_str = pad(image_str)

    str_arr = list(padded_str)
    str_arr_dehexed = "".join(scramble(str_arr))

    return render_template("imageView.html", image=str_arr_dehexed, input=padded_str)

@socketio.on("update")
def update(data):
    key= data['key']
    time_end = data['value']
    batted_ball_data[key]['validated_time'] = time_end
    batted_ball_data[key]['validated'] = True

    js_obj = json.dumps(batted_ball_data)
    file = open('./static/data_mining/hits_data.json', 'w')
    print("saving")
    file.write(js_obj)
    file.close()

@app.route("/hit")
def hit():
    non_validated_data = [key for key in batted_ball_data if "validated" not in batted_ball_data[key]]
    play = sample(non_validated_data, 1)[0]
    return render_template("hit.html", vid_url=batted_ball_data[play]["video url"], title=play, predicted_time=batted_ball_data[play]["predicted_end_time"])

@app.route("/dong")
def dong():
    questions = list()
    validated_keys = [key for key in batted_ball_data if "validated" in batted_ball_data[key]]
    for key in validated_keys:
        questions.append({"title":key, "url": batted_ball_data[key]["video url"], "result": batted_ball_data[key]['result'] ,"stop_time": batted_ball_data[key]["validated_time"]})
    return render_template("dong.html", questions=questions)

@app.route("/play")
def play():
    questions = list()
    
    for _i in range(1000):

        q = dict()
        
        if random() < .5:
            translator = stat_translator_bat         
            data = batters
        else:
            translator = stat_translator_pit            
            data = pitchers

        players = data.sample(2).reset_index()
        question = sample(list(translator.keys()), 1)[0]

        p1 = {'name': players.iloc[0]["Name"], "value": float(Decimal(float(players.iloc[0][question])).quantize(Decimal('1e-4'))), "img":players.iloc[0]["photo"]}
        p2 = {'name': players.iloc[1]["Name"], "value": float(Decimal(float(players.iloc[1][question])).quantize(Decimal('1e-4'))), "img":players.iloc[1]["photo"]}
        
        q['col'] = "Who had " + translator[question] + " in their career?"
        q['players'] = [p1, p2]
        
        questions.append(q)

    return render_template("play.html", questions=questions)
    
@app.route('/lost/<score>')
def lost(score):
    score = int(score)
    text = ""
    if score < 2:
        text = "Swing and a miss..."
        gif_url = sample(gif_dict["zero"], 1)[0]
    elif score < 10:
        text = "You can do better than that..."
        gif_url = sample(gif_dict["bad"], 1)[0]
    elif score < 20:
        text = "Good not great..."
        gif_url = sample(gif_dict['okay'], 1)[0]
    else:
        text = "You will be among the legends now..."
        gif_url = sample(gif_dict["great"], 1)[0]
    return render_template('lost.html', score=str(score), gif_url=gif_url, text=text)
    
if __name__ == "__main__":
    app.run(debug=True)
