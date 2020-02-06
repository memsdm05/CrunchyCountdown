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
        
        self.__graphics()
    
    def __graphics(self):
        self.shows = CSVList()
        self.showObj = self.shows.buildShowObjectList()

        self.combo = Combobox(self.master)
        self.combo['values'] = tuple(self.shows.getShowList())
        self.combo['state'] = 'readonly'
        self.combo.current(0)
        self.combo.selection_clear()

        self.combo.pack(side=TOP, expand=False, fill=BOTH)
        self.cd = Label(self.master, text="00:00:00:00", anchor=CENTER, font=("Helvetica", 72),
                        justify='center')
        self.cd.pack(side=TOP, expand=True, fill=BOTH)

        self.currentShow = self.combo.get()

        self.master.minsize(400, 150)
        self.master.after(0, self.updateHandler)
        
    def deltatime(self):
        return self.shows.getTimestamp(self.currentShow) - self.getCurrentTimestamp()

    def getCurrentTimestamp(self):
        return self.now.weekday() * 1444 + self.now.hour * 60 + self.now.minute

    def getString(self):
        temp = self.deltatime() if self.deltatime() > 0 else self.getCurrentTimestamp() + self.deltatime()
        days = hours = mins = 0
        days = temp // 1440
        temp -= days * 1440
        hours = temp // 60
        temp -= hours * 60
        mins = temp

        return f"{str(days) if len(str(days)) > 1 else '0'+ str(days)}" \
               f":{str(hours) if len(str(hours)) > 1 else '0'+ str(hours)}:" \
               f"{str(mins) if len(str(mins)) > 1 else '0'+ str(mins)}:"

        
    def updateHandler(self):

        self.currentShow = self.combo.get()

        self.now = datetime.now()
        a = self.getString() + str(60-self.now.second)

        self.getString()

        # print(self.showObj[23].timestamp() - self.getCurrentTimestamp())

        size = self.master.winfo_width()// 4 if self.master.winfo_width() < self.master.winfo_height() else \
            self.master.winfo_height()//   3



        self.cd.config(text=a, font=("Helvetica", size))

        self.master.after(100, self.updateHandler)

if __name__ == '__main__':
    App().master.mainloop()