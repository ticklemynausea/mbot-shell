import os
import sys
import requests
import bs4

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

def man():
  print_console("Usage: .hb [g]ames | [b]ooks | [m]obile || Default is 'g'")

def getBundle(b):
  charities = ["Electronic Frontier Foundation", "American Red Cross", "Child's Play Charity",
               "Mozilla Foundation", "CodeNow", "Maker Education Initiative",
               "Save the Children", "charity: water", "Exclusive Dreamcast T-Shirt",
               "AbleGamers", "Willow", "SpecialEffect",
               "GamesAid", "Girls Who Code", "The V Foundation",
               "buildOn", "The IndieCade Foundation", "Extra Life / Children's Miracle Network Hospitals",
               "Heifer International", "Comic Book Legal Defense Fund",
               "More games coming soon!", "More content coming soon!"]
  items = []

  if b is 'm':
    soup = bs4.BeautifulSoup(requests.get("https://humblebundle.com/mobile").text, "html.parser")
  elif b is 'b':
    soup = bs4.BeautifulSoup(requests.get("https://humblebundle.com/books").text, "html.parser")
  else:
    soup = bs4.BeautifulSoup(requests.get("https://humblebundle.com/").text, "html.parser")

  res = soup.find_all('span', 'game-box')

  if res:
    bTitle = soup.find('img', class_="promo-logo")['alt']
    for i in res:
      item = i.find('img')['alt']

      if item not in charities and "Soundtrack" not in item:
        items.append(item)

    print_console("07%s: %s" % (bTitle, ", ".join(items)))

  else:
    print_console("This bundle is over!")


try:
  bundle = sys.argv[1]
except(IndexError):
  bundle = 'g'

if bundle in ['g', 'b', 'm']:
  getBundle(bundle)
else:
  man()
