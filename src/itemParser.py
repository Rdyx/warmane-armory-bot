#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib.request
import time
import re

from bs4 import BeautifulSoup


def getItemInfos(url, isBlacksmith=False):
    if not isBlacksmith:
        response = requests.get(url).text
    else:
        regex = r"&gems=\d+:\d+:\d+"
        gemSlotsStatus = re.search(regex, url).group(0).split(':')
        gemSlotsStatus[0] = gemSlotsStatus[0].replace('&gems=', '')
        url = re.sub(regex, '', url, 0)
        response = requests.get(url).text

    # We can know if an item is enchanted from the url by matching 'ench='
    missingEnchant = False if re.search('ench=', url) else True

    # response = "$utilGrp.regItem('51225', 0, {name_enus: 'Sanctified Ymirjar Lord\'s Battleplate',quality: 4,icon: 'inv_chest_plate_25',tooltip_enus: '<table><tr><td><b class=\"q4\">Sanctified Ymirjar Lord\'s Battleplate<\/b><br /><span class=\"q2\">Heroic<\/span><br />Binds when picked up<br /><table width=\"100%\"><tr><td>Chest<\/td><td align=\'right\'>Plate<\/td><\/tr><\/table>2756 Armor<br />+193 Strength<br />+209 Stamina<br /><span class=\'q2\'>+10 All Stats<\/span><br /><span class=\'socket q1\' style=\'background: url(//cdn.cavernoftime.com/wotlk/icons/tiny/inv_jewelcrafting_gem_37.gif) no-repeat left center;\'>+20 Strength<\/span><br /><span class=\'socket q1\' style=\'background: url(//cdn.cavernoftime.com/wotlk/icons/tiny/inv_misc_gem_pearl_12.gif) no-repeat left center;\'>+10 All Stats<\/span><br /><span class=\'q2\'>Socket Bonus: +6 Strength<\/span><br />Durability 165 / 165<br />Classes: <span class=\'c1\'>Warrior<\/span><br />Requires Level 80<br />Item Level 277<br /><\/td><\/tr><\/table><table><tr><td><span class=\"q2\">Equip: Increases your critical strike rating by 122&nbsp;<small>(<a href=\"javascript:;\" onmousedown=\"return false\" onclick=\"openDB_setRatingLevel(this,80,32,122)\">2.66%&nbsp;@&nbsp;L80<\/a>)<\/small>.<\/span><br /><span class=\"q2\">Equip: Increases your armor penetration rating by 106&nbsp;<small>(<a href=\"javascript:;\" onmousedown=\"return false\" onclick=\"openDB_setRatingLevel(this,80,44,106)\">8.61%&nbsp;@&nbsp;L80<\/a>)<\/small>.<\/span><br /><br /><span class=\"q\"><a href=\"itemset=-259\" class=\"q\">Sanctified Ymirjar Lord\'s Battlegear<\/a> (0/5)<\/span><div class=\"q0 indent\"><span><a href=\"item=51225\">Sanctified Ymirjar Lord\'s Battleplate<\/a><\/span><br /><span><a href=\"item=51226\">Sanctified Ymirjar Lord\'s Gauntlets<\/a><\/span><br /><span><a href=\"item=51227\">Sanctified Ymirjar Lord\'s Helmet<\/a><\/span><br /><span><a href=\"item=51228\">Sanctified Ymirjar Lord\'s Legplates<\/a><\/span><br /><span><a href=\"item=51229\">Sanctified Ymirjar Lord\'s Shoulderplates<\/a><\/span><br /><\/div><br /><span class=\"q0\"><span class=\"q0\"><span>(2) Set: <a href=\"spell=70854\">When your Deep Wounds ability deals damage you have a 3% chance to gain 16% attack power for 10 sec.<\/a><\/span><br /><span>(4) Set: <a href=\"spell=70847\">You have a 20% chance for your Bloodsurge and Sudden Death talents to grant 2 charges of their effect instead of 1, reduce the global cooldown on Execute or Slam by 500.1 sec, and for the duration of the effect to be increased by 100%.<\/a><\/span><br /><\/span><\/span><\/td><\/tr><\/table>'}, 2);"

    # Parse html
    item = BeautifulSoup(response, 'lxml')
    # Get to the interesting data to check if everything is ok
    itemPath = 'table>tr>td>b table>tr>td'

    # Find which slot we are checking
    itemSlot = item.select(itemPath)[0].text
    # Get item status (used to check if we got gems and retrieve item level)
    itemValues = item.select(itemPath)[1]

    if not isBlacksmith:
        missingGems = len(itemValues.findAll(string=re.compile(r"Socket"))) > 1
    else:
        gemSlotsFilled = len([gem for gem in gemSlotsStatus if gem != '0'])
        gemSlots = len(itemValues.findAll(string=re.compile(r"Socket")))

        missingGems = False if (gemSlotsFilled == gemSlots) or (gemSlotsFilled != 0 and gemSlots == 0) else True
        
    itemLevelText = itemValues.find(string=re.compile(r"Item Level"))

    itemLevel = int(itemLevelText.replace('Item Level ', '')) if itemLevelText else 0

    # Be kind with servers <3
    time.sleep(0.5)

    return {'itemSlot': itemSlot, 'missingGems': missingGems, 'missingEnchant': missingEnchant, 'itemLevel': itemLevel}
