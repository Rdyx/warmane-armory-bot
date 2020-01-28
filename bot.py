""" Bot Core """

import os
import random
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv
from src.charsumParser import getCharInfos
from src.charsumFullParser import getFullCharInfos
from src.responseFormatting import (
    formatCharInfosResponse,
    formatGuildInfosResponse,
    formatFullCharInfosResponse,
)
from src.guildSumParser import getGuildInfos
from src.messageCmds import aboutMessage, welcomeMessage
from src.utils import incrementCommandsCounter, getCommandCounter

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_DEV_TOKEN')
BOT = commands.Bot(command_prefix='$')


@BOT.command(name='charsum', help='Get a summary of a character (Default server is Icecrown)')
async def charsum(ctx, charName=None, server='Icecrown'):
    """ Character Summary """
    if charName is not None and server is not None:
        msg = await ctx.send('Processing character **{}** from **{}**...'.format(charName, server))

        charName = charName.capitalize()
        server = server.capitalize()

        charUrl = 'http://armory.warmane.com/character/{}/{}/summary'.format(charName, server)
        charInfos = getCharInfos(charUrl)
        incrementCommandsCounter()

        await msg.edit(content=formatCharInfosResponse(charInfos))
    else:
        await ctx.send("""
            You must give a character name and a server name \n *I.E: !charsum wardyx icecrown*
        """)


@BOT.command(
    name='charsumfull',
    help='Get a detailled summary of a character (Default server is Icecrown)'
)
async def charsumfull(ctx, charName=None, server='Icecrown'):
    """ More detailled character summary """
    if charName is not None and server is not None:
        msg = await ctx.send('Processing character **{}** from **{}**...'.format(charName, server))

        charName = charName.capitalize()
        server = server.capitalize()

        charUrl = 'http://armory.warmane.com/character/{}/{}/summary'.format(
            charName, server)
        charInfos = getFullCharInfos(charUrl)
        incrementCommandsCounter()

        await msg.edit(content=formatFullCharInfosResponse(charInfos))
    else:
        await ctx.send("""
            You must give a character name and a server name \n *I.E: !charsumfull wardyx icecrown*
        """)


@BOT.command(
    name='guildsum',
    help='Get a summary of a guild (if the guild has spaces in name, please use "" around it \
        (Default server is Icecrown)'
)
async def guildSum(ctx, guildName=None, server='Icecrown'):
    """ Guild summary """
    if guildName is not None and server is not None:
        msg = await ctx.send('Processing guild **{}** from **{}**...'.format(guildName, server))

        # Url for guilds are replacing spaces with +
        guildName = guildName.replace(' ', '+')
        guildUrl = 'http://armory.warmane.com/guild/{}/{}/boss-fights'.format(
            guildName, server)
        guildInfos = getGuildInfos(guildUrl)
        incrementCommandsCounter()

        await msg.edit(content=formatGuildInfosResponse(guildInfos))
    else:
        await ctx.send("""
            You must give a guild name and a server name \n *I.E: !guildsum "Stack and Slack" icecrown*
        """)


@BOT.command(name='about', help='More info about this bot')
async def about(ctx):
    """ About this bot message """
    incrementCommandsCounter()
    await ctx.send(aboutMessage(ctx.author.name))


@BOT.command(name='tip', help='Wanna buy me a coin? :D')
async def tip(ctx):
    """ Creator's Tip bot message """
    paypalUrl = 'https://www.paypal.me/rdyx'
    message = 'If you enjoy this bot and want to reward me, feel free to go to **{}** :)'.format(
        paypalUrl)
    incrementCommandsCounter()
    await ctx.send(message)


@BOT.command(name='bischecker', help='BiS lists for every class with quick search')
async def bischecker(ctx):
    """ URL link to BiS class checker """
    bisCheckerUrl = 'https://rdyx.github.io/warmane-bis-class-checker/'
    message = 'Please follow this link: {} :)'.format(bisCheckerUrl)
    incrementCommandsCounter()
    await ctx.send(message)


@BOT.command(name='rand', help='Rand between a defined interval (default 1-100)')
async def rand(ctx, minNumber=1, maxNumber=100):
    """ Random number generator """
    randomNumber = random.randint(minNumber, maxNumber)
    message = '{} rolls **{}** ({}-{})'.format(
        ctx.author.name, randomNumber, minNumber, maxNumber,
    )
    incrementCommandsCounter()
    await ctx.send(message)


@BOT.event
# pylint: disable=invalid-name, missing-function-docstring
async def on_ready():
    print("Logged in as " + BOT.user.name)


@BOT.event
# pylint: disable=invalid-name, missing-function-docstring
async def on_guild_join(guild):
    message = welcomeMessage(len(BOT.guilds), guild.owner)
    await guild.owner.send(message)


@BOT.event
# pylint: disable=invalid-name, missing-function-docstring
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No such command... :thinking:")
    else:
        raise error


def getGuildsAndUsers():
    """ Get number of guilds and users using this bot """
    guilds = BOT.guilds
    guildsNumber = len(BOT.guilds)

    usersNumber = 0
    for guild in guilds:
        usersNumber += len(guild.members)

    return 'used by {} guilds and {} users!'.format(guildsNumber, usersNumber)


def getCommandCounterMessage():
    """ Get command counter tracker """
    commandCounter = getCommandCounter()

    return '{} commands used!'.format(commandCounter)


async def changeGameMessage():
    """ Game message rotation (displayed under bot name) """
    await BOT.wait_until_ready()

    counter = 0
    botInfos = getGuildsAndUsers()
    commandCounter = getCommandCounterMessage()

    funMessage = discord.Game(name="Checking Chicks V0.4")
    helpMessage = '$$help'
    messagesList = [funMessage, botInfos, helpMessage, commandCounter]

    # Used to change bot message every X seconds
    while not BOT.is_closed():
        botInfos = getGuildsAndUsers()
        commandCounter = getCommandCounterMessage()
        messagesList[1] = botInfos
        messagesList[3] = commandCounter

        if counter < len(messagesList):
            counter += 1
        if counter == len(messagesList):
            counter = 0

        activity = discord.Game(name=messagesList[counter])
        await BOT.change_presence(activity=activity)

        await asyncio.sleep(30)


BOT.loop.create_task(changeGameMessage())
BOT.run(BOT_TOKEN)
