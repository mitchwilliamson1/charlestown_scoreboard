COORDINATOR_IP = "192.168.15.200"

DEFAULT_GAME = {
    "game_id": -1,
    "name": "standard",
    "ends":0,
    "competition": {},
    "rink": {},
    "sponsor": {},
    "finish_time": None,
    "competitors": {
        "1": {
            "player_id": "",
            "first_name": "",
            "last_name": "",
            "score": 0,
            "sets": 0,
            "display": {"display": "Default", "display_id": 1},
        },
        "2": {
            "player_id": "",
            "first_name": "",
            "last_name": "",
            "score": 0,
            "sets": 0,
            "display": {"display": "Default", "display_id": 1},
        },
    },
    "clubs": {
        "1": {"club_id": "", "club_name": "", "logo": ""},
        "2": {"club_id": "", "club_name": "", "logo": ""},
    },
}

LOG_CONF = {
    "version": 1,
    "formatters": {
        "void": {"format": ""},
        "standard": {
            "format": "%(asctime)s [%(levelname)s] (%(name)s %(threadName)-9s): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "runtime_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs_runtime.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8",
        },
        "error_handler": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs_error.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "system": {
            "handlers": ["runtime_handler", "error_handler"],
            "level": "DEBUG",
        },
    },
}