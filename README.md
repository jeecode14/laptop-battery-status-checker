# Battery Status Checker
This script can be run on the backround to listen battery status of a laptop. It will trigger the notifications if it reaches its minimum or above threshold limit.


## How to use and run this script?
Install the neccessary libraries by installing requirements.txt
> pip install -r requirements.txt

## Python Version
You can use any latest python version. But it was tested on Python 3.11.

## Create installer with Pyinstaller
> pyinstaller --onefile --name BatteryStatusChecker battery_status.py