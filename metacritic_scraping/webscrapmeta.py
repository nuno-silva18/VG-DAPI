# import libraries
import urllib2, csv, re
from bs4 import BeautifulSoup
from datetime import datetime


# specify the url
title_page = urllib2.Request('http://www.metacritic.com/game/playstation-4/uncharted-4-a-thiefs-end', headers={'User-Agent': 'Mozilla/5.0'})

# query the website and return the html to the variable 'page'
page = urllib2.urlopen(title_page)

# parse the html using Beautiful Soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

# take out the <div> of object to find and get its value
name_box = soup.find('span', attrs={'itemprop': 'name'})
name = name_box.text.strip()

score_box = soup.find('span', attrs={'itemprop': 'ratingValue'})
score = score_box.text

blurb_box = soup.find('span', attrs={'itemprop': 'description'})
blurb = re.sub(u'[,\u2019\u2122]', '', blurb_box.text.strip())

# open a csv file with append, so old date will not be erased
with open('metacritic.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([name, blurb, score])