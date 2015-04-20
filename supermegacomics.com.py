#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date    = "24.09.2013"
__author  = "Bystroushaak"
__email   = "bystrousak@kitakitsune.org"
#
# Interpreter version: python 2.7
# This work is licensed under a Creative Commons 3.0 Unported License
# (http://creativecommons.org/licenses/by/3.0/).
#
#= Imports ====================================================================
import json
import time
import os.path
import datetime


import dhtmlparser
from httpkie import Downloader

from k_rss import RSS



#= Variables ==================================================================
URL = "http://www.supermegacomics.com/"
URL_PICKER = "http://www.supermegacomics.com/index.php?i="

DATA_FILE = "supermegacomix.com_config.json"
HOW_MUCH  = 20



#= Functions & objects ========================================================
def loadData():
	if os.path.exists(DATA_FILE):
		return json.load(open(DATA_FILE))
	else:
		return {"last": 0, "data": {}}


def saveData(data):
	f = open(DATA_FILE, "wt")
	f.write(json.dumps(data))
	f.close()


def toRSS(d):
	rss = RSS(
		title       ="Supermegacomix RSS",
		description ="RSS feed for supermegacomics.com by Bystroushaak. Refresh rate: 12h.",
		link        = URL,
		language    ="en",
	)

	for key in sorted(d.keys(), reverse=True):
		description  = "<a href='" + URL_PICKER + key + "'>"
		description += '<img src="http://www.supermegacomics.com/images/'
		description += key + '.gif" /></a>'

		rss.AddItem(
			title       = key,
			description = description,
			pubDate     = datetime.datetime.fromtimestamp(d[key]),
			link        = URL_PICKER + key
		)

	return rss.Render()



#= Main program ===============================================================
if __name__ == '__main__':
	d = Downloader()
	data = d.download(URL)

	# don't look at that html to keep your sanity
	line = filter(
		lambda x: "MM_preloadImages('runningman_inverted.PNG'" in x,
		data.splitlines()
	)[0]
	dom = dhtmlparser.parseString(line)

	# extract href from first <a>, then extract number from url
	# "index.php?i=426" -> int(426), then add 1 for last posted picture
	last = int(dom.find("a")[0].params["href"].split("=")[1]) + 1

	saved = loadData()

	if saved["last"] < last:
		threshold = last - HOW_MUCH

		for key in saved["data"].keys():
			if saved["data"][key] < threshold:
				del saved["data"][key]

		while threshold <= last:
			if threshold not in saved["data"]:
				saved["data"][str(threshold)] = int(time.time())
			threshold += 1

		print toRSS(saved["data"])

		saved["last"] = last
		saveData(saved)
	else:
		print toRSS(saved["data"])
