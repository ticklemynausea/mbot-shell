# coding=utf8
#!/usr/bin/env python

import sys, os, urllib, urllib2, json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mylib

# curl http://api.urbandictionary.com/v0/define\?term\=yolo | python -mjson.tool

URL = 'http://api.urbandictionary.com/v0/define?%s'

def str_is_int(s):
    try:
        n = int(s)
        return (True, n)
    except ValueError:
        return (False, s)

if __name__=="__main__" and len(sys.argv) > 1:
	p, n = str_is_int(sys.argv[-1])

	if p :
		q = " ".join(sys.argv[1:-1])
	else :
		n, q = 1, " ".join(sys.argv[1:])
	
	par = urllib.urlencode({'term': q })
	res = urllib2.urlopen(urllib2.Request(URL % par))

	res = json.load(res)
	typ = res[u"result_type"]

	if typ == "exact" :
		try:
			l = len(res[u"list"])
			res = res[u"list"][n - 1][u"definition"]
			res = res.replace("\r\n", " ")
			mylib.print_console("\002%d/%d\002  %s" % (n,l,res))
		except IndexError :
			pass

# vim: ts=4:sw=4
