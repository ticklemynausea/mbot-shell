#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

TIMEOUT = 0.5

request = requests.get('https://inquisicao.deadbsd.org/api/degredo', timeout=TIMEOUT)
#response = urlrequest.urlopen('https://inquisicao.deadbsd.org/api/degredo',p)
#data = response.read()
#j = json.loads(data)
j = request.json()

print_console("[%s] %s | Crime: %s | %s" % (j['processo'], j['titulo'], j['crime'], j['sentenca']))
