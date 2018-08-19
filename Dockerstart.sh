#!/usr/bin/env bash

set -e

gunicorn --bind 0.0.0.0:8000 restApiServer:app