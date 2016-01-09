# uchicago-scraper

This project includes two to scrape course data from the University of Chicago course catalog (classes.uchicago.edu).
These scripts are designed to be used in a Django project, using the model Course to represent the course data in the project database.
Note that they are set up as Django management commands
##scrapeclasses
This script takes a quarter (e.g Winter 2015) and returns a list of all the courses offered that quarter.

##addcrosslistings
This script goes through each course currently in the database and accesses its webpage, scraping the cross-listed classes. from it.
It can be easily modified to scrape other data, such as its pre-requisites or its course description. 


