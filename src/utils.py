#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def checkResponseCode(html):
    if len(html.findAll(string=re.compile(r'Page not found'))) > 0:
        return 'Not found, please check your informations and try again.'
    else:
        return html