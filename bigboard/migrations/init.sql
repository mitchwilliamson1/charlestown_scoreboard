-- in terminal
sqlite3.open bigboard.db

CREATE TABLE IF NOT EXISTS scoreboards
(ip_id INTEGER PRIMARY KEY,
scoreboard_ip text DEFAULT NULL);

INSERT INTO scoreboards (ip_id, scoreboard_ip)
VALUES (1, '192.168.15.201'),
(2, '192.168.15.202'),
(3, '192.168.15.203'),
(4, '192.168.15.204');