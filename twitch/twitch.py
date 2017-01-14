# coding=utf-8

import os
import sys
import requests

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console
from apikeys import client_id

#def print_console(x):
#  print(x)

def man():
  # ~:python twitch.py <name>
  print_console('Usage: !twitch <name>')
  exit(-1)

# Clean non-ascii
def c(t):
  return t.encode('ascii', 'ignore')

def getResults(n):

  # Headers
  headers = {
    'Accept': 'application/vnd.twitchtv.v3+json',
    'Client-ID': client_id
  }

  # Request Data
  r=requests.get('https://api.twitch.tv/api/channels/{0}'.format(n), headers=headers)
  l=requests.get('https://api.twitch.tv/kraken/streams?channel={0}'.format(n), headers=headers)

  # Check Status Code
  if r.status_code == 200:

    # Check Account
    j=r.json()
    if 'message' not in j:

      # User Info
      data='Twitch {0}\'s - Title: \002"{1}"\002 - Game: \002"{2}"\002'.format(j["display_name"],c(j["status"]),j["game"])

      # Partner Info
      if j["partner"] != False:
        data+=' [\0036 Partner \003]'

      # Steam Info
      if j["steam_id"] != None:
        data+=' [ Steam: http://steamcommunity.com/profiles/{0} ]'.format(j["steam_id"])

      # Status Info
      if l.status_code == 200:
        l=l.json()

        # If "Online"
        if l["_total"] != 0:

          # User Totals
          sf=l["streams"][0]["channel"]["followers"]
          st=l["streams"][0]["channel"]["views"]
          data+=' [ Totals: {0} Followers | {1} Viewers ]'.format(sf,st)

          # Viewers
          sv=l["streams"][0]["viewers"]
          data+=' [\0039 \002Live\002 w/ {0} viewers \003]'.format(sv)

        else:
          data+=' [\0034 \002Off\002 \003]'

      #Note:
      # - Bold: \002
      # - Color's: \0034 red \0039 green \0036 purle \0003 clear)

      # Output
      print_console('{0} - http://www.twitch.tv/{1}'.format(data,n))

    else:
      print_console('Twitch Returned: {0}'.format(c(j["message"])))

  elif r.status_code == 400 or r.status_code == 404:
    j=r.json()
    print_console('Twitch Returned: {0}'.format(c(j["message"])))

  else:
    print_console('Request Returned: "{0}" status code.'.format(r.status_code))


# Main
if len(sys.argv) < 2:
  man()

name = sys.argv[1]
if name:
  getResults(name)
else:
  man()
