import pylast 
import sys
import os
import code
import re
import pickle

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console
from apikeys import api_key, api_secret

LEL = "0,5last.fm"
NUM_EVENTS = 5
USERFILE = '/home/irc/mbot/lastfm-data/lastfm.users'
CHART_LENGTH = 10
PRETTY_BAR = ["[4====            ]",
              "[4====7====        ]",
              "[4====7====8====    ]",
              "[4====7====8====9====]",
              "[                ]"]

def man():
  print_console(LEL + " available commands:")
  print_console(".np [username] | .setuser <username> | .compare [username] <username2>")
  print_console("!lastfm artistinfo|artistevents <artist name>")
  print_console("!lastfm userinfo|topartists|topalbums|weeklyartists|weeklyalbums [username]")
  exit(-1);

class LastFM:

  def __init__(self, proxy_host = None, proxy_port = None, proxy_enabled = False):
    api = pylast.LastFMNetwork(api_key, api_secret)
    if proxy_enabled:
      api.enable_proxy(host = proxy_host, port = proxy_port)
    
    self.api = api
    self.known_users = {}
  
  def save_user(self, nick, user):
    self.known_users[nick] = user
    try:  
      f = open(USERFILE, "w+")
      pickle.dump(self.known_users, f)
      f.close()

    except Exception as e:
      print e
      return False
    
    return True

  def load_users(self):
    try:
      f = open(USERFILE, "rb")
      self.known_users = pickle.load(f)
      f.close()
      
    except IOError as e:
      if e.errno == 2:
        return True # ignore if file doesn't exist.
      return False
      
    return True

  def get_user_by_nick(self, nick):
    self.load_users()
    try:
      user = self.known_users[nick]
    except KeyError:
      user = None
    
    return user


  def get_user_info(self, user):
    try:
      ui = self.api.get_user(user).get_info()
      
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)
    
    print_console(LEL + " Profile info for %s (%s, %s, %s) - Country: %s - Registered: %s - Play count: %s -- %s" % (ui['name'], ui['realname'], ui['age'], ui['gender'], ui['country'], ui['registered'], ui['playcount'], ui['url']))

  def get_top_artists(self, user):
    try:
      artist_list = self.api.get_user(user).get_top_artists()
      
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)
      
    if len(artist_list) == 0:
      print_console(LEL + " No artists found in %s's weekly charts :(" % user)
      exit(-1)

    parsed_list = ["" + i.item.__str__() + " (" + str(i.weight) + ")" for i in artist_list[:CHART_LENGTH]]

    chart_text = ", ".join(parsed_list);
    print_console(LEL + " Top %d artists for %s: %s" % (CHART_LENGTH, user, chart_text))

  def get_top_albums(self, user):
    try:
      album_list = self.api.get_user(user).get_top_albums()
      
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)
      
    if len(album_list) == 0:
      print_console(LEL + " No albums found in %s's weekly charts :(" % user)
      exit(-1)

    parsed_list = ["" + i.item.__str__() + " (" + str(i.weight) + ")" for i in album_list[:CHART_LENGTH]]

    chart_text = ", ".join(parsed_list);
    print_console(LEL + " Top %d albums for %s: %s" % (CHART_LENGTH, user, chart_text))
  
  
  def get_weekly_artist_charts(self, user):
    try:
      artist_list = self.api.get_user(user).get_weekly_artist_charts()
      
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)
      
    if len(artist_list) == 0:
      print_console(LEL + " No artists found in %s's weekly charts :(" % user)
      exit(-1)

    parsed_list = ["" + i.item.__str__() + " (" + str(i.weight) + ")" for i in artist_list[:CHART_LENGTH]]

    chart_text = ", ".join(parsed_list);
    print_console(LEL + " Weekly Top %d artists for %s: %s" % (CHART_LENGTH, user, chart_text))
    
  def get_weekly_album_charts(self, user):
    try:
      album_list = self.api.get_user(user).get_weekly_album_charts()
      
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)
      
    if len(album_list) == 0:
      print_console(LEL + " No albums found in %s's weekly charts :(" % user)
      exit(-1)

    parsed_list = ["" + i.item.__str__() + " (" + str(i.weight) + ")" for i in album_list[:CHART_LENGTH]]

    chart_text = ", ".join(parsed_list);
    print_console(LEL + " Weekly Top %d albums for %s: %s" % (CHART_LENGTH, user, chart_text))
  
  def compare_users(self, user, user2):
    try:
      comparison = self.api.get_user(user).compare_with_user(user2)
      
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)

    comparison_index = round(float(comparison[0]),2)*100
    if comparison_index < 1.0:
      bar = PRETTY_BAR[4]
    else:
      bar = PRETTY_BAR[int(comparison_index / 25.01)]

    artist_list = comparison[1]
    if artist_list:
      parsed_list = [str(item) for item in artist_list]
      chart_text = ", ".join(parsed_list);
    else:
      chart_text = "N/A"

    print_console(LEL + " Comparison: %s %s %s: Similarity: %d%% - Common Artists: %s" % (user, bar, user2, comparison_index, chart_text))

  def get_artist_info(self, artist):
    try:
      artist_info = self.api.get_artist(artist)

      bio = artist_info.get_bio_summary()
      if bio != None:
        bio = re.sub('<[^<]+?>', '', bio)
      
      name = artist_info.get_name()
      listener_count = artist_info.get_listener_count()
      
      
      tags = artist_info.get_top_tags()
      tag_text = ""
      if tags != []:
        tag_text = ", ".join([tag.item.__str__() for tag in tags[:10]])
        tag_text = "Tags: %s." % tag_text

      similars = artist_info.get_similar()
      similars_text = ", ".join([similar.item.__str__() for similar in similars[:10]])

      print_console(LEL + " %s (%d listeners). %s" % (name, listener_count, tag_text))
      print_console("Similar Artists: %s" % (similars_text))
      
      if bio != None:
        print_console(bio)
    
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)

  def get_artist_events(self, artist):
    try:
      artist_info = self.api.get_artist(artist)
      artist_events = artist_info.get_upcoming_events()

      
      #list comprehensiion wont do cause EXCEPTIONS
      events_str = ""
      n = 0
      for event in artist_events:
        try:
          e_date = event.get_start_date()
          e_name = event.get_title()
          e_url = event.get_url()
          
          events_str += " - %s: %s - %s\n" %(e_date[:-9], e_name, e_url)
          n = n + 1
          
          if n >= NUM_EVENTS:
            break
        except pylast.WSError:
          pass

      if n > 0:
        print_console(LEL + " events for %s:" % artist_info.get_name())
        print_console(events_str)
      else:
        print_console(LEL + " no events found for artist %s." % artist_info.get_name())

    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)
  
  def get_now_playing(self, artist):
    try:
      api_user = self.api.get_user(user)
      track = api_user.get_now_playing()
      
    except pylast.WSError as e:
      print_console(LEL + " WSError %s: %s" % (e.status,e.details))
      exit(-1)

    if track is None:
      print_console(LEL + " %s doesn't seem to be playing anything right now" % user)
    else:

      tags = track.get_top_tags()
      if not tags:
        tags = track.artist.get_top_tags()
      track = track.get_add_info(user.__str__())
      
      if track.userloved == "1":
        loved = " 13<3"
      else:
        loved = ""
      
      try:
        playcount = int(track.userplaycount)
      except (ValueError, TypeError):
        playcount = 1
      
      name = track.__str__()
      
      if tags != []:
        tags = ", ".join([t.item.__str__() for t in tags[:5]])
        s = " %s is now playing: %s (%d plays%s, %s)" % (user, name, playcount, loved, tags)
      else:
        s = " %s is now playing: %s (%d plays%s)" % (user, name, playcount, loved)

      print_console(LEL + s)

  def set_user(self, nick, user):

    if self.load_users() == True and self.save_user(nick, user) == True:
      print_console(LEL + " %s's username is set to %s" % (nick, user))
    else:
      print_console(LEL + " could not set %s's username to %s" % (nick, user))

 
