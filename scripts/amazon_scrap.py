# import libraries
import urllib2
import csv
from amazon.api import AmazonAPI

#setup amazon global variable with (AMAZON_ACCESS_KEY, AMAZON_PRIVATE_KEY, AMAZON_ASSOCIATE_TAG)
AMAZON = AmazonAPI('AKIAJ7Y2EZJUVTOMMVYQ', 'ln7Grxo4fTAY4wkcjE77lp7s5xkPqFyK0ozyHuNN', 'naodameu-20')

def amaz_scrap(vg_name):
    global AMAZON

    # search on Amazon the top 10 search results for the video game name provided in the video games category
    products = AMAZON.search_n(10, Keywords=vg_name, SearchIndex='VideoGames')
    for product in products:
        if product.product_group == 'Video Games':
            # open a csv file with append, so old date will not be erased
            with open('amazon.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([product.title, product.price_and_currency, product.product_group])
                return

# call the module directly for testing
if __name__ == '__main__':
    amaz_scrap('finding nemo')
