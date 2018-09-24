#!/usr/bin/env bash
sleep 5 #Wait for the server to start

STATUS=0

echo "Trusted test"
echo "=========="

python3 ./test_trusted.py
STATUS+=$?

curl -s -X GET 'http://127.0.0.1:5000/api/0.1/shutdown'
exit $STATUS
