#!/usr/bin/env python3

import os
import subprocess
from flask import Flask
from flask import request, jsonify
import json
from flask_cors import CORS

try:
    from w1thermsensor import W1ThermSensor
    tempSensor = W1ThermSensor()
except:
    print("Cannot load w1thermsensor")

try:
    from wireless import Wireless
    wireless = Wireless()
except:
    print("Cannot load wireless")

try:
    import alsaaudio
    mixer = alsaaudio.Mixer("Headphone")
except:
    print("Cannot load alsaaudio")

app = Flask(__name__)
#app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

# Setup -------------------------------

def loadData():
    try:
        with open('config.json', encoding='utf-8') as json_file:
            return json.load(json_file)
    except:
        print("Cannot load config file")
        return

data = loadData()

OHP_PORT = data["server"]["port"]
OHP_DEBUG = data["server"]["debug"]
OHP_HOST = data["server"]["host"]
OHP_KEY = "openhomepanel123" # secret API KEY for HTTP (do not change)

W_SSID = data["wi-fi"]["SSID"]
W_PASWD = data["wi-fi"]["password"]

try:
    wireless.connect(ssid=W_SSID, password=W_PASWD)
except:
    print("Cannot connect to Wi-Fi")


#TODO: init switch state to false !!!

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
        return jsonify(loadData()["switches"])
    else:
        return "UNAUTHORIZED", 401

# Create new switch
@app.route('/add_switch', methods=['POST'])
def add_switch():
    if(request.headers.get('API-KEY') == OHP_KEY):
        data = loadData()
        data["switches"].append({
            'name': request.args.get('name'),
            'pin': int(request.args.get('pin')),
            'state': False
        })
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
            return "OK", 200
    else:
        return "UNAUTHORIZED", 401

# Delete switch
@app.route('/delete_switch', methods=['POST'])
def delete_switch():
    if(request.headers.get('API-KEY') == OHP_KEY):
        data = loadData()
        if len(data['switches']) -1 >= int(request.args.get('index')):
            data["switches"].pop(int(request.args.get('index')))
        else:    
            return "ERROR - Index Out of Range", 400
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        return "OK", 200
    else:
        return "UNAUTHORIZED", 401

# Change switch state
@app.route('/switch', methods=['POST'])
def switch():
    if(request.headers.get('API-KEY') == OHP_KEY):
        data = loadData()
        if(request.args.get('state') == "true"):
            data["switches"][int(request.args.get('index'))]['state'] = True
        elif(request.args.get('state') == "false"):
            data["switches"][int(request.args.get('index'))]['state'] = False
        else:
            return "ERROR - state is not boolean", 400
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        return "OK", 200
    else:
        return "UNAUTHORIZED", 401

# Get current temperature from GPIO sensor
@app.route('/get_temp', methods=['GET'])
def get_temp():
    if(request.headers.get('API-KEY') == OHP_KEY):
        data = loadData()
        try:
            if(data["settings"]["temp-sensor"]["units"] == "metric"):
                return str(tempSensor.get_temperature(W1ThermSensor.DEGREES_C)) + " °C", 200
            else:
                return str(tempSensor.get_temperature(W1ThermSensor.DEGREES_F)) + " °F", 200
        except:
            return "Cannot get temp", 400
    else:
        return "UNAUTHORIZED", 401

# Get Open Weather Map API key
@app.route('/get_OWM_data', methods=['GET'])
def get_APIkey():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            data = loadData()
            return jsonify(
                [data["settings"]["OWM"]["units"],
                data["settings"]["OWM"]["city"],
                data["server"]["OWM-api-key"]]
                ), 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Get Settings
@app.route('/get_settings', methods=['GET'])
def get_settings():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            data = loadData()
            return jsonify(data["settings"]), 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Update settings
@app.route('/update_settings', methods=['POST'])
def update_settings():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            data = loadData()
            data["settings"] = json.loads(request.data)
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            return "settings updated", 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Set brightness
@app.route('/brightness', methods=['POST'])
def brightness():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            b = json.loads(request.data)["brightness"]
            os.system('sudo sh -c "echo {} > /sys/class/backlight/rpi_backlight/brightness"'.format(b))
            return "brightness {}".format(b), 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Get brightness
@app.route('/get_brightness', methods=['GET'])
def get_brightness():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            b_call = subprocess.check_output("cat /sys/class/backlight/rpi_backlight/brightness", shell=True).rstrip().decode("utf-8")
            return "{}".format(b_call) , 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Set volume
@app.route('/volume', methods=['POST'])
def volume():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            volume = json.loads(request.data)["volume"]
            mixer.setvolume(volume)
            return "volume {}".format(volume), 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Get volume
@app.route('/get_volume', methods=['GET'])
def get_volume():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            vol = mixer.getvolume()[0]
            return "{}".format(vol) , 200
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401

# Get wifi
@app.route('/get_wifi', methods=['GET'])
def get_wifi():
    if(request.headers.get('API-KEY') == OHP_KEY):
        try:
            return wireless.current()
        except:
            return "ERROR", 400
    else:
        return "UNAUTHORIZED", 401


# Start server -----------------------------
if __name__ == '__main__':
    app.run(host=OHP_HOST, debug=OHP_DEBUG, port=OHP_PORT)