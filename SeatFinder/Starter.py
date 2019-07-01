import sys
from . SeatFinder import SeatFinder
from config import config
import time


class Starter:

    # @param departureMinute default departure minutes to be shown in an example
    def __init__(self, departure, arrival, departureMinute='00'):
        global input
        try:
            input = raw_input
        except NameError:
            pass

        try:

            if len(sys.argv) < 2:
                self.printUsage(departureMinute)
                date = input('Enter date ( e.g. "25.02", leave empty for today ): ')
                hours = input('Enter hours ( e.g. "10:' + departureMinute + ' 11:' + departureMinute + ' ): ').split(' ')

            elif (len(sys.argv)) == 2:
                date = time.strftime("%d.%m.")
                hours = [sys.argv[1]]

            else:
                date = sys.argv[1],
                if date == 'today' or 'dnes' or 'now':
                    date = time.strftime("%d.%m.")
                hours = sys.argv[2:]
            finder = SeatFinder(departure, arrival, date, hours, config['tariff'])
            finder.login(config['username'], config['password'])
            foundElem = finder.findSeat()
            if not foundElem:
                return
            finder.takeSeat(foundElem)

        except IOError as e:
            print(e.message)
            self.printUsage()
            exit(1)

    def printUsage(self, departureMinute="00"):
        print('Usage: pisekPraha.py <date> <time> [time] [time] ...')
        print('Example pisekPraha.py 0225 10' + departureMinute)
        print('Example pisekPraha.py 25.02. 10:' + departureMinute)
        print('-----------------------------------')
