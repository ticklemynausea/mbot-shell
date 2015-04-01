# -*- coding: utf-8 -*-
import urllib2
import simplejson
import ipaddress
import socket
import sys
import os
import re
import code

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

# http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
def is_valid_ip(ip):
  """Validates IP addresses.
  """
  return is_valid_ipv4(ip) or is_valid_ipv6(ip)

def is_valid_ipv4(ip):
  """Validates IPv4 addresses.
  """
  pattern = re.compile(r"""
    ^
    (?:
      # Dotted variants:
      (?:
      # Decimal 1-255 (no leading 0's)
      [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
      |
      0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
      |
      0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
      )
      (?:          # Repeat 0-3 times, separated by a dot
      \.
      (?:
        [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
      |
        0x0*[0-9a-f]{1,2}
      |
        0+[1-3]?[0-7]{0,2}
      )
      ){0,3}
    |
      0x0*[0-9a-f]{1,8}  # Hexadecimal notation, 0x0 - 0xffffffff
    |
      0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
    |
      # Decimal notation, 1-4294967295:
      429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
      42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
      4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
    )
    $
  """, re.VERBOSE | re.IGNORECASE)
  return pattern.match(ip) is not None

def is_valid_ipv6(ip):
  """Validates IPv6 addresses.
  """
  pattern = re.compile(r"""
    ^
    \s*             # Leading whitespace
    (?!.*::.*::)        # Only a single whildcard allowed
    (?:(?!:)|:(?=:))      # Colon iff it would be part of a wildcard
    (?:             # Repeat 6 times:
      [0-9a-f]{0,4}       #   A group of at most four hexadecimal digits
      (?:(?<=::)|(?<!::):)  #   Colon unless preceeded by wildcard
    ){6}            #
    (?:             # Either
      [0-9a-f]{0,4}       #   Another group
      (?:(?<=::)|(?<!::):)  #   Colon unless preceeded by wildcard
      [0-9a-f]{0,4}       #   Last group
      (?: (?<=::)       #   Colon iff preceeded by exacly one colon
       |  (?<!:)        #
       |  (?<=:) (?<!::) :  #
       )            # OR
     |              #   A v4 address with NO leading zeros 
      (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
      (?: \.
        (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
      ){3}
    )
    \s*             # Trailing whitespace
    $
  """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
  return pattern.match(ip) is not None

if len(sys.argv) < 2:
  print_console("Usage: !geo <host|ip>")
  sys.exit() 

arg = sys.argv[1]

if is_valid_ip(arg):
  ip = arg
  try:
    host = socket.gethostbyaddr(ip)
    host = host[0]
    
  except socket.herror:
    host = ""
else:
  try:
    ip = socket.gethostbyname(arg)
    try:
      host = socket.gethostbyaddr(ip)
      host = host[0]
    except socket.herror:
      host = ""

  except socket.gaierror as e:
    print_console(e[1])
    sys.exit(-1)


url = "https://www.maxmind.com/geoip/v2.1/city/%s?use-downloadable-db=1&demo=1"
headers = {
  'Pragma':'no-cache', 
  'Accept-Encoding':'gzip,deflate,sdch',
  'Host':'www.maxmind.com',
  'Accept-Language':'en-US,en;q=0.8,pt-PT;q=0.6,pt;q=0.4',
  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
  'Accept':'*/*',
  'Referer':'http://www.maxmind.com/en/geoip_demo',
  'X-Requested-With':'XMLHttpRequest',
  'Cookie':' pkit_session_id=8af0e3469734',
  'Connection':'keep-alive',
  'Cache-Control':'no-cache'
}


if host == "":
  print_console("GeoIP Lookup for %s" % (ip))
else:
  print_console("GeoIP Lookup for %s (%s)" % (host, ip))

req = urllib2.Request(url % ip, None, headers)
opener = urllib2.build_opener()

try:
  f = opener.open(req)
  js = simplejson.load(f)


  s = ""
  if "traits" in js.keys():
    if "domain" in js["traits"]:
      s += "Authority: %s " % js["traits"]["domain"]

    if "autonomous_system_number" in js["traits"]:
      s += "AS #%s" % js["traits"]["autonomous_system_number"]

    if "autonomous_system_organization" in js["traits"]:
      s += " %s; " % js["traits"]["autonomous_system_organization"]
    else:
      s += "; "

    if "user_type" in js["traits"]:
      s += "User Type: %s; " % js["traits"]["user_type"]

    if "isp" in js["traits"]:
      s += "ISP: %s; " % js["traits"]["isp"]

    if "organization" in js["traits"]:
      s += "Org: %s; " % js["traits"]["organization"]


  if "city" in js.keys():
    s += "City: %s; " % (js["city"]["names"]["en"])

  if "country" in js.keys():
    s += "Country: %s; " % (js["country"]["names"]["en"])

    if "time_zone" in js["location"]:
      s += "Time Zone: %s; " % js["location"]["time_zone"]

  print_console(s)
  
except urllib2.HTTPError as e:
  print e
