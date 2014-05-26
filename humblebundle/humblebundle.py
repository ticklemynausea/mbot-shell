import os
import sys
import requests
import bs4

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console, unescape
from mylib import strip as stripHTML

soup  = bs4.BeautifulSoup(requests.get("http://humblebundle.com").text)
games = [ unescape(str.strip(stripHTML(str(i)))) for i in soup.find_all('span', 'item-title') if str.strip(stripHTML(str(i))) is not '' ]

print_console(", ".join(games))
