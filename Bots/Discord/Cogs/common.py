import discord
from discord.utils import get
import asyncio
import aiohttp
import requests
import concurrent.futures
from discord.ext import commands
import xml.etree.ElementTree as ElementTree
from utils import *
from aoestat import *
from dateutil.parser import parse
import datetime
from constants import *

class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clan(self, ctx, name:str):
        root = await getXML('http://www.agecommunity.com/query/query.aspx', {'md': 'clan', 'name': name})
        if root.text == 'Failed to find clan':
            await ctx.send('Введите правльное имя!')
            return
        users = root.find('./users')
        futures=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            loop = asyncio.get_event_loop()
            for user in users:
                futures.append(loop.run_in_executor(
                        executor, 
                        requests.get, 
                        'http://www.agecommunity.com/query/query.aspx', {'md': 'user', 'name': user.find('n').text}
                    ))
            responses = await asyncio.gather(*futures)
            data = []
            for response in responses:
                r = ElementTree.fromstring(response.content)
                user = r.find('./user')
                name = user.find('./name').text
                status = user.find('./presence').text
                days = (datetime.datetime.now(datetime.timezone.utc)-parse(user.find('./lastLogin').text)).days
                prNilla = r.find('./ratings/s/skillLevel').text
                prTAD = r.find('./ratings/sy/skillLevel').text
                data.append({'name':name, 'status':status, 'days':days,'prNilla':prNilla,'prTAD':prTAD})

            data.sort(key=lambda x: x['status'], reverse=True)
            guild = self.bot.get_guild(GUILD_ID)
            nilla_emoji = get(guild.emojis, name='nilla')
            tad_emoji = get(guild.emojis, name='tad')
            em = discord.Embed(description='**Имя:** *' + root.find('./clan/name').text + '*\n' + '**Лидер:** *' + root.find('./clan/owner').text + '*', colour=0x000)
            em.set_author(name='Статистика клана ' + root.find('./clan/abbr').text,
                        icon_url='http://xakops.pythonanywhere.com/static/images/0.png')
            chunks = [data[i:i + 24] for i in range(0, len(data), 24)]
            
            for user in chunks[0]:
                info = ''
                if user['status'] == 'offline':
                    if user['days'] == 0:
                        info = '\n' + '*Был в сети* __*сегодня*__'
                    else:
                        info = '\n' + '*Был в сети* __*' + str(user['days']) + getends(user['days'], ' день', ' дня', ' дней') + ' назад*__'
                info += '\n' + str(nilla_emoji) + '  PR' + user['prNilla'] + '     ' + str(tad_emoji) + '  PR' + user['prTAD']
                em.add_field(name = str(get(guild.emojis, name=user['status'])) + '  ' + user['name'], value = info)
            await ctx.send(embed=em)
            if len(chunks) > 1:
                for chunk in chunks[1:]:
                    em = discord.Embed(colour=0x000)   
                    for user in chunk:
                        info = ''
                        if user['status'] == 'offline':
                            if user['days'] == 0:
                                info = '\n' + '*Был в сети* __*сегодня*__'
                            else:
                                info = '\n' + '*Был в сети* __*' + str(user['days']) + getends(user['days'], ' день', ' дня', ' дней') + ' назад*__'
                        info += '\n' + str(nilla_emoji) + '  PR' + user['prNilla'] + '     ' + str(tad_emoji) + '  PR' + user['prTAD']
                        em.add_field(name = str(get(guild.emojis, name=user['status'])) + '  ' + user['name'], value = info)
                    await ctx.send(embed=em)

    @commands.command()
    async def eso(self, ctx):
        try:
            _, _ = await asyncio.wait_for(asyncio.open_connection('connection.agecommunity.com', 2300), timeout=2)
            await ctx.send('ESO бодрствует и готов к победам!')
        except:
            await ctx.send('Шшшш, ESO сейчас спит! :sleeping:')


    @commands.command()
    async def pop(self, ctx):
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
        guild = self.bot.get_guild(GUILD_ID)
        nilla_emoji = get(guild.emojis, name='nilla')
        tad_emoji = get(guild.emojis, name='tad')
        em = discord.Embed(description=str(nilla_emoji) + ' **Ванилла:** ' + str(Nilla) + '\n' + str(tad_emoji) + ' **Династии:** ' + str(TAD), timestamp=datetime.datetime.utcnow(
        ), title='Количество игроков на ESO', url='http://agecommunity.com/_server_status_/', colour=0xFFFF66)
        em.set_footer(text="Обновлено")
        await ctx.send(embed=em)


    @commands.command()
    async def stat(self, ctx, ESO):
        root = await getXML('http://www.agecommunity.com/query/query.aspx', {'md': 'user', 'name': ESO})
        if root.text == 'Failed to find user':
            await ctx.send('Введите правльное имя!')
            return
        user = root.find('./user')
        name = user.find('./name').text
        status = user.find('./presence').text
        if status == 'offline':
            desc = '**Последняя активность:** *' + \
                parse(
                    user.find('./lastLogin').text).strftime("%A, %d %B %Y, %H:%M") + ' UTC*'
            color = 16711680
        else:
            desc = '**Сейчас в сети!**'
            color = 65280
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
        ), title=clanname + name, url="http://aoe3.jpcommunity.com/rating2/player?n=" + ESO, colour=color)
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
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Common(bot))
