import os
import sys
sys.path.append("apps/")

import json
import datetime
from bottle import Bottle, route, run, template, static_file, TEMPLATE_PATH, JSONPlugin, response, request


from players.urls import playersapp
from games.urls import gamesapp

TEMPLATE_PATH.append("dist/")

sys.path.append("apps/players/")
sys.path.append("apps/games/")


bott = Bottle()
bott.mount("/players", playersapp)
bott.mount("/games", gamesapp)



@bott.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@bott.route('/')
def index():
    return template('index.html', author='Mitch Williamson')


@bott.route('/<filename:path>')
def send_static(filename):
    print("filename: ", filename)
    return static_file(filename, root='dist/')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    bott.run(host='0.0.0.0', port=port, debug=True)
