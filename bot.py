# bot.py
import os
import random
import discord
import requests
import urllib.request

from discord import Game
from discord.ext import commands
from dotenv import load_dotenv
from src.armoryParser import getCharInfos
from src.responseFormatting import formatCharInfosResponse, formatGuildInfosResponse
from src.guildSumParser import getGuildInfos

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$$')


@bot.command(name='charsum', help='Get summary of a character (Default server is Icecrown)')
async def charsum(ctx, charName=None, server='Icecrown'):
    if charName != None and server != None:
        msg = await ctx.send('Processing character **{}** from **{}**...'.format(charName, server))
        
        charName = charName.capitalize()
        server = server.capitalize()

        charUrl = 'http://armory.warmane.com/character/{}/{}/summary'.format(charName, server)
        charInfos = getCharInfos(charUrl)

        await msg.edit(content=formatCharInfosResponse(charInfos))
    else:
        await ctx.send("""
            You must give a character name and a server name \n *I.E: !charsum wardyx icecrown*
        """)


@bot.command(name='guildsum', help='Get summary of a guild (if the guild has spaces in name, please use "" around it (Default server is Icecrown)')
async def guildSum(ctx, guildName=None, server='Icecrown'):
    if guildName != None and server != None:
        msg = await ctx.send('Processing guild **{}** from **{}**...'.format(guildName, server))

        # Url for guilds are replacing spaces with +
        guildName = guildName.replace(' ', '+')
        guildUrl = 'http://armory.warmane.com/guild/{}/{}/boss-fights'.format(guildName, server)
        guildInfos = getGuildInfos(guildUrl)

        await msg.edit(content=formatGuildInfosResponse(guildInfos))
    else:
        await ctx.send("""
            You must give a guild name and a server name \n *I.E: !guildsum "Stack and Slack" icecrown*
        """)

@bot.event
async def on_ready():
    activity = discord.Game(name="Checking Chicks 0.1")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Logged in as " + bot.user.name)


bot.run(token)