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


# Functions & classes =========================================================
def filter_programming_closure(dupe_filter):
    def filter_programming(title, link, pub_date, description):
        title = title.lower()

        whitelist = [
            "carmack",
            "clojure",
            "codeless",
            "emacs",
            "lisp",
            "python",
            "racket",
            "reality",
            "scheme",
            "self",
            "smalltalk",
            "stallman",
            "templeos",
            "virtual",
            "vr",
            "digitalmars",
            "dlang",
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
            "haskell",
            "cppcon",
            "javascript",
            "typescript",
            "hack 2.0",
            "c++",
            "c++11",
            "c++14",
            "kotlin",
            "elixir",
            "clang",
            "golang",
            "ruby",

            "jclarity",
            "kafka",
            "webrtc",
            "windows",
            "winrt",
            "gtalkabout",
            "sqlite",
            "angular",
            "udacity",
            "xcode",
            "linq",
            "jetbrains",
            "jdbc",
            "nginx",

            "nodejs",
            "node.js",
            "reactjs",
            "react.js",
            "angularjs",
            "angular.js",
            "gitlab",

            "coderpower",
            ("css", "js"),
            ("node", "js"),
            ("angluar", "js"),
            ("react", "js"),
            ("css", "javascript"),
            ("css", "php"),
            ("c++", "stl"),
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
