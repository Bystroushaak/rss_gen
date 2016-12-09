#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from urlparse import urljoin

import arrow

import httpkie
import dhtmlparser
from feedgen.feed import FeedGenerator


# Variables ===================================================================
URL = "http://liberland.org/cz/news/"
DOWNER = httpkie.Downloader()


# Functions & classes =========================================================
def _parse_link(div):
    # parse link
    link = div.find("a")
    if not link:
        return

    link = link[0].params.get("href", None)
    if not link:
        return

    return urljoin(URL, link)


def _parse_date(div):
    # parse date tag
    date_tag = div.find("h3")
    if not date_tag:
        return

    # parse the actual date
    date = date_tag[0].getContent()
    if not date:
        return

    raw_date = date.split(":")[-1].strip()
    raw_date = raw_date.split("<")[0]  # remove link to the article

    date = arrow.Arrow.strptime(raw_date, "%d.%m.%Y")

    return date.to("Europe/Prague").datetime


def parse(data):
    dom = dhtmlparser.parseString(data)

    for preview in dom.find("div", {"class": "articlePreview"}):
        title_and_link = preview.find("h2")

        # skip items without <h2>
        if not title_and_link:
            continue

        title_and_link = title_and_link[0]

        title = dhtmlparser.removeTags(title_and_link.getContent())
        link = _parse_link(title_and_link)
        date = _parse_date(preview)

        yield title, link, date


def unittest():
    data = DOWNER.download(URL)
    items = list(parse(data))

    return len(items) > 1


# Main program ================================================================
if __name__ == '__main__':
    fg = FeedGenerator()
    fg.id(URL)
    fg.title("Liberland.org - Novinky")
    fg.link(href=URL, rel='alternate')
    fg.language("cs")

    data = DOWNER.download(URL)
    for title, link, date in parse(data):
        fe = fg.add_entry()

        fe.id(link)
        fe.title(title.decode("utf-8"))
        fe.link(href=link)
        fe.updated(date)

    print fg.atom_str(pretty=True)
