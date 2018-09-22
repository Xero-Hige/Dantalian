#!/usr/bin/env bash
sleep 5 #Wait for the server to start

STATUS=0

echo "Login test"
echo "=========="

python3 ./test_login.py
STATUS+=$?