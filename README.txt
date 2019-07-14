Use these scripts on your own responsibility!!

To book a seat you need to run `start.sh` - double click on the file on Windows, or write `python <path>/start.sh` in command line on Mac or Linux

For running the script, only python and Chrome has to be installed ( https://www.python.org/downloads/ )

Scripts refresh the booking page at jizdenky.regiojet.cz webpage and search for empty ticket in time interval
which is set in the beginning.

When the script finds a free seat, it brings the (selenium) browser to the front and then
buys the ticket automatically (when the user fails to log in, the ticket is just reserved)

Multiple times can be checked at once, but only one date.

The webpage must be loaded in Czech language, since some elements are searched by its (czech) label

Chrome version is changing really fast, so we need to change chromedrivers pretty often. When the script fails, it is usualy because your current chromedriver is deprecated. All you have to do is to download a driver for your os and chrome version from http://chromedriver.chromium.org/downloads and replace corresponding file in SeatFinder/src/<version>/chromedrivers (you have to rename it too..)
