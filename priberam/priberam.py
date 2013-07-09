import sys, os
from urllib2 import Request, HTTPError, URLError, urlopen
from BeautifulSoup import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console


L = "13,16Priberam" 

URL = 'http://www.priberam.pt/DLPO/default.aspx?pal='

def usage():
	#print_console(L + " Usage: !priberam palavra")
	exit(-1)

def parsaRegisto(r):
	# obter definicao
	o = [s.replace("\t", " ") for s in r.findAll(text=True)]
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

def procura(palavra):
	# validar palavras
	try:
		req = Request(URL + palavra)
		open_req = urlopen(req)
		content = open_req.read()	
		soup = BeautifulSoup(content, fromEncoding="utf-8") # bad META na pagina

		definicao = soup.find(id="DivDefinicao")

		registos = definicao.findAll("div", {"registo": "true"})
		if len(registos) > 0 :
			# found!
			return '\n'.join([parsaRegisto(r) for r in registos])
		
		sugestoes = definicao.findAll("div", {"id": "FormataSugestoesENaoEncontrados"})
		if len(sugestoes) > 0 :
			sugestoes = [''.join(s.findAll(text=True)) for s in sugestoes]
			return '\002Sugestoes:\002 ' + ', '.join(sugestoes)
		
		return '\002Palavra nao encontrada\002'

	except Exception:
		print_console("Erro ao tentar obter o conteudo.")
		exit(-1)

if __name__=="__main__":

	if len(sys.argv) < 2:
		usage()

	palavra = sys.argv[1]
	print_console(procura(palavra))
	
