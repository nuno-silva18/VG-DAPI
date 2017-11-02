# VG-DAPI

## Requirements
- [Python](https://www.python.org/downloads/)

## Python and MySQL connection
- install wamp64
- in code:
```python
import pymysql
def connectDatabase():
    """Create database connection"""
    global db
    #user and password defined on wamp64 installation, go to localhost/phpmyadmin
    db = pymysql.connect(host='localhost', user='root', password='',    
                         db='vg_dapi', cursorclass=pymysql.cursors.DictCursor,charset='utf8')
```
- learn pymylsq - https://github.com/PyMySQL/PyMySQL
## Setup
To setup node server:
open terminal at the level of the server, same directory where 'server.js' is located and run following commands:
- npm install
- npm start
## How to run

