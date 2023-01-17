from bottle import Bottle, route, run, template, static_file, TEMPLATE_PATH, JSONPlugin, response, request
import urllib
import json
import os
import config
import ipaddress
import socket

import sys

from database import Game



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
    print('1234566')
    return Game().get_game()


@bott.route("/create_game", method=["POST", "OPTIONS"])
def create_game():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Game().create_game(request_params)
    return request.json


@bott.route("/add_score", method=["POST", "OPTIONS"])
def add_score():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Game().add_score(request_params['update'])
    return request.json


@bott.route("/add_ends", method=["POST", "OPTIONS"])
def add_score():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Game().add_ends(request_params['update'])
    return request.json


@bott.route('/<filename:path>')
def send_static(filename):
    print("filename: ", filename)
    return static_file(filename, root='dist/')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8082))
    bott.run(host='0.0.0.0', port=port, debug=True)

