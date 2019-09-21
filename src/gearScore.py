#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Creating a dictionnary
# {itemSlot: {itemLevel: {itemQuality: itemGs}}}
def createGearScoreDictionnary():
    dictionnary = {}

    # Rare, Epic
    # We use this because items with ilvl 200 can be Rare, Epic or Legendary
    itemRarities = ['3', '4', '5']
    itemLevels = [200, 213, 219, 226, 232, 239, 245, 251, 258, 264, 271, 277, 284]
    itemSlots = ['Head', 'Chest', 'Legs', 'Main Hand',
        'One-hand', 'Off Hand', 'Held In Off-Hand', 'Shoulder',
        'Hands', 'Waist', 'Feet', 'Neck',
        'Back', 'Wrist', 'Finger', 'Trinket',
        'Ranged', 'Relic', 'Thrown', 'Two-hand']
    legendarySlots = ['Main Hand', 'Two-Hand']

    highestGsSlotsNames = ['Head', 'Chest', 'Legs', 'Main Hand', 'One-hand', 'Off Hand', 'Held In Off-Hand']
    highestGsSlotsValues = [271, 310, 348, 365, 385, 402, 422, 439, 457, 477, 494, 514, 531, 551]

    secondhighestGsSlotsNames = ['Shoulder', 'Hands', 'Waist', 'Feet']
    secondhighestGsSlotsValues = [203, 233, 261, 274, 289, 301, 316, 329, 342, 357, 370, 385, 398, 413]

    middleGsSlotsNames = ['Neck', 'Back', 'Wrist', 'Finger', 'Trinket']
    middleGsSlotsValues = [152, 174, 195, 205, 216, 226, 237, 247, 257, 268, 278, 289, 298, 310]

    rangedGsSlotNames = ['Ranged', 'Relic', 'Thrown']
    rangedGsSlotValues = [86, 98, 110, 115, 121, 127, 133, 139, 144, 150, 156, 162, 168, 174]

    twoHandGsSlotName = ['Two-hand']
    twoHandGsSlotValues = [543, 621, 696, 730, 770, 805, 845, 879, 914, 954, 988, 1028, 1062, 1103]

    # Those items are sharing ilvl with epics equivalent but have more gs due to their quality difference
    legendaryGsItemsNames = ['Val\'anyr, Hammer of Ancient Kings', 'Shadowmourne']
    legendaryGsItemsValues = [571, 1433]

    for itemSlot in itemSlots:
        gsValuesCopy = []
        dictionnary[itemSlot] = {}

        # Creating a separated copy of array to be able to pop it and use it for multiple itemSlots
        if itemSlot in highestGsSlotsNames:
            gsValuesCopy = highestGsSlotsValues.copy()
        elif itemSlot in secondhighestGsSlotsNames:
            gsValuesCopy = secondhighestGsSlotsValues.copy()
        elif itemSlot in middleGsSlotsNames:
            gsValuesCopy = middleGsSlotsValues.copy()
        elif itemSlot in rangedGsSlotNames:
            gsValuesCopy = rangedGsSlotValues.copy()
        elif itemSlot in twoHandGsSlotName:
            gsValuesCopy = twoHandGsSlotValues.copy()

        for itemLevel in itemLevels:
            # Dict goal, converting int to str to use as key
            itemLevel = str(itemLevel)
            dictionnary[itemSlot][itemLevel] = {}

            for itemRarity in itemRarities:
                # Legendary item, special values, break loop after data is used
                for legendaryGsItemsName in legendaryGsItemsNames:
                    # Break statement earlier to avoid useless process
                    if itemRarity != '5':
                        break
                    elif itemRarity == '5':
                        if itemSlot == 'Main Hand' and itemLevel == '245' and legendaryGsItemsName == legendaryGsItemsNames[0]:
                            dictionnary[itemSlot][itemLevel][itemRarity] = legendaryGsItemsValues[0]
                            break
                        elif itemSlot == 'Two-hand' and itemLevel == '284' and legendaryGsItemsName == legendaryGsItemsNames[1]:
                            dictionnary[itemSlot][itemLevel][itemRarity] = legendaryGsItemsValues[1]
                            break

                # Using .pop() to get the first value and diminish array length each time we loop over itemLevel
                # We ignore rarity 5 because we already used a loop over it before
                if itemLevel == '200' and itemRarity in ['3', '4']:
                    dictionnary[itemSlot][itemLevel][itemRarity] = gsValuesCopy.pop(0)
                elif itemRarity == '4':
                    dictionnary[itemSlot][itemLevel][itemRarity] = gsValuesCopy.pop(0)

    return dictionnary


def getItemGearScore(gearScoreDictionnary, selectedItemSlot, selectedItemLevel, selectedItemQuality):
    if selectedItemSlot in ['Shirt', 'Tabard']:
        return 0

    try:
        itemGearScore = gearScoreDictionnary[selectedItemSlot][selectedItemLevel][selectedItemQuality]
        return itemGearScore
    except:
        return 0

# print (createGearScoreDictionnary())
