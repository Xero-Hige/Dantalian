# Dantalian
This project intends to provide an api to tag gifs with text. Possible use cases include creating a captcha for tagged-gifs corpus building.

## Requirements
* docker
* docker compose
* python 3

## Install instructions

* create a virtualenv with `virtualenv -p python3 venv`
* source it with `source venv/bin/activate`
* install requirements with `pip install -r requirements.txt`
* replace values in example `.yml` and rename them without `example`
* run with `sh StartDocker.sh`

# TODO
* Add initialization script to load testing entities
* Add tests on expected user entity behaviour
* Add tests on expected image serving behaviour
* Add tests on expected classification behaviour