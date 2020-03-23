# OLXPY
Biblioteca para web scraping do site OLX


## Estrutura do Site da OLX
Ele é organizado em páginas com 50 anúncios aproximadamente, cada anúncio possui uma página própria com suas informações detalhadas. Por exemplo:
https://pe.olx.com.br/grande-recife/imoveis?o=1 é a primeira página de anúncios de imóveis na região metropolitana de Recife-PE.
https://pe.olx.com.br/grande-recife/imoveis/vendo-apartamento-tamarineira-730931841 é um exemplo de página detalhada de um dos anúncios da primeira página de anúncios de imóveis na região metropolitana de Recife-PE. (na data em que escrevo isto).

## Estrutura do código

### Inputs
#### url = 'https://pe.olx.com.br/grande-recife/imoveis?o='
URL da região de interesse. Como pode ser observado ela é organizada em:
https:// + UF + .olx.com.br/ + REGIÃO DO ESTADO + /imoveis?o= + Nº DA PÁGINA
O número da página não deve ser acrescentado, pois o próprio código cuidará disso.

#### quant_pag = 100
Quantidade de páginas em que será realizado a mineração.

### ScraperLinks(url, quant_pag)
Esta função coletará o link da pagina detalhada de cada anúncio.

### ScraperPage(link)
Esta função coletará as informações de cada anúncio.

