#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CheckerTools v1.5.1 (10.09.2011) - https://github.com/Bystroushaak/CheckerTools
by Bystroushaak (bystrousak@kitakitsune.org)

This work is licensed under a Creative Commons (http://creativecommons.org/licenses/by/3.0/cz/).

Created in Geany text editor. This module uses epydoc.
"""
#===============================================================================
# Imports ======================================================================
#===============================================================================
import urllib
import urllib2
import re


#===============================================================================
# Variables ====================================================================
#===============================================================================
__version = "1.5.1"


IEHeaders = {
	"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
	"Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain",
	"Accept-Language": "cs,en-us;q=0.7,en;q=0.3",
	"Accept-Charset": "utf-8; windows-1250",
	"Keep-Alive": "300",
	"Connection": "keep-alive",
}
"Headers from Internet explorer."

LFFHeaders = {
	"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; cs; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3",
	"Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain",
	"Accept-Language": "cs,en-us;q=0.7,en;q=0.3",
	"Accept-Charset": "utf-8; windows-1250",
	"Keep-Alive": "300",
	"Connection": "keep-alive",
}
"Headers from Firefox 3.6.3 on linux."


hcookies = False
cookies = {}
"Variable where are stored cookies."

#===============================================================================
#= Functions & objects =========================================================
#===============================================================================
def getDomain(url):
	"""
	Parse domain from url.

	@param url: URL
	@type  url: string

	@return: Domain
	@rtype:  string
	"""
	if "://" in url:
		url = url.split("://")[1]
		
	if "/" in url:
		url = url.split("/")[0]

	return url


def getPage(url, get = None, post = None, headers = IEHeaders, handle_cookies = False):
	"""
	Function for easy work with HTTP protocol.

	@param url: URL - if not "://" in url, url will be transformed into "http://" + url
	@type  url: string

	@param get: Params which will be sended as GET.
	@type  get: dictionary

	@param post: Parameters for url. Default None.
	@type  post: dictionary

	@param headers: Headers sended when downloading url. Default IEHeaders.
	@type  headers: dictionary
	@see: IEHeaders
	@see: LFFHeaders
	
	@param handle_cookies: If True, function will use cookies.
						   Cookies are stored in global variable cookies.
						   If you dont want set this parameter to true with every call,
						   you can set module variable hcookies to True.
	@type  handle_cookies: bool
	@see: hcookies

	@return: content of downloaded url
	@rtype: Binary data or text, depends on type of downloaded content.
	"""
	# POST params
	if post != None:
		post = urllib.urlencode(post)
		
	# append GET params to url
	if get != None:
		get = urllib.urlencode(get)
		if "?" in url:
			if url[-1] == "&":
				url += get
			else:
				url += "&" + get
		else:
			url += "?" + get
			
		get = None
	   
	# url protocol check
	if not "://" in url:
		url = "http://" + url

	# add cokies into headers
	if hcookies or handle_cookies:
		domain = getDomain(url)
		if domain in cookies.keys():
			cookie_string = ""
			for key in cookies[domain].keys():
				cookie_string += key + "=" + str(cookies[domain][key]) + "; "
				
			headers["Cookie"] = cookie_string.strip()

	# download page    
	f = urllib2.urlopen(urllib2.Request(url, post, headers))
	data = f.read()

	# simple cookies handling
	if hcookies or handle_cookies:
		cs = f.info().items()   # get header from server
		
		# parse "set-cookie" string
		cookie_string = ""
		for c in cs:
			if c[0].lower() == "set-cookie":
				cookie_string = c[1]
					
		# parse keyword:values
		tmp_cookies = {}
		for c in cookie_string.split(","):
			cookie = c
			if ";" in c:
				cookie = c.split(";")[0]
			cookie = cookie.strip()
			
			cookie = cookie.split("=")
			keyword = cookie[0]
			value = "=".join(cookie[1:])
			
			tmp_cookies[keyword] = value
		
		# append global variable cookis with new cookies
		if len(tmp_cookies) > 0:
			domain = getDomain(url)
			
			if domain in cookies.keys():
				for key in tmp_cookies.keys():
					cookies[domain][key] = tmp_cookies[key] 
			else:
				cookies[domain] = tmp_cookies
			  
		# check for blank cookies
		if len(cookies) > 0:
			for domain in cookies.keys():
				for key in cookies[domain].keys():
					if cookies[domain][key].strip() == "":
						del cookies[domain][key]
				
				if len(cookies[domain]) == 0:
					del cookies[domain]                
	
	f.close()

	return data


def removeTags(txt):
	"""
	Remove tags from text. Every text field between < and > will be deleted.

	@param txt: Text which will be cleared.
	@type  txt: string

	@return: Cleared text.
	@rtype:  string
	"""
	for i in re.findall(r"""<(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+>""", txt):
		txt = txt.replace(i, "")
		
	return txt.strip()


def getVisibleText(txt):
	"""
	Removes tags and text between <title>, <script> and <style> tags.

	@param txt: Text which will be cleared.
	@type  txt: string

	@return: Cleared text.
	@rtype:  string
	"""
	for i in re.findall(r"""<script.*?>[\s\S]*?</.*?script>""", txt):
		txt = txt.replace(i, "")

	for i in re.findall(r"""<style.*?>[\s\S]*?</.*?style>""", txt):
		txt = txt.replace(i, "")

	for i in re.findall(r"""<title.*?>[\s\S]*?</.*?title>""", txt):
		txt = txt.replace(i, "")

	return removeTags(txt)



#===============================================================================
#= Main program ================================================================
#===============================================================================
if __name__ == "__main__":
	print "CheckerTools v" + __version + " (10.09.2011) by Bystroushaak (bystrousak@kitakitsune.org)"