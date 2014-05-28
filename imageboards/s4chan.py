# -*- coding: utf-8 -*-
import os, sys
import urllib, json

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import unescape, strip, print_console

logo = '54chan 3::5'
logo_1 = '54chan'
logo_2 = '3::'

def man():
  print_console("%s Usage: .4 <board> [index] OR .4 <board> <search terms> [index]" % logo_1)
  print_console("%s Boards: %s" % (logo_2, " ".join(valid_boards)))

def format(comment):

  comment = unescape(comment)
  comment = comment.replace('<br>', ' ')
  comment = comment.replace('<wbr>', '')
  comment = comment.replace('<span class="quote">', '3') #greentext open
  comment = comment.replace('<span class="deadlink">', '3') #greentext open
  comment = comment.replace('</span>', '') #close color
  comment = strip(comment) #remove the rest of html tags
  
  return comment

def search(board, search):
  res = []

  catalog = json.load(urllib.urlopen('https://a.4cdn.org/%s/catalog.json' % board))

  for i in catalog:
    for j in i['threads']:
      if search.lower() in j.get('sub', '').lower() or search.lower() in j.get('com', '').lower():
        subject = j.get('sub', 'No subject')
        subject = unescape(subject)
        post = j.get('com', 'Empty post')
        post = format(post)

        if len(post) > 100:
          post = post[:100] + '...' #close color here also
          
        boardLink = 'https://boards.4chan.org/%s/thread/%s' % (board, j['no'])
        if subject == 'No subject':
          text = u'/%s/ · %s · %s (R:%s, I:%s)' % \
            (board, post, boardLink, j['replies'], j['images'])
        else:
          text = u'/%s/ · %s · %s · %s (R:%s, I:%s)' % \
            (board, subject, post, boardLink, j['replies'], j['images'])
        res.append(text)
  return res

def getValidBoards():
  boards = []

  l = json.load(urllib.urlopen('https://a.4cdn.org/boards.json'))

  for i in l['boards']:
    boards.append(str(i['board']))

  return boards

valid_boards = getValidBoards()

if len(sys.argv) < 2:
  man()
  exit(1)

board = sys.argv[1]
terms = " ".join(sys.argv[2:-1])

try:
  index = int(sys.argv[-1])
  
  # One-based index
  if index < 1:
    index = 0
  else:
    index -= 1
    
except(ValueError):
  index = 0
  terms = " ".join(sys.argv[2:])

if board not in valid_boards:
  print_console("%s /%s/ is not a real board" % (logo_1, board))
  print_console("%s try: %s" % (logo_2, " ".join(valid_boards)))
  exit(1)

res = search(board, terms)
total = len(res)

if res:
  try:
    s = res[index]
    if total > 1 and index + 1 < total:
      logo = logo_1;
      if terms:
        print_console("%s %d threads found! '.4 %s %s %d' for the next one" \
            % (logo, total, board, terms, index + 2))
      else:
        print_console("%s %d threads found! '.4 %s %d' for the next one" \
            % (logo, total, board, index + 2))
      logo = logo_2;
    print_console("%s %s" % (logo, s))
  except(IndexError):
    if terms:
      print_console("%s Out of bounds! Only %d threads available with '%s' on /%s/" % (logo, total, terms, board))
    else:
      print_console("%s Out of bounds! Only %d threads available on /%s/" % (logo, total, board))
else:
  print_console("%s No results for '%s' on /%s/" % (logo, terms, board))
