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


def _parse_description_link(description):
    descr = description.replace("&#34;", '"')\
                       .replace("&lt;", "<")\
                       .replace("&gt;", ">")

    descr_dom = dhtmlparser.parseString(descr)

    link_tags = descr_dom.find("a", fn=lambda x: x.getContent() == "[link]")

    return first(link_tags).params["href"]


def filter_feed(chan_id, filter_item):
    rss = _download_feed(chan_id)
    rss_dom = dhtmlparser.parseString(rss)

    for item in rss_dom.find("item"):
        title = _pick_item_property(item, "title")
        link = _pick_item_property(item, "link")
        pub_date = _pick_item_property(item, "pubDate")
        description = _pick_item_property(item, "description")
        real_link = _parse_description_link(description)

        result = filter_item(
            title=title,
            link=link,
            real_link=real_link,
            pub_date=pub_date,
            description=description,
        )
        if result:
            item.replaceWith(dhtmlparser.HTMLElement(""))

    xml = rss_dom.prettify().splitlines()

    return '<?xml version="1.0" encoding="UTF-8"?>' + "\n".join(xml[1:])


def banned_pattern(banned_words, line):
    line = line.strip().lower()

    for banword in banned_words:
        if banword.lower() in line:
            return True


def banned_pattern_tokens(banned_words, line):
    line = line.strip().lower()

    def test_multiple(words, line):
        test_words = [
            word in line
            for word in words
        ]
        if all(test_words):
            return True

    # create set of words
    split_chars = ".,!?/':;`(){}[]"
    trantab = maketrans(split_chars, len(split_chars) * " ")
    tokens = set(
        line.translate(trantab).split()
    )

    for banword in banned_words:
        if type(banword) in [list, tuple]:
            if test_multiple(banword, tokens):
                return True
        elif banword.lower() in tokens:
            return True
