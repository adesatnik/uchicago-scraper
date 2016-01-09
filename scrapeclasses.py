__author__ = 'Alejandro'
from django.core.management.base import BaseCommand, CommandError
import cookielib
import requests
from bs4 import BeautifulSoup
from planner.models import Quarter, Course

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


def scrapecrosslistings(course):
    lastqoffered = course.quarter_set.extra(order_by = ["-index"])[0]
    html = get_quarter("https://classes.uchicago.edu/courseDetail.php?courseName=" + str(course), str(lastqoffered))
    soup = BeautifulSoup(html, "lxml")
    try:
        crossp = soup.find(id="tabs-1").find("p")
    except:
        crossp = ""

    if crossp:
        for l in crossp.find_all("a"):
            coursename = l.string.split(" ")

            try:
                lastcourseversion = Course.objects.filter(department=coursename[0], code=coursename[1])[0]
            except:
                c = Course(department=coursename[0], code=coursename[1], name=course.name)
                c.save()
                c.quarter_set.add(lastqoffered)
                print "added " + str(c)
                lastcourseversion = c
            course.cross_listings.add(lastcourseversion)


    else:
        return None













class Command(BaseCommand):
    help = "Scrapes cross-listings out of every class in the database"


    def handle(self, *args, **options):
        for c in Course.objects.filter(id__gt=2954):
            scrapecrosslistings(c)

            print c.cross_listings.all()
            print c.id

