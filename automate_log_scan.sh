#!/bin/bash

# gets the current time, formats it
now=$(TZ="America/New_York" date '+%m/%d/%Y %H:%M:%S')

# writes the log entry to an external text file in a folder shared with Windows machine
echo "auth.log last scanned at $now" >> /media/sf_Shared/scans_log.txt

# failed password monitoring - grep command filters auth.log, then sends output to shared text file
tail -n 300 /var/log/auth.log | grep "fail" > /media/sf_Shared/failed_passwords.txt
