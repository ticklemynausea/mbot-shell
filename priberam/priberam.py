# coding=utf8
#!/usr/bin/env python

import sys, os, urllib2
from BeautifulSoup import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mylib

"""
-PARTIR OUTPUT

"""

L = "13,16Priberam" 

URL = 'http://www.priberam.pt/DLPO/default.aspx?pal='

palavra = None

class Definicao():
	def __init__(self, soup, palavra, categoria):
		self.soup = soup
		self.palavra = palavra
		self.categoria = categoria

	def contents(self):
		defs = []
		for c in self.soup.findAll(recursive=False):
			if not attr(c, 'class', "varpb") :
				defs += c.findAll(text=True)

		o = [s.replace("\t", " ") for s in defs]
		o = ''.join(o)

		# marcar linhas e remover \n
		o = [w.strip() for w in o.split('\n')]
		o = [w + '\002;\002 ' if len(w) > 1 else w for w in o]
		o = ''.join(o)

		return o
		
	def __repr__(self):
		return '\002' + self.palavra + '\002 ' + self.categoria + ' ' + self.contents()
		


def usage():
	print_console(L + " Usage: !dic palavra [index]")
	exit(-1)

def attr(soup, attr, value):
	try:
		if soup[attr] == value :
			return True
	except KeyError:
		pass
	return False

def getDefinicoes(r, palavra, categoria=''):
	defs = []
	for c in r.findAll(recursive=False):
		if attr(c, 'class', "varpb") :
			pass
		elif attr(c, 'class', "varpt") :
			categoria = c.div.i.categoria.contents[0]
		elif attr(c, 'style', "padding-left:12px;") :
			defs.append(Definicao(c, palavra, categoria))
		elif attr(c, 'class', "") and c.name == "span":
			defs = defs + getDefinicoes(c, palavra, categoria)

	return defs

def printSignificado(registos, n):
	registos = [
		d for r in registos
			for d in getDefinicoes(r, r.span.b.contents[0])]
	try:
		if n == 0:
			mylib.print_console("%d definições encontradas\002;\002 ? %s 1 para a próxima." % (len(registos), palavra))
		mylib.print_console( registos[n].__repr__())
	except IndexError:
		mylib.print_console(str(n) + ' de ' + str(len(registos)) + ' nao encontrado')
	return

def procura(palavra, n = 0):
	#try:
		req = urllib2.Request(URL + palavra)
		open_req = urllib2.urlopen(req)
		content = open_req.read()	
		soup = BeautifulSoup(content, fromEncoding="utf-8") # bad META na pagina

		definicao = soup.find(id="DivDefinicao")

		registos = definicao.findAll("div", {"registo": "true"})
		if len(registos) > 0 :
			# com resultados!
			return printSignificado(registos, n)
				 		
		sugestoes = definicao.findAll("div", {"id": "FormataSugestoesENaoEncontrados"})
		if len(sugestoes) > 0 :
			# sem resultados :(
			sugestoes = [''.join(s.findAll(text=True)) for s in sugestoes]
			mylib.print_console('\002Sugestoes:\002 ' + ', '.join(sugestoes))
			return
		
		# sem resultados nem sugestoes :((
		mylib.print_console('\002Palavra nao encontrada\002')

	#except Exception:
	#	print_console("Erro ao tentar obter o conteudo.")
	#	exit(-1)

if __name__=="__main__":

	if len(sys.argv) < 2:
		# usage()
		exit(-1)

	palavra = sys.argv[1]
		
	if len(sys.argv) == 2:
		procura(palavra, 0)
	elif len(sys.argv) == 3:
		procura(palavra, int(sys.argv[2]))

	
