import requests
from bs4 import BeautifulSoup
from datetime import datetime

class SimulcastShows:
    def __init__(self, showdict):
        self.d = showdict

    def getShowList(self): return self.d

    def hasShow(self, name: str): return name in self.d.keys()

    def getLink(self, name: str): return self.d[name]['link']

    def getTime(self, name: str): return self.d[name]['time']

    def getDay(self, name: str): return self.d[name]['day']

    def getDayNum(self, name: str): return int(self.d[name]['day_num'])

    def getShowStat(self, name: str):
        return self.d[name]['day'] + " " + self.d[name]['time']

    def buildShowObjectList(self):
        s = []
        for i in self.d.keys():
            s.append(ShowObject(i, self.d))
        return s


class ScrapeList(SimulcastShows):
    def __init__(self, verbose = False, cutoff = 0):
        self.baseurl = 'https://www.crunchyroll.com'
        self.simul = '/videos/anime/simulcasts'

        self.v = verbose;
        self.c = cutoff;

        self.h = []
        self.t = {}
        self.showDict = {}

        self.__buildShowHREF()
        self.__buildShowTimes()
        self.__buildCleanData()

        super().__init__(self.showDict)


    # helper method for pretty printing lists
    def __pl(self, lst):
        for e in lst:
            print(e)
        print(len(lst))
        print()

    # scrapes https://www.crunchyroll.com/videos/anime/simulcasts for hrefs of shows
    def __buildShowHREF(self):
        if self.v: print("Finding Shows...")
        try:
            r = requests.get(self.baseurl + self.simul)
        except requests.ConnectionError:
            quit()

        simulSoup = BeautifulSoup(r.text, "lxml")
        li = simulSoup.find_all('li', {'itemtype': "http://schema.org/TVSeries"})
        for show in li:
            for element in show.findChildren("a", recursive=True):
                self.h.append(element.get("href").rstrip())

        self.h = list(dict.fromkeys(self.h)) # remove dupes
        if self.c > 0: self.h = self.h[:self.c]

    # scrapes shows for times and dates
    def __buildShowTimes(self):
        # r = requests.get(self.baseurl + self.h[0])
        # showSoup = BeautifulSoup(r.text, "lxml")
        # print(showSoup.title.text.split("-")[0])
        # print(showSoup.find('p', {'class': "strong"}).text)

        for href in self.h:
            r = requests.get(self.baseurl + href + "/more")
            showSoup = BeautifulSoup(r.text, "lxml")
            show = showSoup.title.text.split("Show Information")[0].rstrip(" ")
            try:
                time = showSoup.find('p', {'class': "strong"}).text[13:]
            except:
                del showSoup
                continue

            if self.v: print("{:70s} {:10s}".format(show, time))
            self.t[show] = time


    def __buildCleanData(self):
        if self.v: print("Cleaning...")
        day2num = {'Mondays': 0, 'Tuesdays': 1, 'Wednesdays': 2, 'Thursdays': 3, 'Fridays': 4, 'Saturdays': 5,
                   'Sundays': 6}

        hrefindex = 0;
        for show in self.t.keys():
            day = self.t[show].split(" ")[0]
            time = self.t[show].split(" ")[1].split(" ")[0]

            am_pm = time.split(':')[1][2:]

            rtime = datetime.strftime(datetime.strptime(time[:-2]+am_pm.upper(), "%I:%M%p"), "%H:%M")

            day_num = day2num[day]
            self.showDict[show] = {'time':rtime,
                                   'day_num':day_num, "day": day,
                                   "link":self.baseurl + self.h[hrefindex]}
            hrefindex+=1;

    def __len__(self):
        return len(self.showDict)


# ======== PUBLIC METHODS ======== #
    def debugPrint(self):
        for i in self.showDict.keys():
            print(i)
            print(self.showDict[i])

    def buildShowCSV(self, name="output"):
        file = name if name[-4:] == ".csv" else name + ".csv"
        if self.v: print("Creating CSV...")
        with open(file, "w") as f:
            for show in self.showDict:
                f.write(f"{show.replace(', ', ' ')},"
                        f"{self.showDict[show]['time']},"
                        f"{self.showDict[show]['day']},"
                        f"{str(self.showDict[show]['day_num'])},"
                        f"{self.getShowLink(show)}\n")

class CSVList(SimulcastShows):
    def __init__(self, name="output"):
        self.csvDict = {}
        self.file = name if name[-4:] == ".csv" else name + ".csv"
        self.__buildCSVDict()

        super().__init__(self.csvDict)

    def __buildCSVDict(self):
        with open(self.file) as f:
            for line in f:
                line = line.rstrip()
                i = line.split(",")
                self.csvDict[i[0]] = {'time': i[1], 'day': i[2], 'day_num': int(i[3]), 'link': i[4]}

    def __len__(self):
        return len(self.csvDict)
                
    def debugPrint(self):
        for i in self.csvDict.keys():
            for j in self.csvDict[i].values():
                print(j)
            print()



class ShowObject():
    def __init__(self, name, temp: dict):
        if name not in temp:
            raise LookupError("not a valid show")
        self.__name = name
        self.__time = temp[name]['time']
        self.__day = temp[name]['day']
        self.__day_num = int(temp[name]['day_num'])
        self.__link = temp[name]['link']

    def name(self): return self.__name
    def time(self): return self.__time
    def day(self): return self.__day
    def day_num(self): return self.__day_num
    def link(self): return self.__link
