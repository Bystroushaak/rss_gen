#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from reddit_filter import filter_feed
from reddit_filter import banned_pattern
from reddit_filter import banned_pattern_tokens

from dupe_filter import DupeFilter


# Variables ===================================================================
DUPES_FN = "reddit_filter_programming_titles.json"


# Functions & classes =========================================================
def filter_programming_closure(dupe_filter):
    def filter_programming(title, link, pub_date, description):
        title = title.lower()

        whitelist = [
            "carmack",
            "templeos",
            "lisp",
            "self",
            "smalltalk",
            "python",
            "codeless",
        ]

        if banned_pattern(whitelist, title):
            return False

        if dupe_filter.in_dupes(title):
            return True

        banned = [
            "swift",
            "dart",
            "rust",
            "java",
            "scala",
            "javascript",
            "typescript",
            "hack 2.0",

            "webrtc",
            "windows",
            "winrt",
            "gtalkabout",
            "sqlite",
            "angular",
            "udacity",

            "node.js",
            "angularjs",

            "coderpower",
            ("css", "js"),
            ("css", "javascript"),
            ("css", "php"),
            ("full", "stack", "web"),
            ("must", "have", "free"),
        ]

        if banned_pattern_tokens(banned, title):
            return True

    return filter_programming


# Main program ================================================================
if __name__ == '__main__':
    dupe_filter = DupeFilter.load_dupes("reddit_programming_dupes.shelve")

    print filter_feed(
        "programming",
        filter_programming_closure(dupe_filter)
    )

    dupe_filter.save_dupes()
