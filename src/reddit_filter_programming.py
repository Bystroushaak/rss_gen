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
    def filter_programming(title, link, real_link, pub_date, description):
        title = title.lower()

        whitelist = [
            "carmack",
            "clojure",
            "codeless",
            "emacs",
            "lisp",
            "python",
            "pypy",
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

        if banned_pattern_tokens(whitelist, title):
            return False

        if dupe_filter.in_dupes(real_link):
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
            "c++",
            "c++11",
            "c++14",
            "kotlin",
            "elixir",
            "clang",
            "golang",
            "ruby",
            "c#",
            "f#",
            "perl",

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
            "apache",
            "eclipse",
            "wordpress",
            "jquery",
            "twitter",
            "citrix",
            "javafx",
            "android",
            "docker",
            "hhvm",
            "javadoc",
            "intellij",
            "jenkins",
            "devops",
            "phpunit",
            "mongodb",

            "nodejs",
            "node.js",
            "reactjs",
            "react.js",
            "angularjs",
            "angular.js",
            "gitlab",
            "coderpower",

            ("microsoft", "surface"),
            ("css", "js"),
            ("asp", "net"),
            ("node", "js"),
            ("angluar", "js"),
            ("react", "js"),
            ("css", "javascript"),
            ("css", "php"),
            ("c++", "stl"),
            ("google", "chrome"),
            ("modern", "web"),
            ("referrals", "free"),
            ("full", "stack", "web"),
            ("must", "have", "free"),

            # bullshit phrases
            ("how", "i", "learned", "to", "stop", "love"),
            ("considered", "harmful"),
        ]

        if banned_pattern_tokens(banned, title):
            return True

        # senteces as they are -> simple `s in title` check
        banned_sentences = [
            "visual studio",
            "vs 2015",
            "vs2015",
            "hack 2.0",
        ]

        if banned_pattern(banned_sentences, title):
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
