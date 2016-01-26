#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from reddit_filter import filter_feed
from reddit_filter import banned_pattern

from dupe_filter import DupeFilter


# Functions & classes =========================================================
def filter_python_closure(dupe_filter):
    def filter_python(title, link, real_link, pub_date, description):
        title = title.lower()

        if title.strip().endswith("?"):
            return True

        if dupe_filter.in_dupes(real_link):
            return True

        if "twitter" in title:
            return True

        banned = [
            "django",
            "course",
            "pandas",
            "flask",
            "can anyone",
            "can someone",
            "help!",
            "need help",
            "need some help",
            "help with",
            "help me",
            "[help]",
            "(help)",
            "python tutorial",
            "I am new",
            "I am a new",
            "please help",
            "new to coding",
            "new to python",
            "learning python",
            "how to write",
            "newbie",
            "win32",
            "win32com",
            "komodo ide",
            "mezzanine",
            "pycharm",
            "scikit",
            "homework",
            "mysql",
            "trumpscript",

            "windows 10",
            "windows 11",
            "windows 12",
            "windows 13",
            "windows 14",
            "windows 7",
            "windows 8",
            "windows vista",
            "windows xp",
        ]

        if banned_pattern(banned, title):
            return True

    return filter_python


# Main program ================================================================
if __name__ == '__main__':
    dupe_filter = DupeFilter.load_dupes("reddit_python_dupes.shelve")

    print filter_feed(
        chan_id="python",
        filter_item=filter_python_closure(dupe_filter)
    )

    dupe_filter.save_dupes()
