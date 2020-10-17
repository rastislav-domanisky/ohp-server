from flask import Flask
from flask import request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    if(request.headers.get("api_key")==key):
        with open('config.json') as json_file:
            data = json.load(json_file)
        swID = int(request.args["id"])
        if(request.args["state"] == "true"):
            swState = True
        else:
            swState = False
        
        data["switches"][swID]["state"] = swState
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


# Start server -----------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)