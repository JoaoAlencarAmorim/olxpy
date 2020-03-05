from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv

url = 'https://pe.olx.com.br/grande-recife/imoveis?o='
n_pag = 2

# FUNÇÃO QUE COLETARÁ OS LINKS DE ACESSO AS PÁGINAS DOS ANÚNCIOS DE IMÓVEIS
def Scraping_olx_v01(url, n_pag):

	# Abrindo arquivo de relatório sobre o processamento do scraping
	arq  = open('relatorio', 'w')

	# Abrindo arquivo csv para armazenar os links dos anúncios
	file = open('links.csv', 'w')

	for pag in range(1, n_pag + 1, 1):

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

Scraping_olx_v01(url, n_pag)