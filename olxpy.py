from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv
import pandas as pd

url = 'https://pe.olx.com.br/grande-recife/imoveis?o='
quant_pag = 2 # int(input('Quantas páginas serão mineradas? '))

################################################################################
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

links = ScraperLinks(url, quant_pag)

################################################################################
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

dic = {}
chaves_total = []
quant = 0

# Para cada uma das páginas:
for link in links:

	# Chame a função para coletar os dados da página e armazenar nas listas 'chaves' e 'valores'
	chaves, valores = ScraperPage(link)

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



################################################################################