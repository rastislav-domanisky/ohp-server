#!/usr/bin/env python3

from flask import Flask
from flask import request, jsonify
import json
from flask_cors import CORS
import pymongo

key = "openhomepanel123"

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Config -------------------------------

OHP_PORT = 3000 # port for server
OHP_DEBUG = True # use debug only in developement
OHP_HOST = "0.0.0.0" # use "0.0.0.0" for LAN access, or "127.0.0.1" for localhost
OHP_KEY = "openhomepanel123" # secret API KEY for HTTP
OWM_KEY = "b443bc989ffa04f9348d1d5c1f38e271" # your Open Weather Map API KEY

# --------------------------------------


# Setup -------------------------------

#TO-DO: init switch state to false !!!

#with open('config.json') as json_file:
#    data = json.load(json_file)
#    print("Config loaded")

# API ---------------------------------

@app.route('/', methods=['GET'])
def hello():
    if(request.headers.get('API-KEY') == OHP_KEY):
        return "HELLO", 200
    else:
        return "UNAUTHORIZED", 401 
   

# Get all switches as json
@app.route('/get_switches', methods=['GET'])
def get_switches():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
            return jsonify(data["switches"]), 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Create new switch
@app.route('/add_switch', methods=['POST'])
def add_switch():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                data["switches"].append({
                    'name': request.args.get('name'),
                    'pin': int(request.args.get('pin')),
                    'state': False
                })
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            return "OK", 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Delete switch
@app.route('/delete_switch', methods=['POST'])
def delete_switch():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                if len(data['switches']) >= int(request.args.get('index')):
                    data["switches"].pop(int(request.args.get('index')))
                else:    
                    return "ERROR - Index Out of Range", 400
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            return "OK", 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Change switch state
@app.route('/switch', methods=['POST'])
def switch():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                if(request.args.get('state') == "true"):
                    data["switches"][int(request.args.get('index'))]['state'] = True
                elif(request.args.get('state') == "false"):
                    data["switches"][int(request.args.get('index'))]['state'] = False
                else:
                    return "ERROR - state is not boolean"
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            return "OK", 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Get current temperature from GPIO sensor
@app.route('/get_temp', methods=['GET'])
def get_temp():
    if(request.headers.get('API-KEY') == OHP_KEY):
        return "23 °C", 200
    else:
        return "UNAUTHORIZED", 401

# Get Open Weather Map API key
@app.route('/get_OWM_key', methods=['GET'])
def get_APIkey():
    if(request.headers.get('API-KEY') == OHP_KEY):
        return OWM_KEY, 200
    else:
        return "UNAUTHORIZED", 401


# Start server -----------------------------
if __name__ == '__main__':
    app.run(host=OHP_HOST, debug=OHP_DEBUG, port=OHP_PORT)