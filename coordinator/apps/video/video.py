#! /usr/bin/python
#
# COPYRIGHT: Gayner Technical Services Pty Ltd 2011
#
# LICENCE:
# THIS FILE IS SUBJECT TO THE TERMS AND CONDITIONS DEFINED IN THE FILE
# 'LICENCE', WHICH IS PART OF THIS SOURCE CODE PACKAGE

import datetime
import sqlite3
import json
import pickle
import pytz


local_tz = pytz.timezone("Australia/Sydney")

class Budget:
    def __init__(self):
        self.db_path = "apps/budget/budget.db"
        self.init_database_tables()

    def init_database_tables(self):
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS bills
                     (name text NOT NULL, 
                     cost text NOT NULL DEFAULT "",
                     details text NOT NULL DEFAULT "")''')

        c.execute('''CREATE TABLE IF NOT EXISTS saving
                     (name text NOT NULL, 
                     cost text NOT NULL DEFAULT "",
                     details text NOT NULL DEFAULT "")''')

        c.execute('''CREATE TABLE IF NOT EXISTS wage
                     (name text NOT NULL, 
                     cost text NOT NULL DEFAULT "",
                     details text NOT NULL DEFAULT "")''')

        conn.commit()

    def encode_if_required(self, str_val):
        try:
            return str_val.encode()
        except Exception:
            return str_val

    def get_bills(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        bills = cursor.execute('''SELECT * FROM bills''').fetchall()

        for bill in bills:
            parsed_rows.append({
                "name": bill["name"],
                "cost": bill["cost"],
                "details": bill["details"],
            })

        return json.dumps(parsed_rows)

    def get_savings(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        savings = cursor.execute('''SELECT * FROM bills''').fetchall()

        for saving in savings:
            parsed_rows.append({
                "name": saving["name"],
                "cost": saving["cost"],
                "details": saving["details"],
            })

        return json.dumps(parsed_rows)

    def get_wages(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        parsed_rows = []
        wages = cursor.execute('''SELECT * FROM bills''').fetchall()

        for wage in wages:
            parsed_rows.append({
                "name": wage["name"],
                "cost": wage["cost"],
                "details": wage["details"],
            })

        return json.dumps(parsed_rows)

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
