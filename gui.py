import base64
import os
import platform
import time

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
    import ttk

except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
    from tkinter import ttk
from ConfigManager import ConfigManager
from SeatFinder.SeatFinder import SeatFinder


class LightGUI:
    
    window = None

    def __init__(self):
        self.window = Tk()
        self.window.title("RegiojetSeatBooker")
        self.window.geometry('600x300')
        self.locationFrom = ttk.Combobox(self.window, state="readonly", width=10)
        self.locationTo = ttk.Combobox(self.window, state="readonly", width=10)
        self.username_lbl = Label(self.window, text="Username")
        self.username = Entry(self.window, width=10)
        self.password_lbl = Label(self.window, text="Password")
        self.password = Entry(self.window, show="*", width=10)
        self.date_lbl1 = Label(self.window, text="Date")
        self.date_lbl2 = Label(self.window, text="(e.g. 27.7. , leave empty for current date)")
        self.date = Entry(self.window, width=10)

        self.hours_lbl1 = Label(self.window, text="Hours")
        self.hours_lbl2 = Label(self.window, text="(e.g. '19:00 20:00' - to look for multiple times)")
        self.hours = Entry(self.window, width=10)

        self.chrome_version_lbl1 = Label(self.window, text="Chrome version")
        self.chrome_version_lbl2 = Label(self.window, text="(e.g. 74 - you need to find it in chrome settings)")
        self.chrome_version = Entry(self.window, width=10)
        self.tariff_lbl = Label(self.window, text="Tariff")
        self.tariff = ttk.Combobox(self.window, state="readonly", width=10)

        self.find_btn = Button(self.window, text="Find seat", command=self.find_clicked, fg='grey', bg='blue', highlightbackground="blue")
        self.location_switch_btn = Button(self.window, text="< = >", command=self.switch_clicked, fg='grey', bg='blue', highlightbackground="blue")

    def __setup_fields(self):
        config = ConfigManager.get_config()

        cities = list(SeatFinder.cities.keys())

        self.locationFrom['values'] = cities
        self.locationFrom.set(config['from'])

        self.locationTo['values'] = cities
        self.locationTo.set(config['to'])

        self.username.insert(0, config['username'])

        self.password.insert(0, base64.b64decode(config['password']))

        # Setting current date
        self.date.insert(0,time.strftime("%d.%m."))

        self.chrome_version.insert(0, config['chrome_version'])
        self.tariff['values'] = list(SeatFinder.tariffs.keys())
        self.tariff.current(1 if config['tariff'] == 'student' else 0)

    def __build_grid(self):
        self.locationFrom.grid(column=0, row=0)
        self.location_switch_btn.grid(column=1, row=0)
        self.locationTo.grid(sticky='W', column=2, row=0)

        self.username_lbl.grid(column=0, row=1)
        self.username.grid(column=1, row=1)

        self.password_lbl.grid(column=0, row=2)
        self.password.grid(column=1, row=2)

        self.date_lbl1.grid(column=0, row=3)
        self.date.grid(column=1, row=3)
        self.date_lbl2.grid(column=2, row=3)

        self.hours_lbl1.grid(column=0, row=4)
        self.hours.grid(column=1, row=4)
        self.hours_lbl2.grid(column=2, row=4)

        self.chrome_version_lbl1.grid(column=0, row=5)
        self.chrome_version.grid(column=1, row=5)
        self.chrome_version_lbl2.grid(column=2, row=5)

        self.tariff_lbl.grid(column=0, row=6)
        self.tariff.grid(column=1, row=6)

        self.find_btn.grid(column=0, row=7)

    def find_clicked(self):
        config = ConfigManager.get_config()
        config['username'] = self.username.get()

        # Just obscuring the password a little - for some reason b64encode function does not accept strings... and we need to save it as string because of json...
        config['password'] = base64.b64encode(self.password.get().encode("utf-8")).decode('utf-8')

        config['tariff'] = self.tariff.get()
        config['from'] = self.locationFrom.get()
        config['to'] = self.locationTo.get()
        config['chrome_version'] = self.chrome_version.get()

        ConfigManager.set_config(config)

        finder = SeatFinder(
            self.locationFrom.get(),
            self.locationTo.get(),
            self.date.get(),
            self.hours.get().split(' '),
            self.tariff.get(),
            chrome_version=self.chrome_version.get())

        finder.login(self.username.get(), self.password.get())
        foundElem = finder.findSeat()
        if not foundElem:
            return
        finder.takeSeat(foundElem)

    def switch_clicked(self):
        location_from = self.locationFrom.get()
        self.locationFrom.set(self.locationTo.get())
        self.locationTo.set(location_from)

    def show(self):

        self.__setup_fields()
        self.__build_grid()

        self.window.lift()

        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        self.window.mainloop()
        ConfigManager.close()
