# coding=utf8
#!/usr/bin/env python

import sys, os, urllib, urllib2, json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mylib

# curl http://api.urbandictionary.com/v0/define\?term\=yolo | python -mjson.tool

URL = 'http://api.urbandictionary.com/v0/define?%s'
USAGE = ".ud: find argument required"

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
         if n <= 0:
           n = 1
         l = len(res[u"list"])
         res = res[u"list"][n - 1][u"definition"]
         res = res.replace("\r\n", " ")
         if l > 1 and n < l:
            mylib.print_console("%d found '.ud %s %d' for the next one " % (l,q,n+1))
         mylib.print_console("%s" % res)
      except IndexError :
         mylib.print_console("Not found")
   else:
      mylib.print_console("Not found")
else:
    mylib.print_console(USAGE);
# vim: ts=4:sw=4