lastfm = LastFM()

  
if len(sys.argv) < 3:
  man()

  

mask = sys.argv[1]
nick = mask.split("!")[0]
query = sys.argv[2]

if query == "compare":

  if len(sys.argv) < 4:
    print_console(LEL + " First set your username with .setuser. Alternatively use .compare <username1> <username2>")
    exit(-1)

  elif len(sys.argv) < 5:
    user = lastfm.get_user_by_nick(nick)
    user2 = sys.argv[3]
    
    if user == None:
      print_console(LEL + " First set your username with .setuser. Alternatively use .compare <username1> <username2>")
      exit(-1)
      
  else:
    user = sys.argv[3]
    user2 = sys.argv[4]

  
if query in ("artistinfo", "artistevents"):
  if len(sys.argv) < 4:
    print_console(LEL + " !lastfm artistinfo|artistevents <artist name>")
    exit(-1)
  else:
    artist = " ".join(sys.argv[3:])

if query == "nowplaying":
  if len(sys.argv) < 4:
    user = lastfm.get_user_by_nick(nick)
    if user == None:
      print_console(LEL + " First set your username with .setuser. Alternatively use .np <username>")
      exit(-1)
      
  else:
    user = sys.argv[3]
    
if query in ("weeklyartists", "weeklyalbums", "topartists", "topalbums", "userinfo"):
  if len(sys.argv) < 4:
    user = lastfm.get_user_by_nick(nick)
    if user == None:
      print_console(LEL + " First set your username with .setuser. Alternatively use !lastfm %s <username>" % query)
      exit(-1)
      
  else:
    user = sys.argv[3]
    
# will be called as lastfm.py setuser {mask} {usernme}
if query == "setuser":
  if len(sys.argv) < 4:
    print_console(LEL + " .setuser <username>")
    exit(-1)
  else:
    user = sys.argv[3]


if query == "weeklyartists":
  LastFM().get_weekly_artist_charts(user)
elif query == "weeklyalbums":
  LastFM().get_weekly_album_charts(user)
elif query == "topalbums":
  LastFM().get_top_albums(user)
elif query == "topartists":
  LastFM().get_top_artists(user)
elif query == "userinfo":
  LastFM().get_user_info(user)
elif query == "compare":
  LastFM().compare_users(user, user2)
elif query == "artistinfo":
  LastFM().get_artist_info(artist)
elif query == "artistevents":
  LastFM().get_artist_events(artist)  
elif query == "nowplaying":
  if user.lower() == "ticksound":
    print_console(LEL + " tickSound is now playing: Justin Bieber - Baby (600 plays, baby, better than radiohead, bieber, black metal, brutal death metal, emo, fag)");
  else:
    LastFM().get_now_playing(user)
elif query == "setuser":
  LastFM().set_user(nick, user)
else:
  man();

  


