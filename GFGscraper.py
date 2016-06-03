import sys
import os
import prettytable
import requests
from bs4 import BeautifulSoup
import urllib2

class geeksforgeeks():
    menu = []
    chapters = []
    url = ''
    option = -1

    def __init__(self):
            print "GEEKS FOR GEEKS"
            print "---------------"
            self.url = 'http://www.geeksforgeeks.org/'

    def Menu(self):
        notinclue = ['Home', 'Contribute', 'Ask Q', 'AndroidApp', 'Jobs', 'GBlog', 'MCQ', 'Misc' , 'O/P', 'C/C++', 'Job Seekers', 'Employers', 'Advertise with us', 'Internship']
        #Extracting the contents of the url
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")

        #Selectin all a tags
        divs = soup.findAll('div', {'class': 'menu-iconic-container'})

        for atag in divs:
            a = atag.findAll('a')


        del a[2:16]
        del a[3:15]
        i = 1
        l = []
        self.menuTable = prettytable.PrettyTable(["Option", "Topic"])


        for atag in a:
            if atag.text not in notinclue:
                l.append(i)
                l.append(str(atag.text))
                self.menuTable.add_row(l)
                l.append(str(atag.get('href')))
                self.menu.append(l)
                i = i + 1
                l = []
        self.getMenu()

    def getMenu(self):
        print self.menuTable
        self.option = -1
        while(self.option < 0 or self.option > len(self.menu)):
            self.option = input("Enter an option to download: ")

        self.directory = self.menu[self.option - 1][1]
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.getTopic()

    def getTopic(self):

        self.url = self.menu[self.option - 1][2]
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")

        divs = soup.findAll('div', {'class': 'entry-content'})
        #print divs

        if(divs == []):
            divs = soup.findAll('section', {'class': 'site-content'})

        if(divs == []):
            divs = soup.findAll('div', {'class': 'site-content'})
        for atag in divs:
            a = atag.findAll('a')

        if(self.option == 1):
            del a[0:17]
        elif(self.option == 2):
            del a[0:13]
        chapterTable = prettytable.PrettyTable(["Option", "Topic"])
        i = 1
        l = []
        for atag in a:
            l.append(i)
            l.append(atag.text)
            chapterTable.add_row(l)
            l.append(atag.get('href'))
            self.chapters.append(l)
            i = i + 1
            l = []
        print chapterTable
        option = -1
        while(option < 0 or option > len(self.chapters)):
            option = input("Enter an option to download (Enter '0' to download all): ")

        print "Downloading file(s) ........"
        if(option == 0):
            for x in self.chapters:
                rq = urllib2.Request(x[2])
                res = urllib2.urlopen(rq)
                f = open(self.directory + "/" + x[1] + ".html", 'wb')
                f.write(res.read())
                print "File saved to " +  self.directory + "/" + x[1] + ".html"
                f.close()
        else:
            rq = self.chapters[option - 1][2]
            res = urllib2.urlopen(rq)
            f = open(self.directory + "/" + self.chapters[option - 1][1] + ".html", 'wb')
            f.write(res.read())
            print "File saved to " +  self.directory + "/" + self.chapters[option - 1][1] + ".html"
            f.close()

        self.chapters = []
        opt = -1
        print "1. Menu"
        print "2. Topics"
        print "3. Exit"
        while(opt != 1 and opt != 2 and opt != 3):
            opt = input("Enter your option: ")
        if(opt == 1):
            self.getMenu()
        elif(opt == 2):
            self.getTopic()
        else:
            sys.exit();


gfg = geeksforgeeks()
gfg.Menu()
