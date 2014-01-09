import re
import sys
import os
import pytwitter

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console, unescape
from apikeys import consumer_key, consumer_secret, access_token_key, access_token_secret

L = "0,10twitter"

def search(query, n):
  try:
    results = t.GetSearch(term = query, result_type = "recent", count = 15)
    if not results:
      print_console("%s No results for %s" % (L, query))
      exit(-1)
    else:
      user = results[n].GetUser()._screen_name
      tweet = unescape(results[n].GetText()).replace('\n', ' ')
      print_console("%s @%s: %s" % (L, user, tweet))
  except IndexError:
    print_console("%s Error: YOU'VE GONE TOO FAR (keep below 15)" % (L))
    exit(-1)


def getTweet(user, n):
  try:
    username = t.GetUser(None, user)._screen_name
    tweets = t.GetUserTimeline(None, screen_name = username, count = 100)
    if not tweets:
      print_console("%s User: %s has no tweets" % (L, username))
      exit(-1)
    else:
      tweet = tweets[n].GetText()
      tweet = unescape(tweet).replace('\n', ' ')
      print_console("%s @%s: %s" % (L, username, tweet))
  except IndexError:
    print_console("%s Error: YOU'VE GONE TOO FAR (keep below 100)" % (L))
    exit(-1)


def usage():
  print_console("%s Usage: !twitter username [n] || Search: !twitter #hashtag [n]" % L)
  exit(-1)

if len(sys.argv) < 2:
  usage()

query = sys.argv[1]
try:
  n = int(sys.argv[2])
except (IndexError, ValueError):
  n = 0

try:
  t = pytwitter.Api(consumer_key,
                    consumer_secret,
                    access_token_key,
                    access_token_secret
                   )
          
  if (query[0] == '#'):
    search(query, n)
  else:
    getTweet(query, n)

except pytwitter.TwitterError as e:
  print_console("%s nope" % L)
  #print_console("%s Error: %s" % (L, e))
  print >> sys.stderr, "Twitter error %s" % e
  exit(-1)
