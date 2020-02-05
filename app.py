from CRSTimes import *
from tkinter import *
from tkinter.ttk import *
from tkinter.constants import *
from datetime import datetime

class App:
    def __init__(self):
        self.master = Tk()
        self.master.title("Crunchyroll Episode Countdown")
        self.master.minsize()

        shows = CSVList()

        self.combo = Combobox(self.master)
        self.combo['values'] = tuple(shows.getShowList())
        self.combo['state'] = 'readonly'
        self.combo.current(0)
        self.combo.selection_clear()

        self.combo.pack(side=TOP, expand=False, fill=BOTH)
        self.cd = Label(self.master, text="00:00:00:00", anchor=CENTER, font=("Helvetica", 72))
        self.cd.pack(side=TOP, expand=True, fill=BOTH)

        self.master.minsize(400, 150)
        self.master.after(0, self.updateHandler)

    def updateHandler(self):

        self.cd.config()

        self.master.after(3, self.editLabel)

if __name__ == '__main__':
    App().master.mainloop()