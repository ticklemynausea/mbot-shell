# coding=utf8
#!/usr/bin/env python

import sys, os, urllib, urllib2, re
from types import NoneType
from BeautifulSoup import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mylib

"""
TODO:
-categorias
-conjuga
"""

L = "13,16Priberam" 

URL = 'http://www.priberam.pt/dlpo/%s'
CONJURL = 'http://www.priberam.pt/dlpo/Conjugar/%s'

def usage():
 print_console(L + " Usage: !dic palavra [index]")
 exit(-1)

def str_is_int(s):
  try:
    n = int(s)
    return (True, n)
  except ValueError:
    return (False, s)


def getIndex(argv) :
  p, n = str_is_int(argv[-1])
  if p:
    q = " ".join(argv[:-1])
  else :
	q, n = " ".join(argv), 1

  return q, n


def procura(pesquisa, indice = 1):
  if indice < 1:
    return

  parametro = urllib.quote(pesquisa)
  pagina = urllib2.urlopen(URL % parametro)  
  pagina = pagina.read()
  sopa = BeautifulSoup(pagina, fromEncoding="utf-8")

  definicoes = sopa.find("div", {"class":"pb-main-content"})
  definicoes = definicoes.findAll("p")

  contagem = len(definicoes)

  # sugestões
  if contagem < 1 :
    p = sopa.find("div", {"class":"pb-sugestoes-proximas"})
    a = sopa.find("div", {"class":"pb-sugestoes-afastadas"})

    resultado = []
    if type(p) is not NoneType :
      resultado = resultado + p.findAll('a', text=True)

    if type(a) is not NoneType and len(a) > 0 :
      resultado = resultado + a.findAll('a', text=True)

    if len(resultado) <= 0:
      mylib.print_console('Palavra não encontrada.')
      return

    resultado = ''.join(resultado)
    resultado = ' '.join([w.strip() for w in resultado.split('\n')])

    mylib.print_console(u'Sugestões para %s:%s.' % (pesquisa, resultado))
    return

  if indice > contagem :
    return

  if contagem > 1 and indice == 1 :
    mylib.print_console("%d definições encontradas\002;\002 ? %s 2 para a próxima." % (contagem, pesquisa))

  definicao = definicoes[indice - 1]

  # remover cocó pt_BR
  for br in definicao.findAll('span', {'class' :'varpb'}, recursive=True) :
    br.extract()

  # formatação
  resultado = ''.join(definicao.findAll(text=True))
  resultado = [w.strip().replace("=", " = ") for w in resultado.split('\n')]
  #resultado = [w + '\002;\002 ' if len(w) > 1 else w for w in resultado]
  resultado = ''.join(resultado)

  mylib.print_console('\002%s \002%s' % (pesquisa, resultado.encode('utf-8')))


def conjuga(verbo, indice = 1):
  if indice < 1:
    return
  
  par = urllib.quote(verbo)
  res = urllib2.urlopen(CONJURL % par)  
  content = res.read()

  # sacar aquele HTML de dentro do HTML XD
  expressao_regular = re.compile(r'<section>(.*)</section>', re.DOTALL)
  match = re.findall(expressao_regular, content)
  sopa = BeautifulSoup(match[0], fromEncoding="utf-8")
  conteudo = sopa.find("div", {"class":"clearfix"})
  conteudo = conteudo.findAll("div", recursive=False)  

  categoria = ""
  conjugacao = []
  for d in conteudo :
    c = d['class']
    if c == 'tdHEAD' :
      categoria = ''.join(d.contents)
    elif c == 'wrapCONJ' : 
      tempo = d.findAll('div', {'class':'thCONJ'})
      tempo = ''.join([''.join(f.contents) for f in tempo])

      flexoes = d.findAll('div', {'class':'tdCONJ'})
      flexoes = ''.join([' '.join(f.findAll(text=True)) for f in flexoes])
      #flexoes = ''.join([' '.join(f.contents) for f in flexoes])
      flexoes = ''.join([w.replace('.', '') for w in flexoes.split('\n')])

      conjugacao.append('%s %s do verbo \002%s\002: %s' % (tempo, categoria, verbo, flexoes))

  contagem = len(conjugacao)

  if indice > contagem :
    return

  if contagem > 1 and indice == 1 :
    mylib.print_console("%d tempos verbais encontrados\002;\002 ? %s 2 para o próximo." % (contagem, verbo))

  mylib.print_console(conjugacao[indice - 1])


if __name__=="__main__":
  if len(sys.argv) < 2:
    # usage()
    exit(-1)

  if sys.argv[1] == 'conjuga' and len(sys.argv) > 2 :
    conjuga(*getIndex(sys.argv[2:]))
  else: 
    procura(*getIndex(sys.argv[1:]))

   
