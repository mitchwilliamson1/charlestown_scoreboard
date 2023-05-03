import datetime
import sqlite3
import json
import pickle
import pytz


local_tz = pytz.timezone("Australia/Sydney")

class Players:
    def __init__(self):
        self.db_path = "co_ordinator.db"
        self.init_database_tables()

    def init_database_tables(self):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''PRAGMA foreign_keys = ON;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS teams
                     (team_id INTEGER PRIMARY KEY,
                     team_name text NOT NULL DEFAULT "",
                     logo blob NOT NULL, 
                     address text NOT NULL,
                     contact_details text NOT NULL DEFAULT "")''')

        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS players
                     (player_id INTEGER PRIMARY KEY,
                     first_name text NOT NULL,
                     last_name text NOT NULL DEFAULT "",
                     team text NOT NULL DEFAULT "No Team",
                     address text,
                     email text,
                     FOREIGN KEY (team)
                        REFERENCES teams (team_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS competitors
                     (competitor_id INTEGER NOT NULL PRIMARY KEY,
                     player text NOT NULL DEFAULT "No Player",
                     score text NOT NULL DEFAULT "",
                     game INTEGER NOT NULL DEFAULT "No Game",
                     FOREIGN KEY (game)
                        REFERENCES games (game_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
                     FOREIGN KEY (player)
                        REFERENCES players (player_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')

        conn.commit()

    def encode_if_required(self, str_val):
        try:
            return str_val.encode()
        except Exception:
            return str_val

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


    def create_player(self, player):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        print(player)

        sql = f''' INSERT INTO players (first_name, last_name, team, address, email) 
        VALUES("{player['first_name']}", "{player['last_name']}", "{player['team']}", '{player['address']}', '{player['email']}');'''

        print(sql)
        cursor.execute(sql)
        con.commit()


    def create_team(self, team, logo):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo.save("./assets/"+logo.filename)
        except:
            pass

        sql = f''' INSERT INTO teams (team_name, logo, address, contact_details) 
        VALUES('{team['name']}', "{logo.filename}", "{team['address']}", '{team['contact_details']}');'''

        cursor.execute(sql)
        con.commit()

    def update_team(self, js, logo):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo.save("./assets/"+logo.filename)
            logo_update = logo.filename
        except:
            logo_update = js['logo']
            pass

        cmd = f"UPDATE teams SET team_name = '{js['team_name']}', logo = '{logo_update}', address = '{js['address']}', contact_details = '{js['contact_details']}' WHERE team_id = {js['team_id']}"
        res = cursor.execute(cmd)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def save(self, js):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        now = datetime.datetime.utcnow()

        # Extract data from form
        for table_name in js:
            for column in js[table_name]:
                # if len(column['details']) is 0:
                #     column['details'] = None

                sql_string = f"UPDATE {table_name} SET name='{column['name']}', cost={column['cost']}, details='{column['details']}' WHERE name IS '{column['name']}';"
                print(sql_string)
                cursor.execute(sql_string)
                # cursor.execute('''UPDATE ? SET name= ?, cost= ?, details= ? WHERE name IS ? ''',
                #         (table_name, column['name'], column['cost'], column['details'], column['name']))
                con.commit()



    def create_blast(self, js):
        con = sqlite3.connect(self.blast_notif_db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        now = datetime.datetime.utcnow()

        # Extract data from form
        operation = js["operation"]
        site_blast_id = js["site_blast_id"]
        scheduled = datetime.datetime.strptime(js["scheduled_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        pits = pickle.dumps(js.get("pits", None))
        activity = pickle.dumps(js.get("activity", None))
        initiation = pickle.dumps(js.get("initiation", None))
        affected_units = pickle.dumps(js.get("affected_units", None))
        roads = pickle.dumps(js["roads"])

        cursor.execute('''INSERT INTO blasts (created, operation, site_blast_id,
                                                scheduled, pits, activity, 
                                                initiation, affected_units, roads)
                                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (now, operation, site_blast_id, scheduled, pits, activity, 
                    initiation, affected_units, roads)
            )
        con.commit()

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
