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
             "More games coming soon!"]
games = []

soup = bs4.BeautifulSoup(requests.get("https://humblebundle.com").text)
for i in soup.find_all('span', 'game-box'):
  game = i.find('img')['alt']
  if game not in not_games and "Soundtrack" not in game:
    games.append(game)

print_console(", ".join(games))
