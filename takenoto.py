#!/usr/bin/env python
# -*- coding: utf-8 -*-

# O.K. Mister Sunshine!

import argparse
import os
import emojipedia
import noto

def determineTermType(term):
    """Return a guessed emoji term type. Possible results are "emoji",
    "unicodeescape", "hex" and "searchterm"."""
    hexset = set("0x1234567890abcdef, ")
    uniset = set("\\uU1234567890abcdef")
    encodedTerm = term.encode('unicode-escape')
    encodedTermSet = set(encodedTerm.lower())
    if encodedTerm[:2].lower() == '\\u' and encodedTermSet.issubset(uniset):
        return 'emoji'
    elif encodedTerm[:3].lower() == '\\\\u' and encodedTermSet.issubset(uniset):
        return 'unicodeescape'
    elif term[:2] == '0x' and set(term).issubset(hexset):
        return 'hex'
    return 'searchterm'

def getEmojiIdentification(term, termType='auto', first=False):
    """Get a noto.get()-compatible emoji from `term`. If no emoji exactly
    matching the term is found, return a list of search results.
    """
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
        if result.name.lower() == term.lower().strip():
            return result.emoji
    return results

def downloadEmoji(term, outPath="", fileFormat="svg", commitId=None, termType='auto',
    first=False):
    """Fuzzy-dowload an emoji specified by `term` to `outPath`."""
    emoji = getEmojiIdentification(term, termType, first)
    if isinstance(emoji, list):
        if not len(emoji):
            print "No results were found for that search term!"
            return
        print "Several results matching the search term were found."
        print
        print "To download one, either change your search time to the exact " \
            "name of one"
        print "of the emoji, or specify --first to just download the first result."
        print
        print "Results:"
        for result in emoji[:10]:
            print "\t" + result.name
        return

    print "Downloading emoji..."
    emojiData = noto.get(emoji, fileFormat, commitId)
    filename = noto.emojiToNotoFilename(emoji, fileFormat)

    if commitId:
        # Having the commit ID in the default filename should be nice.
        fn, ext = os.path.splitext(filename)
        filename = fn + "_" + commitId[:10] + ext

    # For handling both outPaths as dir paths and as file paths:
    splitPath = os.path.split(outPath)
    if os.path.splitext(splitPath[1])[1]:
        outPath, filename = os.path.split(outPath)

    with open(os.path.join(outPath, filename), 'wb') as f:
        f.write(emojiData)

    print "Downloaded {filename}{toPath}!".format(filename=filename,
        toPath=" to {path}".format(path=outPath) if outPath else "")

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
        help="Where to save the emoji to. Either a directory or a full file " \
        "path. Defaults to the Noto filename in the current working directory.",
        default="",
        dest="outPath"
    )
    parser.add_argument("-f", "--format",
        help="The format of the downloaded emoji file. Defaults to SVG.",
        choices=["svg", "png"],
        default="svg",
        dest="fileFormat"
    )
    parser.add_argument("-p", "--old",
        help="Get old emoji, from before the new yellow people emoji.",
        action="store_true"
    )
    parser.add_argument("-1", "--first",
        help="Grab the first search result no matter how many were found.",
        action="store_true"
    )
    parser.add_argument("-t", "--type",
        help="The type of the emoji argument. Can be \"emoji\" for the " \
        "actual Unicode emoji, \"hex\" for the hex code(s) of the emoji, " \
        "\"unicodeescape\" for a Unicode escape sequence (eg. "\
        "\\U0001f1f8\\U0001f1ea), \"searchterm\" for an Emojipedia search" \
        "term, or \"auto\" to automatically determine. Defaults to auto.",
        choices=["auto", "emoji", "hex", "unicodeescape", "searchterm"],
        default="auto",
        dest="termType"
    )

    args = parser.parse_args()

    # This commit ID is right before the new yellow emoji were put in.
    oldCommitId = "aed0c0d4b9a6187c3fe143141b99332f31b1d69f"

    try:
        downloadEmoji(args.emoji, args.outPath, args.fileFormat,
        (oldCommitId if args.old else None), args.termType, args.first)
    except noto.NonexistentEmojiError:
        print
        print "That emoji does not seem to exist within Noto! Sorry!"
    except IOError:
        print
        print "Couldn't save the emoji. Make sure you've got the right"
        print "permissions and that all directories along the way exist."
