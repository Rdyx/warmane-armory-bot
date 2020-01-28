""" Item parser function """

import time
import re
import requests

from bs4 import BeautifulSoup
from src.gearScore import getItemGearScore


def getItemInfos(url, gearScoreDict, isBlacksmith=False):
    """ Request item url to get item informations """

    if not isBlacksmith:
        response = requests.get(url).text
    else:
        regex = r"&gems=\d+:\d+:\d+"
        gemSlotsStatus = re.search(regex, url)

        # In case regex didn't find match in url,
        # we manually set the array to what it's supposed to be
        if gemSlotsStatus is not None:
            gemSlotsStatus = gemSlotsStatus.group(0).split(':')
        else:
            gemSlotsStatus = ['0', '0', '0']

        gemSlotsStatus[0] = gemSlotsStatus[0].replace('&gems=', '')
        url = re.sub(regex, '', url, 0)
        response = requests.get(url).text

    # We can know if an item is enchanted from the url by matching 'ench='
    missingEnchant = not re.search('ench=', url)

    # Parse html
    item = BeautifulSoup(response, 'lxml')

    # Returning a number which quality depends on (3: Rare, 4: Epic, 5: Legen.. wait for it.. dary)
    itemQuality = re.search(r',quality: \d', item.text).group(0)[-1]

    # Gosh, this html class is horrible, uncomment for item troubleshooting
    # itemName = item.find(class_='\\"q{}\\"'.format(itemQuality)).contents[0].replace('\\', '')

    # Get to the interesting data to check if everything is ok
    itemPath = 'table>tr>td>b table>tr>td'

    # Find which slot we are checking
    itemSlot = item.select(itemPath)[0].text
    # Get item status (used to check if we got gems and retrieve item level)
    itemValues = item.select(itemPath)[1]

    # If char is not blacksmith
    # every item that can be gemmed must have at least once the word "Socket" (from Bonus Socket)
    # If the word Socket is found more than once (i.e Red Socket), that means a gem is missing
    if not isBlacksmith:
        missingGems = len(itemValues.findAll(string=re.compile(r"Socket"))) > 1
    else:
        # Get number of slots filled
        # it must be equal to the number of gem slots available on the item
        gemSlotsFilled = len([gem for gem in gemSlotsStatus if gem != '0'])
        gemSlots = len(itemValues.findAll(string=re.compile(r"Socket")))

        # (gemSlotsFilled != 0 and gemSlots == 0) is used for items with
        # no gem slots available at start (No word Socket can be found on them)
        missingGems = not (gemSlotsFilled == gemSlots) or (gemSlotsFilled != 0 and gemSlots == 0)

    itemLevelText = itemValues.find(string=re.compile(r"Item Level"))

    itemLevel = int(itemLevelText.replace('Item Level ', '')) if itemLevelText else 0

    itemGearScore = getItemGearScore(gearScoreDict, itemSlot, str(itemLevel), itemQuality)

    # Be kind with servers, wait between each request <3
    time.sleep(0.5)

    return {
        'itemSlot': itemSlot,
        'missingGems': missingGems,
        'missingEnchant': missingEnchant,
        'itemLevel': itemLevel,
        'itemGearScore': itemGearScore
    }
