# import libraries
import urllib2
import csv
import re
from bs4 import BeautifulSoup

def metac_scrap(meta_url):
    # specify the url
    title_page = urllib2.Request(meta_url, headers={'User-Agent': 'Mozilla/5.0'})

    # query the website and return the html to the variable 'page'
    page = urllib2.urlopen(title_page)

    # parse the html using Beautiful Soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # take out the <div> of object to find and get its value
    name_box = soup.find('span', attrs={'itemprop': 'name'})
    name = name_box.text.strip()

    score_box = soup.find('span', attrs={'itemprop': 'ratingValue'})
    score = score_box.text

    uscore_box = soup.find('div', attrs={'class': re.compile('^metascore_w user')})
    uscore = uscore_box.text

    # open a csv file with append, so old date will not be erased
    with open('metacritic.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, score, uscore])

    return

# call the module directly for testing
if __name__ == "__main__":
    metac_scrap('')
