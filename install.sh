#!/bin/sh
sudo apt-get -y update
sudo apt-get install -y python3-pip
sudo pip3 install flask
export APP_URL="0.0.0.0"
python3 restapi.py