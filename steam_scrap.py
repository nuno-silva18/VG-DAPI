import requests

def getAppID(appIDListArg,name):
 for i in appIDListArg:
		if i['name'] == name:
			gameAppID = i['appid']
			print(name + " App ID: " + str(gameAppID))
			return gameAppID

if __name__ == '__main__':
	
	#request responsable to return a json object with all the steam games
	r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')

	#store appID and Names of the games into a List
	appIDList = r.json()['applist']['apps']
	
	#get appID given the name of the Game
	appID_Dota = getAppID(appIDList,'Dota 2')

	#with the appID it's possible to use the steam api to do all the get's we need about a game

	r_Dota = requests.get('http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=' + str(appID_Dota) + '&format=json')
	print (r_Dota.json())
