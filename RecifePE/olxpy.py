from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time

url = 'https://pe.olx.com.br/grande-recife/imoveis?o='
quant_pag = 100 # int(input('Quantas páginas serão mineradas? '))

# FUNÇÃO QUE COLETARÁ OS LINKS DE ACESSO AS PÁGINAS DOS ANÚNCIOS DE IMÓVEIS
def ScraperLinks(url, quant_pag):

	# Abrindo arquivo de relatório sobre o processamento do scraping
	arq  = open('relatorio', 'w')

	link_total = []
	# Para cada página:
	for pag in range(1, quant_pag + 1, 1):

		# www.exemplo.com/1, 2, 3...
		site = url + str(pag)

		# - Escrevendo no relatório
		arq.write('PÁGINA: ' + str(pag))
		arq.write('\n')
		arq.write(site)
		arq.write('\n')
		arq.write('- Página acessada;')
		arq.write('\n')

		# Fazendo a requisição ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		req = Request(site, headers = {'User-Agent':'Mozilla/5.0'})
		html = urlopen(req).read()

		# - Escrevendo no relatório
		arq.write('- Requisição feita;')
		arq.write('\n')

		# Parseando requisição ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		soup = BeautifulSoup(html, "html.parser")

		# - Escrevendo no relatório
		arq.write('- Dados HTML da página prontos para serem trabalhados;')
		arq.write('\n')

		#------------------------------#
		print("Link Ok - Página: ", pag)

		# Raspando os links ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		links = soup.find_all('a', class_='fnmrjs-0 iZLVht')
		link = []
		for i in range(len(links)):
			link.append(links[i].get('href'))
			link_total.append(links[i].get('href'))

		# - Escrevendo no relatório
		arq.write('- Links coletados;')
		arq.write('\n')
		for i in range(len(link)):
			arq.write('--- ' + link[i])
			arq.write('\n')

	# - Escrevendo na planilha
	df = pd.DataFrame(link_total)
	file = pd.ExcelWriter('links.xlsx')
	df.to_excel(file)

	arq.close()
	file.save()

	return link

#############################################################################################################################

def ScraperPage(link):

	req = Request(link, headers = {'User-Agent':'Mozilla/5.0'})
	html = urlopen(req).read()
	soup = BeautifulSoup(html, "html.parser")

	chaves  = []
	valores = []

	try:
		chaves.append('Título')
		valores.append(soup.find('h1', class_='sc-bZQynM sc-45jt43-0 bJcANz').get_text())
	except AttributeError:
		pass

	try:
		chaves.append('Preço')
		valores.append(soup.find('h2', class_='sc-bZQynM sc-1wimjbb-0 dSAaHC').get_text())
	except AttributeError:
		pass

	try:
		tags1 = soup.find_all('div', class_='sc-EHOje sc-dVhcbM sc-1f2ug0x-3 bsaFM')
	except AttributeError:
		pass

	for i in range(len(tags1)):
		chaves.append(tags1[i].find('dt').get_text())
		try:
			valores.append(tags1[i].find('dd').get_text())
		except:
			try:
				valores.append(tags1[i].find('a').get_text())
			except:
				pass

	return chaves, valores

#links = ['https://pe.olx.com.br/grande-recife/imoveis/apartamentos-em-prazeres-jaboatao-dos-guararapes-724925921', 'https://pe.olx.com.br/grande-recife/imoveis/ref-433-aptos-em-pau-amarelo-pe-724926028']


# links = ScraperLinks(url, quant_pag)

file = pd.ExcelFile('links.xlsx')
df = pd.read_excel(file)

dic = {}
chaves_total = []
quant = 0
w = 0

# Para cada uma das páginas:
for link in df[0]:
	print(w)
	w += 1
	
	# Chame a função para coletar os dados da página e armazenar nas listas 'chaves' e 'valores'
	try:
		chaves, valores = ScraperPage(link)
	except:
		pass
	# para cada elemento da lista 'chaves':
	for i in range(len(chaves)):

		# Tente acrescentar o valor da lista 'valores' a chave correspondente no dicionário 'dic'
		try:
			dic[chaves[i]].append(valores[i])
		# Caso essa chave não exista:
		except KeyError:
			# Defina para essa chave uma lista vazia
			dic[chaves[i]] = []
			# Acrescente o valor nulo para essa chave nas páginas anteriores
			for j in range(quant):
				dic[chaves[i]].append("")
			# Acrescente o valor de 'valores' nessa lista (após os valores nulos)
			dic[chaves[i]].append(valores[i])

	#Se não existir valor em alguma chave do dicionário já adicionada anteriormente, coloque o valor nulo
	for x in dic:
		if x not in chaves:
			dic[x].append("")

	quant += 1

# Exportação para Excel
df = pd.DataFrame(dic)
df.to_excel(r'/home/joao/Códigos/git/envScraping/olxpy/dados.xlsx')
