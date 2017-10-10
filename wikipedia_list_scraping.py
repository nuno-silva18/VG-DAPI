"""This module scrapes game information from wikipedia lists to compile into a database"""
import pandas as pd
import sys
import pymysql

def connectDatabase():
    global db
    db = pymysql.connect(host='localhost',user='root',password='',db='vg_dapi',cursorclass=pymysql.cursors.DictCursor)

                            

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
    #not needed exclusive = ps4games[ps4games.columns[4]].tolist()
    dateUS = ps4games[ps4games.columns[6]].tolist()
    dateJP = ps4games[ps4games.columns[5]].tolist()
    dateEU = ps4games[ps4games.columns[7]].tolist()

    for count in range(0, 26):
        if(titles[count]!="Title" and titles[count]!="JP"):
            tempList = []
            tempList.append(titles[count])
            if(type(publishers[count]) is float):
                tempList.append("Unknown")
            else:
                tempList.append(publishers[count])
           
            if(type(developers[count]) is float):
                tempList.append("Unknown")
            else:
                tempList.append(developers[count])
            
            if(type(dateUS[count]) is float):
                tempList.append("Unreleased")
            else:
                if(len(dateUS[count])>14):
                    tempList.append(dateUS[count][8:18])
                else:
                    tempList.append(dateUS[count])
            
            if(type(dateJP[count]) is float):
                tempList.append("Unreleased")
            else:
                if(len(dateJP[count])>14):
                    tempList.append(dateJP[count][8:18])
                else:
                    tempList.append(dateJP[count])

            if(type(dateEU[count]) is float):
                tempList.append("Unreleased")
            else:
                if(len(dateEU[count])>14):
                    tempList.append(dateEU[count][8:18])
                else:
                    tempList.append(dateEU[count])
            newGameId = insertGame(tempList) #function returns database id of last inserted game
            #GenreIDs = insertGenre(genres[count])
            #insertGameGenres(newGameId,GenreIDs) 

def insertGame(list):
    try:
        with db.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `game` (`name`, `publishers`, `developers`,`dateUS`,`dateJP`,`dateEU`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, list)
            db.commit()
            return cursor.lastrowid
    except pymysql.err.IntegrityError:
        print("Integrity: Tried to insert duplicate row")
    except pymysql.err.InternalError:
        print("Error: Invalid data")
            
def main():
    """Entry Point"""
    connectDatabase()
    scrape_ps4_games()

if __name__ == '__main__':
    main()
