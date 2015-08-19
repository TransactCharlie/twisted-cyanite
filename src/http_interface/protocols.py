__author__ = 'charlie'

from klein import Klein
import json

app = Klein()

@app.route("/metrics", methods=["GET"])
def render(request):
    request.setHeader('Content-Type', 'application/json')
    return "TODO"

@app.route("/paths")
def paths(request):
    request.setHeader('Content-Type', 'application/json')
    return "TODO"

@app.route("/ping")
def pig(request):
    request.setHeader('Content-Type', 'application/json')
    return json.dumps({"response": "pong"})

endpoints = app.resource
