#!/usr/bin/env bash
cd /home/owl/Documents/GitHub/Craigslist
. venv/bin/activate
echo Start >> runLog.txt
date >> runLog.txt
python3 Craiglist.py > debug.txt
echo Stop >> runLog.txt
date >> runLog.txt

