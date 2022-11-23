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
    return json.dumps(initialise)


@gamesapp.route("/get_games")
def get_games():
    return Games().get_games()


@gamesapp.route("/get_rinks")
def get_rinks():
    return json.dumps(Games().get_rinks())



@gamesapp.route("/create_game", method=["POST", "OPTIONS"])
def create_game():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().create_game(request_params['create_game']) 
    return request.json


@gamesapp.route("/add_score", method=["POST", "OPTIONS"])
def add_score():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Games().add_score(request_params)
    return request.json


 