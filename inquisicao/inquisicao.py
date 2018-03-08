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

    result = j['titulo']
    if j['crime']:
        result = "%s | Crime %s" % (result, j['crime'])
    if j['sentenca']:
        result = "%s | %s" % (result, j['sentenca'])
    result = "%s | %s" % (result, j['url'])

    print_console(result)

def adcautelam(key, page):
    request = requests.get('https://inquisicao.deadbsd.org/api/adcautelam?key=' + key + '&page=' + str(page), timeout=TIMEOUT)

    if request.status_code == 404:
        print_console("Not found")
    else:
        j = request.json()

        result = "[%d/%d] %s" % (
            j['next'] - 1 if j['next'] else j['total'],
            j['total'],
            j['message']['titulo'])
        if j['message']['crime']:
            result = "%s | Crime %s" % (result, j['message']['crime'])
        if j['message']['sentenca']:
            result = "%s | %s" % (result, j['message']['sentenca'])
        result = "%s | %s: %s | %s" % (
            result,
            j['message']['match']['key'],
            j['message']['match']['value'],
            j['message']['url'])

        print_console(result)

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
