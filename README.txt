Use these scripts on your own responsibility!!

for running the script, only python and Chrome has to be installed ( https://www.python.org/downloads/ )

Scripts refresh the booking page at jizdenky.regiojet.cz webpage and search for empty ticket in time interval
which is set in the beginning.

When the script finds a free seat, it brings the (selenium) browser to the front and then
buys the ticket automatically (when the user fails to log in, the ticket is just reserved)

*Credentials for login along with the tariff can be set in the config.py file - rename and edit config_template.py file*

Multiple times can be checked at once, but only one date.

The webpage must be loaded in Czech language, since some elements are searched by its (czech) label

Scripts pisekPraha.py and prahaPisek.py are predefined to find routes between Prague and Pisek. Other towns have
to be yet added. It would be really nice if someone implemented nice user interface.

Usage: prahaPisek.py [date] <time> [time]...'
Example#1: prahaPisek.py 0225 1000'
Example#2: pisekPraha.py 25.02. 10:30 11:30 12:30'.

Chrome version is changing really fast, so we need to change chromedrivers pretty often. When the script fails, it is usualy because your current chromedriver is deprecated. All you have to do is to download a driver for your os and chrome version from http://chromedriver.chromium.org/downloads and replace corresponding file in SeatFinder/src/chromedrivers (you have to rename it too..)
