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

        self.__importShows()
        self.__graphics()

    def __importShows(self):
        self.shows = CSVList()
        self.sl = list(self.shows.getShowList().keys())

    def __graphics(self):
        self.showObj = self.shows.buildShowObjectList()

        self.combo = Combobox(self.master)
        self.combo['state'] = 'readonly'

        self.master.minsize(400, 150)
        self.combo.pack(side=TOP, expand=False, fill=BOTH)
        self.cd = Label(self.master, text="00:00:00:00", anchor=CENTER, font=("Helvetica", 72),
                        justify='center')
        self.cd.pack(side=TOP, expand=True, fill=BOTH)
        self.combo['values'] = tuple(self.sl)

        self.master.after(0, self.updateHandler)
        self.master.after(0, self.watchdog)

        self.combo.current(0)
        self.currentShow = self.combo.get()
        
    def deltatime(self):
        temp = self.shows.getTimestamp(self.currentShow) - self.getCurrentTimestamp() + 15
        return temp if temp > 0 else 10080 + temp

    def getCurrentTimestamp(self):
        return (self.now.weekday() * 1444) + (self.now.hour * 60) + self.now.minute

    def getString(self):
        self.now = datetime.now()
        temp = self.deltatime()
        days = hours = mins = 0
        days = temp // 1440
        temp -= days * 1440
        hours = temp // 60
        temp -= hours * 60
        mins = temp

        return f"{'0' + str(days)}" \
               f":{str(hours) if len(str(hours)) > 1 else '0'+ str(hours)}:" \
               f"{str(mins) if len(str(mins)) > 1 else '0'+ str(mins)}:"

        
    def updateHandler(self):
        self.combo['values'] = list(self.sl)
        self.currentShow = self.combo.get()
        self.now = datetime.now()

        t = str(59-self.now.second)
        a = self.getString() + (t if len(t) > 1 else '0'+t)

        # print(self.showObj[23].timestamp() - self.getCurrentTimestamp())

        # todo fix text scaling
        size = self.master.winfo_width()// 6 if self.master.winfo_width() < self.master.winfo_height() else \
            self.master.winfo_height()//   3



        self.cd.config(text=a, font=("Helvetica", size))

        self.master.after(100, self.updateHandler)

    def watchdog(self):
        self.sl.sort(key = lambda a : self.shows.showDeltatime(a, self.getCurrentTimestamp()))
        self.master.after(180000, self.watchdog)


if __name__ == '__main__':
    App().master.mainloop()