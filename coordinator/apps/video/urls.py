from bottle import Bottle, route, template, request, response
import requests as REQUEST
import json
# from xml.etree import cElementTree as ET
from bs4 import BeautifulSoup



videoapp = Bottle()


@videoapp.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@videoapp.route("/")
def slash():
    return "blah"

@videoapp.route("/get_folders")
def get_vid_names():
    folder_names = []
    names = REQUEST.get('http://127.0.0.1:8001/videos')
    results = BeautifulSoup(names.content, "html.parser")
    for folder in results.find_all("a", href=True):
        folder_names.append(folder.contents[0])
    return json.dumps(folder_names)


@videoapp.route("/get_vid_names/<folder>/")
def get_vid_names(folder):
    links = []
    vid_names = []
    names = REQUEST.get(f'http://127.0.0.1:8001/videos/{folder}')
    results = BeautifulSoup(names.content, "html.parser")
    for vid in results.find_all("a", href=True):
        # links.append(vid['href'])
        vid_names.append(vid.contents[0])
    return json.dumps(vid_names)
 