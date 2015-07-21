# coding=utf-8

import os
import sys
import requests

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

#def print_console(x):
#  print(x)

def man():
  # ~:python twitch.py <name>
  print_console('Usage: !twitch <name>')
  exit(-1)


def getResults(n):

  # Request Data
  r=requests.get('https://api.twitch.tv/api/channels/{0}'.format(n))

  # Check Status Code
  if r.status_code == 200:

    # Check Account
    j=r.json()
    if 'error' not in j:

      # User Info
      data='Twitch {0}: Title: {1} - Game: {2}'.format(j['display_name'],j['status'],j['game'])

      # Partner Info
      if j['partner'] != False: 
        data=' {0} [\0035 Partner \003]'.format(data)

      # Steam Info
      if j['steam_id'] != False:
        data=' {0} [Steam: http://steamcommunity.com/profiles/{1}]'.format(data,j['steam_id'])

      # Status Info
      if j['liverail_id'] != False:
        live='[\0032 Live \003]'
      else:
        live='[\0031 Off \003]'
      data='{0} {1}'.format(data,live)

      # Output
      print_console(data)

    else:
      print_console('Twitch Returned: {1}'.format(n,j['error']))

  else:
    print_console('Request Returned: "{0}" status code.'.format(r.status_code))

if len(sys.argv) < 2:
  man()

name = sys.argv[1]
if name:
  getResults(name)
else:
  man()
