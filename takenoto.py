#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unicodedata
import requests
from urlparse import urljoin
from bs4 import BeautifulSoup

def getSoup(url):
    return BeautifulSoup(requests.get(url).text)

class NonexistentEmojiError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "The emoji \"{}\" does not exist within Noto.".format(
            self.filename
        )

filetypeDirectories = {
    "svg": "svg/",
    "png": "png/128/" # At the moment only 128x128 exist.
}

def emojiToNotoFilename(emoji, extension="svg"):
    """Convert an emoji (or other EmojiRepo.get input format) to a Noto
    filename."""
    filename = "emoji_u"
    emoji = emoji.encode("unicode-escape").replace("\\", "").replace(
        "0x", ""
    ).lower()
    emoji = re.split(r"u|,\s*", emoji)
    emoji = emoji[1:] # The first entry is empty.
    emoji = [code.lstrip("0") for code in emoji]
    emoji = "_".join(emoji)
    filename += emoji + "." + extension

    return filename

def notoFilenameToEmoji(notoFilename):
    """Convert a Noto filename to a Unicode emoji."""
    # Might remove this if it doesn't prove useful.
    # OR NOT HE HE HE HE HE

    codes = notoFilename[7:] # len("emoji_u") is 7
    codes = codes.split(".")[0]
    codes = codes.split("_")
    codes = ["\U" + code.zfill(8) for code in codes]
    codes = [code.decode("unicode-escape") for code in codes]
    emoji = ''.join(codes)
    return emoji

class EmojiRepo(object):
    def __init__(self, commitId=None):
        self.baseUrl = "https://noto.googlecode.com/"
        if commitId:
            self.baseUrl = urljoin(self.baseUrl, "git-history/" + commitId)
        else:
            self.baseUrl = urljoin(self.baseUrl, "git/")
        self.baseUrl = urljoin(self.baseUrl, "color_emoji/")

    def get(self, emoji, filetype="svg"):
        """Get the SVG or PNG data for an emoji. Valid input formats for the
        emoji are: a Unicode character, a comma-separated combination of
        Unicode characters, a hex code (eg. "0x01f633") or a comma-separated
        list of hex codes (eg. "0x01f1f8, 0x01f1ea")
        """
        filename = emojiToNotoFilename(emoji, filetype)

        url = urljoin(self.baseUrl, filetypeDirectories[filetype])
        url = urljoin(url, filename)

        r = requests.get(url)
        if r.status_code == 404:
            raise NonexistentEmojiError(filename)
        return r.content

if __name__ == '__main__':
    EmojiRepo().get(
        "\\U0001f1fa\\U0001f1f8".decode("unicode-escape")
    )
    EmojiRepo().get(
        "0x1f1fa, 0x0001f1f8"
    )
    print "Got emoji successfully! It works!"
