import os
from random import random, sample
from flask import Flask, render_template, url_for, json

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data_mining", "player_data.json")
data = json.load(open(json_url))

pitchers = []
batters = []
batter_table_cols = dict()
pitcher_table_cols = dict()

for player_name in data:
    player_info = data[player_name]
    if "batting_standard" in player_info:
        batters.append(player_name)
    else:
        pitchers.append(player_name)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play")
def play():
    questions = list()
    
    for _i in range(1000):
        row = 'totals'
        if random() < .5:
            row = 'avg'

        q = dict()
        q['row'] = row

        table = "pitching_standard"
        if random() < .5:
            players = sample(pitchers, 2)
        else:
            players = sample(batters, 2)
            table = 'batting_standard'

        cols = set(data[players[0]][table][row].keys())
        cols = cols.intersection(data[players[1]][table][row].keys())

        col = sample(cols, 1)[0]
        p1 = {'name': players[0], "value": data[players[0]][table][row][col], "img":data[players[0]]['img']}
        p2 = {'name': players[1], "value": data[players[1]][table][row][col], "img":data[players[1]]['img']}
        q['col'] = col
        q['players'] = [p1, p2]
        questions.append(q)

    return render_template("play.html", questions=questions)
    
@app.route('/lost')
def lost():
    return render_template('lost.html')
    
if __name__ == "__main__":
    app.run(debug=True)