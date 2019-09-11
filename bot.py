# bot.py
import os
import random
import discord
import requests
import urllib.request

from discord.ext import commands
from dotenv import load_dotenv
from src.armoryParser import getCharInfos

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')


@bot.command(name='summary', help='Get summary of a character')
async def summary(ctx, charName, server):
    charUrl = 'http://armory.warmane.com/character/{}/{}/summary'.format(charName, server)
    test = getCharInfos(charUrl)

    await ctx.send(test)


bot.run(token)