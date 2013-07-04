import feedparser
import re
import sys
import code
import os
import collections
import pickle
import hashlib
import time
import socket
from filelock import FileLock, FileLockException
from mylib import print_console,  print_error, unescape, strip
  
#
# constants
#

FEEDFILE = "feeds.data"
CACHE_LENGTH = 50

#
# set a timeout for the http connection
#
socket.setdefaulttimeout(2)

#
# :(
#

def check_status(f):

  try:
    if f.status == '404':
      print_error("404 Not Found")
      return -1

    if f.bozo == 1:
      # these do not warrant an error
      if (type(f.bozo_exception) not in 
      [feedparser.NonXMLContentType, feedparser.CharacterEncodingOverride]):
        print_error("omg :( %s" % (f.bozo_exception))
        return -1

  except (IndexError, AttributeError):
    print_error("Unable to determine feed status");
    return -1

  return 0

#
# classes
#

class Entry:

  def __init__(self, entry, feed, entryid = None):
    self.entryid = entryid
    self.entry = entry
    self.feed = feed
    self.prehash = entry.title + " " + entry.link
    self.prehash = self.prehash.encode('raw_unicode_escape')
    self.hash = hashlib.md5(self.prehash).hexdigest()
    self.created_at = time.time()

  def __repr__(self):
    return self.hash
    #try:
    #  return ("%05d" % self.entryid) + " " + self.hash + " " + self.entry.published + " " + self.entry.title
    #except AttributeError:
    #  return ("%05d" % self.entryid) + " " + self.hash + " NOTIME " + " " + self.entry.title
  
  def print_me(self, print_summary = False, seen_as_new = False):
    title = self.entry.title
    link = self.entry.link
    
    try:
      summary = unescape(strip(self.entry.summary))
    except AttributeError:
      summary = ""

    if 'published' in self.entry.keys():
      published = self.entry.published.rsplit(' ', 1)[0]
    else:
      published = None

    if seen_as_new:
      str_new = " \x02new!\02 "
    else:
      str_new = " "

    if published is not None:
      print_console("%s%s%s - %s (%s)" % (self.feed.logo, str_new, title, link, published)) 
    else:
      print_console("%s%s%s - %s" % (self.feed.logo, str_new, title, link)) 

    if print_summary:
      for l in summary.split("\n"):
        if len(l) > 0:
          print_console("%s %s" % (self.feed.logo, l))

class Feed:

  def __init__(self, feedid, logo, url):
    self.feedid = feedid
    self.logo = logo
    self.url = url
    self.last = 0
    self.entries = []
    self.seq = 0

  def next(self):
    c = self.seq
    self.seq = self.seq + 1
    return self.seq


  def __str__(self):
    return "%s %s - %s\n" % (self.feedid, self.logo, self.url)
  
  def exists(self, entry):
    for e in self.entries:
      if e.hash == entry.hash:
        return True
    return False

  def add(self, entry):
    e = Entry(entry, self, self.next())
    if not self.exists(e):
      self.entries.append(e)

      #print self.feedid + " len %s %s" % (len(self.entries),  e.__repr__())
      return e
    return None
  
  # n: nth item in the entry list
  def get_item(self, n = 0):
    f = feedparser.parse(self.url)
    
    if check_status(f) == -1:
      print_error("in get_item()")

    try:
      entry = f.entries[n]
    except IndexError:
      print_console("%s Entry %s not available" % (self.logo, n))
      exit(-1)

    e = self.add(entry)
    # is old
    if e is None:
      Entry(entry, self).print_me(print_summary=True)
      
    #is new
    else:
      e.print_me(print_summary=True, seen_as_new=True)

  # n: max number of items to retrieve
  def get_recent(self, n, mark_all_as_read = False):
    f = feedparser.parse(self.url)
    
    if check_status(f) == -1:
      print_error("in get_recent()")

    i = 0
    for entry in f.entries:
      e = self.add(entry)
      if e is None:
        pass
      else:
        e.print_me()
        i = i + 1
        
      if not i < n:
        break

  def mark_all_as_read(self):
    f = feedparser.parse(self.url)
    
    if check_status(f) == -1:
      print_error("in mark_all_as_read()")

    for entry in f.entries:
      e = self.add(entry)


class Reader:

  def __init__(self):    
    self.feeds = {}
    self.load();  
  
  def __str__(self):
    s = "Reader Object:\n"
    for feed in self.feeds.keys():
      s += self.feeds[feed].__str__()
    return s

  def save(self):
    try:
      f = open(FEEDFILE, "w+")
      obj = f
      pickle.dump(self.feeds, obj)
      f.close()

    except Exception as e:
      print_console(e)

  def load(self):
    try:
      f = open(FEEDFILE, "rb")
      obj = pickle.load(f)
      self.feeds = obj
      f.close()
    except IOError as e:
      if e.errno == 2: #ignore when file doesn't exist
        pass
        
    except Exception as e:
      print_console(e)

  def add(self, feedid, logo, url):
    f = Feed(feedid, logo, url)
    self.feeds[feedid] = f
    
  def delete(self, feedid):
    del(feeds[feedid])

#
# global functions
#

