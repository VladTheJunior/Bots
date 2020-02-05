import aiohttp
import asyncio
import json
import xml.etree.ElementTree as ElementTree
from dateutil.parser import parse
from dateutil import tz
import logging

def getends(n, s1, s2, s3):
    num = n % 100
    num1 = n % 10
    if num1 == 1 and num != 11:
        return s1
    if (num1 == 2 and num != 12) or (num1 == 3 and num != 13) or (num1 == 4 and num != 14):
        return s2
    return s3

logging.basicConfig(format = u'[%(asctime)s] [LINE:%(lineno)d]# %(levelname)-8s %(message)s', level = logging.ERROR, filename = u'log.txt')
access_token = 'ced883c1f82e44fce3c55c2862735b7ebd432689bf80aa5df7027cd68bae21b8998b7117707039e4e9db9'
v = '5.80'
KEYBOARD = {
    'one_time': False,
    'buttons': [[{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '5'}),
            'label': '!help',
        },
        'color': 'positive'
    }],
    [{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '1'}),
            'label': '!streams',
        },
        'color': 'primary'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '2'}),
            'label': '!eso',
        },
        'color': 'primary'
    }],[
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '3'}),
            'label': '!gay',
        },
        'color': 'negative'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '4'}),
            'label': '!bitch',
        },
        'color': 'negative'
    }
    
    ]]
}

async def getJSON(URL, params):    
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params = params, timeout = 5) as resp:
            return await resp.json()

async def postJSON(URL, params):    
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, params = params) as resp:
            return await resp.json()

async def postDataJSON(URL, data):    
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data = data, timeout = 5) as resp:
            return await resp.json()

async def ESO():
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection('connection.agecommunity.com', 2300), timeout = 2)
        return 'ESO бодрствует и готов к победам! &#9786;'
    except:
        return 'Шшшш, ESO сейчас спит! &#128564;'

async def getXML(URL, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params = params, timeout = 5) as resp:
            return ElementTree.fromstring(await resp.text())

def LocalDate(date):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Moscow')
    return date.replace(tzinfo = from_zone).astimezone(to_zone)

def FormatPR(Rating):
    if (Rating < 3):
        return 'Новобранец (Уровень ' + str(Rating) + ')'
    if (Rating > 2 and Rating < 8):
        return 'Рядовой (Уровень ' + str(Rating) + ')'
    if (Rating > 7 and Rating < 11):
        return 'Младший капрал (Уровень ' + str(Rating) + ')'
    if (Rating > 10 and Rating < 14):
        return 'Капрал (Уровень ' + str(Rating) + ')'
    if (Rating > 13 and Rating < 17):
        return 'Сержант (Уровень ' + str(Rating) + ')'
    if (Rating > 16 and Rating < 20):
        return 'Старший сержант (Уровень ' + str(Rating) + ')'
    if (Rating > 19 and Rating < 23):
        return 'Младший лейтенант (Уровень ' + str(Rating) + ')'
    if (Rating > 22 and Rating < 26):
        return 'Старший лейтенант (Уровень ' + str(Rating) + ')'
    if (Rating > 25 and Rating < 29):
        return 'Капитан (Уровень ' + str(Rating) + ')'
    if (Rating > 28 and Rating < 32):
        return 'Майор (Уровень ' + str(Rating) + ')'
    if (Rating > 31 and Rating < 35):
        return 'Подполковник (Уровень ' + str(Rating) + ')'
    if (Rating > 34 and Rating < 38):
        return 'Полковник (Уровень ' + str(Rating) + ')'
    if (Rating > 37 and Rating < 41):
        return 'Бригадный генерал (Уровень ' + str(Rating) + ')'
    if (Rating > 40 and Rating < 44):
        return 'Генерал-майор (Уровень ' + str(Rating) + ')'
    if (Rating > 43 and Rating < 47):
        return 'Генерал-лейтенант (Уровень ' + str(Rating) + ')'
    if (Rating > 46 and Rating < 50):
        return 'Генерал (Уровень ' + str(Rating) + ')'
    if (Rating > 49):
        return 'Фельдмаршал (Уровень ' + str(Rating) + ')'
    return str(Rating);


