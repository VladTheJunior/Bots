
import aiohttp
import asyncio
import json
import logging
from datetime import timedelta, datetime

logging.basicConfig(format = u'[%(asctime)s] [LINE:%(lineno)d]# %(levelname)-8s %(message)s', level = logging.ERROR, filename = u'log.txt')
access_token = 'c2611eab77ee0536ec2f6efcbda25ec4ad97a4d9d82bb34aee30db78cbdb38b7e4850121d8feb77167b63'
v = '5.80'
KEYBOARD = {
    'one_time': False,
    'buttons': [
        [{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '1'}),
            'label': '!help',
        },
        'color': 'positive'
    },   
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '4'}),
            'label': '!today',
        },
        'color': 'primary'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '5'}),
            'label': '!tomorrow',
        },
        'color': 'primary'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '6'}),
            'label': '!week',
        },
        'color': 'primary'
    }]
    ,[   {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '4'}),
            'label': '!now',
        },
        'color': 'primary'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '5'}),
            'label': '!next',
        },
        'color': 'primary'
    }],[
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '6'}),
            'label': '!monday',
        },
        'color': 'default'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '6'}),
            'label': '!tuesday',
        },
        'color': 'default'
    }
        ,    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '6'}),
            'label': '!friday',
        },
        'color': 'default'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '6'}),
            'label': '!saturday',
        },
        'color': 'default'
    }]]
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

# Сохранение JSON в файл
def saveJSON(Path, data):
    with open(Path, 'w+', encoding = 'utf-8') as f:
        json.dump(data, f, ensure_ascii = False, sort_keys = True)

# Открытие JSON из файла
def openJSON(Path):
    with open(Path, encoding = 'utf-8') as data_file:
        return json.loads(data_file.read())


def info():
    message = 'Список команд\n'
    message += '!help'
    message += ' - Показать список команд\n'

    message += '!now'
    message += ' - Узнать текущую пару\n'

    message += '!next'
    message += ' - Узнать следующую пару\n'

    message += '!today'
    message += ' - Узнать расписание на сегодня\n'

    message += '!tomorrow'
    message += ' - Узнать расписание на завтра\n'

    message += '!week'
    message += ' - Узнать расписание на неделю\n'

    message += '!monday'
    message += ' - Узнать расписание на понедельник\n'

    message += '!tuesday'
    message += ' - Узнать расписание на вторник\n'

    message += '!friday'
    message += ' - Узнать расписание на пятницу\n'

    message += '!saturday'
    message += ' - Узнать расписание на субботу\n'
    return message
#HELP

# Текущий день
def CurDay():
    date = datetime.now()
    return date.isoweekday()

# Текущая неделя
def CurWeek():
    date = datetime.now()
    return date.isocalendar()[1]

# Замена чисел на юникод ВК
def ReplaceNum(s):
    s = s.replace("0", ".").replace("1", ",").replace("2", "*").replace("3", "/").replace("4", "-").replace("5", "+").replace("6", "[").replace("7", "]").replace("8", "{").replace("9", "}")
    return s.replace(".", "0&#8419;").replace(",", "1&#8419;").replace("*", "2&#8419;").replace("/", "3&#8419;").replace("-", "4&#8419;").replace("+", "5&#8419;").replace("[", "6&#8419;").replace("]", "7&#8419;").replace("{", "8&#8419;").replace("}", "9&#8419;")


def nw():
    message = ''
    if CurDay() > 6:
        message = "&#128519; Сегодня занятий нет!"
    else:
        data = openJSON('timetable.json')
        if CurWeek() % 2 != 0:
            week = data["oddWeek"]
        else:
            week = data["evenWeek"]
        if CurDay() == 1:
            day = week["monday"]
        if CurDay() == 2:
            day = week["tuesday"]
        if CurDay() == 3:
            day = week["wednesday"]
        if CurDay() == 4:
            day = week["thursday"]
        if CurDay() == 5:
            day = week["friday"]
        if CurDay() == 6:
            day = week["saturday"]
        if not day:
            return "&#128519; Сегодня занятий нет!"
        for pair in day:
            times = ReplaceNum(pair["time"])
            ptime = datetime.strptime(pair["time"], '%H:%M')
            now = datetime.now()
            etime = ptime
            etime += timedelta(minutes = 95)
            t1 = timedelta(hours = now.hour, minutes = now.minute)
            t2 = timedelta(hours = etime.hour, minutes = etime.minute)
            hours = (t2 - t1).seconds // 3600
            minutes = (t2 - t1).seconds % 3600 // 60

            if ptime.time() < now.time() and now.time() < etime.time():
                message += times + '\n&#128218; "' + pair["title"] + '"\n&#128270; В аудитории ' + str(pair["classRoom"]) + "\n"
                message += "&#128591; До конца пары : " + str(hours) + getends(hours, ' час ', ' часа ',' часов ')  + str(minutes) + getends(minutes, ' минута', ' минуты',' минут') + "\n"
    if message == '':
        message = '&#127939; Пара еще не началась или уже закончилась!'
    return message

