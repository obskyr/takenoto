#!/usr/bin/env python
# -*- coding: utf-8 -*-

# O.K. Mister Sunshine!

import argparse
import os
import emojipedia
import noto

def determineTermType(term):
    encodedTerm = term.encode('unicode-escape')
    if encodedTerm[:2].lower() == '\\u':
        return 'emoji'
    elif encodedTerm[:3].lower() == '\\\\u':
        return 'unicodeescape'
    elif term[:2] == '0x':
        return 'hex'
    return 'searchterm'

def getEmojiIdentification(term, termType='auto', first=False):
    """Get a noto.get()-compatible emoji from `term`."""
    if termType == 'auto':
        termType = determineTermType(term)

    if termType in ['emoji', 'hex', 'unicodeescape']:
        # Doesn't always return the same format, but hey, as long as this
        # is only used with noto.get()...
        return term

    results = emojipedia.search(term)
    if first and len(results):
        return results[0].emoji
    for result in results:
        if result.title == term.strip():
            return result.emoji

    return results



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get a Noto emoji source file."
    )
    parser.add_argument("emoji",
        help="The emoji to get. Can be an emoji, a search term (in which" \
        "case it will only be grabbed if the term exactly matches the name " \
        "or --first is specified) or a (potentially comma-separated" \
        "combination of) hex codes (eg. 0x1f60e or 0x1f1f8,0x1f1ea)."
    )
    parser.add_argument("-o", "--outpath",
        help="Where to save the emoji to. Defaults to current working " \
        "directory.",
        default=""
    )
    parser.add_argument("-f", "--format",
        help="The format of the downloaded emoji file. Defaults to SVG.",
        choices=["svg", "png"],
        default="svg"
    )
    parser.add_argument("-1", "--first",
        help="Grab the first search result no matter how many were found.",
        action="store_true"
    )
    parser.add_argument("-t", "--type",
        help="The type of the emoji argument. Can be \"emoji\" for the " \
        "actual Unicode emoji, \"hex\" for the hex code(s) of the emoji, " \
        "\"searchterm\" for an Emojipedia search term, or \"auto\" to " \
        "automatically determine. Defaults to auto.",
        choices=["auto", "emoji", "hex", "searchterm"],
        default="auto",
        dest="termType"
    )

    inputFormats = [ # Should register as...
        "0x1f603", # hex
        "0x1f1f8,0x1f1ea", # hex
        u"\U0001f348", # emoji
        "\\U0001f348", # unicodeescape
        "Sure, why not?", # searchterm
        "0xHahah, yeah, no problem.", # searchterm
        "\\UCool face" # searchterm
    ]

    for s in inputFormats:
        print s.__repr__().ljust(35) + determineTermType(s)
