#!/usr/bin/env sh
sudo pip install --upgrade pip
sudo pip install -r back/requirements.freeze.txt
cd front && yarn install && yarn main
