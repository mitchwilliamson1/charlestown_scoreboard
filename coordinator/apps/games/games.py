import datetime
import sqlite3
import json
import pickle
import pytz
import requests


local_tz = pytz.timezone("Australia/Sydney")

class Games:
    def __init__(self):
        self.db_path = "co_ordinator.db"
        self.init_database_tables()

    def init_database_tables(self):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS types
                     (type_id INTEGER PRIMARY KEY,
                     players text"",
                     gender text"",
                     type text, "")''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS genders
                     (gender_id INTEGER PRIMARY KEY,
                     gender text, "")''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS rounds
                     (round_id INTEGER PRIMARY KEY,
                     round text, "")''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS levels
                     (level_id INTEGER PRIMARY KEY,
                     level text, "")''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS grades
                     (grade_id INTEGER PRIMARY KEY,
                     grade text, "")''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS rinks
                     (rink_id INTEGER PRIMARY KEY,
                     rink text,
                     ip text, "")''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS masterboards
                     (masterboard_id INTEGER PRIMARY KEY,
                     masterboard text,
                     ip text, "")''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS master_link
                     (master_link_id INTEGER PRIMARY KEY,
                     masterboard INTEGER DEFAULT NULL,
                     rink INTEGER DEFAULT NULL,
                     FOREIGN KEY (masterboard)
                        REFERENCES masterboards (masterboard_id),
                    FOREIGN KEY (rink)
                        REFERENCES rinks (rink_id))''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS games
                     (game_id INTEGER PRIMARY KEY,
                     name text DEFAULT NULL,
                     type INTEGER DEFAULT NULL,
                     gender INTEGER DEFAULT NULL,
                     round INTEGER DEFAULT NULL,
                     grade INTEGER DEFAULT NULL,
                     level INTEGER DEFAULT NULL,
                     rink INTEGER DEFAULT NULL,
                     start_time text,
                     finish_time text,
                     ends int DEFAULT 0,
                     winner INTEGER DEFAULT NULL,
                     FOREIGN KEY (type)
                        REFERENCES types (type_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (gender)
                        REFERENCES genders (gender_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (round)
                        REFERENCES rounds (round_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (level)
                        REFERENCES levels (level_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                    FOREIGN KEY (grade)
                        REFERENCES grades (grade_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (rink)
                        REFERENCES rinks (rink_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (winner)
                        REFERENCES players (player_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')
        conn.commit()
    
    def get_types(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        types = cursor.execute('''SELECT * FROM types''').fetchall()

        for game_type in types:
            parsed_rows.append({
                "type_id": game_type["type_id"],
                "type": game_type["type"],
                "gender": game_type["gender"],
                "players": game_type["players"],
            })

        return parsed_rows

    def get_genders(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        genders = cursor.execute('''SELECT * FROM genders''').fetchall()

        for gender in genders:
            parsed_rows.append({
                "gender": gender["gender"],
                "gender_id": gender["gender_id"],
            })

        return parsed_rows

    def get_rounds(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        rounds = cursor.execute('''SELECT * FROM rounds''').fetchall()

        for _round in rounds:
            parsed_rows.append({
                "round": _round["round"],
                "round_id": _round["round_id"],
            })

        return parsed_rows

    def get_levels(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        levels = cursor.execute('''SELECT * FROM levels''').fetchall()

        for level in levels:
            parsed_rows.append({
                "level": level["level"],
                "level_id": level["level_id"],
            })

        return parsed_rows

    def get_grades(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        grades = cursor.execute('''SELECT * FROM grades''').fetchall()

        for grade in grades:
            parsed_rows.append({
                "grade": grade["grade"],
                "grade_id": grade["grade_id"],
            })

        return parsed_rows

    def get_rinks(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        rinks = cursor.execute('''SELECT * FROM rinks''').fetchall()

        for rink in rinks:
            parsed_rows.append({
                "rink": rink["rink"],
                "ip": rink["ip"],
                "rink_id": rink["rink_id"],
            })

        return parsed_rows

    def get_masterboards(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        masterboards = cursor.execute('''SELECT * FROM masterboards''').fetchall()

        for masterboard in masterboards:
            sql = f'''SELECT r.rink, r.ip, r.rink_id from master_link ml
                    inner join masterboards m 
                    on ml.masterboard = m.masterboard_id
                    inner join rinks r 
                    on ml.rink = r.rink_id
                    where m.masterboard_id = {masterboard['masterboard_id']}'''
            
            rink_ips = cursor.execute(sql).fetchall()
            rinks = []
            for rink_ip in rink_ips:
                rinks.append({
                    "rink": rink_ip[0],
                    "ip": rink_ip[1],
                    "rink_id": rink_ip[2],

                 })

            parsed_rows.append({
                "masterboard": masterboard["masterboard"],
                "ip": masterboard["ip"],
                "masterboard_id": masterboard["masterboard_id"],
                "rink_ips": rinks,
            })
        return parsed_rows


    def get_games(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        games = cursor.execute('''SELECT *, r.rink as rink_name FROM games g inner join rinks r on g.rink = r.rink_id ''').fetchall()

        for game in games:
            sql = f'''SELECT player_id, p.first_name, p.last_name, c.score, t.logo FROM competitors AS c
                    INNER JOIN players AS p
                    ON c.player = p.player_id 
                    INNER JOIN teams AS t
                    ON p.team = t.team_id 
                    WHERE c.game = {game['game_id']}'''
            
            players = cursor.execute(sql).fetchall()

            competitors = []
            for player in players:
                competitors.append({
                    "player_id": player[0],
                    "first_name": player[1],
                    "last_name": player[2],
                    "score": player[3],
                    "logo": player[4]
                 })
            
            parsed_rows.append({
                "game_id": game["game_id"],
                "name": game["name"],
                "type": game["type"],
                "gender": game["gender"],
                "round": game["round"],
                "level": game["level"],
                "grade": game["grade"],
                "rink": {'rink':game["rink_name"], 'rink_id':game["rink_id"], 'ip':game["ip"]},
                "ends": game["ends"],
                "start_time": game["start_time"],
                "finish_time": game["finish_time"],
                "winner": game["winner"],
                "competitors": competitors
            })

        return json.dumps(parsed_rows)


    def get_players(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        players = cursor.execute('''SELECT * FROM players''').fetchall()

        for player in players:
            parsed_rows.append({
                "player_id": player["player_id"],
                "first_name": player["first_name"],
                "last_name": player["last_name"],
                "team": player["team"],
                "address": player["address"],
                "email": player["email"],
            })

        return json.dumps(parsed_rows)

    def get_teams(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        teams = cursor.execute('''SELECT * FROM teams''').fetchall()

        for team in teams:
            parsed_rows.append({
                "team_id": team["team_id"],
                "team_name": team["team_name"],
                "logo": team["logo"],
                "address": team["address"],
                "contact_details": team["contact_details"],
            })

        return json.dumps(parsed_rows)


    def create_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        utc = datetime.datetime.strptime(js["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.timezone('UTC'))

        sql = f'''INSERT INTO games (name, type, gender, round, level, grade, rink, start_time) 
            VALUES("{js["name"]}", "{js["type"]["type_id"]}", "{js["gender"]["gender_id"]}", "{js["round"]["round_id"]}", "{js["level"]["level_id"]}", "{js["grade"]["grade_id"]}", "{js["rink"]["rink_id"]}", '{utc}')
            RETURNING game_id;'''
        game_id = cursor.execute(sql)

        print(js)

        for i in game_id:
            game_id = i
        for player in js['players']:
            sql = f'''INSERT INTO competitors (player, score, game) 
                    VALUES({js['players'][player]['player_id']},'0', {game_id[0]});'''
            cursor.execute(sql)
        con.commit()

        js['game_id'] = game_id[0]


        response = self.write_scoreboard(js)
        if response == 500:
            #remmove rink from above
            print('5000000000000')
        else:
            print(response)
            for i in response:
                print(i)


    def add_score(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE competitors SET score = ? WHERE player = ? and game = ?"
        params = (js["score"], js["player_id"], js["game_id"])
        res = cursor.execute(cmd, params)
        print(res.fetchone())
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }



    def write_scoreboard(self, js):
        response = requests.post('http://'+js["rink"]["ip"]+'/create_game', json = js)
        return response.status_code

    def update_scoreboard(self, js):
        response = requests.post('http://'+js["rink"]["ip"]+'/update_game', json = js)
        print(response)
        return response.status_code


    def get_masterboard(self, masterboard_id):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        masterboard = cursor.execute('''SELECT * FROM masterboards WHERE masterboard_id = ?''', (masterboard_id, )).fetchone()
        
        return masterboard


    def create_rink(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f"INSERT INTO rinks (ip, rink) VALUES (?, ?)"
        params = (js['ip'], js['rink'])
        
        res = cursor.execute(cmd,params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def create_masterboard(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f"INSERT INTO masterboards (ip, masterboard) VALUES (?, ?)"
        params = (js['ip'], js['masterboard'])
        
        res = cursor.execute(cmd,params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE games SET name = ?,type = ?,gender = ?,round = ?,level = ?,grade = ?,rink = ?,ends = ?,start_time = ?,finish_time = ?,winner = ? WHERE game_id = ?"
        params = (js['name'],js['type'], js['gender'], js['round'], js['level'], js['grade'], js["rink"]["rink_id"],js['ends'], js['start_time'], js['finish_time'], js['winner'], js['game_id'] )

        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
            self.write_scoreboard(js)
        return {
                "status": "ok",
        }


    def update_rink(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f"UPDATE rinks SET ip = '{js['ip']}', rink = '{js['rink']}' WHERE rink_id = {js['rink_id']}"
        res = cursor.execute(cmd)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_masterboards(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f"UPDATE masterboards SET ip = '{js['ip']}', masterboard = '{js['masterboard']}' WHERE masterboard_id = {js['masterboard_id']}"
        res = cursor.execute(cmd)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_master_link(self, js, master_id):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f"DELETE from master_link WHERE masterboard = '{master_id}'"
        res = cursor.execute(cmd)

        for rink in js:
            if rink['show'] is True:
                cmd = f"INSERT INTO master_link (masterboard,  rink) values ({master_id}, {rink['rink_id']})"
                res = cursor.execute(cmd)
        if res.fetchone() is None:
            con.commit()
            self.write_masterboard(js, master_id)
        return {
                "status": "ok",
        }

    def write_masterboard(self, js, master_id):
        ips = []
        for rink in js:
            if rink['show']:
                tpl = (rink['ip'], rink['rink_id'])
                ips.append(tpl)

        masterboard_ip = self.get_masterboard(master_id)

        response = requests.post('http://'+masterboard_ip['ip']+'/setup', json = ips)
        print(response)
        return response.status_code


    def update_team(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f"UPDATE teams SET team_name = '{js['team_name']}', address = '{js['address']}', contact_details = '{js['contact_details']}' WHERE team_id = {js['team_id']}"
        res = cursor.execute(cmd)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }

    def update_player(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f"UPDATE players SET first_name = '{js['first_name']}', last_name = '{js['last_name']}', team = '{js['team']}', address = '{js['address']}', email = '{js['email']}' WHERE player_id = {js['player_id']}"
        res = cursor.execute(cmd)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }



