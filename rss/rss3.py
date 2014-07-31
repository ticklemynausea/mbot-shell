# encoding=utf8
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
from xml.sax import SAXParseException
from filelock import FileLock, FileLockException

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console,  print_error, unescape, strip

#
# socket timeout for http connection
#
socket.setdefaulttimeout(5)

#
# constants
#

CACHE_LENGTH = 50
FEEDS = [
  {"id":"b4chan", "logo":"-4chan /b/-", "url":"http://boards.4chan.org/b/index.rss"},
  {"id":"a4chan", "logo":"-4chan /a/-", "url":"http://boards.4chan.org/a/index.rss"},
  {"id":"g4chan", "logo":"-4chan /g/-", "url":"http://boards.4chan.org/g/index.rss"},
  {"id":"v4chan", "logo":"-4chan /v/-", "url":"http://boards.4chan.org/v/index.rss"},
  {"id":"gif4chan", "logo":"-4chan /gif/-", "url":"http://boards.4chan.org/gif/index.rss"},
  {"id":"pplware", "logo": "11,2PPLWARE", "url":"http://pplware.sapo.pt/feed/"},
  {"id":"apod", "logo": "1,15APOD", "url":"http://apod.nasa.gov/apod.rss"},
  {"id":"tugaleaks", "logo": "14,01TUGALEAKS", "url":"http://feeds.feedburner.com/tugaleaks"},
  {"id":"gunshow", "logo": "0,1Gun Show", "url":"http://www.rsspect.com/rss/gunshowcomic.xml"},
#  {"id":"qc", "logo": "10,12QC", "url":"http://www.questionablecontent.net/QCRSS.xml"},
  {"id":"xkcd", "logo": "1,0xkcd", "url":"http://xkcd.com/rss.xml"},
  {"id":"mojang", "logo":"Mojang", "url":"http://mojang.com/feed"},
  {"id":"bukkit", "logo":"bukkit", "url":"http://forums.bukkit.org/forums/bukkit-news.2/index.rss"},
  {"id":"spigot", "logo":"spigot", "url":"http://www.spigotmc.org/forums/news-and-announcements.2/index.rss"},
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
  {"id":"yt_jamesnintendonerd", "logo":"1,0YOU0,4TUBE JamesNintendoNerd", "url":"http://www.youtube.com/rss/user/JamesNintendoNerd/videos.rss"},
  {"id":"skepticsguide", "logo":"Skeptics' Guide to the Universe", "url":"http://www.theskepticsguide.org/rss.xml"},
  {"id":"fakescience", "logo":"Fake Science", "url":"http://fakescience.tumblr.com/rss"},
  {"id":"vice", "logo":"Vice PT", "url":"http://www.vice.com/pt/rss"},
  {"id":"weebls", "logo":"Weebls' Stuff", "url":"http://www.weebls-stuff.com/misc/rss/toons.php"},
  {"id":"abola", "logo":"A Bola", "url":"http://www.abola.pt/rss/index.aspx"},
  {"id":"blol", "logo":"blol", "url":"http://blol.org/feed"},
  {"id":"hackern", "logo":"hacker news", "url":"https://news.ycombinator.com/rss"},
  {"id":"sfocus", "logo":"SecurityFocus", "url":"http://www.securityfocus.com/rss/news.xml"},
  {"id":"zz_resultados", "logo":"ZeroZero: Resultados", "url":"http://www.zerozero.pt/rss/resultados.php"},
  {"id":"zz_noticias", "logo":"ZeroZero", "url":"http://www.zerozero.pt/rss/noticias.php"},
  {"id":"mcpt", "logo":"Blog MCPT", "url":"http://blog.minecraft.pt/feed/"},
  {"id":"feup", "logo":"feup news", "url":"http://sigarra.up.pt/feup/pt/noticias_web.rss"},
  {"id":"vilametal", "logo":"vilametal", "url":"http://vilametal.blogspot.com/feeds/posts/default?alt=rss"},
  {"id":"blabbermouth", "logo":"blabbermouth.net", "url":"http://feeds.feedburner.com/blabbermouth"},
  {"id":"yt_tso", "logo":"YouTube ThanatoSchizO", "url":"http://youtube.com/rss/user/thanatoschizo"},
  {"id":"yt_inl", "logo":"YouTube InsomniousNightLift", "url":"http://youtube.com/rss/user/insomniousnightlift"},
  {"id":"mcpt-dev", "logo":"13Minecraftia! RSS-DEV", "url":"https://bitbucket.org/ticklemynausea/minecraftia/rss?token=7bd3166f6d3489a0a90060a9509d5782"},
  {"id":"mcpt-fb", "logo":"0,2facebook minecraft.pt", "url":"https://www.facebook.com/feeds/notifications.php?id=208693402526378&viewer=1042203820&key=AWjYVLgN8nQXI2Vl&format=rss20"},
  {"id":"irssi-github", "logo":"irssi-github", "url":"https://github.com/irssi/irssi/commits/master.atom"}
]
#
# :(
#

def check_status(f, feedid):

  try:
    if f.status == '404':
      print_error("404 Not Found")
      return -1

    if f.bozo == 1:
      # these do not warrant an error
      if (type(f.bozo_exception) not in 
      [feedparser.NonXMLContentType, feedparser.CharacterEncodingOverride, SAXParseException]):
        print_error("omg :( %s %s " % (type(f.bozo_exception), f.bozo_exception))
        return -1

  except (IndexError, AttributeError):
    print_error("%s: Unable to determine feed status" % feedid);
    return -1

  return 0

