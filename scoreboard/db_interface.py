import datetime
import sqlite3
import json
import pickle
import pytz
import requests
import os


DEFAULT_GAME = {"game_id":-1, 
        "name":"standard", 
        'competition': {'competition_id': 3}, 
        'sponsor': {'sponsor_logo': 'belle_whitebg.png'}, 
        "finish_time":None, 
        'competitors': {
            '1': {'1': {'player_id':'1', 'first_name': 'Player', 'last_name':'1', 'is_skipper': 1, 'score': 0, 'sets': 0, 'display':{'display': 'Default', 'display_id': 1} }},
            '2': {'1': {'player_id':'2', 'first_name': 'Player', 'last_name':'2', 'is_skipper': 1, 'score': 0, 'sets': 0, 'display':{'display': 'Default', 'display_id': 1} }},
        },
    'clubs': {
        '1': {'club_id': 1, 'club_name': 'Merewether', 'logo': 'charls.jpeg'}, 
        '2': {'club_id': 2, 'club_name': 'Charlestown', 'logo': 'away.jpeg'},
        }
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

        c.execute('''CREATE TABLE IF NOT EXISTS displays
                     (display_id INTEGER PRIMARY KEY,
                     display text, "")''')
        conn.commit()
        c.execute('''INSERT into displays (display_id, display)
                    VALUES (1, 'Default'),
                            (2, 'Logo'),
                            (3, 'First Initial'),
                            (4, 'Fist and Last Initial') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS competitions
                     (competition_id INTEGER PRIMARY KEY,
                     competition TEXT, "")''')
        conn.commit()
        c.execute('''INSERT into competitions (competition_id, competition)
                    VALUES (1, 'Gala'),
                            (2, 'Pennants'),
                            (3, 'Club'),
                            (4, 'BPL')
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS games
                     (game_id INTEGER PRIMARY KEY,
                     name text DEFAULT NULL,
                     competition INTEGER DEFAULT NULL,
                     sponsor TEXT NOT NULL DEFAULT "",
                     start_time text DEFAULT NULL, 
                     finish_time text DEFAULT NULL, 
                     ends int DEFAULT 0,
                     winner text DEFAULT "",
                     coordinator_ip text DEFAULT "127.0.0.1:8000",
                     FOREIGN KEY (competition)
                        REFERENCES competitions (competition_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS competitors
                     (competitor_id INTEGER NOT NULL PRIMARY KEY,
                     player_id INTEGER DEFAULT "No Player",
                     first_name text DEFAULT "",
                     last_name text DEFAULT "",
                     score text DEFAULT 0,
                     sets text DEFAULT 0,
                     logo text DEFAULT "",
                     display INTEGER NOT NULL DEFAULT 1,
                     game INTEGER NOT NULL DEFAULT "No Game",
                     FOREIGN KEY (display)
                        REFERENCES displays (display_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (game)
                        REFERENCES games (game_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')

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
        
        games = cursor.execute('''SELECT *, c.competition as comp FROM games g
                                INNER JOIN competitions c
                                ON g.competition = c.competition_id
                                WHERE finish_time is NULL''').fetchall()

        if not games:
            self.create_game(DEFAULT_GAME, "127.0.0.1")
        else:
            for game in games:
                if game['ends'] < 0:
                    self.create_game(DEFAULT_GAME, "127.0.0.1")

                sql = """SELECT competitor_id, player_id, first_name, last_name, score, sets, logo, d.display FROM competitors as c
                        INNER JOIN displays AS d
                        ON c.display = d.display_id
                        where game = ?"""
                params = (game['game_id'],)
                players = cursor.execute(sql, params).fetchall()
                competitors = []
                tie_break = []
                for player in players:
                    # BPL RULES
                    if game['comp'] == 'BPL':
                        if float(player['sets']) > 2:
                            reset = self.reset_sets()
                        if player['sets'] == '1':
                            tie_break.append(1)

                    competitors.append({
                        "competitor_id": player['competitor_id'],
                        "player_id": player['player_id'],
                        "first_name": player['first_name'],
                        "last_name": player['last_name'],
                        "score": player['score'],
                        "sets": player['sets'],
                        "logo": player['logo'],
                        "competitor_display": player['display'],
                     })
                # check if both players have sets == 1
                if len(tie_break) == 2:
                    tie = True
                else:
                    tie = False

                parsed_rows.append({
                    "game_id": game["game_id"],
                    "name": game["name"],
                    "competition": game["comp"],
                    "start_time": game["start_time"],
                    "finish_time": game["finish_time"],
                    "ends": game["ends"],
                    "tie_break": tie,
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

            sql = "DELETE FROM games"
            cursor.execute(sql)
            sql = "DELETE FROM competitors"
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
        js['finish_time'] = None

        sql = "INSERT INTO games (game_id, name, competition, sponsor, start_time, finish_time, coordinator_ip) VALUES(?,?,?,?,?,?,?);"
        params = (js['game_id'], js['name'], js["competition"]["competition_id"], js["sponsor"]["sponsor_logo"], utc, js['finish_time'], coordinator_ip)
        game_id = cursor.execute(sql, params)

        for teams in js['competitors']:
            for player in js['competitors'][teams]:
                competitor = js['competitors'][teams][player]

                if competitor['is_skipper']:
                    sql = "INSERT INTO competitors (player_id, first_name, last_name, score, sets, logo, display, game) VALUES(?,?,?,?,?,?,?,?);"
                    params = (competitor['player_id'], competitor['first_name'], competitor['last_name'], competitor['score'], competitor['sets'], js['clubs'][teams]['logo'], competitor['display']['display_id'], js['game_id'])
                    cursor.execute(sql, params)
        con.commit()


    def update_game(self, js, coordinator_ip):
        self.delete_all_games()

        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))

        coordinator_ip += ':8000'
        js['finish_time'] = None

        sql = "INSERT INTO games (game_id, name, competition, start_time, finish_time, coordinator_ip) VALUES(?,?,?,?,?,?);"
        params = (js['game_id'], js['name'], js["competition"]["competition_id"], utc, js['finish_time'], coordinator_ip)
        game_id = cursor.execute(sql, params)

        for player in js['competitors']:
            if player['is_skipper']:
                sql = "INSERT INTO competitors (player_id, first_name, last_name, score, sets, logo, display, game) VALUES(?,?,?,?,?,?,?,?);"
                params = (player['player_id'], player['first_name'], player['last_name'], player['score'], player['sets'], player['logo'], player['display']['display_id'], js['game_id'])
                cursor.execute(sql, params)
        con.commit()


    def add_ends(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE games SET ends = ? WHERE game_id = ?"
        params = [js["ends"], js["game_id"]]

        res = cursor.execute(cmd, params)

        con.commit()
        # if res.fetchone() is None:
        #     try:
        #         r_code = self.write_coordinator_ends(js)
        #     except:
        #         pass
        return {
                "status": "ok",
        }

    def reset_score(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET score = 0"

        res = cursor.execute(cmd)
        con.commit()

        if res.fetchone() is None:
            return True
        else:
            return False


    def add_score(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET score = ? WHERE player_id=?"
        params = [js["score"], js["player"]["player_id"]]

        res = cursor.execute(cmd, params)
        con.commit()

        return {
                "status": "ok",
        }

    def reset_sets(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET sets = 0"

        res = cursor.execute(cmd)
        con.commit()

        if res.fetchone() is None:
            self.reset_score()
            return True
        else:
            return False


    def add_sets(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        print(js)

        cmd = "UPDATE competitors SET sets = ? WHERE player_id=?"
        params = [js["sets"], js["player"]["player_id"]]

        res = cursor.execute(cmd, params)
        con.commit()

        if res.fetchone() is None:
            reset = self.reset_score()
            if reset:
                return True
        return False 


    def coordinator_ip(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()
        return cursor.execute('''SELECT coordinator_ip FROM games''').fetchone()


    def write_coordinator_score(self, js):
        response = requests.post('http://'+self.coordinator_ip()+'/games/add_score', json = js)
        return response.status_code


    def write_coordinator_ends(self, js):
        response = requests.post('http://'+self.coordinator_ip()+'/games/add_ends', json = js)
        return response.status_code
