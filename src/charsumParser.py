#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib.request
import re

from bs4 import BeautifulSoup
from src.itemParser import getItemInfos
from src.utils import getHtmlText


def processItems(itemsList, isBlacksmith, isHunter):
    notEnchantedItems = []
    notGemmedItems = []
    totalItemLvl = 0
    equippedItems = 0

    excludedSlots = ['Shirt', 'Tabard']
    itemsToBeEnchant = ['Head', 'Shoulder', 'Back', 'Chest', 
                        'Wrist', 'Hands', 'Legs', 'Feet', 
                        'One-hand', 'Off Hand', 'Two-hand']
    if isHunter:
        itemsToBeEnchant.append('Ranged')

    # Blacksmith can get another gem slot on some items (badly reported in url)
    itemsToBeBlacksmithEnchant = ['Wrist', 'Hands']

    for item in itemsList:
        # Power is there to reach an 'API' (not a real one btw...)
        itemUrl = item.find('a').get('href') + '&power=true'
        infosFromRel = item.find('a').get('rel')
        itemAdditionnalInfos = re.search('&{1}.*', infosFromRel[0]) if infosFromRel is not None else None


        if itemAdditionnalInfos is not None:
            itemAdditionnalInfos = itemAdditionnalInfos.group(0)
            itemUrl += itemAdditionnalInfos
        
        if '#self' not in itemUrl:
            itemInfos = getItemInfos(itemUrl)
            itemSlot = itemInfos['itemSlot']

            hasToHaveBonusGemSlot = itemSlot == 'Waist' or (itemSlot in itemsToBeBlacksmithEnchant and isBlacksmith)
            if hasToHaveBonusGemSlot:
                itemInfos = getItemInfos(itemUrl, hasToHaveBonusGemSlot)

            # Checking what is missing in item
            if itemInfos['missingGems']:
                notGemmedItems.append(itemSlot)
            if itemInfos['missingEnchant'] and itemSlot in itemsToBeEnchant:
                notEnchantedItems.append(itemSlot)
            if itemSlot not in excludedSlots:
                equippedItems += 1
                totalItemLvl += itemInfos['itemLevel']

    if equippedItems != 0:
        avgItemLvl = "%.2f" % float(totalItemLvl/equippedItems)
    else:
        avgItemLvl = 0

    return {'notEnchantedItems': notEnchantedItems, 'notGemmedItems': notGemmedItems, 'avgItemLvl': avgItemLvl}


def processList(providedList):
    items = []

    for item in providedList.findAll(class_ = 'text'):
        items.append(' '.join(item.text.split()).replace(' / ', '/'))

    return items


def getCharInfos(url = 'http://armory.warmane.com/character/Wardyx/Icecrown/summary', htmlText=None):
    if htmlText == None:
        html = getHtmlText(url)
    else:
        html = htmlText

    # Ensure char is found before scrap anything else
    if len(html.findAll(string=re.compile(r'Page not found'))) > 0:
        return 'Character not found, please check your informations and try again.'
    else:
        # Grouping variables: 
        # First group is html info retrieving
        # Second is extracted data
        charMainInfos = html.find(class_ = 'information-left')

        # Hunter will need to have Ranged slot checked (enchant)
        isHunter = True if 'Hunter' in charMainInfos.text else False

        charAndGuildName = charMainInfos.find(class_ = 'name').text.split(' ')
        itemsPath = html.findAll(class_ = 'item-slot')
        specsPath = html.find(class_ = 'specialization')
        professionsSummary = []
        professionsPath = html.findAll(class_ = 'profskills')
        isBlacksmith = False

        charName = charAndGuildName.pop(0).strip()
        guildName = ' '.join(charAndGuildName) if charAndGuildName[0] != u'\xa0' else 'No Guild'
        lvlRaceClass = charMainInfos.find(class_ = 'level-race-class').text.strip()

        professions = []
        for professionsType in professionsPath:
            professions.append(processList(professionsType))

        # Processing multiple arrays into one (1 array per professionType (main & secondary profs))
        for professionType in professions:
            for profession in professionType:
                if 'Blacksmithing' in profession:
                    # We have to check blacksmith level to ensure the bonus gem slots are available
                    blacksmithLevel = int(re.search(r'\d+', profession)[0])
                    if blacksmithLevel >= 400:
                        isBlacksmith = True
                professionsSummary.append(profession)

        getSpecializations = processList(specsPath)
        itemsCheck = processItems(itemsPath, isBlacksmith, isHunter)
        
        summary = {
            'url': url,
            'charName': charName,
            'guildName': guildName,
            'lvlRaceClass': lvlRaceClass,
            'professions': professionsSummary,
            'specs': getSpecializations,
            'itemsCheck': itemsCheck
        }

        return summary

# getCharInfos()