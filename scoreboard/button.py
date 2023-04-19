from gpiozero import LED, Button
from time import sleep
from signal import pause

import datetime
import sqlite3
import json
import pickle
import pytz
import requests

COORDINATOR_IP = "10.0.0.41:8000"

local_tz = pytz.timezone("Australia/Sydney")
db_path = "/home/scoreboard/scoreboard/scoreboard.db"
#db_path = "/home/scoreboard/Desktop/scoreboard/game.db"

plyr_a_up = Button(2)
plyr_a_dn = Button(3)

plyr_b_up = Button(5)
plyr_b_dn = Button(6)

ends_up = Button(17)
ends_dn = Button(27)

print("running")

def write_coordinator_score(js):
        response = requests.post('http://'+COORDINATOR_IP+'/games/add_score', json = js, timeout=5)
        return response.status_code
    

def write_coordinator_ends(js):
        response = requests.post('http://'+COORDINATOR_IP+'/games/add_ends', json = js)
        print(response)
        return response.status_code


def commit_score(competitor):
    
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cmd = f'UPDATE competitors SET score = {competitor["score"]} WHERE competitor_id={competitor["competitor_id"]}'
    print(cmd)
    res = cursor.execute(cmd)
    con.commit()
 #   if res.fetchone() is None:
 #       try:
 #           r_code = write_coordinator_score(competitor)
 #       except:
 #           pass
    return {
            "status": "ok",
    }

def update_score(button):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    parsed_rows = []
    
    sql = f'''SELECT competitor_id, player_id, first_name, last_name, score, game FROM competitors'''
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
                print(i['competitor_id'])
                score += 1
            if button.pin.number == 3:
                score -= 1            
            i['score'] = str(score)
            commit_score(i)
        if i['competitor_id'] == 2:
            score = int(i['score'])
            if button.pin.number == 5:
                print(i)
                score += 1
            if button.pin.number == 6:
                score -= 1            
            i['score'] = str(score)
            commit_score(i)
            
def commit_ends(js):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cmd = f'UPDATE games SET ends = {js["ends"]} WHERE game_id = {js["game_id"]}'
    
    print(cmd)
    res = cursor.execute(cmd)
#    if res.fetchone() is None:
#        try:
#            r_code = write_coordinator_ends(js)
#        except:
#            pass
    
    con.commit()
    return {
            "status": "ok",
    }        

def update_ends(button):
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    parsed_rows = []
    
    games = cursor.execute('''SELECT * FROM games WHERE finish_time is NULL''').fetchall()
    
    print(games)
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
        print(i)
        ends = int(i['ends'])
        if button.pin.number == 17:
            ends += 1
        if button.pin.number == 27:
            ends -= 1            
        i['ends'] = str(ends)
        commit_ends(i)


def get(button):
    print(button.pin.number)

while True:
    plyr_a_up.when_pressed = update_score
    plyr_a_dn.when_pressed = update_score
    
    plyr_b_up.when_pressed = update_score
    plyr_b_dn.when_pressed = update_score
    
    ends_up.when_pressed = update_ends
    ends_dn.when_pressed = update_ends
#     plyr_a_dn.when_pressed = get_game(plyr_a_dn, 1, "down")


