""" Utilities Functions """

import os
import requests
from bs4 import BeautifulSoup

SCRIPT_PATH = os.path.dirname(__file__)
COMMAND_COUNTER_FILE_PATH = os.path.join(
    SCRIPT_PATH, '../data/commandCounter.txt')


# def checkIfCharClassExists(characterLvlRaceClass, classList, returnedValue):
#     """ Check the character class is existing """
#     if any(charClass in characterLvlRaceClass for charClass in classList):
#         return returnedValue


def getClassTypes(lvlRaceClass):
    """ Get class 'type' of a character """
    typesDict = {
        'melee': ['Death Knight', 'Rogue', 'Warrior', 'Monk'],
        'ranged': ['Hunter'],
        'caster': ['Mage', 'Priest', 'Warlock'],
        'hybrid': ['Paladin', 'Druid', 'Shaman']
    }

    for classType, classList in typesDict.items():
        if any(charClass in lvlRaceClass for charClass in classList):
            charClassType = classType
        else:
            charClassType = None

        # if charClassType is not None:
    return charClassType


def createCommandCounterFile(defaultString):
    """ Create used command counter tracking file """
    with open(COMMAND_COUNTER_FILE_PATH, 'w') as commandCounterFile:
        commandCounterFile.write(defaultString)
        commandCounterFile.close()


def incrementCommandsCounter():
    """ Increment command counter tracker """
    # Increment counter, if file doesn't exists, create it
    try:
        with open(COMMAND_COUNTER_FILE_PATH, 'r+') as commandCounterFile:
            counter = int(commandCounterFile.readline()) + 1
            commandCounterFile.seek(0)
            commandCounterFile.write(str(counter))
    except FileNotFoundError:
        createCommandCounterFile('1')


def getCommandCounter():
    """ Get command counter tracker """
    # Get counter, if file doesn't exists, create it
    try:
        with open(COMMAND_COUNTER_FILE_PATH, 'r') as commandCounterFile:
            return commandCounterFile.read()
    except FileNotFoundError:
        createCommandCounterFile('0')


def getHtmlText(url):
    """ Get HTML as text """
    response = requests.get(url)

    # Check if server is up
    if response.status_code == 200:
        response = response.text
        return BeautifulSoup(response, 'lxml')

    return 'Something wrong has happened with your provided informations. \
        Please check and try again.'


def getTheoricalMaxDps(avgItemLevel, characterLvlRaceClass):
    """ Calculate max theorical DPS of a character based on its average item level """
    result = {'base': {}, 'calculated': {}}

    # Data based on https://gamefaqs.gamespot.com/boards/534914-world-of-warcraft/55886296
    dpsList = {
        'Death Knight': {'Unholy': 16540, 'Frost': 15985, 'Blood': 14276},
        'Druid': {'Feral': 16689, 'Balance': 14924},
        'Hunter': {'Marksmanship': 17021, 'Survival': 13997},
        'Mage': {'Fire': 17799, 'Arcane': 15414, },
        'Paladin': {'Retribution': 17213},
        'Priest': {'Shadow': 15807},
        'Rogue': {'Combat': 17671, 'Assassination': 17052},
        'Shaman': {'Enhancement': 15275, 'Elemental': 14538},
        'Warlock': {'Affliction': 16144, 'Demonology': 15396, 'Destruction': 14157},
        'Warrior': {'Fury': 18107, 'Arms': 12563}
    }

    for dpsClassName, dpsClassValues in dpsList.items():
        if dpsClassName in characterLvlRaceClass:
            for specName, specDpsValue in dpsClassValues.items():
                theoricalMaxDps = "%.2f" % float(
                    (specDpsValue/279)*avgItemLevel)

                result['base'][specName] = specDpsValue
                result['calculated'][specName] = theoricalMaxDps

    return result
