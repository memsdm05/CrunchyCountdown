from CRSTimes import *
from tkinter import *
from tkinter.ttk import *
from tkinter.constants import *

# creating Tk window
master = Tk()
master.title("Crunchyroll Episode Countdown")
master.minsize()

shows = CSVReader("output")

combo = Combobox(master)
combo['values'] = tuple(shows.getShowList())
combo['state'] = 'readonly'
combo.set("Select an Anime")

combo.pack(side=TOP, expand=False, fill=BOTH)
countdown = Label(master, text="00:00:00:00", anchor=CENTER, font=("Helvetica", 72))
countdown.pack(side=TOP, expand=True, fill=BOTH)



master.minsize(400, 150)

mainloop()