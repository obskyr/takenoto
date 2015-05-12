# takenoto.py

A script to take Notos. Ha!

Seriously, though - `takenoto.py` lets you easily download [Noto](https://www.google.com/get/noto/) (Google's emoji font) emoji in both SVG and PNG format. Check it out:

```
takenoto.py sushi
takenoto.py "rice ball"
takenoto.py 0x01f60e
takenoto.py 🍈
takenoto.py \U0001f1f8\U0001f1ea
```

These are all valid ways to download emoji files! For more advanced options, try things like:

```
takenoto.py cool --first
takenoto.py watermelon --format png
takenoto.py 0x1f1ef,0x1f1f5 -o japaneseflag.svg
```

Have fun! For more info on the command line parameters, just run `takenoto.py -h`
.

## Requirements

Before running `takenoto.py`, there are a few things you have to do. First of all, make sure you have [Python 2](https://python.org/download/) downloaded (and in your PATH, if you're a Windows user). Then make sure you have [pip](https://pip.pypa.io/en/stable/installing.html) (download and run `get-pip.py`).

Once you have pip, run these commands to install the required modules:

```
pip install requests
pip install beautifulsoup4
```

Then you should be all set to just run `takenoto.py!`

## noto.py and emojipedia.py

`takenoto.py` uses two other scripts - `noto.py` and `emojipedia.py` - these are actually kind of APIs for their respective projects. Feel free to use them if you want. If you take a look in the respective files you might find they're not terribly hard to use.

`noto.py` provides an API for downloading emoji files (`noto.get` + `noto.EmojiRepo`), and `emojipedia.py` provides an API for searching Emojipedia (`emojipedia.search`).

## Contact

If you've got any questions or just want to talk for a bit, you can find me at [@obskyr](http://twitter.com/obskyr) on Twitter, or [e-mail me](mailto:powpowd@gmail.com). If you want a fast answer, Twitter is the place to go!

If there's a problem with takenoto, or a feature you think should be added, feel free to open an issue or pull request here on GitHub.
