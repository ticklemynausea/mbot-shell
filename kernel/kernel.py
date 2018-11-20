#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from requests import get
from bs4 import BeautifulSoup

# ../mylib.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

URL = 'https://www.kernel.org/'

if __name__ == "__main__":
    KERNEL = {}

    RESPONSE = get(URL)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')

    TABLE = SOUP.find("table", {'id': 'releases'})
    TRS = TABLE.find_all("tr")
    for TR in TRS:
        TD = TR.find_all("td")
        BRANCH = TD[0].text.strip()[:-1]

        if BRANCH == "longterm":
            continue

        if BRANCH not in KERNEL:
            KERNEL[BRANCH] = TD[1].text.strip()

    OUTPUT = "Latest Kernel: "
    for k, v in KERNEL.items():
        OUTPUT = OUTPUT + "{}: {}, ".format(k, v)

    print_console(OUTPUT[:-2])
