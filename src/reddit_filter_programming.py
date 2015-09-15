#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from reddit_filter import filter_feed
from reddit_filter import banned_pattern
from reddit_filter import banned_pattern_tokens


# Functions & classes =========================================================
def filter_programming(title, link, pub_date, description):
    title = title.lower()

    banned = [
        "swift",
        "webrtc",
        "dart",
        ("rust",),  # whole words only
        "windows",
        "node.js",
        "gtalkabout",
        "sqlite",
        "angularjs",
        ("java",),  # whole words only
        "javascript",
        "typescript",
        ("css", "js"),
        ("css", "javascript"),
        ("css", "php"),
    ]

    if banned_pattern_tokens(banned, title):
        return True


# Main program ================================================================
if __name__ == '__main__':
    print filter_feed("programming", filter_programming)
