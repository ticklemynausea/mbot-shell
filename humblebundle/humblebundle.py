import os
import sys
import requests
import bs4

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

not_games = ["Electronic Frontier Foundation",
             "American Red Cross",
             "Child's Play Charity",
             "Mozilla Foundation",
             "CodeNow",
             "Maker Education Initiative",
             "Save the Children",
             "charity: water",
             "Exclusive Dreamcast T-Shirt",
             "AbleGamers",
             "Willow",
             "SpecialEffect",
             "GamesAid",
             "Girls Who Code",
             "The V Foundation",
             "buildOn",
             "The IndieCade Foundation",
             "Extra Life / Children's Miracle Network Hospitals",
             "More games coming soon!",
             "More content coming soon!"]
games = []

soup = bs4.BeautifulSoup(requests.get("https://humblebundle.com").text, "html.parser")
res = soup.find_all('span', 'game-box')

if res:
  bTitle = soup.find('img', class_="promo-logo")['alt']
  for i in res:
    game = i.find('img')['alt']

    if game not in not_games and "Soundtrack" not in game:
      games.append(game)

  print_console("07%s: %s" % (bTitle, ", ".join(games)))

else:
  print_console("This bundle is over!")
