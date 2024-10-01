from bottle import Bottle, route, template, request, response, static_file
from .players import Players
import urllib
import json

playersapp = Bottle()


@playersapp.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@playersapp.route("/", method=["OPTIONS", "POST"])
def slash():
    if request.method == "OPTIONS":
        return
    json_obj = json.loads(request.body.read())
    response.status = 200
    return json.dumps({"pass": True})
    if json_obj['pass'] == PASS:
        return json.dumps({"pass": True})
    else:
        return "false"

@playersapp.route("/get_players")
def get_players():
    return Players().get_players()


@playersapp.route("/get_clubs")
def get_clubs():
    return Players().get_clubs()


@playersapp.route("/get_logo/<logo>")
def get_logo(logo):
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logo = static_file(logo, root="./assets")
    
    return logo


@playersapp.route("/create_player", method=["POST", "OPTIONS"])
def create_player():
    if request.method == "OPTIONS":
        return
    json_obj = json.loads(request.body.getvalue())
    Players().create_player(json_obj['create_player']) 
    return request.json


@playersapp.route("/create_club", method=["POST", "OPTIONS"])
def create_club():
    if request.method == "OPTIONS":
        return

    logo = request.files.get('file')
    club = request.forms.get('club')

    Players().create_club(json.loads(club), logo)
    return request.json


@playersapp.route("/update_club", method=["POST", "OPTIONS"])
def update_club():
    if request.method == "OPTIONS":
        return

    logo = request.files.get('file')
    if not logo:
        response.status = 300
        response.body = json.dumps({'blah':"No File Uploaded"})
        return
        # print()
        # return "No File Uploaded"

    club = request.forms.get('club')

    Players().update_club(json.loads(club), logo)
    print("JSON: ", request.json)

    return request.json


@playersapp.route("/save", method="POST")
def save():
    json_obj = json.loads(request.body.read())
    Players().save(json_obj) 
    return request.json


