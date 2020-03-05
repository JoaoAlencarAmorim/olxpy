from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv

url = 'https://pe.olx.com.br/grande-recife/imoveis?o='
quant_pag = 2 # int(input('Quantas páginas serão mineradas? '))

# FUNÇÃO QUE COLETARÁ OS LINKS DE ACESSO AS PÁGINAS DOS ANÚNCIOS DE IMÓVEIS
def ScraperLinks(url, quant_pag):

	# Abrindo arquivo de relatório sobre o processamento do scraping
	arq  = open('relatorio', 'w')

	# Abrindo arquivo csv para armazenar os links dos anúncios
	file = open('links.csv', 'w')

	for pag in range(1, quant_pag + 1, 1):

		site = url + str(pag)

		#----------------------------------------------------------------------
		print("Acessando a página: ", pag)

		arq.write('PÁGINA: ' + str(pag))
		arq.write('\n')
		arq.write(site)
		arq.write('\n')
		arq.write('- Página acessada;')
		arq.write('\n')

		req = Request(site, headers = {'User-Agent':'Mozilla/5.0'})
		html = urlopen(req).read()

		arq.write('- Requisição feita;')
		arq.write('\n')

		#----------------------------------------------------------------------
		print("Requisição feita")

		soup = BeautifulSoup(html, "html.parser")

		arq.write('- Dados HTML da página prontos para serem trabalhados;')
		arq.write('\n')

		#----------------------------------------------------------------------
		print("HTML parseado")

		links = soup.find_all('a', class_='fnmrjs-0 iZLVht')
		link = []
		for i in range(len(links)):
			link.append(links[i].get('href'))
		
		arq.write('- Links coletados;')
		arq.write('\n')
		writer = csv.writer(file)

		for i in range(len(link)):
			arq.write('--- ' + link[i])
			arq.write('\n')
			writer.writerow(f'"{link[i]}"')

	arq.close()
	file.close()

	return link

#links = ScraperLink(url, n_pag)


def ScraperPage(link):

	req = Request(link, headers = {'User-Agent':'Mozilla/5.0'})
	html = urlopen(req).read()
	soup = BeautifulSoup(html, "html.parser")

	try:
		titulo = soup.find('h1', class_='sc-bZQynM sc-45jt43-0 bJcANz').get_text()
	except AttributeError:
		titulo = ""

	try:
		preco = soup.find('h2', class_='sc-bZQynM sc-1wimjbb-0 dSAaHC').get_text()
	except AttributeError:
		preco = ""

	"""try:
					categoria = soup.find('a', class_='sc-57pm5w-0 sc-1f2ug0x-2 dBeEuJ').get_text()
				except AttributeError:
					categoria = ""
			
				try:
					tipo = soup.find('a', class_='sc-57pm5w-0 sc-1f2ug0x-2 dBeEuJ').get_text()
				except AttributeError:
					tipo = ""
			
				try:
					preco = soup.find('h2', class_='sc-bZQynM sc-1wimjbb-0 dSAaHC').get_text()
				except AttributeError:
					preco = """

	print(titulo)
	print(preco)


links = ['https://pe.olx.com.br/grande-recife/imoveis/apartamentos-em-prazeres-jaboatao-dos-guararapes-724925921', 'https://pe.olx.com.br/grande-recife/imoveis/ref-433-aptos-em-pau-amarelo-pe-724926028']

for link in links:
	ScraperPage(link)