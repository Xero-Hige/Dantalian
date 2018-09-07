#!/usr/bin/env bash

set -e
sleep 10
gunicorn --bind 0.0.0.0:8000 restApiServer:app
