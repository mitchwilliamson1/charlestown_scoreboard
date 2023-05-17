import datetime
import sqlite3
import json
import pickle
import pytz
import requests
import os


DEFAULT_GAME = {"game_id":-1, "name":"standard", 'competitors':
                    [{'player_id':'1', 'first_name': 'Player', 'last_name':'1', 'score': 0, 'logo':'charls.jpeg', 'competitor_display':{'competitor_display': 'default', 'competitor_display_id': 4}, 'team': '1'},
                    {'player_id':'2', 'first_name': 'Player', 'last_name':'2', 'score': 0, 'logo':'away.jpeg', 'competitor_display':{'competitor_display': 'default', 'competitor_display_id': 4} ,'team': '2'}],
                }


local_tz = pytz.timezone("Australia/Sydney")

class Game:
    def __init__(self):
        self.db_path = "scoreboard.db"
        self.init_database_tables()

    def init_database_tables(self):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS games
                     (game_id INTEGER PRIMARY KEY,
                     name text DEFAULT NULL,
                     start_time text, 
                     finish_time text, 
                     ends int DEFAULT 0,
                     winner text DEFAULT "",
                     coordinator_ip text DEFAULT "127.0.0.1:8000")''')

        c.execute('''CREATE TABLE IF NOT EXISTS competitors
                     (competitor_id INTEGER NOT NULL PRIMARY KEY,
                     player_id INTEGER DEFAULT "No Player",
                     first_name text DEFAULT "",
                     last_name text DEFAULT "",
                     score text DEFAULT "",
                     logo text DEFAULT "",
                     competitor_display INTEGER NOT NULL DEFAULT 4,
                     game INTEGER NOT NULL DEFAULT "No Game",
                     FOREIGN KEY (competitor_display)
                        REFERENCES competitor_displays (competitor_display_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (game)
                        REFERENCES games (game_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')

        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS competitor_displays
                     (competitor_display_id INTEGER PRIMARY KEY,
                     competitor_display text, "")''')
        conn.commit()

    def encode_if_required(self, str_val):
        try:
            return str_val.encode()
        except Exception:
            return str_val

    def coordinator_running(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()
        parsed_rows = []
        
        coordinator_ip = cursor.execute('''SELECT coordinator_ip FROM games''').fetchone()

        from ipaddress import ip_address
        ip, separator, port = coordinator_ip[0].rpartition(':')
        assert separator # separator (`:`) must be present
        port = int(port) # convert to integer
        ip = ip_address(ip)
        return self.check(ip, port)

    def check(self, host,port,timeout=5):
        import socket
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #presumably 
        sock.settimeout(timeout)
        try:
           sock.connect((str(host),port))
        except:
            return False
        else:
            sock.close()
            return True


    def get_game(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        parsed_rows = []
        
        games = cursor.execute('''SELECT * FROM games WHERE finish_time is NULL''').fetchall()

        if not games:
            self.create_game(DEFAULT_GAME, "127.0.0.1")
        else:
            for game in games:
                if game['ends'] < 0:
                    self.create_game(DEFAULT_GAME, "127.0.0.1")
                sql = """SELECT competitor_id, player_id, first_name, last_name, score, logo, cd.competitor_display FROM competitors as c
                        INNER JOIN competitor_displays AS cd
                        ON c.competitor_display = cd.competitor_display_id
                        where game = ?"""
                params = (game['game_id'],)
                # print("PARAMS ", type(params))
                players = cursor.execute(sql, params).fetchall()
                competitors = []
                for player in players:
                    print(player['competitor_display'])
                    competitors.append({
                        "competitor_id": player['competitor_id'],
                        "player_id": player['player_id'],
                        "first_name": player['first_name'],
                        "last_name": player['last_name'],
                        "score": player['score'],
                        "logo": player['logo'],
                        "competitor_display": player['competitor_display'],
                     })
                
                parsed_rows.append({
                    "game_id": game["game_id"],
                    "name": game["name"],
                    "start_time": game["start_time"],
                    "finish_time": game["finish_time"],
                    "ends": game["ends"],
                    "winner": game["winner"],
                    "coordinator": game["coordinator_ip"],
                    "coordinator_running": self.coordinator_running(),
                    "competitors": competitors,
                })

        return json.dumps(parsed_rows)

    def delete_all_games(self):
        try:
            con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            con.row_factory = sqlite3.Row
            cursor = con.cursor()

            sql = f'''DELETE FROM games '''
            cursor.execute(sql)
            sql = f'''DELETE FROM competitors '''
            cursor.execute(sql)
            con.commit()
        except:
            return "no data"


    def create_game(self, js, coordinator_ip):
        self.delete_all_games()

        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))

        coordinator_ip += ':8000'


        sql = "INSERT INTO games (game_id, name, start_time, coordinator_ip) VALUES(?,?,?,?);"
        params = (js['game_id'], js['name'], utc, coordinator_ip)
        game_id = cursor.execute(sql, params)

        for competitor in js['competitors']:
            print('COMPETITOR: ', competitor)
            sql = "INSERT INTO competitors (player_id, first_name, last_name, score, logo, competitor_display, game) VALUES(?,?,?,?,?,?,?);"
            params = (competitor['player_id'], competitor['first_name'], competitor['last_name'], competitor['score'], competitor['logo'], competitor['competitor_display']['competitor_display_id'], js['game_id'])
            cursor.execute(sql, params)
        con.commit()


    def add_ends(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f'UPDATE games SET ends = {js["ends"]} WHERE game_id = {js["game_id"]}'

        res = cursor.execute(cmd)
        con.commit()
        if res.fetchone() is None:
            try:
                r_code = self.write_coordinator_ends(js)
            except:
                pass
        
        return {
                "status": "ok",
        }


    def add_score(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f'UPDATE competitors SET score = {js["score"]} WHERE player_id={js["player_id"]} and game = {js["game_id"]}'

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

    def write_coordinator_score(self, js):
        response = requests.post('http://'+COORDINATOR_IP+'/games/add_score', json = js)
        print(response)
        return response.status_code


    def write_coordinator_ends(self, js):
        response = requests.post('http://'+COORDINATOR_IP+'/games/add_ends', json = js)
        print(response)
        return response.status_code



