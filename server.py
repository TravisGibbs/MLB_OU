import os
from random import random, sample
from flask import Flask, render_template, url_for, json
from flask_socketio import SocketIO

gif_dict = {"zero":["https://i.pinimg.com/originals/05/88/a0/0588a024b5ba9a1310c2adbd03ae3a2d.gif","https://media1.giphy.com/media/ZIIeLTjVC119j0gKxf/giphy.gif", "https://i.gifer.com/76co.gif", "https://i.pinimg.com/originals/dc/bb/11/dcbb11b1e36e709d309e89a4b123e272.gif", "https://media4.giphy.com/media/3oEduEy55omiUyJWRa/200.gif", "https://1.bp.blogspot.com/-HxtpTBp3PEE/XxhSFxNRRRI/AAAAAAAAuw0/q0Vm-s1QspESuUOkupp7IlKbCxov1WqPwCLcBGAsYHQ/s1600/200.gif", "https://media4.giphy.com/media/3o6Zt1TrXW8uW2lE2I/giphy.gif"], 
    "bad":["https://media3.giphy.com/media/QXg3OUQ5hV74CkYJSa/giphy.gif","https://media3.giphy.com/media/XNDjiA7dGilsm3lX5v/giphy.gif?cid=ecf05e47jg0q1bxknagjo9qht5cyqosfpf8l6o115e6x3ikw&rid=giphy.gif&ct=g", "https://1.bp.blogspot.com/-ocdhldZmvAU/XxhSYhgFeUI/AAAAAAAAuxQ/fwAK5vtuLeM7-ZAwsNBl6mbmdkFVIG7aQCLcBGAsYHQ/s1600/tumblr_mm38p7bIiO1qz5922o1_400.gif", "https://1.bp.blogspot.com/-Kq98uMU_4k4/XxhSVTIsVXI/AAAAAAAAuxE/lZCyH92BRr0-m7lfvGlcnFW567J2xSQ5wCLcBGAsYHQ/s1600/giphy-2.gif", "https://c.tenor.com/xD_c_ZJD6IgAAAAC/strike-ponche.gif"], 
    "okay":["https://media3.giphy.com/media/MfHEgWjIL7mCtYt17w/giphy.gif?cid=ecf05e47jg0q1bxknagjo9qht5cyqosfpf8l6o115e6x3ikw&rid=giphy.gif&ct=g", "https://media0.giphy.com/media/VlMUdPvZ360m6aoi7N/giphy.gif", "https://media3.giphy.com/media/dcj2SyXR36vuw/giphy.gif", "https://i.pinimg.com/originals/b8/bd/29/b8bd293d8235355159e6c5d6553f681c.gif"], 
    "great":["https://media1.giphy.com/media/RbaNKznn9mnJ5UgW56/giphy.gif?cid=6c09b9524169ed8d773be82f3a13657cf2d54c5dbbef2f1e&rid=giphy.gif&ct=g","http://cdn3.vox-cdn.com/assets/4420793/bonds-piro.gif", "https://media2.giphy.com/media/7T5sCHY5Wo8tO5ElNb/giphy.gif?cid=ecf05e47dp7xa0nzorggyrtydqfd3namsvcrf2vowsrpqsbn&rid=giphy.gif&ct=g", "https://media3.giphy.com/media/l2SpUepuM4qgdzbeU/giphy.gif?cid=ecf05e47a1q6aqu3dhx7dbilusm3u4968ip1jz21x8vgnql6&rid=giphy.gif&ct=g", 'https://media3.giphy.com/media/1rMYYnUiubloSDL2yr/giphy.gif?cid=ecf05e47rgit1gaozn0q9s41qdh4dvcuu4sdajreafrvoww5&rid=giphy.gif&ct=g']}


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
player_data_json_url = os.path.join(SITE_ROOT, "static/data_mining", "player_data.json")
batted_ball_data_json_url = os.path.join(SITE_ROOT, "static/data_mining", "hits_data.json")

player_data = json.load(open(player_data_json_url))
batted_ball_data =json.load(open(batted_ball_data_json_url))

pitchers = []
batters = []
batter_table_cols = dict()
pitcher_table_cols = dict()

for player_name in player_data:
    player_info = player_data[player_name]
    if "batting_standard" in player_info:
        batters.append(player_name)
    else:
        pitchers.append(player_name)

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")


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
    non_validated_data = [key for key in batted_ball_data if "validated" in batted_ball_data[key]]
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
        row = 'totals'

        q = dict()
        q['row'] = row

        table = "pitching_standard"
        if random() < .5:
            players = sample(pitchers, 2)
        else:
            players = sample(batters, 2)
            table = 'batting_standard'

        cols = set(player_data[players[0]][table][row].keys())
        cols = cols.intersection(player_data[players[1]][table][row].keys())

        col = sample(cols, 1)[0]
        img0 = player_data[players[0]]['img']
        img1 = player_data[players[1]]['img']
        if 'card' in player_data[players[0]]:
            img0 = player_data[players[0]]['card']
        if 'card' in player_data[players[1]]:
            img1 = player_data[players[1]]['card']
        p1 = {'name': players[0], "value": float(player_data[players[0]][table][row][col]), "img":img0}
        p2 = {'name': players[1], "value": float(player_data[players[1]][table][row][col])  , "img":img1}
        q['col'] = "Who had " + col + " in their career?"
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