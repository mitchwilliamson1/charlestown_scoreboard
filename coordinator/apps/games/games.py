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


    def get_games(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        games = cursor.execute('''SELECT * FROM games''').fetchall()

        for game in games:
            sql = f'''SELECT p.first_name, p.last_name, c.score FROM competitors AS c
                    INNER JOIN players AS p
                    ON c.player = p.player_id 
                    WHERE c.game = {game['game_id']}'''
            
            players = cursor.execute(sql).fetchall()

            competitors = []
            for player in players:
                competitors.append({
                    "first_name": player[0],
                    "last_name": player[1],
                    "score": player[2]
                 })
            
            parsed_rows.append({
                "game_id": game["game_id"],
                "name": game["name"],
                "type": game["type"],
                "gender": game["gender"],
                "round": game["round"],
                "level": game["level"],
                "grade": game["grade"],
                "rink": game["rink"],
                "ends": game["ends"],
                "start_time": game["start_time"],
                "finish_time": game["finish_time"],
                "winner": game["winner"],
                "competitors": competitors
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


        for i in game_id:
            game_id = i
        for player in js['players']:
            sql = f'''INSERT INTO competitors (player, score, game) 
                    VALUES({js['players'][player]['player_id']},'0', {game_id[0]});'''
            cursor.execute(sql)
        con.commit()

        js['game_id'] = game_id[0]

        print(js)

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

        cmd = f'UPDATE competitors SET score = {js["score"]} WHERE player={js["player_id"]} and game = {js["game_id"]}'
        print(cmd)
        res = cursor.execute(cmd)
        print(res.fetchone())
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }



    def write_scoreboard(self, js):
        response = requests.post('http://'+js["rink"]["ip"]+'/create_game', json = js)
        return response.status_code


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def cancel_blast(self, js):
        con = sqlite3.connect(self.blast_notif_db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cursor.execute('''UPDATE blasts SET status=? WHERE site_blast_id=?''', (-99, js["site_blast_id"]))
        con.commit()

        return {
                "status": "ok",
        }

    def edit_blast(self, js):
        con = sqlite3.connect(self.blast_notif_db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        now = datetime.datetime.utcnow()

        # Extract data from form
        uuid = js["uuid"]
        operation = js["operation"]
        site_blast_id = js["site_blast_id"]
        scheduled = datetime.datetime.strptime(js["scheduled_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        pits = pickle.dumps(js.get("pits", None))
        activity = pickle.dumps(js.get("activity", None))
        initiation = pickle.dumps(js.get("initiation", None))
        affected_units = pickle.dumps(js.get("affected_units", None))
        roads = pickle.dumps(js.get("roads", []))

        # Create the edited blast
        cursor.execute('''INSERT INTO blasts (created, operation, site_blast_id,
                                                scheduled, pits, activity, 
                                                initiation, affected_units, roads, parent)
                                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (now, operation, site_blast_id, scheduled, pits, activity, 
                    initiation, affected_units, roads, uuid)
            )

        con.commit()

        return {
                "uuid": uuid,
                "site_blast_id": site_blast_id,
                "operation": operation,
                "scheduled_date": scheduled.isoformat(),
                "activity": pickle.loads(activity),
                "pits": pickle.loads(pits),
                "affected_units": pickle.loads(affected_units),
                "initiation": pickle.loads(initiation),
                "roads": pickle.loads(roads),
            }

    def add_recipient(self, phone):
        if not phone.startswith("+61"):
            raise Exception("Malformed phone number")
        if len(phone) != 12:
            raise Exception("Malformed phone number")

        # Connect to DB
        con = sqlite3.connect(self.blast_notif_db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        # See if number already exists
        subs = cursor.execute('''SELECT * FROM subscribers WHERE phone_number = ?''', (phone,)).fetchall()

        if len(subs) != 0:
            raise Exception("Number already subscribed")

        # Alright ass number into database
        cursor.execute('''INSERT INTO subscribers (phone_number, subscribed_on) VALUES (?, ?)''', (phone, datetime.datetime.utcnow(),))
        cursor.execute('''INSERT INTO jobs (phone_number, job_type) VALUES (?, ?)''',
                                (phone, 
                                "subscribe"))

        con.commit()
