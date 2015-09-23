# encoding=utf8
import feedparser
import sys
import os
import pickle
import hashlib
import time
import socket
from xml.sax import SAXParseException
from filelock import FileLock, FileLockException

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console, print_error, unescape, strip

#
# socket timeout for http connection
#
socket.setdefaulttimeout(5)

#
# constants
#
PATHFILENAME = "./rss-data/%s.feeddata"
CACHE_LENGTH = 50
FEEDS = [
  {"id": "pplware", "logo": "\x0311,2PPLWARE\x03", "url": "http://pplware.sapo.pt/feed/"},
  {"id": "apod", "logo": "\x031,15APOD\x03", "url": "http://apod.nasa.gov/apod.rss"},
  {"id": "tugaleaks", "logo": "\x0314,01\x02TUGALEAKS\x02\x03", "url": "http://feeds.feedburner.com/tugaleaks"},
  {"id": "gunshow", "logo": "\x030,1Gun Show\x03", "url": "http://www.rsspect.com/rss/gunshowcomic.xml"},
  {"id": "qc", "logo": "\x0310,12QC\x03", "url": "http://www.questionablecontent.net/QCRSS.xml"},
  {"id": "xkcd", "logo": "\x031,0xkcd\x03", "url": "http://xkcd.com/rss.xml"},
  {"id": "mojang", "logo": "\x02Mojang\x02", "url": "http://mojang.com/feed"},
  {"id": "bukkit", "logo": "\x02bukkit\x02", "url": "http://forums.bukkit.org/forums/bukkit-news.2/index.rss"},
  {"id": "spigot", "logo": "\x02spigot\x02", "url": "http://www.spigotmc.org/forums/news-and-announcements.2/index.rss"},
  {"id": "wotd", "logo": "-palavra do dia-", "url": "http://priberam.pt/dlpo/DoDiaRSS.aspx"},
  {"id": "blitz", "logo": "\x02BLITZ.pt\x02", "url": "http://blitz.aeiou.pt/gen.pl?p=rss"},
  {"id": "smbc", "logo": "\x02smbc\x02", "url": "http://www.smbc-comics.com/rss.php"},
  {"id": "kritzkast", "logo": "\x02kritzkast\x02", "url": "http://www.kritzkast.com/feed?cat=-14"},
  {"id": "tf2", "logo": "\x02TF2 Official Blog\x02", "url": "http://www.teamfortress.com/rss.xml"},
  {"id": "universetoday", "logo": "\x02Universe Today\x02", "url": "http://www.universetoday.com/feed/"},
  {"id": "hackernews", "logo": "\x02Hacker News\x02", "url": "http://news.ycombinator.com/rss"},
  {"id": "thepiratebay", "logo": "\x02ThePirateBay\x02", "url": "http://rss.thepiratebay.se/0"},
  {"id": "hackaday", "logo": "\x02Hack A Day\x02", "url": "http://www.hackaday.com/rss.xml"},
  {"id": "astronomycast", "logo": "\x02Astronomy Cast\x02", "url": "http://feeds.feedburner.com/astronomycast"},
  {"id": "yt_jamesnintendonerd", "logo": "\x031,0YOU\x030,4TUBE\x03 JamesNintendoNerd", "url": "http://www.youtube.com/rss/user/JamesNintendoNerd/videos.rss"},
  {"id": "skepticsguide", "logo": "\x02Skeptics' Guide to the Universe\x02", "url": "http://www.theskepticsguide.org/rss.xml"},
  {"id": "fakescience", "logo": "\x02Fake Science\x02", "url": "http://fakescience.tumblr.com/rss"},
  {"id": "vice", "logo": "\x02Vice PT\x02", "url": "http://www.vice.com/pt/rss"},
  {"id": "weebls", "logo": "\x02Weebls' Stuff\x02", "url": "http://www.weebls-stuff.com/misc/rss/toons.php"},
  {"id": "abola", "logo": "\x02A Bola\x02", "url": "http://www.abola.pt/rss/index.aspx"},
  {"id": "blol", "logo": "\x02blol\x02", "url": "http://blol.org/feed"},
  {"id": "sfocus", "logo": "\x02SecurityFocus\x02", "url": "http://www.securityfocus.com/rss/news.xml"},
  {"id": "zz_resultados", "logo": "\x02ZeroZero: Resultados\x02", "url": "http://www.zerozero.pt/rss/resultados.php"},
  {"id": "zz_noticias", "logo": "\x02ZeroZero\x02", "url": "http://www.zerozero.pt/rss/noticias.php"},
  {"id": "mcpt", "logo": "\x02Blog MCPT\x02", "url": "http://blog.minecraft.pt/feed/"},
  {"id": "feup", "logo": "\x02feup news\x02", "url": "http://sigarra.up.pt/feup/pt/noticias_web.rss"},
  {"id": "vilametal", "logo": "\x02vilametal\x02", "url": "http://vilametal.blogspot.com/feeds/posts/default?alt=rss"},
  {"id": "blabbermouth", "logo": "\x02blabbermouth.net\x02", "url": "http://feeds.feedburner.com/blabbermouth"},
  {"id": "yt_tso", "logo": "YouTube ThanatoSchizO", "url": "http://youtube.com/rss/user/thanatoschizo"},
  {"id": "yt_inl", "logo": "YouTube InsomniousNightLift", "url": "http://youtube.com/rss/user/insomniousnightlift"},
  {"id": "mcpt-dev", "logo": "\x0313Minecraftia! RSS-DEV\x03", "url": "https://bitbucket.org/ticklemynausea/minecraftia/rss?token=7bd3166f6d3489a0a90060a9509d5782"},
  {"id": "mcpt-fb", "logo": "\x030,2facebook minecraft.pt\x03", "url": "https://www.facebook.com/feeds/notifications.php?id=208693402526378&viewer=1042203820&key=AWjYVLgN8nQXI2Vl&format=rss20"},
  {"id": "irssi-github", "logo": "\x02irssi-github\x02", "url": "https://github.com/irssi/irssi/commits/master.atom"}
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
      if (type(f.bozo_exception) not in [feedparser.NonXMLContentType, feedparser.CharacterEncodingOverride, SAXParseException]):
        print_error("omg :( %s %s " % (type(f.bozo_exception), f.bozo_exception))
        return -1

  except (IndexError, AttributeError):
    print_error("%s: Unable to determine feed status" % feedid)
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
    # try:
    #  return ("%05d" % self.entryid) + " " + self.hash + " " + self.entry.published + " " + self.entry.title
    # except AttributeError:
    #  return ("%05d" % self.entryid) + " " + self.hash + " NOTIME " + " " + self.entry.title

  # Prints information about this Entry
  def print_me(self, print_summary=False, seen_as_new=False):
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
      print_console("%s%s%s - \x1f%s\x1f (%s)" % (self.feed.logo, str_new, title, link, published))
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
    self.feedfile = PATHFILENAME % self.feedid
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
      # ignore when file doesn't exist
      if e.errno == 2:
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

      # print self.feedid + " len %s %s" % (len(self.entries),  e.__repr__())
      return e
    return None

  # Prints the nth item in the entry list
  def get_item(self, n=0):
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

    # is new
    else:
      e.print_me(print_summary=True, seen_as_new=True)

  # Prints recent items in the feed list
  # n: max number of items to retrieve
  def get_recent(self, n, mark_all_as_read=False):
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

  if not os.path.exists("./rss-data"):
    os.makedirs("./rss-data")

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
      f.get_recent(n, mark_all_as_read=True)
      f.save()

  if not exists:
    print_console("Feed %s doesn't exist! :(" % feedid)


# removes marked as seen from all entries of a certain feedid
def reset(feedid):
  exists = False
  for feed in FEEDS:
    if feed["id"] == feedid:
      f = Feed(feed["id"], feed["logo"], feed["url"])
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
# print_error("%s pid start " % os.getpid())

# # #
sys.setrecursionlimit(1500)

l = len(sys.argv)
if l < 2:
  usage()

arg1 = sys.argv[1]
if arg1 in ["feed", "new", "new+"]:
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
