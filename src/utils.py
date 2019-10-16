#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import requests
from bs4 import BeautifulSoup

scriptPath = os.path.dirname(__file__)
commandCounterFilePath = os.path.join(scriptPath, '../data/commandCounter.txt')


def classChecker(characterLvlRaceClass, classList, returnedValue):
    if any(charClass in characterLvlRaceClass for charClass in classList):
        return returnedValue


def classTypes(lvlRaceClass):
    allList = {
        'melee': ['Death Knight', 'Rogue', 'Warrior', 'Monk'],
        'ranged': ['Hunter'],
        'caster': ['Mage', 'Priest', 'Warlock'],
        'hybrid': ['Paladin', 'Druid', 'Shaman']
    }

    for classType, classList in allList.items():
        charClass = classChecker(lvlRaceClass, classList, classType)

        if charClass != None:
            return charClass


def commandsCounterIncrement():
    # Increment counter, if file doesn't exists, create it
    try:
        with open(commandCounterFilePath, 'r+') as f:
            counter = int(f.readline()) + 1
            f.seek(0)
            f.write(str(counter))
    except:
        with open(commandCounterFilePath, 'w') as f:
            f.write('1')
            f.close()

def getCommandCounter():
    # Get counter, if file doesn't exists, create it
    try:
        with open(commandCounterFilePath, 'r') as f:
            return f.read()
    except:
        with open(commandCounterFilePath, 'w') as f:
            f.write('0')
            f.close()


def getHtmlText(url):
    response = requests.get(url)

    # Check if server is up
    if response.status_code == 200:
        response = response.text
        return BeautifulSoup(response, 'lxml')
    else:
        return 'Something wrong has happened with your provided informations. Please check and try again.'


def theoricalMaxDps(avgItemLevel, characterLvlRaceClass):
    result = {'base': {}, 'calculated': {}}
    
    # Data based on https://gamefaqs.gamespot.com/boards/534914-world-of-warcraft/55886296
    dpsList = {
        'Death Knight': {'Unholy': 16540, 'Frost': 15985, 'Blood': 14276},
        'Druid': {'Feral': 16689, 'Balance': 14924},
        'Hunter': {'Marksmanship': 17021, 'Survival': 13997},
        'Mage': {'Fire': 17799, 'Arcane': 15414,},
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
                theoricalMaxDps = "%.2f" % float((specDpsValue/279)*avgItemLevel)

                result['base'][specName] = specDpsValue
                result['calculated'][specName] = theoricalMaxDps

    return result
