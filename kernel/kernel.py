#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get
from bs4 import BeautifulSoup

# ../mylib.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

url = 'https://www.kernel.org/'

response = get(url)

soup = BeautifulSoup(response.text, 'html.parser')

kernel = {}
table = soup.find("table", { 'id': 'releases'})
trs = table.find_all("tr")
for tr in trs:
    td = tr.find_all("td")
    branch = td[0].text.strip()[:-1]

    if branch == "longterm":
        continue

    if branch not in kernel:
        kernel[branch] = td[1].text.strip()

output = "Latest Kernel: "

for k,v in kernel.items():
    output = output + "{}: {}, ".format(k, v)

print_console(output[:-2])
