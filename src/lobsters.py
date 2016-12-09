#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Translate links to articles to links to comments.
"""
# Imports =====================================================================
import httpkie
import dhtmlparser
from dhtmlparser import first


# Functions & classes =========================================================
def _download_feed():
    downer = httpkie.Downloader()

    return downer.download(
        "https://lobste.rs/rss" +
        "?token=99mPCT94XQfIwe8IyvctD0QQBhHPhyIuRdg8vOOjgxCRszqyk6KS81dgXmtG"
    )


def _find_comments_link(item):
    comments_link = item.find("comments")

    if not comments_link:
        return None

    return first(comments_link).getContent()


def _find_link_element(item):
    link_el = item.find("link")

    if not link_el:
        return None

    return first(link_el)


def _construct_new_link_el(url):
    dom = dhtmlparser.parseString("<link>%s</link>" % url)

    return first(dom.find("link"))


def link_to_comments_instead_of_url(feed):
    rss_dom = dhtmlparser.parseString(feed)

    for item in rss_dom.find("item"):
        # print item
        comments_url = _find_comments_link(item)
        link_element = _find_link_element(item)

        if comments_url and link_element:
            link_element.replaceWith(
                _construct_new_link_el(comments_url)
            )

    return rss_dom.prettify()


# Main program ================================================================
if __name__ == '__main__':
    print link_to_comments_instead_of_url(_download_feed())
