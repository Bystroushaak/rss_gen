#!/usr/bin/env python
# -*- coding: utf-8 -*-
__name    = "zpovedka.cz rss generator based on karrigell rss module\n"
__version = "1.0.1"
__date    = "05.02.2013"
__author  = "Bystroushaak"
__email   = "bystrousak@kitakitsune.org"
# 
# Interpreter version: python 2.7
# This work is licensed under a Creative Commons 3.0 
# Unported License (http://creativecommons.org/licenses/by/3.0/).
# Created in Sublime text 2 editor.
#
# Notes:
    # 
#= Imports =====================================================================
import time
import shelve
import datetime

from k_rss import RSS
import dhtmlparser as d
import CheckerTools as c



#= Variables ===================================================================
URL           = "http://zpovedka.cz"
POST_CACHE    = "zpovedka.cz.cache.shelve"
MAX_POST      = 20
MAX_POST_SIZE = 500000



#= Functions & objects =========================================================
def toUTF(s):
	return unicode(s, "windows-1250").encode("utf-8")


class ZpovedkaPost:
	def __init__(self, title, author, url):
		self.title   = title
		self.author  = author
		self.url     = url
		self.date    = None
		self.content = ""
		self.updated = False

	def update(self):
		"Download post content and parse date."

		self.content = c.getPage(self.url)
		self.content = toUTF(self.content)

		dom = d.parseString(self.content)

		# parse date
		p_date = dom.find("font", {"color":"#C0C0C0"})[0].getContent()
		p_date = p_date.splitlines()
		p_date = p_date[3] + " " + p_date[5]

		# convert to datetime object
		self.date = time.strptime(p_date, "%d.%m.%Y %H:%M:%S")
		self.date = datetime.datetime(*self.date[:6])

		self.__updateContent(dom)

		self.updated = True

	def __updateContent(self, dom):
		self.content = dom.find("font", {"color":"#FFD680"})[0].getContent()

		self.content = c.removeTags(self.content)

		# cut content
		self.content = self.content if len(self.content) < MAX_POST_SIZE else self.content[:MAX_POST_SIZE - 1] + "..."
		

	def __str__(self):
		return self.url



#= Main program ================================================================
if __name__ == '__main__':
	f = shelve.open(POST_CACHE)
	old_posts = f["old_posts"] if "old_posts" in f else {}


	# init rss generator
	rss = RSS(
		title       = u"Zpověďka.cz RSS by Bystroushaak.",
		link        = URL,
		description = "RSS feed pro server zpovedka.cz. Refresh rate: 12h.",
		language    = "cs",
	)


	data = c.getPage(URL)
	dom  = d.parseString(toUTF(data))


	# parse posts on title page
	cnt = 0
	posts = {}
	for table in dom.find("table", {"bgcolor":"#0c2847", "width":"717"}):
		cnt += 1
		if cnt > MAX_POST:
			break

		# parse posts url
		link = map(
			lambda x: 
				x.params["href"].strip(), 
			table.find("a")
		)
		link = filter(lambda x: not x.startswith("autor"), link)[0]
		link = URL + "/" + link.strip()

		# post cache - old posts are not processed again
		if link in old_posts:
			posts[link] = old_posts[link]
			continue

		# parse page title
		title = table.find("font", {"color":"#FFD680"})[0].getContent().strip()

		# parse author
		author = filter(
			lambda x:
				x.params["color"] == "#A5BFDA" or
				x.params["color"] == "#C0C0C0",
			table.find("font")
		)[2].getContent().strip()

		posts[link] = ZpovedkaPost(title, author, link)


	# read content of the new posts
	for link in posts.keys():
		if not posts[link].updated:
			posts[link].update()

	# dict to array, sorted by date
	rss_posts = posts.values()
	rss_posts.sort(key = lambda x: x.date, reverse = True)


	# generate rss feed
	for post in rss_posts:
		rss.AddItem(
			author      = unicode(post.author, "utf-8", "ignore"),
			title       = unicode(post.title, "utf-8", "ignore"),
			description = unicode(post.content, "utf-8", "ignore"),
			pubDate     = post.date,
			link        = unicode(post.url, "utf-8", "ignore")
		)

	print rss.Render("utf-8")

	# save fresh posts
	f["old_posts"] = posts
	f.sync()
	f.close()