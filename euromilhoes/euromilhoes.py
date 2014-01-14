import os
import sys
import requests
import bs4

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console
from mylib import strip as stripHTML

def man():
  print_console('Usage: .euromilhoes | .totoloto | .joker') # ~:python euromilhoes.py [e | t | j]
  exit(-1)


def getResults(c):

  # EUROMILHOES
  emInfoStyle = 'border-bottom:1px solid white; background-color:#e2e2e2;padding:2px; padding-left:6px;\\'

  emNumStyle = 'font-weight:bold; width: 25px; height: 25px; background-position:center; background-repeat:no-repeat; text-align:center; vertical-align:middle; background-image:url(/_media/img/2008/Jan/tmpl_fe_fundo_numero_on_ufuv.jpg);padding:2px; '

  emStarStyle = 'padding:2px;font-weight:bold; width: 27px; height: 25px; background-position:center; background-repeat:no-repeat; text-align:center; vertical-align:middle; background-image:url(/_media/img/2008/Jan/tmpl_fe_fundo_estrela_on_dwma.jpg); '

  emNum1 = []
  emNum2 = []
  emInfo1 = ''
  emInfo2 = ''

  # TOTOLOTO
  totInfoStyle = 'border-bottom:1px solid white; background-color:#e2e2e2;padding:2px; padding-left:6px;'

  totStarStyle = 'padding:2px;font-weight:bold; width: 27px; height: 25px; background-position:center; background-repeat:no-repeat; text-align:center; vertical-align:middle; background-image:url(/_media/img/2008/Jan/tmpl_fe_fundo_estrela_on_dwma2.jpg); '

  totNum1 = []
  totNum2 = []
  totInfo1 = ''
  totInfo2 = ''

  # JOKER
  jokerStyle = 'padding:8px; padding-left:6px; font-weight:bold; border-bottom:1px solid white; background-color:white;  background-repeat:repeat-x; background-image:url(http://www.euromilhoes.com/_include/images/fundo_row.png); color:#666666; font-size:14px; color:#990000; text-align:center;'

  jokerInfo = ''
  
  # Get the results
  soup = bs4.BeautifulSoup(requests.get('http://www.euromilhoes.com/index_intro.php').text)

  res = soup.findAll('td', {'style': emInfoStyle}) # euromilhoes info
  emInfo1 = str.strip(stripHTML(str(res[0])))
  emInfo1 = emInfo1[:23] + ' ' + emInfo1[23:]
  emInfo2 = str.strip(stripHTML(str(res[1])))
  emInfo2 = emInfo2[:23] + ' ' + emInfo2[23:]


  res = soup.findAll('td', {'style': emNumStyle}) # all numbers (no stars)
  for i in res[:5]:
    emNum1.append(str.strip(stripHTML(str(i))))
  for i in res[5:10]:
    emNum2.append(str.strip(stripHTML(str(i))))
  for i in res[10:15]:
    totNum1.append(str.strip(stripHTML(str(i))))
  for i in res[15:20]:
    totNum2.append(str.strip(stripHTML(str(i))))

  
  res = soup.findAll('td', {'style': emStarStyle}) # euromilhoes stars
  emNum1.append(str.strip(stripHTML(str(res[0]) + '*')))
  emNum1.append(str.strip(stripHTML(str(res[1]) + '*')))
  emNum2.append(str.strip(stripHTML(str(res[2]) + '*')))
  emNum2.append(str.strip(stripHTML(str(res[3]) + '*')))


  res = soup.findAll('td', {'style': totInfoStyle}) # totoloto info and joker(last)
  totInfo1 = str.strip(stripHTML(str(res[0])))
  totInfo1 = totInfo1[:23] + ' ' + totInfo1[23:]
  totInfo2 = str.strip(stripHTML(str(res[1])))
  totInfo2 = totInfo2[:23] + ' ' + totInfo2[23:]
  #joker
  jokerInfo = str.strip(stripHTML(str(res[2])))
  jokerInfo = jokerInfo[:23] + ' ' + jokerInfo[23:]


  res = soup.findAll('td', {'style': totStarStyle}) # totoloto stars
  totNum1.append(str.strip(stripHTML(str(res[0]) + '*')))
  totNum2.append(str.strip(stripHTML(str(res[1]) + '*')))


  res = soup.findAll('td', {'style': jokerStyle}) # joker number
  joker = str.strip(stripHTML(str(res[0])))

  if (c == 'e'): # Euromilhoes
    print_console(emInfo1)
    print_console(', '.join(emNum1))
    print_console(emInfo2)
    print_console(', '.join(emNum2))

  if (c == 't'): # Totoloto
    print_console(totInfo1)
    print_console(', '.join(totNum1))
    print_console(totInfo2)
    print_console(', '.join(totNum2))

  if (c == 'j'): # Joker
    print_console(jokerInfo)
    print_console(joker)


if len(sys.argv) < 2:
  man()
  
contest = sys.argv[1]
if contest in ['e', 't', 'j']:
  getResults(contest)
else:
  man()
