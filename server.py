#!/usr/bin/env python3

from flask import Flask
from flask import request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

key = "openhomepanel123"

# Setup -------------------------------

#TO-DO: init switch state to false !!!

#with open('config.json') as json_file:
#    data = json.load(json_file)
#    print("Config loaded")

# API ---------------------------------

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/get_pin', methods=['GET'])
def get_pin():
    if(request.headers.get("api_key")==key):
        with open('config.json') as json_file:
            data = json.load(json_file)
        return jsonify(data["settings"][0]["pin"]), 200
    else:
        return 'bad request!', 400


@app.route('/change_pin', methods=['POST'])
def change_pin():
    if(request.headers.get("api_key")==key):
        with open('config.json') as json_file:
            data = json.load(json_file)
        data["settings"][0]["pin"] = request.args["pin"]
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)
        return 'OK', 200
    else:
        return 'bad request!', 400


@app.route('/switch', methods=['POST'])
def switch():
    if(json.loads(request.data.decode('UTF-8'))['headers']['api_key']==key):
        sw_id = json.loads(request.data.decode('UTF-8'))['body']['id']
        sw_state = json.loads(request.data.decode('UTF-8'))['body']['state']
        with open('config.json') as json_file:
            data = json.load(json_file)
        data['switches'][sw_id]['state'] = sw_state
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)
        return 'OK', 200
    else:
        return 'bad request!', 400


@app.route('/get_switches', methods=['GET'])
def get_switches():
    if(request.headers.get("api_key")==key):
        with open('config.json') as json_file:
            data = json.load(json_file)
        return jsonify(data["switches"]), 200
    else:
        return 'bad request!', 400

@app.route('/get_temp', methods=['GET'])
def get_temp():
    if(request.headers.get("api_key")==key):
        return "23 °C", 200
    else:
        return 'bad request!', 400

@app.route('/get_APIkey', methods=['GET'])
def get_APIkey():
    if(request.headers.get("api_key")==key):
        with open('config.json') as json_file:
            data = json.load(json_file)
        return jsonify(data["settings"][0]["API-key"]), 200
    else:
        return 'bad request!', 400


# Start server -----------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)