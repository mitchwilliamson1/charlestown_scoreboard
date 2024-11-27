from bottle import Bottle, route, run, template, static_file, TEMPLATE_PATH, JSONPlugin, response, request
import urllib
import json
import os
import ipaddress
import socket

import sys

from db_api import Masterboard



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


@bott.route("/get_masterboard")
def get_masterboard():
    return Masterboard().get_masterboard()


@bott.route("/<logo>")
def get_logo(logo):
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logo = static_file(logo, root="./assets")
    return logo


@bott.route("/setup", method=["POST", "OPTIONS"])
def create_game():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Masterboard().setup(request_params)
    return request.json


@bott.route("/add_score", method=["POST", "OPTIONS"])
def add_score():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Masterboard().add_score(request_params['update'])
    return request.json


@bott.route("/add_ends", method=["POST", "OPTIONS"])
def add_score():
    if request.method == "OPTIONS":
        return
    request_params = json.loads(request.body.getvalue())
    Masterboard().add_ends(request_params['update'])
    return request.json


@bott.route('/<filename:path>')
def send_static(filename):
    print("filename: ", filename)
    return static_file(filename, root='dist/')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8083))
    bott.run(host='0.0.0.0', port=port, debug=True)

