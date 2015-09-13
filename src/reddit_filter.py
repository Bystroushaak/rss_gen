#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from string import maketrans

import httpkie
import dhtmlparser
from dhtmlparser import first


# Variables ===================================================================
URL = "https://www.reddit.com"


# Functions & classes =========================================================
def _download_feed(chan_id):
    downer = httpkie.Downloader()

    data = downer.download("%s/r/%s/.rss" % (URL, chan_id))

    search_link = (
        '<atom:link rel="self" ' +
        'href="%s/subreddits/search.rss?q=%s" ' % (URL, chan_id) +
        'type="application/rss+xml" />'
    )

    if search_link in data:
        raise ValueError("Incorrect `chan_id`: '%s'!" % chan_id)

    return data


def _pick_item_property(item, item_property):
    prop = item.find(item_property)

    if not prop:
        return None

    return first(prop).getContent()


def filter_feed(chan_id, filter_item):
    rss = _download_feed(chan_id)
    rss_dom = dhtmlparser.parseString(rss)

    for item in rss_dom.find("item"):
        title = _pick_item_property(item, "title")
        link = _pick_item_property(item, "link")
        pub_date = _pick_item_property(item, "pubDate")
        description = _pick_item_property(item, "description")

        if filter_item(title, link, pub_date, description):
            item.replaceWith(dhtmlparser.HTMLElement(""))

    xml = rss_dom.prettify().splitlines()

    return '<?xml version="1.0" encoding="UTF-8"?>' + "\n".join(xml[1:])


def banned_pattern(banned_words, line):
    def test_multiple(words, line):
        test_words = [
            word in line
            for word in words
        ]
        if all(test_words):
            return True

    # create set of words
    trantab = maketrans(".,!?/", "     ")
    tokens = set(
        line.translate(trantab).split()
    )

    for banword in banned_words:
        if type(banword) in [list, tuple]:
            if test_multiple(banword, tokens):
                return True
        elif banword in tokens:
            return True
