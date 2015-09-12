#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from reddit_filter import filter_feed
from reddit_filter import banned_pattern


# Functions & classes =========================================================
def filter_programming(title, link, pub_date, description):
    title = title.lower()

    banned = [
        "swift",
    ]

    if banned_pattern(banned, title):
        return True


# Main program ================================================================
if __name__ == '__main__':
    print filter_feed("programming", filter_programming)
