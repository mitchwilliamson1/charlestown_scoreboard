-- in terminal
sqlite3.open bigboard.db

CREATE TABLE IF NOT EXISTS bigboard
(ip_id INTEGER PRIMARY KEY,
ip text DEFAULT NULL,
rink_id text"");

INSERT INTO bigboard (ip_id, ip, rink_id)
VALUES (1, '192.168.15.201', 1),
(2, '192.168.15.202', 2),
(3, '192.168.15.203', 3),
(4, '192.168.15.204', 4);