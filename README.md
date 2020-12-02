### OHP Server

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3 python3-pip

sudo apt-get install python3-w1thermsensor
sudo apt-get install python3-alsaaudio

clone this repo 
cd ohp-server

pip3 install -r requirements.txt

CONFIG:

host: "0.0.0.0" for LAN or "localhost"

OWM-api-key: Open Weather Map API key https://openweathermap.org/

security pin for screen ... default is "1234"

Wi-Fi:

SSID: "My Wifi"
"password": "My Wifi Password"

do not change something else
