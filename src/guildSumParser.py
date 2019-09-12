#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib.request
import time
import re

from bs4 import BeautifulSoup


def getGuildInfos(url = 'http://armory.warmane.com/guild/Stack+and+Slack/Icecrown/boss-fights'):
    response = requests.get(url)

    # Check if server is up
    if response.status_code == 200:
        response = response.text
        html = BeautifulSoup(response, 'lxml')

        # Ensure guild is found before scrap anything else
        if len(html.findAll(string=re.compile(r'Page not found'))) > 0:
            return 'Guild not found, please check your informations and try again.'
        else:
            guildPath = html.find(class_ = 'information-left')
            guildName = guildPath.find(class_ = 'name').text.strip()
            lvlFactionRealm = guildPath.find(class_ = 'level-faction-realm').text

            guildInfos = []
            for index in lvlFactionRealm.split('\n'):
                if index.strip() != '':
                    guildInfos.append(index.strip())

            guildSum = {
                'url': url,
                'guildName': guildName,
                'guildStatus': guildInfos[0],
                'guildPoints': guildInfos[1]
            }

            return guildSum
    else:
        return 'Something wrong has happened with your provided informations. Please check and try again.'



getGuildInfos()

