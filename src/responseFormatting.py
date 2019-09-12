#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def notOptimisedText(itemsList, checkedValue):
    text = ''

    if len(itemsList) > 0:
        text = 'Missing {} on: '.format(checkedValue)
        for item in itemsList:
            text += '**{}**, '.format(item)
        
        text = re.sub(r', $', '.', text, 0)

        return text
    else:
        return 'Fully {}'.format(checkedValue)

def formatCharInfosResponse(charInfos):
    if type(charInfos) is str:
        return charInfos
    else:
        isOptimisedText = ''
        enchantsStatus = charInfos['itemsCheck']['notEnchantedItems']
        gemsStatus = charInfos['itemsCheck']['notGemmedItems']

        if len(enchantsStatus) == 0 and len(gemsStatus) == 0:
            isOptimisedText = 'This char seems optimised :white_check_mark:'
        else:
            isOptimisedText = 'This char is not optimised :x:'

        # Wtf this is super ugly but discord is taking tabs into account...
        text = """
{}
**{}** - **{}**
{}
{}
{}
Average Item Level: {}
{}
{}
{}
            """.format(
                charInfos['url'],
                charInfos['charName'],
                charInfos['guildName'],
                charInfos['lvlRaceClass'],
                ', '.join(charInfos['professions']),
                ', '.join(charInfos['specs']),
                charInfos['itemsCheck']['avgItemLvl'],
                notOptimisedText(enchantsStatus, 'Enchant'),
                notOptimisedText(gemsStatus, 'Gem'),
                isOptimisedText
            )

        return text


def formatGuildInfosResponse(guildInfos):
    if type(guildInfos) is str:
        return guildInfos
    else:
        # Wtf this is super ugly but discord is taking tabs into account when posting...
        text = """
{}
**{}**
{}
{}
            """.format(
                guildInfos['url'],
                guildInfos['guildName'],
                guildInfos['guildStatus'],
                guildInfos['guildPoints']
            )

        return text