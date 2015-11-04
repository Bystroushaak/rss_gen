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
        if ".NET" in title.split():
            return True

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
            "rms",
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
            "php",

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
            "xamarin",
            "mysql",
            "nanofl",

            "nodejs",
            "reactjs",
            "angularjs",
            "gitlab",
            "coderpower",
            "ifttt",
            "windbg",
            "hipchat",
            "neo4j",
            "aurelia",
            "atlasdb",
            "redis",
            "postgresql",
            "libreoffice",
            "openoffice",
            "javaone",
            "swagger",
            "phonegap",
            "fizzbuzz",
            "matlab",

            ("microsoft", "surface"),
            ("css", "js"),
            ("php", "framework"),
            ("asp", "net"),
            ("node", "js"),
            ("angluar", "js"),
            ("react", "js"),
            ("selected", "js"),
            ("sql", "injection"),
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
            ".js",
            "visual studio",
            "vs 2015",
            "vs2015",
            "hack 2.0",
            "riot.js",
            "node.js",
            "react.js",
            "angular.js",
            "ms sql",
            "windows xp",
            "windows vista",
            "windows 7",
            "windows 8",
            "windows 10",
            "windows 11",
            "windows 12",
            "windows 13",
            "windows 14",
            "amish programmer",
        ]

        if banned_pattern(banned_sentences, title):
            return True

    return filter_programming


# Main program ================================================================
if __name__ == '__main__':
    dupe_filter = DupeFilter.load_dupes("reddit_programming_dupes.shelve")

    print filter_feed(
        chan_id="programming",
        filter_item=filter_programming_closure(dupe_filter)
    )

    dupe_filter.save_dupes()
