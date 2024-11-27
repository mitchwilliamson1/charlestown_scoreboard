import datetime
import sqlite3
import json
import pickle
import pytz
import requests
import config


DEFAULT_MASTER = [{'game_id': -1,'coordinator_ip':'192.168.15.200', 'name': 'standard', 'start_time': '2023-02-16 07:08:47.105881+00:00', 'finish_time': None, 'ends': 0, 'winner': '', 'competitors': [{'competitor_id': 1, 'player_id': 1, 'first_name': 'Player', 'last_name': '1', 'score': '0'}, {'competitor_id': 2, 'player_id': 2, 'first_name': 'Player', 'last_name': '2', 'score': '0'}]}]


local_tz = pytz.timezone("Australia/Sydney")

class Masterboard:
    def __init__(self):
        self.db_path = "bigboard.db"


    def setup(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        sql = "DELETE FROM masterboard;"
        cursor.execute(sql)

        sql = "INSERT INTO masterboard (ip, rink_id) VALUES(?, ?);"
        game_id = cursor.executemany(sql, js)

        con.commit()


    def encode_if_required(self, str_val):
        try:
            return str_val.encode()
        except Exception:
            return str_val

    def get_masterboard(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        player_1_score=0
        player_2_score=0
        ends=0

        player_1_logo = 'charls.jpeg'
        player_2_logo = 'away.jpeg'

        coordinator_ip = '192.168.15.200:8000'

        summed = []
        ips = cursor.execute('''SELECT * FROM bigboard''').fetchall()
        for ip in ips:
            try:
                response = requests.get('http://'+ip['ip']+'/get_game', timeout=2)
            except:
                continue
            data = json.loads(response.content)
            ends += int(data[0]['ends'])
            coordinator_ip = data[0]['coordinator']

            for i in data[0]['competitors']:
                if i['competitor_id'] == 1:
                    player_1_score += int(i['score'])
                    player_1_logo = i['logo']
                if i['competitor_id'] == 2:
                    player_2_score += int(i['score'])
                    player_2_logo = i['logo']

        for i in DEFAULT_MASTER[0]['competitors']:
            if i['player_id'] == 1:
                i['score'] = str(player_1_score)
                i['logo'] = str(player_1_logo)
            if i['player_id'] == 2:
                i['score'] = str(player_2_score)
                i['logo'] = str(player_2_logo)

        DEFAULT_MASTER[0]['ends'] = ends
        DEFAULT_MASTER[0]['coordinator_ip'] = coordinator_ip

        return json.dumps(DEFAULT_MASTER, indent=4, sort_keys=True)


    def write_coordinator_score(self, js):
        response = requests.post('http://'+config.COORDINATOR_IP+'/games/add_score', json = js)
        print(response)
        return response.status_code


    def write_coordinator_ends(self, js):
        response = requests.post('http://'+config.COORDINATOR_IP+'/games/add_ends', json = js)
        print(response)
        return response.status_code

