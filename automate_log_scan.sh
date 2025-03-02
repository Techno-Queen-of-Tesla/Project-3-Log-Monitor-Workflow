#!/bin/bash

# gets the current time, formats the time into MM/DD/YYY HH:MM:SS format
now=$(TZ="America/New_York" date '+%m/%d/%Y %H:%M:%S')

# writes the log entry to an external .txt file
echo "auth.log last scanned at $now" > /workspaces/Project-2-Log-Monitor-Workflow/tmp/send_email.txt

# FAILED PASSWORD MONITORING - running a grep command and sending the output to failed_passwords.txt
tail -n 300 /workspaces/Project-2-Log-Monitor-Workflow/var/log/auth.log | grep "fail" > /workspaces/Project-2-Log-Monitor-Workflow/tmp/failed_passwords.txt

# UNUSUAL SERVER TRAFFIC - run the traffic_script.py file to check the web server access log
python3 traffic_script.py