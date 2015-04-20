#!/usr/bin/env python
# -*- coding: utf-8 -*-
__name    = "awarenetwork.org rss generator based on karrigell rss module\n"
__version = "1.0.1"
__date    = "30.09.2013"
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
import re
import sys
import time
import datetime

from k_rss import RSS
import dhtmlparser as d
import CheckerTools as c



#= Variables ===================================================================
URL = "http://www.awarenetwork.org/"



#= Functions & objects =========================================================
def write(s, out=sys.stdout):
	out.write(str(s))
	out.flush()
def writeln(s, out=sys.stdout):
	write(s + "\n")
def version():
	return __name + " v" + __version + " (" + __date + ") by " + __author + " (" + __email + ")"


def cut(data, start, stop, include_ss = False):
	out = []

	tmp = []
	cut_enabled = False
	for line in data.splitlines():
		if start in line:
			cut_enabled = True

			# skip current line if not enabled include_ss
			if not include_ss:
				continue

		if include_ss:
			if cut_enabled:
				tmp.append(line)

		if stop in line:
			out.append("\n".join(tmp))
			tmp = []
			cut_enabled = False

		if not include_ss:
			if cut_enabled:
				tmp.append(line)



	return out



#= Main program ================================================================
if __name__ == '__main__':
	data = c.getPage(URL)

	data = cut(
		data,
		'<table width="100%" border="0" cellspacing="0" cellpadding="7">', 
		" </tr></table></td></tr></table><br>",
		True
	)[0]
	data = cut(
		data,
		'<table width="100%" border="0" cellspacing="0" cellpadding="7">', 
		"</table></td></tr>",
		False
	)[0]

	data = re.sub(r'(<script.*>).*(</script>)', r"", data)

	rss = RSS(
		title       = ".aware", 
		link        = URL, 
		description = "RSS feed for .aware news by Bystroushaak. Refresh rate: 12h.",
		language    = "en",
	)

	for new in data.split("\n\n"):
		dom = d.parseString(new)

		title       = dom.find("td")[0].find("b")[0].getContent()
		author_time = dom.find("td")[0].find("small")[0]
		author      = author_time.find("noscript")[0].getContent()

		# parse time
		post_time = author_time.getContent().splitlines()[-1]
		post_time = post_time.split("on")[1].strip()
		post_time = time.strptime(post_time, "%m/%d/%y %H:%M")
		post_time = datetime.datetime(*post_time[:6]) # convert time to datetime object

		content = dom.find("td")[1].getContent().strip()

		rss.AddItem(
			author      = author,
			title       = title,
			description = content,
			pubDate     = post_time,
			link        = URL
		)

	print rss.Render()
