import mysql.connector
from utils import *

config = {
  'user': 'root',
  'password': '1',
  'host': '127.0.0.1',
  'database': 'discord'
}

add_player = ("INSERT IGNORE INTO players (name) VALUES (%s)")

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
data = openJSON('Data/players.json')
print(data['players'])
cursor.executemany(add_player, [tuple(s.split()) for s in data['players']])
print(cursor.rowcount)
cnx.commit()

cursor.close()
cnx.close()
