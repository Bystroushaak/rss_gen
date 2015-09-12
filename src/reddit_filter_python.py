#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from reddit_filter import filter_feed
from reddit_filter import banned_pattern


# Functions & classes =========================================================
def filter_python(title, link, pub_date, description):
    title = title.lower()

    if title.strip().endswith("?"):
        return True

    banned = [
        "django",
        "course",
        "pandas",
        "can anyone",
        "can someone",
        "help!",
        "flask",
    ]

    if banned_pattern(banned, title):
        return True


# Main program ================================================================
if __name__ == '__main__':
    print filter_feed("python", filter_python)
