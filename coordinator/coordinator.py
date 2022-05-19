import os
import sys
sys.path.append("apps/")

import json
import datetime
from bottle import Bottle, route, run, template, static_file, TEMPLATE_PATH, JSONPlugin, response, request

# from urls import budgetapp
from budget.urls import budgetapp
from video.urls import videoapp

TEMPLATE_PATH.append("dist/")

sys.path.append("apps/budget/")
sys.path.append("apps/video/")


bott = Bottle()
bott.mount("/budget", budgetapp)
bott.mount("/video", videoapp)



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
