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
                     competitior_display INTEGER NOT NULL DEFAULT 1,
                     FOREIGN KEY (competitior_display)
                        REFERENCES competitior_displays (competitior_display_id)
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
        teams = cursor.execute("SELECT * FROM teams").fetchall()

        for team in teams:
            parsed_rows.append({
                "team_id": team["team_id"],
                "team_name": team["team_name"],
                "logo": team["logo"],
                "address": team["address"],
                "contact_details": team["contact_details"],
            })

        return json.dumps(parsed_rows)


    def update_team(self, js, logo):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo.save("./assets/"+logo.filename)
        except:
            pass

        cmd = "UPDATE teams SET team_name = ?, address = ?, contact_details = ? WHERE team_id = ?"
        params = [js['team_name'], js['address'], js['contact_details'], js['team_id']]
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

        sql = 'INSERT INTO players (first_name, last_name, team, address, email) VALUES(?, ?, ?, ?, ?);'
        params = [player['first_name'], player['last_name'], player['team'], player['address'], player['email']]
        cursor.execute(sql, params)
        con.commit()


    def create_team(self, team, logo):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        try:
            logo.save("./assets/"+logo.filename)
        except:
            pass

        sql = 'INSERT INTO teams (team_name, logo, address, contact_details) VALUES(?, ?, ?, ?);'
        params = [team['name'], logo.filename, team['address'], team['contact_details']]

        cursor.execute(sql, params)
        con.commit()

