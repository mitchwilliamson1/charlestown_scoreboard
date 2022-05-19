from bottle import Bottle, route, template, request, response
from .budget import Budget
import urllib
import json

budgetapp = Bottle()


@budgetapp.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

PASS = "nicetry"


@budgetapp.route("/", method=["OPTIONS", "POST"])
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

@budgetapp.route("/get_bills")
def get_bills():
    return Budget().get_bills()

@budgetapp.route("/get_savings")
def get_savings():
    return Budget().get_savings()

@budgetapp.route("/get_wages")
def get_wages():
    return Budget().get_wages()

@budgetapp.route("/save", method="POST")
def save():
    json_obj = json.loads(request.body.read())
    Budget().save(json_obj) 
    return request.json

@budgetapp.route("/create_bill", method="POST")
def create_bill():
    Budget().create_bill(request.json)
    return request.json

