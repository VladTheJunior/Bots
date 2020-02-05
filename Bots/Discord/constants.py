GUILD_ID = 538569074016256012
TOKEN = 'NTMyNDUxNzM0ODcwODE4ODI3.Dy75pA.pqD49SxUudjjstfNsyIIcZI0GSQ'
TOKEN_EVENT = 'NTQ0MDA4MzE2NDE0NTkwOTk2.D3T-Qg.8p6MtSqf-0hqA57R0RKIoZsIXl8'
BOT_PREFIX = '!'
#LOBBIES_CHANNEL_ID = 532196097607598082
STREAMS_CHANNEL_ID = 538577668380033025
NEWS_CHANNEL_ID = 538577422044626954
JOINED_ID = 538587298434908171
RULES_ID = 538577291622613003
POP_CHANNEL_ID = 541079949763936256
RUSSIANS_CHANNEL_ID = 544737388027576320
EVENT_LADDER_ID = 557912707077242931
v = '5.92'
ACCESS_TOKEN = 'ec3fd9058644a6044380c72b6745a5cf867d76a800496bebfe0b93833d628179a7ad057479fda1daf88ed'


TOP_NILLA = 548370037593866240
TOP_TAD_RUSH = 548370207622561793
TOP_TAD_TREATY = 548370446207156225

config = {
  'user': 'root',
  'password': '1',
  'host': '127.0.0.1',
  'database': 'discord'
}

add_player = ("INSERT IGNORE INTO players (name) VALUES (%s)")
remove_player = ("DELETE from players where lower(name) = lower(%s)")
select_player = ("select * from players order by name")

add_pop = ("INSERT INTO population (tad, nilla, time) VALUES (%s, %s, %s)")
select_pop = ("SELECT * from population WHERE  time >= UTC_TIMESTAMP() - INTERVAL 24 HOUR")

add_stream = ("INSERT INTO streams (name, id) VALUES (%s, %s) on duplicate key update id=values(id)")
select_stream = ("select * from streams")
delete_stream = ("delete from streams where name=%s")

select_member = ("select * from members")
add_member = ("insert ignore into members (name) values (%s)")
remove_member = ("delete from members where name=%s")

select_event = ("select * from event")
add_event = ("insert into event (name, nSP, tSP, tTR, sum) values (%s, %s, %s, %s, %s) on duplicate key update nSP=values(nSP), tSP=values(tSP), tTR=values(tTR), sum=values(sum)")
remove_event = ("delete from event where name=%s")

