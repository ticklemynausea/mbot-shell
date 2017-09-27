import os
import sys
import requests
import bs4
import re

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

def man():
  print_console("Usage: .hb [g]ames | [b]ooks || Default is 'g'")

def getBundle(b):
  charities = [u"Electronic Frontier Foundation", u"American Red Cross", u"Child's Play Charity",
               u"Mozilla Foundation", u"CodeNow", u"Maker Education Initiative",
               u"Save the Children", u"charity: water", u"Exclusive Dreamcast T-Shirt",
               u"AbleGamers", u"Willow", u"SpecialEffect",
               u"GamesAid", u"Girls Who Code", u"The V Foundation",
               u"buildOn", u"The IndieCade Foundation", u"Extra Life / Children's Miracle Network Hospitals",
               u"Heifer International", u"Comic Book Legal Defense Fund",
               u"More games coming soon!", u"More content coming soon!"]
  items = []

  color1 = 14
  color2 = 15

  if b is 'b':
    soup = bs4.BeautifulSoup(requests.get("https://humblebundle.com/books").text, "html.parser")
  else:
    soup = bs4.BeautifulSoup(requests.get("https://humblebundle.com/").text, "html.parser")

  res = soup.find_all('div', class_='game-boxes')

  if res:
    bTitle = unicode(re.search("(.+) \(.+\)", soup.title.text).group(1))
    colorToggler = True

    for i in res:
      item = unicode(i.find('div', class_='dd-image-box-caption').text.strip())

      if item not in charities and u"Soundtrack" not in item:
        game = u"%02d%s" % ((color1 if colorToggler else color2), item)
        items.append(game)
        # This toggles the bool
        colorToggler = not colorToggler

    print_console(u"07%s: %s" % (bTitle, u", ".join(items)))

  else:
    print_console(u"This bundle is over!")


try:
  bundle = sys.argv[1]
except(IndexError):
  bundle = 'g'

if bundle in ['g', 'b']:
  getBundle(bundle)
else:
  man()
