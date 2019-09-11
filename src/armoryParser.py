#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup


def getCharInfos(url):
    response = requests.get(url)

    # Check if server is up
    if response.status_code == 200:
        response = response.text
        html = BeautifulSoup(response, 'lxml')

        # Ensure char is found before scrap anything else
        if len(html.findAll(string=re.compile(r'Page not found'))) == 0:
            return url
        else:
            return 'Character not found, please check your informations and try again.'
    else:
        return 'Something wrong has happened with your provided informations. Please check and try again.'