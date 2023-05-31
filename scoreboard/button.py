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
db_path = "/home/scoreboard/scoreboard/scoreboard.db"

plyr_a_up = Button(2)
plyr_a_dn = Button(3)

plyr_b_up = Button(5)
plyr_b_dn = Button(6)

ends_up = Button(17)
ends_dn = Button(27)


def coordinator_ip(self):
    con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = con.cursor()
    return cursor.execute('''SELECT coordinator_ip FROM games''').fetchone()

def write_coordinator_score(js):
        response = requests.post('http://'+coordinator_ip()+'/games/add_score', json = js, timeout=10)
        return response.status_code
    

def write_coordinator_ends(js):
        response = requests.post('http://'+coordinator_ip()+'/games/add_ends', json = js, timeout=10)
        return response.status_code


def commit_score(competitor):
    
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cmd = "UPDATE competitors SET score = ? WHERE competitor_id=?"
    params = [competitor["score"], competitor["competitor_id"]]
    res = cursor.execute(cmd, params)
    con.commit()
    return {
            "status": "ok",
    }

def update_score(button):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    parsed_rows = []

    sql = "SELECT competitor_id, player_id, first_name, last_name, score, game FROM competitors"
    players = cursor.execute(sql).fetchall()

    competitors = []
    for player in players:
        competitors.append({
            "competitor_id": player['competitor_id'],
            "player_id": player['player_id'],
            "first_name": player['first_name'],
            "last_name": player['last_name'],
            "score": player['score'],
            "game_id": player['game']
         })  

    for i in competitors:
        
        if i['competitor_id'] == 1:
            score = int(i['score'])
            if button.pin.number == 2:
                score += 1
            if button.pin.number == 3:
                score -= 1            
            i['score'] = str(score)
            commit_score(i)
        if i['competitor_id'] == 2:
            score = int(i['score'])
            if button.pin.number == 5:
                score += 1
            if button.pin.number == 6:
                score -= 1            
            i['score'] = str(score)
            commit_score(i)
            
def commit_ends(js):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cmd = "UPDATE games SET ends = ? WHERE game_id = ?"
    params = [js["ends"], js["game_id"]]
    res = cursor.execute(cmd, params)

    con.commit()
    return {
            "status": "ok",
    }        

def update_ends(button):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    parsed_rows = []
    
    games = cursor.execute("SELECT * FROM games WHERE finish_time is NULL").fetchall()

    current_game = []
    for game in games:
        current_game.append({
            "game_id": game["game_id"],
            "name": game["name"],
            "start_time": game["start_time"],
            "finish_time": game["finish_time"],
            "ends": game["ends"],
            "winner": game["winner"],
         })  

    for i in current_game:
        ends = int(i['ends'])
        if button.pin.number == 17:
            ends += 1
        if button.pin.number == 27:
            ends -= 1            
        i['ends'] = str(ends)
        commit_ends(i)


while True:
    plyr_a_up.when_pressed = update_score
    plyr_a_dn.when_pressed = update_score
    
    plyr_b_up.when_pressed = update_score
    plyr_b_dn.when_pressed = update_score
    
    ends_up.when_pressed = update_ends
    ends_dn.when_pressed = update_ends