def nxt():
    message = ''
    if CurDay() > 6:
        message = "&#128519; Сегодня занятий нет!"
    else:
        data = openJSON('timetable.json')
        if CurWeek() % 2 != 0:
            week = data["oddWeek"]
        else:
            week = data["evenWeek"]
        if CurDay() == 1:
            day = week["monday"]
        if CurDay() == 2:
            day = week["tuesday"]
        if CurDay() == 3:
            day = week["wednesday"]
        if CurDay() == 4:
            day = week["thursday"]
        if CurDay() == 5:
            day = week["friday"]
        if CurDay() == 6:
            day = week["saturday"]
        if not day:
            return "&#128519; Сегодня занятий нет!"
        for pair in day:
            times = ReplaceNum(pair["time"])
            ptime = datetime.strptime(pair["time"], '%H:%M')
            now = datetime.now()
            t1 = timedelta(hours = now.hour, minutes = now.minute)
            t2 = timedelta(hours = ptime.hour, minutes = ptime.minute)
            hours = (t2 - t1).seconds // 3600
            minutes = (t2 - t1).seconds % 3600 // 60

            if ptime.time() > now.time():
                message += times + '\n&#128218; "' + pair["title"] + '"\n&#128270; В аудитории ' + str(pair["classRoom"]) + "\n"
                message += "&#9200; До начала пары : " + str(hours) + getends(hours, ' час ', ' часа ',' часов ')  + str(minutes) + getends(minutes, ' минута', ' минуты',' минут') + "\n"
                break
    if message == '':
        message = '&#127939; На сегодня пары уже закончились!'
    return message

def tmr():
    message = ''
    if CurDay() == 6 or CurDay() == 2 or CurDay() == 3:
        message = "&#128519; Завтра занятий нет!"
    else:
        message = day('завтра')
    return message

def td():
    message = ''
    if CurDay() == 6 or CurDay() == 2 or CurDay() == 3:
        message = "&#128519; Сегодня занятий нет!"
    else:
        message = day(str(CurDay()))
    return message

def day(body):
    message = ''
    data = openJSON('timetable.json')
    if body == 'завтра':
        if CurDay() != 7:
            if CurWeek() % 2 != 0:
                week = data["oddWeek"]
            else:
                week = data["evenWeek"]
        else:
            if (CurWeek() + 1) % 2 != 0:
                week = data["oddWeek"]
            else:
                week = data["evenWeek"]
        if CurDay() == 1:
            day = week["tuesday"]
            message += "\nВТОРНИК\n"
        if CurDay() == 2:
            day = week["wednesday"]
            message += "\nСРЕДА\n"
        if CurDay() == 3:
            day = week["thursday"]
            message += "\nЧЕТВЕРГ\n"
        if CurDay() == 4:
            day = week["friday"]
            message += "\nПЯТНИЦА\n"
        if CurDay() == 5:
            day = week["saturday"]
            message += "\nСУББОТА\n"
        if CurDay() == 7:
            day = week["monday"]
            message += "\nПОНЕДЕЛЬНИК\n"
    else:
        if CurWeek() % 2 != 0:
            week = data["oddWeek"]
        else:
            week = data["evenWeek"]
        if body == "понедельник" or body == "1":
            day = week["monday"]
            message += "\nПОНЕДЕЛЬНИК\n"
        if body == "вторник" or body == "2":
            day = week["tuesday"]
            message += "\nВТОРНИК\n"
        if body == "среда" or body == "3":
            day = week["wednesday"]
            message += "\nСРЕДА\n"
        if body == "четверг" or body == "4":
            day = week["thursday"]
            message += "\nЧЕТВЕРГ\n"
        if body == "пятница" or body == "5":
            day = week["friday"]
            message += "\nПЯТНИЦА\n"
        if body == "суббота" or body == "6":
            day = week["saturday"]
            message += "\nСУББОТА\n"
    for pair in day:
        time = ReplaceNum(pair["time"])
        message += time + '\n&#128218; "' + pair["title"] + '"\n&#128270; В аудитории ' + str(pair["classRoom"]) + "\n"
    return message

def wk():
    message = ''
    message += day("1")
    message += day("2")
    message += day("5")
    message += day("6")
    return message

async def main():
    #try:
    longPoll = await getJSON('https://api.vk.com/method/groups.getLongPollServer', {'group_id': 169726049, 'access_token': access_token, 'v': v})
    server, key, ts = longPoll['response']['server'], longPoll['response']['key'], longPoll['response']['ts']
    while True:
        longPoll = await postJSON(server, {'act': 'a_check', 'key': key, 'ts': ts, 'wait': 25})
        if 'updates' in longPoll:
            if len(longPoll['updates']) > 0:
                for update in longPoll['updates']:
                    if update['type'] == 'message_new':
                        if update['object']['text'] == '!today':
                            msg = td()
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!now':
                            msg = nw()
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!tomorrow':
                            msg = tmr()
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!week':
                            msg = wk()
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!next':
                            msg = nxt()
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!monday':
                            msg = day("понедельник")
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!tuesday':
                            msg = day("вторник")
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!wednesday':
                            msg = day("среда")
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!thursday':
                            msg = day("четверг")
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!friday':
                            msg = day('пятница')
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!saturday':
                            msg = day("суббота")
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
                        elif update['object']['text'] == '!help':
                            msg = info()
                            message = await postDataJSON('https://api.vk.com/method/messages.send', {'peer_id': update['object']['peer_id'], 'message': msg, 'keyboard': str(json.dumps(KEYBOARD, ensure_ascii = False)), 'access_token': access_token, 'v': v})
        ts = longPoll['ts']
    #except Exception as e:
    #    logging.error('Ошибка: '+ str(e))
		
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

loop.run_until_complete(asyncio.sleep(0))
loop.close()
