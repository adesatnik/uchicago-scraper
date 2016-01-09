__author__ = 'Alejandro'
import urllib
import urllib2
import requests
import cookielib
from bs4 import BeautifulSoup
from planner.models import Quarter, Course
from django.core.management.base import BaseCommand, CommandError







def get_quarter(url,quarter):
    URL = url
    cookie_file = "cookies.lwp"

    cj = cookielib.LWPCookieJar(cookie_file)

    try:
        cj.load()
    except:
        pass

    s = requests.Session()
    s.cookies = cj

    s.get(URL)
    cj.save(ignore_discard=True)

    return s.post(URL, data = {"TermName" : quarter}).text


def parse_department_page(url, q):

    html = get_quarter(url, q.quarter + " " + str(q.year))
    soup = BeautifulSoup(html, "lxml")
    classes = []


    rows =soup(class_="resultrow")

    for row in rows:
        classes.append([
            row.find(class_="name").a.next_sibling.strip(),
            row.find(class_="two").string.strip()
        ])





    for cl in classes:
        if not Course.objects.filter(name=cl[1], department=(cl[0].split(" "))[0],
                   code=(((cl[0].split(" "))[1]).split("/"))[0]):
            c = Course(name=cl[1], department=(cl[0].split(" "))[0],
                       code=(((cl[0].split(" "))[1]).split("/"))[0]  )
            c.save()


            c.quarter_set.add(q)

        else:
            c = Course.objects.get(name=cl[1], department=(cl[0].split(" "))[0],
                   code=(((cl[0].split(" "))[1]).split("/"))[0])

            c.quarter_set.add(q)


class Command(BaseCommand):
    help = "Scrapes classes.uchicago for classes on the given quarter"

    def add_arguments(self, parser):
        parser.add_argument("quarter", nargs="+" ,type=str)
        parser.add_argument("year", nargs="+", type=int)

    def handle(self, *args, **options):

            linkstrings = []

            html = get_quarter("https://classes.uchicago.edu/browse.php",
                               str(options["quarter"][0]) + " " + str(options["year"][0]))

            soup = BeautifulSoup(html, "lxml")
            if Quarter.objects.filter(quarter = options["quarter"][0], year = int(options["year"][0])):
                q = Quarter.objects.get(quarter = options["quarter"][0], year = int(options["year"][0]))
            else:
                q = Quarter(quarter = options["quarter"][0], year = int(options["year"][0]))
                q.save()

            filtered = soup.find(id="tabs-1")
            filtered = filtered("li")

            for link in filtered:
                linkstrings.append("https://classes.uchicago.edu/" + link.find("a").get("href"))




            for link in linkstrings:
                parse_department_page(link,q)
                print(link + " done")






