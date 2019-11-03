# Regiojet Seat Booker

This script uses a Selenium webdriver to login, periodically search for empty seat for given time and reserve or buy a ticket for this seat on 
`jizdenky.regiojet.cz` webpage. It is able to book tickets for both buses and trains.

## Requirements

You only need a Python and Chrome installed. It runs on Mac Windows and Linux and on python >2.7 or >3.6
Python can be downloaded from https://www.python.org/downloads/

## How to run
To start the script, run `start.py` file - either double-click on it on Windows or type `python <path>/start.py` 
on Mac or Linux.

After that, you should see a form window, where you can enter your credentials.

To run the script correctly, you need to choose correct Chrome version

## Chrome version
For the script to run properly, you need to have a compatible Chrome. 
**GUI now tries to identify correct version automatically so you probably don't need to worry about the stuff below**... But just in case:

You can find your Chrome's version
From Google's manual:
- Click on the icon in the upper right corner that looks like 3 short bars.
- Select About Google Chrome to display the version number.


If your chrome version is not listed when you run the script, you can download a corresponding chromedriver from 
http://chromedriver.chromium.org/downloads.

Unzip the file and put it to `SeatFinder/src/chromedrivers/<version_number>/<platform_name>` - platform names are 
    - `lin` for Linux
    - `mac` for MacOS
    - `win.exe` for Windows
So for example on windows with chromeversion 77, you would put the unzipped file to 
`SeatFinder/src/chromedrivers/77/` and name it `win.exe`

##Technical details
TBD
