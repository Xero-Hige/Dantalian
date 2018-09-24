#!/usr/bin/env bash
sleep 5 #Wait for the server to start

STATUS=0

echo "Trusted test"
echo "=========="

python3 ./test_trusted.py
STATUS+=$?
