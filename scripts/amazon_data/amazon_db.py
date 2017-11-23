# import libraries
import csv
import pymysql
from amazon.api import AmazonAPI

#setup amazon global variable with (AMAZON_ACCESS_KEY, AMAZON_PRIVATE_KEY, AMAZON_ASSOCIATE_TAG)
AMAZON = AmazonAPI('AKIAJ7Y2EZJUVTOMMVYQ', 'ln7Grxo4fTAY4wkcjE77lp7s5xkPqFyK0ozyHuNN', 'naodameu-20')

def connectDatabase():
    """Create database connection"""
    global db
    db = pymysql.connect(host='localhost', user='root', password='',
                         db='vg_dapi', cursorclass=pymysql.cursors.DictCursor,charset='utf8')

def amaz_scrap(vg_name):
    global AMAZON
    # search on Amazon the top 10 search results for the video game name
    try:
        products = AMAZON.search_n(10, Keywords=vg_name, SearchIndex='VideoGames')
    except:
        return

    for product in products:
        if product.product_group == 'Video Games' and product.price_and_currency[0] is not None:
            if product.price_and_currency[0] < 90.0:
                vg_metac_list = [product.price_and_currency[0], product.detail_page_url, vg_name]
                vg_metac_sql = "UPDATE `gameplatform` SET `amazon_price`= %s, `amazon_link` = %s WHERE (SELECT `id` FROM `game` WHERE `name` = %s) = `gameID`"
                cur.execute(vg_metac_sql, vg_metac_list)
                db.commit()
                print('Grabbed Amazon price and data for ' + vg_name)
                break

    return


# call the module directly for testing
if __name__ == '__main__':
    connectDatabase()
    cur = db.cursor()
    cur.execute("SELECT name FROM game")
    vgnames_list = cur.fetchall()
    for vgname in vgnames_list:
        amaz_scrap(vgname['name'])