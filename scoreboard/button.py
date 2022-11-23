from gpiozero import LED, Button
from time import sleep
from signal import pause

import datetime
import sqlite3
import json
import pickle
import pytz
import requests

local_tz = pytz.timezone("Australia/Sydney")
db_path = "/home/scoreboard/scoreboard/game.db"
led = LED(4)

button = Button(2)
count = [0]
count1 = 0


def add_score(competitor):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cmd = f'UPDATE competitors SET score = {competitor["score"]} WHERE competitor_id={competitor["competitor_id"]}'
    print(cmd)

    res = cursor.execute(cmd)
    if res.fetchone() is None:
        try:
            r_code = self.write_coordinator_score(js)
        except:
            pass

    con.commit()
    return {
            "status": "ok",
    }

def get_game():
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    parsed_rows = []
    
    sql = f'''SELECT competitor_id, player_id, first_name, last_name, score FROM competitors'''
    players = cursor.execute(sql).fetchall()

    competitors = []
    for player in players:
        competitors.append({
            "competitor_id": player['competitor_id'],
            "player_id": player['player_id'],
            "first_name": player['first_name'],
            "last_name": player['last_name'],
            "score": player['score']
         })

    for i in competitors:
        if i['competitor_id'] == 1:
            score = int(i['score'])
            score += 1
            i['score'] = str(score)
            add_score(i)
    return json.dumps(parsed_rows)

def add():
    count[0]+=1
    print(count)


while True:
    button.when_pressed = get_game

#	if button.is_pressed:
#		count1 += 1
#		print(count1)



