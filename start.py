from Tkinter import *
from ttk import Combobox
import os
import json
from SeatFinder.SeatFinder import SeatFinder
import platform


f = open("config.json", "r+")
try:
    config = json.load(f)
except ValueError:
    config = {
        'username': '',
        'password': '',
        'tariff': 'regular'
    }

window = Tk()

window.title("RegiojetSeatBooker")

window.geometry('600x300')


locations = Combobox(window, state="readonly", width=10)
locations['values']= ("Pisek->Praha", "Praha->Pisek")
locations.current(0)
username_lbl = Label(window, text="Username")
username = Entry(window, width=10)
username.insert(0, config['username'])

password_lbl = Label(window, text="Password")
password = Entry(window, show="*", width=10)
password.insert(0, config['password'])

date_lbl1 = Label(window, text="Date")
date_lbl2 = Label(window, text="(e.g. 27.7. , leave empty for current date)")
date = Entry(window, width=10)

hours_lbl1 = Label(window, text="Hours")
hours_lbl2 = Label(window, text="(e.g. '19:00 20:00' - to look for multiple times)")
hours = Entry(window, width=10)

tariff_lbl = Label(window, text="Tariff")
tariff = Combobox(window, state="readonly", width=10)
tariff['values'] = ("regular", "student")
tariff.current(1 if config['tariff'] == 'student' else 0)


locations.grid(column=1, row=0)

username_lbl.grid(column=0, row=1)
username.grid(column=1, row=1)

password_lbl.grid(column=0, row=2)
password.grid(column=1, row=2)

date_lbl1.grid(column=0, row=3)
date.grid(column=1, row=3)
date_lbl2.grid(column=2, row=3)

hours_lbl1.grid(column=0, row=4)
hours.grid(column=1, row=4)
hours_lbl2.grid(column=2, row=4)

tariff_lbl.grid(column=0, row=5)
tariff.grid(column=1, row=5)


def clicked():
    config['username'] = username.get()
    config['password'] = password.get()
    config['tariff'] = tariff.get()
    f.seek(0)  # <--- should reset file position to the beginning.
    json.dump(config, f, indent=4)
    f.truncate()

    locations_array = locations.get().split("->")

    finder = SeatFinder(locations_array[0], locations_array[1], date.get(), hours.get().split(' '), tariff.get())
    finder.login(username.get(), password.get())
    foundElem = finder.findSeat()
    if not foundElem:
        return
    finder.takeSeat(foundElem)


btn = Button(window, text="Find seat", command=clicked)

btn.grid(column=0, row=6)
window.lift()

if platform.system() == 'Darwin':
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

window.mainloop()
f.close()



