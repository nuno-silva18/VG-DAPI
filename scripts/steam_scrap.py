import pymysql
import urllib.request
from bs4 import BeautifulSoup
import requests

def connectDatabase():
    """Create database connection"""
    global db
    db = pymysql.connect(host='localhost', user='root', password='',
                         db='vg_dapi', cursorclass=pymysql.cursors.DictCursor,charset='utf8')

def getappid(appid_games_list, name):
    """ Function responsable to get the App ID of a game, given a name"""
    for i in appid_games_list:
        if i['name'] == name:
            print(name + " App ID: " + str(i['appid']))
            return i['appid']

def getgameinfo(urlsteam, appid, vgnamesteam):
    
    pageurl = urllib.request.Request(urlsteam + str(appid))
    #Query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(pageurl)
    #Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page, "lxml")

    reviews = soup.find('span', class_='nonresponsive_hidden responsive_reviewdesc')
 

    if reviews is None:
        pass
    else:
        vgsteamscores_list = [appid, reviews.text, vgnamesteam]
        vgsteamscores_sql = "UPDATE `gameplatform` SET `steamID` = %s, `steam_score` = %s WHERE (SELECT `id` FROM `game` WHERE `name` = %s) = `gameID`"
        cur.execute(vgsteamscores_sql, vgsteamscores_list)
        db.commit()

if __name__ == '__main__':    
    url = "http://store.steampowered.com/app/"
    
    #request responsable to return a json object with all the steam games
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')

    #store appID and Names of the games into a List
    gameslist = r.json()['applist']['apps']

    connectDatabase()
    cur = db.cursor()
    cur.execute("SELECT name FROM game")
    vgnames_list = cur.fetchall()
    for vgname in vgnames_list:
        if getappid(gameslist, vgname['name']) is None:
            pass
        else:
            appidgame = getappid(gameslist, vgname['name'])
            getgameinfo(url, appidgame, vgname['name'])