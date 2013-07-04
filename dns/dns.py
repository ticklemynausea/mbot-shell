import socket
import sys
import os

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

if len(sys.argv) < 3:
  print_console("Usage: !dns <name> | !rdns <ip address>");
  exit(-1)
  
t = sys.argv[1]
p = sys.argv[2]

try:
  if t == "r":
    a = socket.gethostbyaddr(p)
    print_console("rDNS lookup for %s: %s" % (p, a[0]))
  elif t == "l":
    a = socket.gethostbyname(p)
    print_console("DNS lookup for %s: %s" % (p, a))
    
except socket.gaierror:
  print_console("DNS lookup for %s failed" % p) 
  
