from bottle import Bottle, route, template, request, response
import requests as REQUEST
from .games import Games

import json



gamesapp = Bottle()


@gamesapp.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@gamesapp.route("/")
def slash():
    return "blah"

@gamesapp.route("/init")
def init():
    initialise = {}
    initialise["gender"] = Games().get_genders()
    initialise["type"] = Games().get_types()
    initialise["round"] = Games().get_rounds()
    initialise["grade"] = Games().get_grades()
    initialise["level"] = Games().get_levels()
    initialise["rink"] = Games().get_rinks()
    initialise["masterboard"] = Games().get_masterboards()
    return json.dumps(initialise)


@gamesapp.route("/get_games")
def get_games():
    return Games().get_games()


@gamesapp.route("/get_rinks")
def get_rinks():
    return json.dumps(Games().get_rinks())


@gamesapp.route("/get_masterboards")
def get_masterboard():
    return json.dumps(Games().get_masterboards())



@gamesapp.route("/create_game", method=["POST", "OPTIONS"])
def create_game():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().create_game(request_params['create_game']) 
    return request.json


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
    Games().update_game(request_params[0])
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



@gamesapp.route("/update_team", method=["POST", "OPTIONS"])
def update_team():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().update_team(request_params)
    return request.json


@gamesapp.route("/update_player", method=["POST", "OPTIONS"])
def update_player():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().update_player(request_params)
    return request.json

 

