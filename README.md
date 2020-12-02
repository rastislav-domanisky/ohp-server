# OHP Server

Server for Open Home Panel

## Dependencies

* Raspberry Pi OS (Raspbian)
* Internet connection

## Installation

Update system
```bash
sudo apt-get update
sudo apt-get upgrade
```
Install Python3 and pip3
```bash
sudo apt-get install python3 python3-pip
```
Install python dependiencies
```bash
sudo apt-get install python3-w1thermsensor
sudo apt-get install python3-alsaaudio
```
Download server
```bash
git clone https://github.com/rastislav-domanisky/ohp-server.git
```
Change directory to server root folder
```bash
cd ohp-server
```
Install other python requirements
```bash
pip3 install -r requirements.txt
```

## Configuration

Open config.json file
```bash
nano config.json
```
Server host
```json
host: "0.0.0.0" or "localhost"
```
Change lock-screen PIN
```json
pin: "1234"
```
Setup Wi-Fi connection
```json
SSID: "My Wifi Name"
password: "wifi password"
```
Setup Open Weather Map
https://openweathermap.org/
```json
OWM-api-key: "my OWM API key"
```

## Run server
Add permission
```bash
chmod +x server.py
```
Run server
```json
./server.py
```

##### Do not edit something else...
