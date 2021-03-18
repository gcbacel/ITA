import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://aeitaonline.com.br/wiki/index.php?title=Turma_de_"
websites = {}
years = [str(year) for year in range(1951, 2026)]
for year in years:
    url_full = url + year
    if year == '1982': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Turma_de_1982_completa'
    if year == '1985': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Formandos_da_Turma_1985'
    if year == '1990': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Nojentos'
    if year == '2005': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Formandos_da_Turma_2005'
    if year == '2009': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Formandos_da_Turma_2009'
    websites[year] = url_full
for year in years:
    html = urlopen(websites[year])
    bs = BeautifulSoup(html, 'html.parser')
    images2 = bs.find_all('img', {'src':re.compile('.jpg')})
    for image in images2: 
        print(image['src'])
        r = urlopen('http://aeitaonline.com.br' + image['src'])
        name = year + '_' + image['src'].split('/')[-1]
        with open(name, "wb") as f:
            f.write(r.read())
