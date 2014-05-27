import os, sys
import urllib, json

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import unescape, strip, print_console

logo = '3::54chan'

def man():
  print_console("%s Usage: !4chan <board> <index> OR <board> <search terms> [index]" % logo)

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

        text = '%s /%s/ | %s | %s | %s (R:%s, I:%s)' % (logo, board, subject, post, boardLink, j['replies'], j['images'])
        res.append(text)
  return res

def getValidBoards():
  boards = []

  l = json.load(urllib.urlopen('https://a.4cdn.org/boards.json'))

  for i in l['boards']:
    boards.append(str(i['board']))

  return boards

if len(sys.argv) < 3:
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


if board not in getValidBoards():
  print_console("/%s/ is not a real board" % board)
  exit(1)

res = search(board, terms)
total = len(res)

if res:
  try:
    print_console("%d/%d | %s" % (index + 1, total, res[index]))
  except(IndexError):
    print_console("%s: Out of bounds! Only %d threads available with '%s' on /%s/" % (logo, total, terms, board))

else:
  print_console("No results for %s on /%s/" % (terms, board))
