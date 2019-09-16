#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from src.utils import classTypes


def notOptimisedText(itemsList, checkedValue):
    text = ''

    if len(itemsList) > 0:
        text = 'Missing {} on ['.format(checkedValue)
        
        for item in itemsList:
            text += '**{}**, '.format(item)
        
        text = re.sub(r', $', ']', text, 0)

        return text
    else:
        return 'Full {}'.format(checkedValue)

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

**{}** - **{}**
{}

**Armory Link**: {}
**Professions**: {}
**Specs**: {}
**Average Item Level**: {}
**Enchant Status**: {}
**Gems Status**: {}
{}
            """.format(
                charInfos['charName'],
                charInfos['guildName'],
                charInfos['lvlRaceClass'],
                charInfos['url'],
                ', '.join(charInfos['professions']),
                ', '.join(charInfos['specs']),
                charInfos['itemsCheck']['avgItemLvl'],
                notOptimisedText(enchantsStatus, 'Enchant'),
                notOptimisedText(gemsStatus, 'Gem'),
                isOptimisedText
            )

        return text


def statsSummaryText(lvlRaceClass, statsDict):
    def formatStatArrayToStr(statType, statArray, newLine=False):
        return '**{}**{}{}'.format(statType, ', '.join(statArray), ('\n' if newLine else ''))
        # return '**' + statType + '**' + ', '.join(statArray) + ('\n' if newLine else '')

    text = """**Stats Summary**
{}{}
""".format(
                formatStatArrayToStr('Attributes: ', statsDict['Attributes'], True),
                formatStatArrayToStr('Defense: ', statsDict['Defense']),
            )

    charClassType = classTypes(lvlRaceClass)

    if charClassType == 'melee':
        text += formatStatArrayToStr('Melee: ', statsDict['specRelated']['Melee'])
    elif charClassType == 'ranged':
        text += formatStatArrayToStr('Ranged: ', statsDict['specRelated']['Ranged'])
    elif charClassType == 'caster':
        text += formatStatArrayToStr('Spell: ', statsDict['specRelated']['Spell'])
    else:
        text += formatStatArrayToStr('Melee: ', statsDict['specRelated']['Melee'], True)
        text += formatStatArrayToStr('Ranged: ', statsDict['specRelated']['Ranged'], True)
        text += formatStatArrayToStr('Spell: ', statsDict['specRelated']['Spell'])

    return text


def theoricalDpsText(theoricalDpsDict, charItemLvl):
    text = '**Theorical Max Dps**\n'

    for baseSpec, baseSpecDps in theoricalDpsDict['base'].items():
        text += '**{}** (~279 ilvl): {}, **You** ({} ilvl): {}'.format(baseSpec, baseSpecDps, charItemLvl, theoricalDpsDict['calculated'][baseSpec]) + '\n'

    return text


def formatFullCharInfosResponse(charInfos):
    if type(charInfos) is str:
        return charInfos
    else:
        baseFormatting = formatCharInfosResponse(charInfos)

        text = """
{}
{}

{}
*Please note that dps calculation is using a very basic formula ((maxDps/279)\*yourAverageItemLevel) and is not seriously reliable. 279 is the average max item level available.
ICC's 30% Damages Buff is taken in account in maxDps.*
    """.format(
                baseFormatting,
                statsSummaryText(charInfos['lvlRaceClass'], charInfos['stats']),
                theoricalDpsText(charInfos['theoricalDps'], charInfos['itemsCheck']['avgItemLvl'])
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
