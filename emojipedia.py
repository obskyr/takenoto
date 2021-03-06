#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ...I'm writing a kind of Emojipedia API. What about it.
# Note: the emojipedia servers are incredibly slow most of the time.
# I can't do much about it!

import requests
from urllib import quote_plus
from bs4 import BeautifulSoup

def getSoup(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

class SearchResult(object):
    def __init__(self, li):
        a = li.find('a')
        self.emoji, self.name = list(a.stripped_strings)[:2]

    def __repr__(self):
        return "<Emoji search result {code} - {name}>".format(
            code=self.emoji.encode('unicode-escape'), name=self.name
        )

def search(term):
    url = "http://emojipedia.org/?s="
    # Thankfully, emojipedia's search does URL-encoded emoji too.
    url += quote_plus(term.encode('utf-8'))

    soup = getSoup(url)
    results = []
    for li in soup.find('ol', class_='search-results')('li'):
        if li.find('h2'):
            results.append(SearchResult(li))

    return results

if __name__ == '__main__':
    import sys
    def doIt():
        try:
            term = sys.argv[1]
        except IndexError:
            print "Please provide a search term as parameter."

        for result in search(term):
            print result.emoji.encode('unicode-escape').ljust(11) + result.name

    doIt()
