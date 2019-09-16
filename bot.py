#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import discord
import requests
import urllib.request
import asyncio

from discord import Game
from discord.ext import commands
from dotenv import load_dotenv
from src.charsumParser import getCharInfos
from src.charsumFullParser import getFullCharInfos
from src.responseFormatting import formatCharInfosResponse, formatGuildInfosResponse, formatFullCharInfosResponse
from src.guildSumParser import getGuildInfos

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$$')


@bot.command(name='charsum', help='Get a summary of a character (Default server is Icecrown)')
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


@bot.command(name='charsumfull', help='Get a detailled summary of a character (Default server is Icecrown)')
async def charsumfull(ctx, charName=None, server='Icecrown'):
    if charName != None and server != None:
        msg = await ctx.send('Processing character **{}** from **{}**...'.format(charName, server))
        
        charName = charName.capitalize()
        server = server.capitalize()

        charUrl = 'http://armory.warmane.com/character/{}/{}/summary'.format(charName, server)
        charInfos = getFullCharInfos(charUrl)

        await msg.edit(content=formatFullCharInfosResponse(charInfos))
    else:
        await ctx.send("""
            You must give a character name and a server name \n *I.E: !charsumfull wardyx icecrown*
        """)


@bot.command(name='guildsum', help='Get a summary of a guild (if the guild has spaces in name, please use "" around it (Default server is Icecrown)')
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
    print("Logged in as " + bot.user.name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No such command... :thinking:")
    else:
        raise error


def getGuildsAndUsers():
    guilds = bot.guilds
    guildsNumber = len(bot.guilds)

    usersNumber = 0
    for guild in guilds:
        usersNumber += len(guild.members)

    return {'guildsNumber': guildsNumber, 'usersNumber': usersNumber}


async def changeGameMessage():
    await bot.wait_until_ready()
    
    counter = 0

    botInfos = getGuildsAndUsers()
    
    guildsNumber = 'used by {} guilds and {} users!'.format(botInfos['guildsNumber'], botInfos['usersNumber'])

    funMessage = discord.Game(name="Checking Chicks V0.2")
    helpMessage = '$$help'
    messagesList = [funMessage, guildsNumber, helpMessage]

    # Used to change bot message every X seconds
    while not bot.is_closed():
        if counter < len(messagesList):
            counter += 1
        if counter == len(messagesList):
            counter = 0
        
        activity = discord.Game(name=messagesList[counter])
        await bot.change_presence(activity = activity)

        await asyncio.sleep(30)


bot.loop.create_task(changeGameMessage())
bot.run(token)