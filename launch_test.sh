#!/bin/sh
# lauch_test.sh
# navigate to directory and run pygame test application
cd /home/pi/LTF-SM/lcdTest/

python3 main.py

## In order to log app output replace the line above with this one
# python3 main.py >> /home/pi/LTF-SM/app_logs/logs.py.log 2>&1
