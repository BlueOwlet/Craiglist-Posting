#!/usr/bin/env bash
echo "Starting Installation"
cp /Webdrivers/geckodriver /usr/bin/
cp /Webdrivers/chromedriver /usr/bin/
echo "Webdrivers copied to /usr/bin/"
python3 -m venv venv
echo "Venv Created"
. venv/bin/activate
echo "venv Activated"
pip install -r req.txt
echo "Requirements Installed"
crontab -l > tmpfile
echo "*/10 * * * * ${pwd}/run.sh" >> tmpfile
crontab tmpfile
rm tmpfile
echo "CronJob created"
echo "Intallation Complete - Ready to start"
touch runLog.txt
touch debug.txt
echo "Initial Installation completed" > runLog.txt
echo "Ready to use =3"
