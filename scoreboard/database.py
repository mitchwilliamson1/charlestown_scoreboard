import datetime
import sqlite3
import json
import pickle
import pytz
import requests

# COORDINATOR_IP = "127.0.0.1:8000"
COORDINATOR_IP = "10.0.0.41:8000"


local_tz = pytz.timezone("Australia/Sydney")

class Game:
    def __init__(self):
        self.db_path = "game.db"
        self.init_database_tables()

    def init_database_tables(self):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS games
                     (game_id INTEGER PRIMARY KEY,
                     game int,
                     name text DEFAULT NULL,
                     start_time text, 
                     finish_time text, 
                     ends int DEFAULT 0,
                     winner text DEFAULT "")''')

        c.execute('''CREATE TABLE IF NOT EXISTS competitors
                     (competitor_id INTEGER NOT NULL PRIMARY KEY,
                     player_id INTEGER DEFAULT "No Player",
                     first_name text DEFAULT "",
                     last_name text DEFAULT "",
                     score text DEFAULT "",
                     game INTEGER NOT NULL DEFAULT "No Game",
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

    def get_game(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        parsed_rows = []
        
        games = cursor.execute('''SELECT * FROM games WHERE finish_time is NULL''').fetchall()
        for game in games:
            sql = f'''SELECT player_id, first_name, last_name, score FROM competitors WHERE game = {game['game']}'''
            
            players = cursor.execute(sql).fetchall()
            print(players)
            competitors = []
            for player in players:
                print(player)
                print(player[0])
                competitors.append({
                    "player_id": player['player_id'],
                    "first_name": player['first_name'],
                    "last_name": player['last_name'],
                    "score": player['score']
                 })
            
            parsed_rows.append({
                "game_id": game["game_id"],
                "name": game["name"],
                "start_time": game["start_time"],
                "finish_time": game["finish_time"],
                "ends": game["ends"],
                "winner": game["winner"],
                "competitors": competitors,
            })

        print('SCORE PARSE: ', parsed_rows)
        return json.dumps(parsed_rows)


    def create_game(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        utc = datetime.datetime.strptime(js["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.timezone('UTC'))

        sql = f'''INSERT INTO games (game, name, start_time) 
            VALUES("{js["game_id"]}", "{js["name"]}", '{utc}');'''
        game_id = cursor.execute(sql)

        for player in js['players']:
            sql = f'''INSERT INTO competitors (player_id, first_name, last_name, score, game) 
                    VALUES({js['players'][player]['player_id']}, "{js['players'][player]['first_name']}", "{js['players'][player]['last_name']}", 0, {js['game_id']});'''
            print(sql)
            cursor.execute(sql)
        con.commit()


        # utc = datetime.datetime.strptime(js["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.timezone('UTC'))
        # player_a = js["player_a"]['first_name']
        # player_b = js["player_b"]['first_name']

        # cursor.execute('''INSERT INTO game (id,
        #                                     start_time,
        #                                     player_a, 
        #                                     player_b)
        #                                     VALUES (?, ?, ?, ?)''',
        #                                     ('', utc, player_a, player_b)
        #     )
        # con.commit()


    def add_ends(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = f'UPDATE games SET ends = {js["ends"]} WHERE game_id = {js["game_id"]}'

        res = cursor.execute(cmd)
        if res.fetchone() is None:
            try:
                r_code = self.write_coordinator_ends(js)
            except:
                pass
        
        con.commit()
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
