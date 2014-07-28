# coding=utf8
#!/usr/bin/env python


"""
.tr [form(default:auto)] <to> <texto>
.tr sem args: halp
"""

import sys, os, urllib, urllib2, json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mylib


URL = "http://translate.google.pt/translate_a/t?%s"

LANGS = [
  "af","sq","ar","hy","az","eu","be","bn","bs","bg",
  "ca","ceb","zh-CN","hr","cs","da","nl","en","eo","et","tl",
  "fi","fr","gl","ka","de","el","gu","ht","iw","hi","hmn",
  "hu","is","id","ga","it","ja","jw","kn","km","ko","lo",
  "la","lv","lt","mk","ms","mt","mr","no","fa","pl","pt",
  "ro","ru","sr","sk","sl","es","sw","sv","ta","te","th",
  "tr","uk","ur","vi","cy","yi"]

def help():
  mylib.print_console(".tr [from] <to> <text>")
  mylib.print_console("languages: " + " ".join(LANGS))

if __name__=="__main__":
  q = sys.argv[1:]
  l = len(q)

  if l < 2 :
    help()
    exit(0)

  sl = q[0]

  if sl not in LANGS :
    help()
    exit(0)

  tl = q[1]
  if tl not in LANGS :
    tl = sl
    sl = "auto"
    q = " ".join(q[1:])
  else:
    q = " ".join(q[2:])

  par = {
    'client' : 't',
    'hl' : 'pt-PT',
    'ie' : 'UTF-8',
    'oc' : '1',
    'oe' : 'UTF-8',
    'otf': '1',

    'q'  : q,
    'sc' : '2',
    'sl' : sl, # input language (en, ...)
    'ssel':'0',
    'tl' : tl,   # output language
    'tsel': '0'
  }

  par = urllib.urlencode(par)
  head= { 'User-Agent' : 'YoMomma/6.9' }
  req = urllib2.Request(URL % par, None, head)
  res = urllib2.urlopen(req)

  res = res.read()
  res = res.replace(",,",",\"\",")
  res = res.replace(",,",",\"\",") # XXX triple comas :P
  res = json.loads(res)
  
  mylib.print_console("\002[%s>%s]\002 %s" % (res[2], tl, res[0][0][0]))


# vim: ts=4:sw=4
