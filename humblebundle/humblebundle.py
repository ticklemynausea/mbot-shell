import os
import sys
import requests
import bs4

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console
from mylib import strip as stripHTML

soup  = bs4.BeautifulSoup(requests.get("http://humblebundle.com").text)
games = [str.strip(stripHTML(str(i))) for i in soup.find_all('span', 'item-title')]

print_console(", ".join(games))
