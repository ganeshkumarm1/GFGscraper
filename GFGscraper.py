import os
import prettytable
import requests
from bs4 import BeautifulSoup
import urllib2

class geeksforgeeks():
    menu = []
    chapters = []
    #numbers = []
    #names = []
    #links = []
    url = ''
    option = -1

    def __init__(self):
            print "GEEKS FOR GEEKS"
            print "---------------"
            self.url = 'http://www.geeksforgeeks.org/'

    def getMenu(self):
        notinclue = ['Home', 'Contribute', 'Ask Q', 'AndroidApp', 'Jobs', 'GBlog', 'MCQ', 'Misc' , 'O/P', 'C/C++']
        #Extracting the contents of the url
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")

        #Selectin all a tags
        divs = soup.findAll('div', {'class': 'menu-iconic-container'})

        for atag in divs:
            a = atag.findAll('a')

        #Zipping links with names and numbers
        i = 1
        l = []
        menuTable = prettytable.PrettyTable(["Option", "Topic"])

        for atag in a:
            if atag.text not in notinclue:
                l.append(i)
                l.append(str(atag.text))
                menuTable.add_row(l)
                l.append(str(atag.get('href')))
                self.menu.append(l)
                i = i + 1
                l = []
        #del self.menu[0]
        print menuTable
        self.option = self.selectOption(menuTable, 0)
        self.directory = self.menu[option - 1][1]
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        #print self.option
        #self.menu = []
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
        #print a
        #print self.links
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
        #print self.chapters[option - 1][2]
        #for x in self.chapters:
            #print x.split('/')[-2]
            #print len(self.chapters)

        if(option == 0):
            for x in self.chapters:
                rq = urllib2.Request(x[2])
                res = urllib2.urlopen(rq)
                f = open(self.directory + "/" + x[1] + ".html", 'wb')
                f.write(res.read())
                f.close()
        else:
            rq = self.chapters[option - 1][2]
            res = urllib2.urlopen(rq)
            f = open(self.directory + "/" + self.chapters[option - 1][1] + ".html", 'wb')
            f.write(res.read())
            f.close()

    def selectOption(self, Table, minValue):
        option = input("Enter any option: ")
        if option <= minValue:
            print "Invalid Option"
            self.selectOption(Table)
        elif option > len(self.menu):
            print "Invalid Option"
            self.selectOption(Table)
        else:
            return option

gfg = geeksforgeeks()
gfg.getMenu()
#gfg.getTopic()
