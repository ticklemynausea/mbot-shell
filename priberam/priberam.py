import sys, os
from urllib2 import Request, HTTPError, URLError, urlopen
from BeautifulSoup import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console


"""

-ultimas pesquisas :>
-top pesquisas -> cloud





"""

L = "13,16Priberam" 

URL = 'http://www.priberam.pt/DLPO/default.aspx?pal='

def usage():
	print_console(L + "%s Usage: !priberam palavra")
	exit(-1)

def parsaRegisto(r):
	# obter definicao
	o = [s.replace("\t", " ") for s in r.findAll(text=True, recursive=True)]
	o = ''.join(o)

	# marcar primeira palavra e limpar os espacos
	o = o.split(' ')
	o[0] = '\002' + o[0] + '\002'
	o = ' '.join(o)

	# marcar linhas e remover \n
	o = [w.strip() for w in o.split('\n')]
	o = [w + '\002;\002 ' if len(w) > 1 else w for w in o]
	o = ''.join(o)

	return o

def parsaSugestoes(r):
	o = r.findAll("div", { "id" : "FormataSugestoesENaoEncontrados" })
	if len(o) > 1 :
		o = [''.join(w.findAll(text=True, recursive=True)) for w in o]
		return u'\002Sugestoes:\002 ' + ', '.join(o)
	else :
		return '\002Palavra nao encontrada\002'

def procura(palavra):
	# validar palavras
	try:
		req = Request(URL + palavra)
		open_req = urlopen(req)
		content = open_req.read()	
		soup = BeautifulSoup(content, fromEncoding="utf-8") # bad META na pagina

		d = soup.find(id="DivDefinicao")
		r = d.find(registo="true")
		
		if r :
			# found!
			return parsaRegisto(r)
		else :
			return parsaSugestoes(d)

	except Exception:
		print_console("Erro ao tentar obter o conteudo.")
		exit(-1)

if __name__=="__main__":

	if len(sys.argv) < 2:
		usage()

	palavra = sys.argv[1]
	print_console(procura(palavra))
	
