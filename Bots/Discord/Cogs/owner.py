import discord
from discord.ext import commands
#import mysql.connector
from utils import *
from constants import *

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # @commands.is_owner()
    # async def add(self, ctx, player: str):
    #     root = await getXML('http://www.agecommunity.com/query/query.aspx', {'md': 'user', 'name': player})
    #     if root.text == 'Failed to find user':
    #         await ctx.send('Введите правльное имя!')
    #         return
    #     user = root.find('./user')
    #     name = user.find('./name').text
    #     cnx = mysql.connector.connect(**config)
    #     cursor = cnx.cursor()
    #     cursor.execute(add_player, (name, ))
    #     result = cursor.rowcount
    #     cnx.commit()

    #     cursor.close()
    #     cnx.close()
    #     if result == 0:
    #         await ctx.send('Этот игрок уже добавлен в список!')
    #     else:
    #         await ctx.send('**' + name + '** был добавлен в список.')

    # @commands.command()
    # @commands.is_owner()
    # async def rem(self, ctx, player: str):
    #     cnx = mysql.connector.connect(**config)
    #     cursor = cnx.cursor()
    #     cursor.execute(remove_player, (player, ))
    #     result = cursor.rowcount
    #     cnx.commit()
    #     cursor.close()
    #     cnx.close()
    #     if result == 0:
    #         await ctx.send('Этот игрок отсутствует в списке!')
    #     else:
    #         await ctx.send('**' + player + '** был удален из списка.')

    @commands.command()
    @commands.is_owner()
    async def notificate(self, ctx):
        await ctx.message.delete()
        guild = self.bot.get_guild(GUILD_ID)
        members = list(filter(lambda x: len(x.roles) == 1, guild.members))   
        if len(members) == 0:
            return
        else:
            notification = ', '.join(user.mention for user in members)
            await ctx.send(notification + ' Вам нужно установить роль в виде звания на ESO! Для этого __**измените свой никнейм в Дискорде**__ (правый клик по вашему имени в списке справа) на имя в ESO и __**наберите команду**__ `!update` в чат. Если у Вас нет акаунта на ESO или возникли сложности с добавлением роли, то напишите об этом в чат. Спасибо за внимание!')

    @commands.command()
    @commands.is_owner()
    async def clear(self, ctx, amount: int, user: discord.User = None):
        await ctx.message.delete()
        if user:
            await ctx.channel.purge(limit = amount, check = lambda m: m.author == user)
        else:
            await ctx.channel.purge(limit = amount)

def setup(bot):
    bot.add_cog(Owner(bot))
