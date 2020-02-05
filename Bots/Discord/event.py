
import asyncio
import concurrent.futures
import copy
import datetime
import hashlib
import heapq
import locale
import logging
import xml.etree.ElementTree as ElementTree
import mysql.connector
from bs4 import BeautifulSoup
import numpy
import requests
from dateutil.parser import parse

from aoestat import *
from constants import *
from utils import *



async def event_ladder():
    while True:
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()

            cursor.execute(select_member)
            members = [row[0] for row in cursor.fetchall()]

 
            scores = {}
            current_date = datetime.datetime.utcnow()
            responses = []
            futures = []
            ySP = "age3ySPOverall"
            nSP = "age3SPOverall"
            yTR = "age3yTROverall"
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                loop = asyncio.get_event_loop()
                for member in members:
                    futures.append(
                        loop.run_in_executor(
                            executor,
                            requests.get,
                            "http://aoe3.jpcommunity.com/rating2/player",
                            {
                                "n": member,
                                "t": ySP,
                                "v": 100,
                                "p1": "",
                                "p2": "",
                                "p3": "",
                                "p4": "",
                                "p5": "",
                                "p6": "",
                                "p7": "",
                                "mc": 0,
                                "oc": 0,
                                "map": "",
                                "lenf": "",
                                "lent": "",
                                "ft": 1,
                            },
                        )
                    )
                    futures.append(
                        loop.run_in_executor(
                            executor,
                            requests.get,
                            "http://aoe3.jpcommunity.com/rating2/player",
                            {
                                "n": member,
                                "t": nSP,
                                "v": 100,
                                "p1": "",
                                "p2": "",
                                "p3": "",
                                "p4": "",
                                "p5": "",
                                "p6": "",
                                "p7": "",
                                "mc": 0,
                                "oc": 0,
                                "map": "",
                                "lenf": "",
                                "lent": "",
                                "ft": 1,
                            },
                        )
                    )
                    futures.append(
                        loop.run_in_executor(
                            executor,
                            requests.get,
                            "http://aoe3.jpcommunity.com/rating2/player",
                            {
                                "n": member,
                                "t": yTR,
                                "v": 100,
                                "p1": "",
                                "p2": "",
                                "p3": "",
                                "p4": "",
                                "p5": "",
                                "p6": "",
                                "p7": "",
                                "mc": 0,
                                "oc": 0,
                                "map": "",
                                "lenf": "",
                                "lent": "",
                                "ft": 1,
                            },
                        )
                    )
                responses.extend(await asyncio.gather(*futures))

            for response in responses:
                if response.status_code != requests.codes.ok:
                    print('bad response')
                    continue
                soup = BeautifulSoup(response.content, "html.parser")
                GamesTable = soup.find("table", class_="alter-table", style=True)
                if GamesTable != None:
                    for Game in list(GamesTable)[1:]:
                        cells = Game.find_all("td")
                        # if it is not header
                        if len(cells) > 0:
                            # if it is this month and year
                            game_date = datetime.datetime.strptime(
                                cells[8].get_text(), "%Y/%m/%d %H:%M:%S"
                            )
                            if (
                                current_date.year == game_date.year
                                and current_date.month == game_date.month
                            ):
                                # if it is win
                                if cells[1].find(class_="myname"):
                                    # if it is not point trading
                                    if get_sec(cells[7].get_text()) >= 300:
                                        # checking for noob bashing
                                        current_elo = cells[2].find(class_="myname").get_text()
                                        player_name = cells[1].find(class_="myname").get_text()
                                        winner_elos = [
                                            int(x.get_text()) for x in cells[2].find_all("p")
                                        ]
                                        loser_elos = [
                                            int(x.get_text()) for x in cells[5].find_all("p")
                                        ]

                                        N = len(winner_elos) + len(loser_elos)
                                        deltaR = (
                                            6400 * N + 32 * (sum(loser_elos) - sum(winner_elos))
                                        ) / (400 * N - 64)

                                        ELO = int(current_elo) - max(min(deltaR, 31), 1)
                                        delta = 15
                                        if ELO >= 1200:
                                            delta = CalcDelta(ELO)
                                        # it is not noobbashing
                                        if deltaR >= delta:
                                            score = 0
                                            if N == 2:
                                                score = 8
                                            if N == 4:
                                                score = 7
                                            if N == 6:
                                                score = 6
                                            if N == 8:
                                                score = 5
                                            if yTR in response.url:
                                                score *= 2

                                            if player_name in scores:
                                                buf = scores[player_name]
                                            else:
                                                buf = {"yTR": 0, "ySP": 0, "nSP": 0, "sum": 0}
                                            if yTR in response.url:
                                                buf["yTR"] += score
                                            if ySP in response.url:
                                                buf["ySP"] += score
                                            if nSP in response.url:
                                                buf["nSP"] += score
                                            buf["sum"] += score 
                                            scores[player_name] = buf
                            # if it is not current month then skip all next games
                            else:
                                if cells[1].find(class_="myname"):
                                    player_name = cells[1].find(class_="myname").get_text()
                                else:
                                    player_name = cells[4].find(class_="myname").get_text()


                                if not player_name in scores:
                                    buf = {"yTR": 0, "ySP": 0, "nSP": 0, "sum": 0}                                
                                    scores[player_name] = buf
                                break
                else:
                    print('Bad response ' + response.url)
            cursor.execute(select_event)
            event_table = cursor.fetchall()
            need_to_remove = numpy.setdiff1d(numpy.array([row[0] for row in event_table]), numpy.array(members), assume_unique = True)
            cursor.executemany(remove_event, [tuple(s.split()) for s in need_to_remove])
            cnx.commit()
            cursor.executemany(add_event, [tuple([k, v['nSP'], v['ySP'], v['yTR'], v['sum']]) for k, v in scores.items()])
            cnx.commit()

            

        except Exception as e:
            logging.error('Ошибка: '+ str(e))
        finally:
            cursor.close()
            cnx.close()
        await asyncio.sleep(3600)

try:
    logging.basicConfig(format = u'[%(asctime)s] [LINE:%(lineno)d]# %(levelname)-8s %(message)s', level = logging.ERROR, filename = u'log_event.txt')
    loop = asyncio.get_event_loop()
    coro = event_ladder()
    loop.run_until_complete(coro)
except KeyboardInterrupt:
    pass