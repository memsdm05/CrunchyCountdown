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
        self.showObj = shows.buildShowObjectList()

        self.combo = Combobox(self.master)
        self.combo['values'] = tuple(shows.getShowList())
        self.combo['state'] = 'readonly'
        self.combo.current(0)
        self.combo.selection_clear()

        self.combo.pack(side=TOP, expand=False, fill=BOTH)
        self.cd = Label(self.master, text="00:00:00:00", anchor=CENTER, font=("Helvetica", 72),
                        justify='center')
        self.cd.pack(side=TOP, expand=True, fill=BOTH)

        self.master.minsize(400, 150)
        self.master.after(0, self.updateHandler)

    def updateHandler(self):

        self.currentShow = self.combo.get()

        print(self.currentShow)
        self.now = datetime.now()
        a = self.now.strftime('%W:%H:%M:%S')

        # print(self.showObj[23].timestamp() - self.getCurrentTimestamp())

        size = self.master.winfo_width()// 4 if self.master.winfo_width() < self.master.winfo_height() else \
            self.master.winfo_height()//   3



        self.cd.config(text=a, font=("Helvetica", size))

        self.master.after(100, self.updateHandler)

    def getCurrentTimestamp(self):
        return self.now.weekday() * 1444 + self.now.hour * 60 + self.now.minute

if __name__ == '__main__':
    App().master.mainloop()