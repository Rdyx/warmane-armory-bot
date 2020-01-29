""" Formatting bot's response to commands functions """

import re
from src.utils import getClassTypes


def notOptimisedText(itemsList, checkedValue):
    """ Avoid DRY about optimisation message """
    text = ''

    if len(itemsList) > 0:
        text = 'Missing {} on ['.format(checkedValue)

        for item in itemsList:
            text += '**{}**, '.format(item)

        text = re.sub(r', $', ']', text, 0)

        return text

    return 'Full {}'.format(checkedValue)


def formatCharInfosResponse(charInfos):
    """ Formatting Character informations for humand readability """
    if isinstance(charInfos, str):
        return charInfos

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
**Average Item Level**: {} - **Gearscore**: {}
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
        charInfos['itemsCheck']['itemGearScore'],
        notOptimisedText(enchantsStatus, 'Enchant'),
        notOptimisedText(gemsStatus, 'Gem'),
        isOptimisedText
    )

    return text


def getStatsSummaryText(lvlRaceClass, statsDict):
    """ Get and format character statistics string """

    def formatStatArrayToStr(statType, statArray, newLine=False):
        return '**{}**{}{}'.format(statType, ', '.join(statArray), ('\n' if newLine else ''))
        # return '**' + statType + '**' + ', '.join(statArray) + ('\n' if newLine else '')

    text = """**Stats Summary**
{}{}
""".format(
        formatStatArrayToStr('Attributes: ', statsDict['Attributes'], True),
        formatStatArrayToStr('Defense: ', statsDict['Defense']),
    )

    charClassType = getClassTypes(lvlRaceClass)

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


def getTheoricalDpsText(theoricalDpsDict, charItemLvl):
    """ Get and format theorical dps string """
    text = '**Theorical Max Dps**\n'

    for baseSpec, baseSpecDps in theoricalDpsDict['base'].items():
        text += '**{}** (~279 ilvl): {}, **You** ({} ilvl): {}'.format(
            baseSpec, baseSpecDps, charItemLvl, theoricalDpsDict['calculated'][baseSpec]
        ) + '\n'

    return text


def formatFullCharInfosResponse(charInfos):
    """ Formatting Full Character informations for humand readability """
    if isinstance(charInfos, str):
        return charInfos

    baseFormatting = formatCharInfosResponse(charInfos)

    text = """
{}
{}
{}
*Please note that dps calculation is using a very basic formula ((maxDps/279)\\*yourAverageItemLevel) and is not seriously reliable. 279 is the average max item level available.
ICC's 30% Damages Buff is taken in account in maxDps.*
    """.format(
        baseFormatting,
        getStatsSummaryText(charInfos['lvlRaceClass'], charInfos['stats']),
        getTheoricalDpsText(charInfos['theoricalDps'], charInfos['itemsCheck']['avgItemLvl'])
    )

    return text


def formatGuildInfosResponse(guildInfos):
    """ Formatting Guild informations for humand readability """
    if isinstance(guildInfos, str):
        return guildInfos

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