# initializes the reader file
def init(mark_all_as_read = False):
  list_a = [
    {"id":"b4chan", "logo":"-4chan /b/-", "url":"http://boards.4chan.org/b/index.rss"},
    {"id":"a4chan", "logo":"-4chan /a/-", "url":"http://boards.4chan.org/a/index.rss"},
    {"id":"g4chan", "logo":"-4chan /g/-", "url":"http://boards.4chan.org/g/index.rss"},
    {"id":"v4chan", "logo":"-4chan /v/-", "url":"http://boards.4chan.org/v/index.rss"},
    {"id":"gif4chan", "logo":"-4chan /gif/-", "url":"http://boards.4chan.org/gif/index.rss"},
    {"id":"pplware", "logo": "11,2PPLWARE", "url":"http://pplware.sapo.pt/feed/"},
    {"id":"apod", "logo": "1,15APOD", "url":"http://apod.nasa.gov/apod.rss"},
    {"id":"tugaleaks", "logo": "14,01TUGALEAKS", "url":"http://feeds.feedburner.com/tugaleaks"},
    {"id":"gunshow", "logo": "0,1Gun Show", "url":"http://www.rsspect.com/rss/gunshowcomic.xml"},
    {"id":"qc", "logo": "10,12QC", "url":"http://www.questionablecontent.net/QCRSS.xml"},
    {"id":"xkcd", "logo": "1,0xkcd", "url":"http://xkcd.com/rss.xml"},
    {"id":"mojang", "logo":"Mojang", "url":"http://mojang.com/feed"},
    {"id":"bukkit", "logo":"bukkit", "url":"http://forums.bukkit.org/forums/bukkit-news.2/index.rss"},
    {"id":"wotd", "logo":"-palavra do dia-", "url":"http://priberam.pt/dlpo/DoDiaRSS.aspx"},
    {"id":"blitz", "logo":"BLITZ.pt", "url":"http://blitz.aeiou.pt/gen.pl?p=rss"},
    {"id":"smbc", "logo":"smbc", "url":"http://www.smbc-comics.com/rss.php"},
    {"id":"ptsec", "logo":"ptsec", "url":"https://ptsec.info/wp/feed/"},
    {"id":"kritzkast", "logo":"kritzkast", "url":"http://www.kritzkast.com/feed?cat=-14"},
    {"id":"tf2", "logo":"TF2 Official Blog", "url":"http://www.teamfortress.com/rss.xml"},
    {"id":"universetoday", "logo":"Universe Today", "url":"http://www.universetoday.com/feed/"},
    {"id":"hackernews", "logo":"Hacker News", "url":"http://news.ycombinator.com/rss"},
    {"id":"sceper", "logo":"Sceper", "url":"http://sceper.eu/feed"},
    {"id":"thepiratebay", "logo":"ThePirateBay", "url":"https://rss.thepiratebay.se/0"},
    {"id":"hackaday", "logo":"Hack A Day", "url":"http://www.hackaday.com/rss.xml"},
    {"id":"astronomycast", "logo":"Astronomy Cast", "url":"http://feeds.feedburner.com/astronomycast"},
    {"id":"yt_jamesnintendonerd", "logo":"1,00,4 JamesNintendoNerd", "url":"http://www.youtube.com/rss/user/JamesNintendoNerd/videos.rss"},
    {"id":"blol", "logo":"0,13BLOL", "url":"http://blol.org/feed"},
    ##{"id":"", "logo":"", "url":""},
  ]

  for a in list_a:
    r.add(a["id"], a["logo"], a["url"])

  if mark_all_as_read:
    for f in r.feeds:
      print_error("Init ", r.feeds[f].feedid)
      r.feeds[f].mark_all_as_read()
    print_console("All unseen items marked as read.")

  r.save()
  
# prints recents items of a certain feedid
def item(feedid, n):
  exists = False
  for f in r.feeds:
    if r.feeds[f].feedid == feedid:
      exists = True
      r.feeds[f].get_item(n)
      r.save()
      
  if not exists:
    print_console("Feed %s doesn't exist! :(" % feedid)

# prints recents items of a certain feedid
def recent(feedid, n):
  exists = False

  for f in r.feeds:
    if r.feeds[f].feedid == feedid:
      exists = True
      r.feeds[f].get_recent(n, mark_all_as_read = True)
      r.save()

  if not exists:
    print_console("Feed %s doesn't exist! :(" % feedid)

# removes marked as seen from all entries of a certain feedid
def reset(feedid):
  exists = False
  for f in r.feeds:
    if r.feeds[f].feedid == feedid:
      exists = True
      r.feeds[f].entries = []
      print_console("Cleared feed %s" % feedid)

  if not exists:
    print_console("Feed %s doesn't exist! :(" % feedid)
  else:
    r.save()

# usage
def usage():
  print_console("Usage: !feedname [n]")
  exit(-1)

#
# main(ly ugly argument parsing)
#
#print_error("%s pid start " % os.getpid())
try:
  with FileLock(FEEDFILE, timeout=20):
    r = Reader()

    l = len(sys.argv)
    if l < 2:
      usage()

    arg1 = sys.argv[1]
    if arg1 == 'feed' or arg1 == 'new':
      if l < 3:
        usage()

      feedid = sys.argv[2]
      n = 0
      if l >= 3:
        try: 
          n = int(sys.argv[3])
        except ValueError:
          n = 0
        except IndexError:
          n = 0

      if arg1 == 'feed':  
        if n < 0:
          n = 0
        item(feedid, n)
      elif arg1 == 'new':
        if n == 0:
          n = 1
        feedids = sys.argv[2:]
        for feedid in feedids:
          recent(feedid, n)

    elif arg1 == 'init':
      init(mark_all_as_read = True)

    else:
      usage()

except FileLockException:
  print_error("Lock Timeout")

#print_error("%s pid stop " % os.getpid())
