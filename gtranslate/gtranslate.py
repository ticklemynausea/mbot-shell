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

def parse_args():
  args = sys.argv[1:]
  l = len(args)

  if l < 2 :
    help()
    exit(0)

  input_lang = args[0]

  if input_lang not in LANGS :
    help()
    exit(0)

  output_lang = args[1]
  if output_lang not in LANGS :
    output_lang = input_lang
    input_lang = "auto"
    args = " ".join(args[1:])
  else:
    args = " ".join(args[2:])

  return (input_lang, output_lang, args)

def api_request(input_lang, output_lang, args):
  parameters = {
    'client' : 't',
    'hl' : 'pt-PT',
    'ie' : 'UTF-8',
    'oc' : '1',
    'oe' : 'UTF-8',
    'otf': '1',

    'q'  : args,
    'sc' : '2',
    'sl' : input_lang, # input language (en, ...)
    'ssel':'0',
    'tl' : output_lang,   # output language
    'tsel': '0'
  }

  parameters = urllib.urlencode(parameters)
  head = { 'User-Agent' : 'YoMomma/6.9' }
  request = urllib2.Request(URL % parameters, None, head)
  result = urllib2.urlopen(request)

  result = result.read()
  result = result.replace(",,",",\"\",")
  result = result.replace(",,",",\"\",") # XXX triple comas :P
  result = json.loads(result)
  
  return result

def output(output_lang, result):
  mylib.print_console("\002[%s>%s]\002 %s" % (result[2], output_lang, result[0][0][0]))

if __name__=="__main__":

  (input_lang, output_lang, args) = parse_args()
  result = api_request(input_lang, output_lang, args)
  output(output_lang, result);
