COORDINATOR_IP = "127.0.0.1"

DEFAULT_GAME = {
    "game_id": -1,
    "name": "standard",
    "ends":0,
    "competition": {"competition_id": 3},
    "sponsor": {"sponsor_logo": "your_ad_here.png"},
    "finish_time": None,
    "competitors": {
        "1": {
            "player_id": "1",
            "first_name": "Player",
            "last_name": "1",
            "score": 0,
            "sets": 0,
            "display": {"display": "Logo", "display_id": 2},
        },
        "2": {
            "player_id": "2",
            "first_name": "Player",
            "last_name": "2",
            "score": 0,
            "sets": 0,
            "display": {"display": "Logo", "display_id": 2},
        },
    },
    "clubs": {
        "1": {"club_id": 1, "club_name": "Moama", "logo": "moama_steamers.png"},
        "2": {"club_id": 2, "club_name": "Away", "logo": "away.jpeg"},
    },
    "displays": {
        "1": {"display": "Default", "display_id": 1},
        "2": {"display": "Default", "display_id": 1},
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