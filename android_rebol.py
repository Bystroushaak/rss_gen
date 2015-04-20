#!/usr/bin/env python
# -*- coding: utf-8 -*-
__name    = ""
__version = "1.0.0"
__date    = "06.02.2013"
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
import sys
import time
import datetime

from k_rss import RSS
import dhtmlparser as d
import CheckerTools as web



#= Variables ===================================================================
URL = "http://development.saphirion.com/experimental/"


#= Functions & objects =========================================================
def write(s, out=sys.stdout):
	out.write(str(s))
	out.flush()
def writeln(s, out=sys.stdout):
	write(s + "\n")
def version():
	return __name + " v" + __version + " (" + __date + ") by " + __author + " (" + __email + ")"



#= Main program ================================================================
if __name__ == '__main__':
	data = web.getPage(URL)

	data = data.splitlines()
	data = filter(lambda x: ".apk" in x, data)

	rss = RSS(
		title       = "Rebol for android.", 
		link        = URL, 
		description = "RSS feed for experimental android rebol.",
		language    = "en",
	)

	for apk in data:
		apk = apk.split()
		timestamp = time.strptime(apk[2] + apk[3], "%d-%b-%Y%H:%M")

		link = apk[0] + " " + apk[1]
		link = d.parseString(link).find("a")[0].params["href"]

		link = URL + link

		rss.AddItem(
			author      = "Saphirion",
			title       = "New version of rebol for android",
			description = "<a href='" + link + "'>" + link + "</a>",
			pubDate     = datetime.datetime(*timestamp[:6]),
			link        = link
		)

		print rss.Render()