# coding=utf-8

import os
import sys
import requests
import bs4

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console


def man():
  # ~:python euromilhoes.py [e | t | j]
  print_console('Usage: .euromilhoes | .totoloto | .joker')
  exit(-1)


def getResults(c):

  # Pick source
  if c is 'e':
    soup = bs4.BeautifulSoup(requests.get('https://www.jogossantacasa.pt/web/SCCartazResult/euroMilhoes').text)
    game = u"Euromilhões"
  if c is 't':
    soup = bs4.BeautifulSoup(requests.get('https://www.jogossantacasa.pt/web/SCCartazResult/totolotoNew').text)
    game = u"Totoloto"
  if c is 'j':
    soup = bs4.BeautifulSoup(requests.get('https://www.jogossantacasa.pt/web/SCCartazResult/joker').text)
    game = u"Joker"

  # Contest date
  dateInfo = soup.find('span', class_='dataInfo').stripped_strings
  date = " | ".join(dateInfo)

  # The numbers
  numberInfo = soup.find('ul', class_='colums').find('li').text

  # Output
  print_console('%s: %s - %s' % (game, numberInfo, date))


if len(sys.argv) < 2:
  man()

contest = sys.argv[1]
if contest in ['e', 't', 'j']:
  getResults(contest)
else:
  man()
