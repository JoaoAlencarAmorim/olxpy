# olxpy
Biblioteca para web scraping do site OLX

### Inputs

#### url = 'https://pe.olx.com.br/grande-recife/imoveis?o='
URL da região de interesse. Como pode ser observado ela é organizada em:

https:// + UF + .olx.com.br/ + REGIÃO DO ESTADO + /imoveis?o= + Nº DA PÁGINA

O número da página não deve ser acrescentado, pois o próprio código cuidará disso.

#### quant_pag = 100


### ScraperLinks(url, quant_pag)

### ScraperPage(link)
