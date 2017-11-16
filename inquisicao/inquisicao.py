#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest

# ../mylib.py
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

response = urlrequest.urlopen('https://inquisicao.deadbsd.org/api/degredo')
data = response.read()
j = json.loads(data)

print_console("[%s] Crime: %s | %s" % (j['processo'], j['crime'], j['sentenca']))
