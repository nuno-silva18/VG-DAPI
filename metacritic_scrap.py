# import libraries
import urllib2
import csv
import re
from bs4 import BeautifulSoup

def metac_scrap(vg_name):

    # replace spaces with unicode char
    vg_name = vg_name.replace(' ', '%20')

    # search Metacritic for the video game's page
    search_page = urllib2.Request('http://www.metacritic.com/search/all/' + vg_name + '/results', headers={'User-Agent': 'Mozilla/5.0'})

    # query the website and return the html to the variable 's_page'
    s_page = urllib2.urlopen(search_page)

    # parse the html using BeautifulSoup and store in variable 's_soup'
    s_soup = BeautifulSoup(s_page, 'html.parser')

    # grab the Metacritic URL for the video game's page on the domain
    meta_url_box = s_soup.find('h3', attrs={'class': 'product_title basic_stat'})
    meta_url = 'http://metacritic.com' + meta_url_box.find('a')['href']

    # specify the url
    title_page = urllib2.Request(meta_url, headers={'User-Agent': 'Mozilla/5.0'})

    # query the website and return the html to the variable 't_page'
    t_page = urllib2.urlopen(title_page)

    # parse the html using Beautiful Soup and store in variable 't_soup'
    t_soup = BeautifulSoup(t_page, 'html.parser')

    # take out the <span> of object to find and get its value
    name_box = t_soup.find('span', attrs={'itemprop': 'name'})
    name = name_box.text.strip()

    score_box = t_soup.find('span', attrs={'itemprop': 'ratingValue'})
    score = score_box.text

    uscore_box = t_soup.find('div', attrs={'class': re.compile('^metascore_w user')})
    uscore = uscore_box.text

    # open a csv file with append, so old date will not be erased
    with open('metacritic.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, score, uscore])

    return

# call the module directly for testing
if __name__ == "__main__":
    metac_scrap('uncharted 2')
