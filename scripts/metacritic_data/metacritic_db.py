# import libraries
import pymysql
import csv

def connectDatabase():
    """Create database connection"""
    global db
    db = pymysql.connect(host='localhost', user='root', password='', db='vg_dapi', cursorclass=pymysql.cursors.DictCursor,charset='utf8')

def metac_scrap():
    nfiles_csv = ['ps4_games.csv', 'xboxone_games.csv', 'switch_games.csv']
    for nfile in nfiles_csv:
        with open(nfile, newline='', encoding="utf8") as f:
            reader = csv.reader(f)
            cur = db.cursor()
            for row in reader:
                if row != []:
                    if row[13] == 'NA':
                        row[13] = 0
                    else:
                        pass
                    vg_descrip_list = [row[1], row[11]]
                    vg_descrip_sql = "UPDATE `game` SET `description`=%s WHERE `name`=%s"
                    cur.execute(vg_descrip_sql, vg_descrip_list)
                    db.commit()
                    vg_metac_list = [row[7], row[13], row[0], row[11]]
                    vg_metac_sql = "UPDATE `gameplatform` SET `metacritic`=%s, `metacritic_user` = %s, `metacritic_number_reviews` = %s WHERE (SELECT `id` FROM `game` WHERE `name` = %s) = `gameID`"
                    cur.execute(vg_metac_sql, vg_metac_list)
                    db.commit()
                    print("Added description and Metacritic score and user score to " + row[11])

    return

# call the module directly for testing
if __name__ == "__main__":
    connectDatabase()
    metac_scrap()
