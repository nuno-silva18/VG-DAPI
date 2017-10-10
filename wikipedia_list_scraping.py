"""This module scrapes game information from wikipedia lists to compile into a database"""
import pandas as pd
import MySQLdb

def connectDatabase():
    db=MySQLdb.connect()
    
def scrape_ps4_games():
    """Scrapes PS4 games info from wikipedia lists"""

    url = r'https://en.wikipedia.org/wiki/List_of_PlayStation_4_games'
    url2 = r'https://en.wikipedia.org/wiki/List_of_PlayStation_4_games_(M-Z)'

    tables = pd.read_html(url) # Returns list of all tables on page
    tables2 = pd.read_html(url2)
    ps4games = pd.concat([tables[2], tables2[0]]) # Select table of interest
    titles = ps4games[ps4games.columns[0]].tolist()
    genres = ps4games[ps4games.columns[1]].tolist()
    developers = ps4games[ps4games.columns[2]].tolist()
    publishers = ps4games[ps4games.columns[3]].tolist()
    exclusive = ps4games[ps4games.columns[4]].tolist()
    dateJP = ps4games[ps4games.columns[5]].tolist()
    dateUS = ps4games[ps4games.columns[6]].tolist()
    dateEU = ps4games[ps4games.columns[7]].tolist()
    
    for count in range(0, len(titles)):
        print(str(count)+": Title:"+titles[count]+"   |  Genre(s):"+str(genres[count])+"  |  Developer(s):"+str(developers[count])+"  |  Publisher(s):"+str(publishers[count])+"  |  DateUS(s):"+str(dateUS[count]))

def main():
    """Entry Point"""
    scrape_ps4_games()

if __name__ == '__main__':
    main()
