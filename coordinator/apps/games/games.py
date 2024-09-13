import datetime
import sqlite3
import json
import pickle
import pytz
import requests
import threading


local_tz = pytz.timezone("Australia/Sydney")

class Games:
    def __init__(self):
        self.db_path = "co_ordinator.db"
        self.init_database_tables()

    def init_database_tables(self):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS game_types
                     (game_type_id INTEGER PRIMARY KEY,
                     players INTEGER"",
                     game_type TEXT, "")''')
        conn.commit()
        c.execute('''INSERT into game_types (game_type_id, players, game_type)
                    VALUES (1, 2, 'Singles'),
                            (2, 4, 'Pairs'),
                            (3, 6, 'Triples'),
                            (4, 8, 'Fours') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS competitions
                     (competition_id INTEGER PRIMARY KEY,
                     competition TEXT, "")''')
        conn.commit()
        c.execute('''INSERT into competitions (competition_id, competition)
                    VALUES (1, 'Bowls / Pennants'),
                            (2, 'BPL'),
                            (3, 'Consistency Singles')
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS genders
                     (gender_id INTEGER PRIMARY KEY,
                     gender text, "")''')
        conn.commit()
        c.execute('''INSERT into genders (gender_id, gender)
                    VALUES (1, 'Mens'),
                            (2, 'Ladies'),
                            (3, 'Mixed'),
                            (4, 'Open') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS rounds
                     (round_id INTEGER PRIMARY KEY,
                     round text, "")''')
        conn.commit()
        c.execute('''INSERT into rounds (round_id, round)
                    VALUES (1, 64),
                            (2, 32),
                            (3, 16),
                            (4, 'Quarter'),
                            (5, 'Semi'),
                            (6, 'Final') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

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

        c.execute('''CREATE TABLE IF NOT EXISTS grades
                     (grade_id INTEGER PRIMARY KEY,
                     grade text, "")''')
        conn.commit()
        c.execute('''INSERT into grades (grade_id, grade)
                    VALUES (1, 'Premiere'),
                            (2, '1'),
                            (3, '2'),
                            (4, '3'),
                            (5, '4'),
                            (6, '5'),
                            (7, '6') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS sponsors
                     (sponsor_id INTEGER PRIMARY KEY,
                     sponsor TEXT NOT NULL DEFAULT "",
                     sponsor_logo TEXT NOT NULL)''')
        conn.commit()
        c.execute('''INSERT into sponsors (sponsor_id, sponsor, sponsor_logo)
                    VALUES (1, 'Bell Property', 'belle_whitebg.png'),
                            (2, 'XXXX', 'xxxx.png') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS rinks
                     (rink_id INTEGER PRIMARY KEY,
                     rink text,
                     ip text, "")''')
        conn.commit()
        c.execute('''INSERT into rinks (rink_id, rink, ip)
                    VALUES (1, 'Rink 1', '192.168.15.201:8081'),
                            (2, 'Rink 2', '192.168.15.202:8081'),
                            (3, 'Rink 3', '192.168.15.203:8081'),
                            (4, 'Rink 4', '192.168.15.204:8081'),
                            (5, 'Rink 5', '192.168.15.205:8081'),
                            (6, 'Rink 6', '192.168.15.206:8081'),
                            (7, 'Rink 7', '192.168.15.207:8081'),
                            (8, 'Rink 8', '192.168.15.208:8081'),
                            (9, 'Rink 9', '192.168.15.209:8081'),
                            (10, 'Rink 10', '192.168.15.210:8081'),
                            (11, 'Rink 11', '192.168.15.211:8081'),
                            (12, 'Rink 12', '192.168.15.212:8081'),
                            (13, 'Rink 13', '192.168.15.213:8081'),
                            (14, 'Rink 14', '192.168.15.214:8081') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS masterboards
                     (masterboard_id INTEGER PRIMARY KEY,
                     masterboard text,
                     ip text, "")''')
        conn.commit()
        c.execute('''INSERT into masterboards (masterboard_id, masterboard, ip)
                    VALUES (1, 'Masterboard 1', '192.168.15.215:8081'),
                            (2, 'Masterboard 2', '192.168.15.216:8081'),
                            (3, 'Masterboard 3', '192.168.15.217:8081'),
                            (4, 'Masterboard 4', '192.168.15.218:8081') 
                            ON CONFLICT DO NOTHING;''')
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
                     game_type INTEGER DEFAULT NULL,
                     gender INTEGER DEFAULT NULL,
                     competition INTEGER DEFAULT NULL,
                     round INTEGER DEFAULT NULL,
                     grade INTEGER DEFAULT NULL,
                     rink INTEGER DEFAULT NULL,
                     sponsor INTEGER DEFAULT NULL,
                     start_time text,
                     finish_time text,
                     ends INTEGER DEFAULT 0,
                     winner INTEGER DEFAULT NULL,
                     FOREIGN KEY (game_type)
                        REFERENCES game_type (game_type_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (gender)
                        REFERENCES genders (gender_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (competition)
                        REFERENCES competitions (competition_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (round)
                        REFERENCES rounds (round_id)
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
                    FOREIGN KEY (sponsor)
                        REFERENCES sponsors (sponsor_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                    FOREIGN KEY (winner)
                        REFERENCES competitors (team)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')
        conn.commit()

    def get_game_types(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        game_types = cursor.execute("SELECT * FROM game_types").fetchall()

        for game_type in game_types:
            parsed_rows.append({
                "game_type_id": game_type["game_type_id"],
                "game_type": game_type["game_type"],
                "players": game_type["players"],
            })

        return parsed_rows

    def get_genders(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        genders = cursor.execute("SELECT * FROM genders").fetchall()

        for gender in genders:
            parsed_rows.append({
                "gender": gender["gender"],
                "gender_id": gender["gender_id"],
            })

        return parsed_rows

    def get_competitions(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        competitions = cursor.execute("SELECT * FROM competitions").fetchall()

        for competition in competitions:
            parsed_rows.append({
                "competition": competition["competition"],
                "competition_id": competition["competition_id"],
            })

        return parsed_rows

    def get_rounds(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        rounds = cursor.execute("SELECT * FROM rounds").fetchall()

        for _round in rounds:
            parsed_rows.append({
                "round": _round["round"],
                "round_id": _round["round_id"],
            })

        return parsed_rows


    def get_displays(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        displays = cursor.execute("SELECT * FROM displays").fetchall()

        for display in displays:
            parsed_rows.append({
                "display": display["display"],
                "display_id": display["display_id"],
            })

        return parsed_rows

    def get_grades(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        grades = cursor.execute("SELECT * FROM grades").fetchall()

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
        rinks = cursor.execute("SELECT * FROM rinks").fetchall()

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
        masterboards = cursor.execute("SELECT * FROM masterboards").fetchall()

        for masterboard in masterboards:
            sql = f'''SELECT r.rink, r.ip, r.rink_id from master_link ml
                    inner join masterboards m 
                    on ml.masterboard = m.masterboard_id
                    inner join rinks r 
                    on ml.rink = r.rink_id
                    where m.masterboard_id = ?'''
            params = [masterboard['masterboard_id']]
            rink_ips = cursor.execute(sql, params).fetchall()
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


    def get_sponsors(self, dump):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        sponsors = cursor.execute("SELECT * FROM sponsors").fetchall()

        for sponsor in sponsors:
            parsed_rows.append({
                "sponsor_id": sponsor["sponsor_id"],
                "sponsor": sponsor["sponsor"],
                "sponsor_logo": sponsor["sponsor_logo"],
            })
        if dump:
            return json.dumps(parsed_rows)
        else:
            return parsed_rows


    def get_games(self, get_current):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        if get_current:
            sql = '''SELECT *, r.rink as rink_name, s.sponsor as sponsor_name, c.competition as comp_name FROM games g
                    inner join rinks r
                    on g.rink = r.rink_id
                    inner join sponsors s
                    on g.sponsor = s.sponsor_id
                    inner join competitions c
                    on g.competition = c.competition_id
                    inner join sponsors
                    on g.sponsor = sponsors.sponsor_id
                    WHERE finish_time IS NULL'''
        else:
            sql = '''SELECT *, r.rink as rink_name FROM games g
                    inner join rinks r
                    on g.rink = r.rink_id
                    WHERE finish_time IS NOT NULL'''
    
        games = cursor.execute(sql).fetchall()

        for game in games:
            sql = '''SELECT player_id, cd.display, cd.display_id, p.first_name, p.last_name, club.logo, c.team, c.is_skipper, c.score, c.sets FROM competitors AS c
                    INNER JOIN players AS p
                    ON c.player = p.player_id 
                    INNER JOIN displays AS cd
                    ON c.display = cd.display_id
                    INNER JOIN clubs AS club
                    ON p.club = club.club_id
                    WHERE c.game = ?'''
            params = [game['game_id']]
            players = cursor.execute(sql, params).fetchall()

            competitors = []
            for player in players:
                competitors.append({
                    "player_id": player['player_id'],
                    "first_name": player['first_name'],
                    "last_name": player['last_name'],
                    "score": player['score'],
                    "sets": player['sets'],
                    "logo": player['logo'],
                    "team": player['team'],
                    "is_skipper": player['is_skipper'],
                    "display": {'display':player['display'],'display_id':player['display_id']},
                 })
            
            parsed_rows.append({
                "game_id": game["game_id"],
                "name": game["name"],
                "game_type": game["game_type"],
                "competition": {"competition":game["comp_name"], "competition_id":game["competition_id"]},
                "gender": game["gender"],
                "round": game["round"],
                "grade": game["grade"],
                "rink": {"rink":game["rink_name"], "rink_id":game["rink_id"], "ip":game["ip"]},
                "sponsor": {"sponsor":game["sponsor_name"], "sponsor_id":game["sponsor_id"], "sponsor_logo":game["sponsor_logo"]},
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
        players = cursor.execute("SELECT * FROM players").fetchall()

        for player in players:
            parsed_rows.append({
                "player_id": player["player_id"],
                "first_name": player["first_name"],
                "last_name": player["last_name"],
                "club": player["club"],
                "address": player["address"],
                "email": player["email"],
            })

        return json.dumps(parsed_rows)

    def get_clubs(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        clubs = cursor.execute("SELECT * FROM clubs").fetchall()

        for club in clubs:
            parsed_rows.append({
                "club_id": club["club_id"],
                "club_name": club["club_name"],
                "logo": club["logo"],
                "address": club["address"],
                "contact_details": club["contact_details"],
            })

        return json.dumps(parsed_rows)


    def create_game(self, js):
        try:
            con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            con.row_factory = sqlite3.Row
            cursor = con.cursor()

            utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))

            sql = "INSERT INTO games (name, competition, rink, sponsor, start_time) VALUES(?, ?, ?, ?, ?) returning game_id;"

            params = [js["name"], js["competition"]["competition_id"], js["rink"]["rink_id"], js["sponsor"]["sponsor_id"], utc]
            cursor.execute(sql, params)

            game_id = cursor.lastrowid

            scoreboard_competitors = {}

            for _game_id in game_id:
                js['game_id'] = _game_id
                for player in js['competitors']:
                    sql = "INSERT INTO competitors (player, score, sets, game, display) VALUES(?, ?, ?, ?, ?);"
                    params = [js['competitors'][player]['player_id'],
                        js['competitors'][player]['score'],
                        js['competitors'][player]['sets'],
                        _game_id,
                        js['competitors'][player]['display']['display_id']]
                    cursor.execute(sql, params)
                con.commit()


            x = threading.Thread(target=self.write_scoreboard, args=(js,))
            x.start()
            return {"status": "ok",}
        except:
            return {"status": 300}


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
        try:
            response = requests.post('http://'+js["rink"]["ip"]+'/create_game', json = js, timeout=2)
            return response.status_code
        except Exception as e:
            print("FAIL", e)
            return "fail"


    def update_scoreboard(self, js):
        try:
            response = requests.post('http://'+js["rink"]["ip"]+'/update_game', json = js, timeout=2)
            return response.status_code
        except Exception as e:
            print("FAIL", e)
            return "fail"



    def get_masterboard(self, masterboard_id):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        masterboard = cursor.execute("SELECT * FROM masterboards WHERE masterboard_id = ?", (masterboard_id, )).fetchone()
        
        return masterboard


    def create_rink(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "INSERT INTO rinks (ip, rink) VALUES (?, ?)"
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

        cmd = "INSERT INTO masterboards (ip, masterboard) VALUES (?, ?)"
        params = (js['ip'], js['masterboard'])
        
        res = cursor.execute(cmd,params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()

        cmd = "UPDATE games SET name = ?,game_type = ?,competition = ?,gender = ?,round = ?,grade = ?,rink = ?,sponsor = ?,ends = ?,start_time = ?,finish_time = ?,winner = ? WHERE game_id = ?"
        params = (js['name'],js['game_type'], js["competition"]["competition_id"], js['gender'], js['round'], js['grade'], js["rink"]["rink_id"], js["sponsor"]["sponsor_id"],js['ends'], js['start_time'], js['finish_time'], js['winner'], js['game_id'] )

        res = cursor.execute(cmd, params)

        for competitor in js['competitors']:
            
            if competitor['is_skipper']:
                cmd = "UPDATE competitors SET score = ?,display = ? WHERE team = ? AND game = ?"
                params = (competitor['score'], competitor['display']['display_id'], competitor['team'], js['game_id'])
                res = cursor.execute(cmd, params)

        if res.fetchone() is None:
            con.commit()
            con.close()

            x = threading.Thread(target=self.update_scoreboard, args=(js,))
            x.start()
            return


    def finish_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = con.cursor()

        utc = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
        js['finish_time'] = utc

        cmd = "UPDATE games SET finish_time = ?,winner = ? WHERE game_id = ?"
        params = (js['finish_time'], js['winner'], js['game_id'] )

        js['finish_time'] = str(js['finish_time'])

        res = cursor.execute(cmd, params)

        if res.fetchone() is None:
            con.commit()
            con.close()

            x = threading.Thread(target=self.write_scoreboard, args=(js,))
            x.start()
            return


    def update_rink(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE rinks SET ip = ?, rink = ? WHERE rink_id = ?"
        params = [js['ip'], js['rink'], js['rink_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_masterboards(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE masterboards SET ip = ?, masterboard = ? WHERE masterboard_id = ?"
        params = [js['ip'], js['masterboard'], js['masterboard_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def update_master_link(self, js, master_id):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "DELETE from master_link WHERE masterboard = ?"
        params = [master_id]
        res = cursor.execute(cmd, params)

        for rink in js:
            if rink['show'] is True:
                cmd = "INSERT INTO master_link (masterboard,  rink) values (?, ?)"
                params = [master_id, rink['rink_id']]
                res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
            x = threading.Thread(target=self.write_masterboard, args=(js, master_id,))
            x.start()
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
        print("URL: ", 'http://'+masterboard_ip['ip']+'/setup')
        try:
            response = requests.post('http://'+masterboard_ip['ip']+'/setup', json = ips)
            return response.status_code
        except:
            return "fail"


    def update_club(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE clubs SET club_name = ?, address = ?, contact_details = ? WHERE club_id = ?"
        params = [js['club_name'], js['address'], js['contact_details'], js['club_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }

    def update_player(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "UPDATE players SET first_name = ?, last_name = ?, club = ?, bowls_number = ?, grade = ? WHERE player_id = ?"
        params = [js['first_name'], js['last_name'], js['club'], js['bowls_number'], js['grade'], js['player_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }



