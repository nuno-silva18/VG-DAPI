"""
File responsable to get information about steam games
"""
#import the library used to query a website
import urllib2

#import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup

#import the request to get the appID
import requests

def getappid(appid_games_list, name):
    """ Function responsable to get the App ID of a game, given a name"""
    for i in appid_games_list:
        if i['name'] == name:
            print(name + " App ID: " + str(i['appid']))
            return i['appid']

def getgameinfo(urlsteam, appid):
    
    pageurl = urllib2.Request(urlsteam + str(appid))
    #Query the website and return the html to the variable 'page'
    page = urllib2.urlopen(pageurl)
    #Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page, "lxml")

    reviews = soup.findAll('span', class_='nonresponsive_hidden responsive_reviewdesc')

    game_description = soup.find('div', class_='game_description_snippet')

    game_price = soup.find('div', class_='game_purchase_price price')

    #possibility to recomended games (NOT FINISHED)
    games_recomended = soup.find_all('a', class_="small_cap")
    print([reviews,game_description.string,game_price.string,games_recomended])

if __name__ == '__main__':    
    #request responsable to return a json object with all the steam games
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')

    #store appID and Names of the games into a List
    gameslist = r.json()['applist']['apps']
    #get appID given the name of the Game
    appiddota = getappid(gameslist, 'Dota 2')

    #specify steam url
    url = "http://store.steampowered.com/app/"
    
    getgameinfo(url, appiddota)