async def statESO(ESO):
    message = ''
    try:       
        root = await getXML('http://www.agecommunity.com/query/query.aspx', {'md': 'user', 'name': ESO})
        user = root.find('./user')
        name = user.find('./name').text
        status = user.find('./presence').text
        status = 'В сети: ' + status.replace('offline', '&#9940;').replace('online', '&#10004;')
        login = 'Последняя активность (МСК): ' + LocalDate(parse(user.find('./lastLogin').text)).strftime('%d.%m.%Y %H:%M:%S')
        try:
            clanname = user.find('./clanName').text
            clanname = 'Клан: ' + user.find('./clanAbbr').text + ' - ' + clanname
        except:
            clanname = ''
        nillaSP = 'Нилла (раш): ' + FormatPR(int(root.find('./ratings/s/skillLevel').text))
        tadSP = 'TAD (раш): ' + FormatPR(int(root.find('./ratings/sy/skillLevel').text))
        tadTR = 'TAD (перемирие): ' + FormatPR(int(root.find('./ratings/ty/skillLevel').text))
        message = name + '\n' + status + '\n' + login + '\n'
        if clanname != '':
            message += clanname + '\n'
        message += nillaSP + '\n' + tadSP + '\n' + tadTR
    except:
        message = '&#8252; Ошибка получения статистики!'
    return message

async def streams():
    try:
        s = []
        J = await getJSON('https://api.twitch.tv/kraken/streams/', {'game': 'Age of Empires III: The Asian Dynasties', 'live':'', 'client_id': '9rrpybi820nvoixrr2lkqk19ae8k4ef'})
        for streamer in J["streams"]:
            s.append(streamer['channel']['display_name'] + ' - ' + str(streamer['viewers']) + getends(streamer['viewers'], ' зритель', ' зрителя', ' зрителей') + '\n' + streamer['channel']['url'])
        if len(s) > 0:
            s.insert(0, '&#9889; Twitch стримы: ')    
        return '\n'.join(s)
    except:
        return '&#8252; Ошибка получения стримов!'


async def main():
    try:
        longPoll = await getJSON('https://api.vk.com/method/groups.getLongPollServer', {'group_id': 4243069, 'access_token': access_token, 'v': v})
        server, key, ts = longPoll['response']['server'], longPoll['response']['key'], longPoll['response']['ts']
        while True:
            longPoll = await postJSON(server, {'act': 'a_check', 'key': key, 'ts': ts, 'wait': 25})
            if 'updates' in longPoll:
                if len(longPoll['updates']) > 0:
                    for update in longPoll['updates']:
                        if update['type'] == 'message_new':
                            if update['object']['text'] == '!eso':
                                msg = await ESO()
                                message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                            if update['object']['text'] == '!streams':
                                msg = await streams()
                                message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                            elif update['object']['text'] == '!bitch':
                                msg = 'Сцука! &#128520;'
                                message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                            elif update['object']['text'] == '!gay':
                                msg = 'Гейство! &#128545;'
                                message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                            elif update['object']['text'] == '!help':
                                msg = '&#9888; Список команд:\n'
                                msg += '!help'
                                msg += ' - Показать команды\n'

                                msg += '!streams'
                                msg += ' - Активные стримы по AoE3\n'
                                msg += '!eso'
                                msg += ' - Проверить ESO\n'

                                msg += '!stat имя'
                                msg += ' - Проверить статситику игрока ESO\n'

                                msg += '&#128286; Особые:\n'
                                msg += '!gay\n'
                                msg += '!bitch\n'
                                message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})

                            elif len(update['object']['text'].split()) == 2:
                                if update['object']['text'].split()[0] == '!stat':
                                    msg = await statESO(update['object']['text'].split()[1])
                                    message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                                                
                                
            ts = longPoll['ts'] 
    except Exception as e:
        logging.error('Ошибка: '+ str(e))
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

loop.run_until_complete(asyncio.sleep(0))
loop.close()
