""" Character Summary parsing functions """

import re

from src.itemParser import getItemInfos
from src.utils import getHtmlText
from src.gearScore import createGearScoreDictionnary


def hasEnchantProfession(profession, minProfLvl):
    """ Check if character has profession enchant above a determined level """
    profLvl = int(re.search(r'\d+', profession).group(0))
    return profLvl >= minProfLvl


def processItems(itemsList, isBlacksmith, isEnchanter, isHunter, isWarrior):
    """ Process each items to know if they are fully optimised """

    notEnchantedItems = []
    notGemmedItems = []
    totalItemLvl = 0
    totalGearScore = 0
    equippedItems = 0
    # Fury war has special calculation method taking in account having 2 2H weaps
    hasAlreadyATwoHandWeapOn = False
    twoHandWeapGearScore = [0, 0]
    # Calling it here so we only create it once per command
    gearScoreDict = createGearScoreDictionnary()

    excludedSlots = ['Shirt', 'Tabard']
    itemsToBeEnchant = ['Head', 'Shoulder', 'Back', 'Chest',
                        'Wrist', 'Hands', 'Legs', 'Feet',
                        'One-hand', 'Off Hand', 'Two-hand']

    if isEnchanter:
        itemsToBeEnchant.append('Finger')
    if isHunter:
        itemsToBeEnchant.append('Ranged')

    # Blacksmith can get another gem slot on some items (badly reported in url)
    itemsToBeBlacksmithEnchant = ['Wrist', 'Hands']

    for item in itemsList:
        # Power is there to reach an 'API' (not a real one btw...)
        itemUrl = item.find('a').get('href') + '&power=true'
        infosFromRel = item.find('a').get('rel')
        itemAdditionnalInfos = re.search(
            '&{1}.*', infosFromRel[0]) if infosFromRel is not None else None

        if itemAdditionnalInfos is not None:
            itemAdditionnalInfos = itemAdditionnalInfos.group(0)
            itemUrl += itemAdditionnalInfos

        if '#self' not in itemUrl:
            itemInfos = getItemInfos(itemUrl, gearScoreDict)
            itemSlot = itemInfos['itemSlot']

            hasToHaveBonusGemSlot = itemSlot == 'Waist' or (
                itemSlot in itemsToBeBlacksmithEnchant and isBlacksmith)
            if hasToHaveBonusGemSlot:
                itemInfos = getItemInfos(itemUrl, gearScoreDict, hasToHaveBonusGemSlot)

            # Checking what is missing in item
            if itemInfos['missingGems']:
                notGemmedItems.append(itemSlot)
            if itemInfos['missingEnchant'] and itemSlot in itemsToBeEnchant:
                notEnchantedItems.append(itemSlot)
            if itemSlot not in excludedSlots:
                equippedItems += 1
                totalItemLvl += itemInfos['itemLevel']
                totalGearScore += itemInfos['itemGearScore']

                # pylint: disable=too-many-boolean-expressions
                if isWarrior and (itemInfos['itemSlot'] == 'Two-hand' or (
                        (hasAlreadyATwoHandWeapOn and itemInfos['itemSlot'] == 'Two-hand') or
                        (hasAlreadyATwoHandWeapOn and itemInfos['itemSlot'] == 'One-hand') or
                        (hasAlreadyATwoHandWeapOn and itemInfos['itemSlot'] == 'Off Hand') or
                        (hasAlreadyATwoHandWeapOn and itemInfos['itemSlot'] == 'Held In Off-Hand')
                )):
                    minGs = min(twoHandWeapGearScore)
                    twoHandWeapMinIndex = twoHandWeapGearScore.index(minGs)
                    twoHandWeapGearScore[twoHandWeapMinIndex] = itemInfos['itemGearScore']

                    # Getting new values after modifications
                    minGs = min(twoHandWeapGearScore)
                    maxGs = max(twoHandWeapGearScore)

                    # To calculate gearscore, we have to ignore the second 2H weap GS,
                    # get the difference between Main Hand and Off Hand
                    # divide it by 2, round it up and substract it to the total sum
                    # If difference is equal to 1
                    # That means we are crawling first weapon or the character is wearing only
                    # one Two hands weapon
                    if minGs != 0:
                        differenceBetweenTwoHandWeaps = int((maxGs - minGs)/2) + 1

                    if hasAlreadyATwoHandWeapOn:
                        totalGearScore -= minGs + differenceBetweenTwoHandWeaps
                    else:
                        hasAlreadyATwoHandWeapOn = True

    if equippedItems != 0:
        avgItemLvl = "%.2f" % float(totalItemLvl/equippedItems)
    else:
        avgItemLvl = 0

    return {
        'notEnchantedItems': notEnchantedItems,
        'notGemmedItems': notGemmedItems,
        'avgItemLvl': avgItemLvl,
        'itemGearScore': totalGearScore,
    }


def processList(providedList):
    """ Process the provided items list """
    items = []

    for item in providedList.findAll(class_='text'):
        items.append(' '.join(item.text.split()).replace(' / ', '/'))

    return items


def getCharInfos(
        url='http://armory.warmane.com/character/Ashaladin/Icecrown/summary', htmlText=None
):
    """ Get character informations """

    if htmlText is None:
        html = getHtmlText(url)
    else:
        html = htmlText

    # Ensure char is found before scrap anything else
    if len(html.findAll(string=re.compile(r'Page not found'))) > 0:
        return 'Character not found, please check your informations and try again.'

    charMainInfos = html.find(class_='information-left')

    # Hunter will need to have Ranged slot checked (enchant)
    isHunter = 'Hunter' in charMainInfos.text
    isWarrior = 'Warrior' in charMainInfos.text

    # Grouping variables:
    # First group is html info retrieving
    # Second is extracted data
    charAndGuildName = charMainInfos.find(class_='name').text.split(' ')
    itemsPath = html.findAll(class_='item-slot')
    specsPath = html.find(class_='specialization')
    professionsSummary = []
    professionsPath = html.findAll(class_='profskills')
    isBlacksmith = False
    isEnchanter = False

    charName = charAndGuildName.pop(0).strip()
    guildName = ' '.join(charAndGuildName) if charAndGuildName[0] != u'\xa0' else 'No Guild'
    lvlRaceClass = charMainInfos.find(class_='level-race-class').text.strip()

    professions = []
    for professionsType in professionsPath:
        professions.append(processList(professionsType))

    # Processing multiple arrays into one (1 array per professionType (main & secondary profs))
    for professionType in professions:
        for profession in professionType:
            # We have to check blacksmith level to ensure the bonus gem slots are available
            if 'Blacksmithing' in profession:
                isBlacksmith = hasEnchantProfession(profession, 400)
            if 'Enchanting' in profession:
                isEnchanter = hasEnchantProfession(profession, 400)
            professionsSummary.append(profession)

    getSpecializations = processList(specsPath)
    itemsCheck = processItems(itemsPath, isBlacksmith, isEnchanter, isHunter, isWarrior)

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
