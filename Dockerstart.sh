#!/usr/bin/env bash

set -e
sleep 20
python3 model/model.py
#python3 bach/pexels.py --category people --pages 1
python3 model/devenv_setup.py

sleep 10

#FIXME: DO NOT PUSH THIS ON MASTER
rm -r /coverage/*
coverage run ./restApiServer.py -R &
cd ../Testing
rm -f ./test_results
bash run_curl_tests.sh >> ./test_results
STATUS=$?
cd ../Raphael
coverage3 combine
if [ "$TRAVIS" = "" ]
then
    coverage3 html
    cp .coverage /coverage/
    cp -r htmlcov /coverage/htmlcov
    cp ../Testing/test_results /coverage/test_results
else
    coverage3 report -m
    grep -e "- ERROR" ../Testing/test_results
fi
exit $STATUS
#FIXME: REMOVE
