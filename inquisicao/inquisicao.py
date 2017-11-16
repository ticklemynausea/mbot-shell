#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest

import json

response = urlrequest.urlopen('https://inquisicao.deadbsd.org/api/degredo')
data = response.read()
j = json.loads(data)

print("[%s] Crime: %s | %s" % (j['processo'], j['crime'], j['sentenca']))