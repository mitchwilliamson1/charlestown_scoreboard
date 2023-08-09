from bottle import Bottle, route, run, template, static_file, TEMPLATE_PATH, JSONPlugin, response, request
import urllib
import json
import os
import ipaddress
import socket

import sys

from db_interface import Game

TEMPLATE_PATH.append("dist/")
bott = Bottle()


@bott.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@bott.route('/')
def index():
    return template('index.html')


@bott.route("/get_game")
def get_game():
    return Game().get_game()


@bott.route("/<logo>")
def get_logo(logo):
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logo = static_file(logo, root="./assets")
    return logo


@bott.route("/create_game", method=["POST", "OPTIONS"])
def create_game():
    if request.method == "OPTIONS":
        return
    client_ip = request.environ.get('REMOTE_ADDR')
    request_params = json.loads(request.body.getvalue())
    Game().create_game(request_params, client_ip)
    return request.json


@bott.route("/update_game", method=["POST", "OPTIONS"])
def update_game():
    if request.method == "OPTIONS":
        return
    client_ip = request.environ.get('REMOTE_ADDR')
    request_params = json.loads(request.body.getvalue())
    Game().update_game(request_params, client_ip)
    return request.json


@bott.route("/add_score", method=["POST", "OPTIONS"])
def add_score():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Game().add_score(request_params['update'])
    return request.json


@bott.route("/add_ends", method=["POST", "OPTIONS"])
def add_ends():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Game().add_ends(request_params['update'])
    return request.json


@bott.route("/add_sets", method=["POST", "OPTIONS"])
def add_sets():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Game().add_sets(request_params['update'])
    return request.json


@bott.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='dist/')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    bott.run(host='0.0.0.0', port=port, debug=True)

