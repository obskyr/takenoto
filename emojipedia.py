#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ...I'm writing an Emojipedia API. What about it.

import requests
from bs4 import BeautifulSoup

def getSoup(url):
    return BeautifulSoup(requests.get(url).text)

if __name__ == '__main__':
    # Alternatively soup.find("div", class_="entry-header").find("h1")
    # for more redundancy / future-proofing.
    # A regex (or even a split at space, I suppose) could separate the emoji
    # from the title.
    print getSoup("http://emojipedia.org/flag-for-sweden/").find("h1") \
        .text.__repr__()