#
# classes
#

class Entry:

  # Constructor
  def __init__(self, entry, feed):
    self.entry = entry
    self.feed = feed
    self.prehash = entry.title + " " + entry.link
    self.prehash = self.prehash.encode('raw_unicode_escape')
    self.hash = hashlib.md5(self.prehash).hexdigest()
    self.created_at = time.time()

  # Each entry is represented by its hash
  def __repr__(self):
    return self.hash
    #try:
    #  return ("%05d" % self.entryid) + " " + self.hash + " " + self.entry.published + " " + self.entry.title
    #except AttributeError:
    #  return ("%05d" % self.entryid) + " " + self.hash + " NOTIME " + " " + self.entry.title
  
  # Prints information about this Entry
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
        l = l.strip()
        if len(l) > 0:
          print_console("%s %s" % (self.feed.logo, l))

class Feed:
  
  # Constructor
  def __init__(self, feedid, logo, url):
    self.feedid = feedid
    self.logo = logo
    self.url = url
    self.feedfile = "rss-data/%s.feeddata" % self.feedid
    self.entries = []
    self.load()


  def __str__(self):
    return "%s %s - %s\n" % (self.feedid, self.logo, self.url)

  # Saves this feed from a file
  def save(self):
    try:
      with FileLock(self.feedfile, timeout=5):
        f = open(self.feedfile, "w+")
        obj = f
        pickle.dump(self.entries, obj)
        f.close()

    except Exception as e:
      print_console(e)

    except FileLockException:
      print_error("Lock Timeout")


  # Loads this feed from a file
  def load(self):
    try:
      with FileLock(self.feedfile, timeout=5):
        f = open(self.feedfile, "rb")
        obj = pickle.load(f)
        self.entries = obj
        f.close()

    except IOError as e:
      if e.errno == 2: #ignore when file doesn't exist
        pass

    except Exception as e:
      print_error(e)

    except FileLockException:
      print_error("Lock Timeout")

  # Checks if an entry already exists in the entry list for this feed
  def exists(self, entry):
    for e in self.entries:
      if e.hash == entry.hash:
        return True
    return False
  
  # Adds a new entry to this feed
  # returns None if it's not a new entry
  def add(self, entry):
    e = Entry(entry, self)
    if not self.exists(e):
      self.entries.append(e)

      #print self.feedid + " len %s %s" % (len(self.entries),  e.__repr__())
      return e
    return None
  
  # Prints the nth item in the entry list
  def get_item(self, n = 0):
    f = feedparser.parse(self.url)
    
    if check_status(f, self.feedid) == -1:
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
      
    #is newcha
    else:
      e.print_me(print_summary=True, seen_as_new=True)

  # Prints recent items in the feed list
  # n: max number of items to retrieve
  def get_recent(self, n, mark_all_as_read = False):
    f = feedparser.parse(self.url)
    
    if check_status(f, self.feedid) == -1:
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
    
    if check_status(f, self.feedid) == -1:
      print_error("in mark_all_as_read()")

    for entry in f.entries:
      e = self.add(entry)



#
# global functions
#

# initializes the reader files
def init():

  for feed in FEEDS:
    f = Feed(feed["id"], feed["logo"], feed["url"])
    print_console("Init %s" % f.feedid)
    f.mark_all_as_read()
    f.save()
  print_console("All unseen items marked as read.")

  
# prints recents items of a certain feedid
def item(feedid, n):
  exists = False
  for feed in FEEDS:
    if feed["id"] == feedid:
      f = Feed(feed["id"], feed["logo"], feed["url"])
      exists = True
      f.get_item(n)
      f.save()
      
  if not exists:
    print_console("Feed %s doesn't exist! :(" % feedid)
  
# prints recents items of a certain feedid
def recent(feedid, n):
  exists = False
  for feed in FEEDS:
    if feed["id"] == feedid:
      f = Feed(feed["id"], feed["logo"], feed["url"])
      exists = True
      f.get_recent(n, mark_all_as_read = True)
      f.save()

  if not exists:
    print_console("Feed %s doesn't exist! :(" % feedid)


# removes marked as seen from all entries of a certain feedid
def reset(feedid):
  exists = False
  for feed in FEEDS:
    if feed["id"] == feedid:
      f = Feed(feed["id"], a["logo"], a["url"])
      exists = True
      f.entries = []
      f.save
      print_console("Cleared feed %s" % feedid)

  if not exists:
    print_console("Feed %s doesn't exist! :(" % feedid)


# usage
def usage():
  print_console("Usage: !feedname [n]")
  exit(-1)

#
# main(ly ugly argument parsing)
#
#print_error("%s pid start " % os.getpid())

l = len(sys.argv)
if l < 2:
  usage()

arg1 = sys.argv[1]
if arg1 == 'feed' or arg1 == 'new' or arg1 == 'new+':
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
    feedids = sys.argv[2:]
    for feedid in feedids:
      recent(feedid, 1)
  elif arg1 == 'new+':
    feedids = sys.argv[2:]
    for feedid in feedids:
      recent(feedid, 10)

elif arg1 == 'init':
  init()

else:
  usage()
