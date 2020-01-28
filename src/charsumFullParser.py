""" Character 'full' parser """

import re

from src.charsumParser import getCharInfos
from src.utils import getHtmlText, getTheoricalMaxDps


def sanitizeStats(charStatsInfo):
    """ Make text (character statistics) human readable """
    sortedDivs = {}

    # Processing <div class="stub"/> split
    stubDivs = charStatsInfo.findAll(class_='text')

    for div in stubDivs:
        # Ugly but the way the website is formatted is forcing it...
        # What a good idea to use <br/> to place text blocks
        statCategory1 = div.contents[0].strip()
        statCategoryValues1 = div.contents[3].text.split('\n')
        statCategory2 = div.contents[7].strip()
        statCategoryValues2 = div.contents[10].text.split('\n')

        sortedDivs[statCategory1] = statCategoryValues1
        sortedDivs[statCategory2] = statCategoryValues2

    for category, categoryValues in sortedDivs.items():
        # Lambda to remove every extra s*** spaces
        stripText = map(lambda value: value.strip(), categoryValues)
        # Filtering to remove s*** \n from html
        sortedDivs[category] = list(filter(None, stripText))

    return sortedDivs


def getFullCharInfos(url='http://armory.warmane.com/character/Rdyx/Icecrown/summary'):
    """ Get character stats from url request """

    html = getHtmlText(url)

    if isinstance(html, str):
        return html
    # Ensure char is found before scrap anything else
    if len(html.findAll(string=re.compile(r'Page not found'))) > 0:
        return 'Character not found, please check your informations and try again.'

    # Process basics info same as $$charsum then we get more data from page and process it
    charBaseInfos = getCharInfos(url, html)
    # class_ is special word for beautyfull soup so we can get some element in html
    # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
    charStatsInfo = html.find(class_='character-stats')
    charStats = sanitizeStats(charStatsInfo)

    statsToReturn = {
        'stats':
        {
            'Attributes': charStats['Attributes'],
            'Defense': charStats['Defense'],
            'specRelated': {},
        }
    }

    statsToReturn['stats']['specRelated']['Melee'] = charStats['Melee']
    statsToReturn['stats']['specRelated']['Ranged'] = charStats['Ranged']
    statsToReturn['stats']['specRelated']['Spell'] = charStats['Spell']

    statsToReturn['theoricalDps'] = getTheoricalMaxDps(
        float(charBaseInfos['itemsCheck']['avgItemLvl']), charBaseInfos['lvlRaceClass'])

    # Enriching base dict with new data
    charBaseInfos = dict(charBaseInfos)
    charBaseInfos.update(statsToReturn)

    return charBaseInfos
