"""
File responsable to get information about steam games
"""
import requests

def getappid(appid_games_list, name):
    """ Function responsable to get the App ID of a game, given a name"""
    for i in appid_games_list:
        if i['name'] == name:
            print(name + " App ID: " + str(i['appid']))
            return i['appid']

if __name__ == '__main__':
    #request responsable to return a json object with all the steam games
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')

    #store appID and Names of the games into a List
    games_list = r.json()['applist']['apps']
    #get appID given the name of the Game
    appid_dota = getappid(games_list, 'Dota 2')

    #with the appID it's possible to use the steam api to do all the get's we need about a game

    r_dota = requests.get('http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=' + str(appid_dota) + '&format=json')
    print (r_dota.json())
