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

        c.execute('''CREATE TABLE IF NOT EXISTS clubs
                     (club_id INTEGER PRIMARY KEY,
                     club_name TEXT NOT NULL DEFAULT "",
                     logo TEXT NOT NULL, 
                     address TEXT NOT NULL,
                     contact_details TEXT NOT NULL DEFAULT "")''')
        conn.commit()
        c.execute('''INSERT into clubs (club_id, club_name, logo, address, contact_details)
                    VALUES (1, 'Merewether', 'merelogo.jpeg', 'burwood street', 'None'),
                            (2, 'Charlestown', 'charls.jpeg', 'Cardiff street', 'None') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS players
                     (player_id INTEGER PRIMARY KEY,
                     first_name TEXT NOT NULL,
                     last_name TEXT NOT NULL DEFAULT "",
                     club INTEGER NOT NULL DEFAULT "No Team",
                     bowls_number TEXT,
                     grade TEXT,
                     FOREIGN KEY (club)
                        REFERENCES clubs (club_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT)''')
        conn.commit()
        c.execute('''INSERT into players (player_id, first_name, last_name, club, bowls_number, grade)
                    VALUES (1, 'Mitchell', 'Williamson', 1, '12453', 'None'),
                            (2, 'Dave', 'King', 2, '2134', 'None') 
                            ON CONFLICT DO NOTHING;''')
        conn.commit()

        c.execute('''CREATE TABLE IF NOT EXISTS competitors
                     (competitor_id INTEGER NOT NULL PRIMARY KEY,
                     player TEXT NOT NULL DEFAULT "No Player",
                     score TEXT NOT NULL DEFAULT "",
                     game INTEGER NOT NULL DEFAULT "No Game",
                     display INTEGER NOT NULL DEFAULT 2,
                     team TEXT NOT NULL DEFAULT "",
                     is_skipper BOOL NOT NULL DEFAULT FALSE,
                     FOREIGN KEY (display)
                        REFERENCES displays (display_id)
                            ON UPDATE CASCADE
                            ON DELETE SET DEFAULT,
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
        players = cursor.execute("SELECT * FROM players").fetchall()

        for player in players:
            parsed_rows.append({
                "player_id": player["player_id"],
                "first_name": player["first_name"],
                "last_name": player["last_name"],
                "club": player["club"],
                "bowls_number": player["bowls_number"],
                "grade": player["grade"],
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


    def update_club(self, js, logo):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo.save("./assets/"+logo.filename)
        except:
            pass

        cmd = "UPDATE clubs SET club_name = ?, address = ?, contact_details = ? WHERE club_id = ?"
        params = [js['club_name'], js['address'], js['contact_details'], js['club_id']]
        res = cursor.execute(cmd, params)
        if res.fetchone() is None:
            con.commit()
        return {
                "status": "ok",
        }


    def create_player(self, player):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        sql = 'INSERT INTO players (first_name, last_name, club, bowls_number, grade) VALUES(?, ?, ?, ?, ?);'
        params = [player['first_name'], player['last_name'], player['club'], player['bowls_number'], player['grade']]
        cursor.execute(sql, params)
        con.commit()


    def create_club(self, club, logo):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo.save("./assets/"+logo.filename)
        except:
            pass

        sql = 'INSERT INTO clubs (club_name, logo, address, contact_details) VALUES(?, ?, ?, ?);'
        params = [club['name'], logo.filename, club['address'], club['contact_details']]

        cursor.execute(sql, params)
        con.commit()

