#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

TIMEOUT = 5

def degredo():
    request = requests.get('https://inquisicao.deadbsd.org/api/degredo', timeout=TIMEOUT)
    j = request.json()
    print_console("[%s] %s | Crime: %s | %s" % (j['processo'], j['titulo'], j['crime'], j['sentenca']))

def adcautelam(key, page):
    request = requests.get('https://inquisicao.deadbsd.org/api/adcautelam?key=' + key + '&page=' + str(page), timeout=TIMEOUT)

    print(request.status_code)

    if request.status_code == 404:
        print_console("Not found")
    else:
        j = request.json()
        print_console("[%d/%d] %s | %s: %s | #%s" %
                    (j['next'] - 1 if j['next'] else j['total'],
                     j['total'], j['message']['titulo'],
                     j['message']['match']['key'],
                     j['message']['match']['value'],
                     j['message']['processo']))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        degredo()
    if len(sys.argv) > 1:
        ARGS = ' '.join(sys.argv[1:])

        KEY = False
        PAGE = 1

        MATCH = re.search(r"^(?P<key>.*?)(?P<page> \d+)?$", ARGS)
        if MATCH.group('key'):
            KEY = MATCH.group('key')
        if MATCH.group('page'):
            PAGE = int(MATCH.group('page').strip())

        if KEY:
            adcautelam(KEY, PAGE)
