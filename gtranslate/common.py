# coding=utf8

import urllib, urllib2, json

url = "http://translate.google.pt/translate_a/t?%s"

langs = [
  "af","sq","ar","hy","az","eu","be","bn","bs","bg",
  "ca","ceb","zh-CN","hr","cs","da","nl","en","eo","et","tl",
  "fi","fr","gl","ka","de","el","gu","ht","iw","hi","hmn",
  "hu","is","id","ga","it","ja","jw","kn","km","ko","lo",
  "la","lv","lt","mk","ms","mt","mr","no","fa","pl","pt",
  "ro","ru","sr","sk","sl","es","sw","sv","ta","te","th",
  "tr","uk","ur","vi","cy","yi"]
  
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
  request = urllib2.Request(url % parameters, None, head)
  result = urllib2.urlopen(request)

  result = result.read()
  result = result.replace(",,",",\"\",")
  result = result.replace(",,",",\"\",") # XXX triple comas :P
  result = result.replace("[,","[") # XXX triple comas :P
  
  try:
    result = json.loads(result)
  except ValueError:
    print "ValueError! %s" % result
  
  return result