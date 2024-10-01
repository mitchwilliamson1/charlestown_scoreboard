from bottle import Bottle, route, template, request, response, static_file
import requests as REQUEST
from .games import Games

import json


_ALLOW_CORS = "*"
_ALLOW_METHODS = "PUT, GET, POST, DELETE, OPTIONS"
_ALLOW_HEADERS = "Authorization, Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"

gamesapp = Bottle()

@gamesapp.hook('after_request')
def enable_cors():
    response.headers["Access-Control-Allow-Origin"] = _ALLOW_CORS
    response.headers["Access-Control-Allow-Methods"] = _ALLOW_METHODS
    response.headers["Access-Control-Allow-Headers"] = _ALLOW_HEADERS
    response.headers["Access-Control-Allow-Credentials"] = "true"


@gamesapp.route("/")
def slash():
    return "blah"


@gamesapp.route("/init")
def init():
    initialise = {}
    initialise["competition"] = Games().get_competitions()
    initialise["display"] = Games().get_displays()
    initialise["rink"] = Games().get_rinks()
    initialise["sponsor"] = Games().get_sponsors(False)
    # initialise["gender"] = Games().get_genders()
    # initialise["game_type"] = Games().get_game_types()
    # initialise["round"] = Games().get_rounds()
    # initialise["grade"] = Games().get_grades()
    return json.dumps(initialise)


@gamesapp.route("/get_games")
def get_games():
    return Games().get_games(True)


@gamesapp.route("/get_finished_games")
def get_finished_games():
    return Games().get_games(False)


@gamesapp.route("/get_rinks")
def get_rinks():
    return json.dumps(Games().get_rinks())


@gamesapp.route("/get_masterboards")
def get_masterboard():
    return json.dumps(Games().get_masterboards())


@gamesapp.route("/get_sponsors")
def get_sponsors():
    return Games().get_sponsors(True)


@gamesapp.route("/create_sponsor", method=["POST", "OPTIONS"])
def create_sponsor():
    if request.method == "OPTIONS":
        return

    logo_file = request.files.get('file')
    sponsor_name = request.forms.get('sponsor_name')

    Games().create_sponsor(logo_file, sponsor_name)
    return request.json


@gamesapp.route("/create_game", method=["POST", "OPTIONS"])
def create_game():
    if request.method == "OPTIONS":
        return

    request_params = json.loads(request.body.getvalue())
    created = Games().create_game(request_params['create_game'])
    if created == "success":
        response.status = 200
    else:
        response.status = 400
    return json.dumps(created)


@gamesapp.route("/create_rink", method=["POST", "OPTIONS"])
def create_rink():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().create_rink(request_params['create_rink']) 

    return request.json

@gamesapp.route("/create_masterboard", method=["POST", "OPTIONS"])
def create_masterboard():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().create_masterboard(request_params['create_masterboard']) 

    return request.json

@gamesapp.route("/add_score", method=["POST", "OPTIONS"])
def add_score():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().add_score(request_params)
    return request.json


@gamesapp.route("/update_game", method=["POST", "OPTIONS"])
def update_game():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().update_game(request_params['update_game']) 
    return request.json


@gamesapp.route("/finish_game", method=["POST", "OPTIONS"])
def finish_game():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().finish_game(request_params['finish_game'])
    return request.json


@gamesapp.route("/update_rink", method=["POST", "OPTIONS"])
def update_rink():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().update_rink(request_params)
    return request.json


@gamesapp.route("/update_masterboards", method=["POST", "OPTIONS"])
def update_masterboards():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().update_masterboards(request_params['masterboard'])
    Games().update_master_link(request_params['ips'], request_params['masterboard']['masterboard_id'])
    return request.json



@gamesapp.route("/update_sponsor", method=["POST", "OPTIONS"])
def update_sponsor():
    if request.method == "OPTIONS":
        return

    logo_file = request.files.get('file')
    if not logo_file:
        print("No File Uploaded")
        return "No File Uploaded"
    sponsor_name = json.loads(request.forms.get('sponsor_name'))

    Games().update_sponsor(logo_file, sponsor_name)
    return request.json


@gamesapp.route("/update_player", method=["POST", "OPTIONS"])
def update_player():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().update_player(request_params)
    return request.json

 

