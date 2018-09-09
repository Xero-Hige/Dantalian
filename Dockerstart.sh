#!/usr/bin/env bash

set -e
sleep 4
python3 model/model.py
python3 bach/pexels.py --category people --pages 1
python3 bach/pexels.py --category dogs --pages 1
gunicorn --bind 0.0.0.0:8000 restApiServer:app
