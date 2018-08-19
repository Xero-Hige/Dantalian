#!/usr/bin/env bash
# bash ./CleanContainers.sh

set -e

docker-compose build
docker-compose up --abort-on-container-exit
