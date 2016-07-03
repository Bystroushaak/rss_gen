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

        # usually with "python", so the whitelist lets it go
        if "trupscript" in title:
            return True

        whitelist = [
            "carmack",
            "clojure",
            "codeless",
            "digitalmars",
            "dlang",
            "emacs",
            "lisp",
            "pypy",
            "python",
            "pharo",
            "racket",
            "reality",
            "rms",
            "scheme",
            "self",
            "smalltalk",
            "stallman",
            "templeos",
            "virtual",
            "vr",
        ]

        if banned_pattern_tokens(whitelist, title):
            return False

        if dupe_filter.in_dupes(real_link):
            return True

        banned = [
            "c#",
            "c++",
            "c++11",
            "c++14",
            "clang",
            "dart",
            "elixir",
            "f#",
            "fortran",
            "golang",
            "haskell",
            "java",
            "javascript",
            "kotlin",
            "perl",
            "php",
            "ruby",
            "rust",
            "scala",
            "swift",
            "typescript",

            "ageism",
            "android",
            "angular",
            "angularjs",
            "apache",
            "atlasdb",
            "aurelia",
            "citrix",
            "codepile",
            "coderpower",
            "cppcon",
            "devops",
            "dijkstra",
            "docker",
            "eclipse",
            "feminism",
            "fizzbuzz",
            "forth",
            "gitlab",
            "gnocchi",
            "godmin",
            "gtalkabout",
            "hhvm",
            "hipchat",
            "houndify",
            "ifttt",
            "instagram",
            "intellij",
            "javadoc",
            "javafx",
            "javaone",
            "jclarity",
            "jdbc",
            "jekyll",
            "jenkins",
            "jetbrains",
            "jquery",
            "kafka",
            "kaminari",
            "lamp",
            "libreoffice",
            "linq",
            "makara",
            "matlab",
            "mongodb",
            "monocoque",
            "mysql",
            "nanofl",
            "neo4j",
            "netbeans",
            "nginx",
            "nodejs",
            "npm",
            "openoffice",
            "paas",
            "phonegap",
            "phpunit",
            "platformio",
            "postgresql",
            "protractor",
            "reactjs",
            "redis",
            "redox",
            "rxjava",
            "selenium",
            "sqlite",
            "swagger",
            "twitter",
            "udacity",
            "webgl",
            "webrtc",
            "windbg",
            "windows",
            "winrt",
            "wordpress",
            "xamarin",
            "xcode",
            "trumpscript",
            "women",
            "phpstorm",
            "harrasment",
            "microaggression",
            "gender",

            ("micro", "aggression"),
            ("microsoft", "surface"),
            ("microsoft", "azure"),
            ("anypoint", "studio"),
            ("css", "js"),
            ("css", "trick"),
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
            ("mobile", "ux"),
            ("recruit", "manage"),
            ("manage", "startup"),

            ("full", "stack", "web"),
            ("must", "have", "free"),
            ("growing", "tech", "stack"),
            ("data", "analysis", "r"),

            # bullshit phrases
            ("how", "i", "learned", "to", "stop", "love"),
            ("considered", "harmful"),
        ]

        if banned_pattern_tokens(banned, title):
            return True

        # senteces as they are -> simple `s in title` check
        banned_sentences = [
            ".js",
            "amish programmer",
            "android app",
            "angular.js",
            "billing software",
            "hack 2.0",
            "help me",
            "komodo ide",
            "ms sql",
            "node.js",
            "react.js",
            "riot.js",
            "technical debt",
            "visual studio",
            "vs 2015",
            "vs2015",
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
