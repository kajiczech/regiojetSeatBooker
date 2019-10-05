import base64
import os
import platform
import time

from selenium.common.exceptions import WebDriverException

try:
    # for Python2
    from Tkinter import *
    import ttk

except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import ttk
from ConfigManager import ConfigManager
from SeatFinder.SeatFinder import SeatFinder
from SeatFinder.webdriver_management import *


class LightGUI:
    
    window = Tk()

    def __init__(self):
        self.window.title("RegiojetSeatBooker")
        self.window.geometry('600x300')
        self.location_from = ttk.Combobox(self.window, state="readonly", width=10)
        self.location_to = ttk.Combobox(self.window, state="readonly", width=10)
        self.username_lbl = Label(self.window, text="Username")
        self.username = Entry(self.window, width=10)
        self.password_lbl = Label(self.window, text="Password")
        self.password = Entry(self.window, show="*", width=10)
        self.date_lbl1 = Label(self.window, text="Date")
        self.date_lbl2 = Label(self.window, text="(e.g. 27.7. , leave empty for current date)")
        self.date = Entry(self.window, width=10)

        self.times_lbl1 = Label(self.window, text="Times")
        self.times_lbl2 = Label(self.window, text="(e.g. '19:00 20:00' - to look for multiple times)")
        self.times = Entry(self.window, width=10)

        self.chrome_version_lbl1 = Label(self.window, text="Chrome version")
        self.chrome_version_lbl2 = Label(self.window, text="If you don't see your version here, see readme file")
        self.chrome_version = ttk.Combobox(self.window, state="readonly", width=10)
        self.tariff_lbl = Label(self.window, text="Tariff")
        self.tariff = ttk.Combobox(self.window, state="readonly", width=10)

        self.find_btn = Button(
            self.window, text="Find seat", command=self.find_clicked, fg='grey', bg='blue', highlightbackground="blue"
        )
        self.location_switch_btn = Button(
            self.window, text="< = >", command=self.switch_clicked, fg='grey', bg='blue', highlightbackground="blue"
        )

    def __setup_fields(self):
        config = ConfigManager.get_config()

        cities = list(SeatFinder.cities.keys())

        self.location_from['values'] = cities
        self.location_from.set(config['from'])

        self.location_to['values'] = cities
        self.location_to.set(config['to'])

        self.username.insert(0, config['username'])

        self.password.insert(0, base64.b64decode(config['password']))

        # Setting current date
        self.date.insert(0, time.strftime("%d.%m."))
        self.chrome_version['values'] = get_available_chrome_versions()
        self.chrome_version.set(config['chrome_version'])
        self.tariff['values'] = list(SeatFinder.tariffs.keys())
        self.tariff.current(1 if config['tariff'] == 'student' else 0)

    def __build_grid(self):
        self.location_from.grid(column=0, row=0)
        self.location_switch_btn.grid(column=1, row=0)
        self.location_to.grid(sticky='W', column=2, row=0)

        self.username_lbl.grid(column=0, row=1)
        self.username.grid(column=1, row=1)

        self.password_lbl.grid(column=0, row=2)
        self.password.grid(column=1, row=2)

        self.date_lbl1.grid(column=0, row=3)
        self.date.grid(column=1, row=3)
        self.date_lbl2.grid(column=2, row=3)

        self.times_lbl1.grid(column=0, row=4)
        self.times.grid(column=1, row=4)
        self.times_lbl2.grid(column=2, row=4)

        self.chrome_version_lbl1.grid(column=0, row=5)
        self.chrome_version.grid(column=1, row=5)
        self.chrome_version_lbl2.grid(column=2, row=5)

        self.tariff_lbl.grid(column=0, row=6)
        self.tariff.grid(column=1, row=6)

        self.find_btn.grid(column=0, row=7)

    def find_clicked(self):
        self.save_config()
        try:
            self.find_and_take_seat()
        except WebDriverException as e:

            if 'session not created: This version of ChromeDriver only supports Chrome version' not in e.msg:
                raise e

            latest_version = find_latest_chromedriver_version()
            if not latest_version:
                raise Exception("Chromedriver not found!")

            self.chrome_version.set(latest_version)

            self.save_config()
            self.find_and_take_seat()

    def find_and_take_seat(self):
        finder = SeatFinder(
            self.location_from.get(),
            self.location_to.get(),
            self.date.get(),
            self.times.get().split(' '),
            self.tariff.get(),
            chrome_version=self.chrome_version.get()
        )

        finder.login(self.username.get(), self.password.get())
        found_elem = finder.find_seat()
        if not found_elem:
            return
        finder.take_seat(found_elem)

    def save_config(self):
        config = {
            'username': self.username.get(),
            'password': base64.b64encode(self.password.get().encode("utf-8")).decode('utf-8'),
            'tariff': self.tariff.get(),
            'from': self.location_from.get(),
            'to': self.location_to.get(),
            'chrome_version': self.chrome_version.get()
        }
        ConfigManager.set_config(config)

    def switch_clicked(self):
        location_from = self.location_from.get()
        self.location_from.set(self.location_to.get())
        self.location_to.set(location_from)

    def show(self):

        self.__setup_fields()
        self.__build_grid()

        self.window.lift()

        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        self.window.mainloop()
