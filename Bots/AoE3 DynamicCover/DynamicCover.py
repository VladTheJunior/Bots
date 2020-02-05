from PIL import Image, ImageDraw, ImageFont
import aiohttp
import json
from heapq import nlargest
import asyncio
import logging
import datetime
from datetime import date
import io

def getends(n, s1, s2, s3):
    num = n % 100
    num1 = n % 10
    if num1 == 1 and num != 11:
        return s1
    if (num1 == 2 and num != 12) or (num1 == 3 and num != 13) or (num1 == 4 and num != 14):
        return s2
    return s3

async def getJSON(URL, params):    
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params = params, timeout = 5) as resp:
            return await resp.json()
            
async def getFile(URL):    
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, timeout = 5) as resp:
            return await resp.read()

async def postJSON(URL, data):    
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, data = data) as resp:
            return await resp.json()

def saveJSON(Path, data):
    with open(Path, 'w+', encoding = 'utf-8') as f:
        json.dump(data, f, ensure_ascii = False, sort_keys = True)

def find_between(first, last, s):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
        
async def Task():
    while True:
        try:
            logging.info(u'Открываем обложку') 
            image = Image.open('Cover.png')
            draw = ImageDraw.Draw(image)

            font = ImageFont.truetype("cambria.ttc", 34)
            color = 'rgb(255, 255, 255)'

            ESO = 0
            Nilla = 0
            TAD = 0
            logging.info(u'Получаем ESO популяцию')
            async with aiohttp.ClientSession() as session:
                async with session.get('http://www.agecommunity.com/_server_status_/', timeout = 10) as response:
                    data = await response.text()
                    TADPopulation = find_between("Users Online : The Asian Dynasties</td><td>", "</td>", data);
                    NillaPopulation = find_between("Users Online : Age3</td><td>", "</td>", data);
                    TWCPopulation = find_between("Users Online : War Chiefs</td><td>", "</td>", data);
                    ESO = int(TADPopulation) + int(NillaPopulation) + int(TWCPopulation)
                    TAD = int(TADPopulation)
                    Nilla = int(NillaPopulation)

            draw.text((50, 30), "Игроков на ESO", fill = color, font = font) 
            draw.text((50, 73), "Всего: ", fill = color, font = font)
            draw.text((50, 110), 'Ванилла:', fill = color, font = font)
            draw.text((50, 147), 'Династии:', fill = color, font = font)

            size = draw.textsize("Игроков на ESO", font = font)
            offset = font.getoffset("Игроков на ESO")
            draw.text((50 + size[0] + offset[0] - draw.textsize(str(ESO), font = font)[0], 73), str(ESO), fill = color, font = font)
            draw.text((50 + size[0] + offset[0] - draw.textsize(str(Nilla), font = font)[0], 110), str(Nilla), fill = color, font = font)
            draw.text((50 + size[0] + offset[0] - draw.textsize(str(TAD), font = font)[0], 147), str(TAD), fill = color, font = font)

            
            #Распродажа 31.10.18
            
            
            logging.info(u'Получаем последние посты, лайки и комменты')
            Posts = await getJSON('https://api.vk.com/method/wall.get', {'owner_id': -4243069, 'count': 10, 'access_token': '16b6d11c16b6d11c16b6d11c4516d43e1b116b616b6d11c4c497b50ef2cbd344defb07e', 'v': '5.80'})
            top = {}
            for post in Posts["response"]["items"]:
                Comments = await getJSON('https://api.vk.com/method/wall.getComments', {'owner_id': -4243069, 'post_id': post['id'], 'access_token': '16b6d11c16b6d11c16b6d11c4516d43e1b116b616b6d11c4c497b50ef2cbd344defb07e', 'v': '5.80'})
                Likes = await getJSON('https://api.vk.com/method/likes.getList', {'type': 'post', 'filter': 'likes', 'owner_id': -4243069, 'item_id': post['id'], 'access_token': '16b6d11c16b6d11c16b6d11c4516d43e1b116b616b6d11c4c497b50ef2cbd344defb07e', 'v': '5.80'}) 
                for comment in Comments["response"]["items"]:
                    if not comment['from_id'] in top:
                        top[comment['from_id']] = 2
                    else:
                        top[comment['from_id']] += 2
                for like in Likes["response"]["items"]:
                    if not like in top:
                        top[like] = 1
                    else:
                        top[like] += 1
            logging.info(u'Получаем ТОП 3 пользователей')
            topThree = nlargest(3, top, key = top.get)
            s = ','.join(map(str, topThree))
            topUsers = await getJSON('https://api.vk.com/method/users.get', {'lang': 'ru', 'user_ids': s, 'fields': 'photo_50', 'access_token':'16b6d11c16b6d11c16b6d11c4516d43e1b116b616b6d11c4c497b50ef2cbd344defb07e', 'v': '5.80'})    
            i1 = await getFile(topUsers['response'][0]['photo_50'])
            
            im = Image.open(io.BytesIO(i1))
            bigsize = (im.size[0] * 3, im.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draws = ImageDraw.Draw(mask) 
            draws.ellipse((0, 0) + bigsize, fill = 255)
            mask = mask.resize(im.size, Image.ANTIALIAS)
            im.putalpha(mask)

            image.paste(im, (1140, 75), im)
            i2 = await getFile(topUsers['response'][1]['photo_50'])
            im = Image.open(io.BytesIO(i2))
            im.putalpha(mask)
            image.paste(im, (1140, 130), im)
            i3 = await getFile(topUsers['response'][2]['photo_50'])
            im = Image.open(io.BytesIO(i3))
            im.putalpha(mask)
            image.paste(im, (1140, 185), im)
            draw.text((1140, 30), "Топ активных участников", fill = color, font = font) 
            draw.text((1205, 80), topUsers['response'][0]['first_name'] + ' ' + topUsers['response'][0]['last_name'], fill = color, font = font)
            draw.text((1205, 136), topUsers['response'][1]['first_name'] + ' ' + topUsers['response'][1]['last_name'], fill = color, font = font)
            draw.text((1205, 190), topUsers['response'][2]['first_name'] + ' ' + topUsers['response'][2]['last_name'], fill = color, font = font)

            #font1 = ImageFont.truetype("cambria.ttc", 34)
            #font2 = ImageFont.truetype("cambria.ttc", 37)
            #font3 = ImageFont.truetype("cambria.ttc", 70)
            #size1 = draw.textsize("Распродажа в Steam через", font = font1)
            #offset1 = font1.getoffset("Распродажа в Steam через")
            #draw.text((1140, 260), "Распродажа в Steam через", fill = color, font = font1)
            #draw.text((1140 + (size1[0] + offset1[0] - draw.textsize("30 октября 2018", font = font2)[0]) // 2 , 286), "30 октября 2018", fill = color, font = font2)
            #days_between = (date(2018, 11, 21) - datetime.datetime.utcnow().date()).days
            #draw.text((1140 + (size1[0] + offset1[0] - draw.textsize(str(days_between) + getends(days_between, ' день', ' дня', ' дней'), font = font3)[0]) // 2 , 294), str(days_between) + getends(days_between, ' день', ' дня', ' дней'), fill = color, font = font3)

            logging.info(u'Сохраняем обложку') 
            image.save('DynamicCover.jpg', subsampling = 0, quality = 100)
            logging.info(u'Получаем адрес для загрузки обложки') 
            cover = await getJSON('https://api.vk.com/method/photos.getOwnerCoverPhotoUploadServer', {'group_id': 4243069, 'crop_x': 0, 'crop_y': 0, 'crop_x2': 1590, 'crop_y2': 400, 'access_token': '8fe022994546e98ba2ce5a579953850d69a5496145e5be48ee81361a1fed1760a84193cf8745200817ee3', 'v': '5.80'})
            with open('DynamicCover.jpg', 'rb') as f:
                logging.info(u'Загружаем обложку') 
                r = await postJSON(cover['response']['upload_url'], {'photo': f})
                logging.info(u'Обновляем обложку')
                result = await getJSON('https://api.vk.com/method/photos.saveOwnerCoverPhoto', {'hash': r['hash'], 'photo': r['photo'], 'access_token': '8fe022994546e98ba2ce5a579953850d69a5496145e5be48ee81361a1fed1760a84193cf8745200817ee3', 'v': '5.80'})
        except Exception as e:
            logging.error('Ошибка: '+ str(e))
        await asyncio.sleep(300)

try:
    logging.basicConfig(format = u'[%(asctime)s] [LINE:%(lineno)d]# %(levelname)-8s %(message)s', level = logging.ERROR, filename = u'log.txt')
    loop = asyncio.get_event_loop()
    coro = Task()
    loop.run_until_complete(coro)
except KeyboardInterrupt:
    pass
