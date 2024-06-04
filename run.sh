#!/bin/bash

nohup php -S localhost:8000 -t VulnerableApplications/Classic_Ping/ > phpd.log 2>&1 &
PHP_SERVER_PID=$$
echo "PHP Server PID: $PHP_SERVER_PID"
URL="http://localhost:8000"
python3 bash_rl.py $PHP_SERVER_PID $URL
PYTHON_PID=$$

function cleanup {
    kill $PHP_SERVER_PID
    kill $PYTHON_PID
}

trap cleanup EXIT
trap cleanup SIGINT

