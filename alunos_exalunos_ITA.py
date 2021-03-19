############################################################################
##   Python program to scrape Wikita pages to get ITA Alumni information  ##
##   Author: Gunther Bacellar (ITA T-97)                                  ##
##   Email: gcbacel@hotmail.com                                           ##
############################################################################

from bs4 import BeautifulSoup 
import requests as req 
import re
import pandas as pd
years = [str(year) for year in range(1951, 2026)]
url = [{year: 'Turma_de_' + year for year in years}][0]
url['1982'] = 'Turma_de_1982_completa'
url['1990'] = 'Nojentos'
for year in ['1985', '2005', '2009']:
    url[year] = 'Formandos_da_Turma_' + year
url = [{u:'http://aeitaonline.com.br/wiki/index.php?title=' + url[u] for u in url}][0]
map_year = {'1959':0, '1963':1, '1994':0, '2004':2, '2005':1}
map_curso = {'Computação':'COMP', 'Eletrônica': 'ELE', 'Aeronáutica': 'AER', 'Mecânica':'MEC', 'Infra':'INFRA', 'Eletronica':'ELE', 'IN':'FUND', 'Saiu':'FUND', 'Desligado':'FUND'}
map_saiu = [".", "IN", "Saiu", "Desligado", "Turma", "École", "MIT/EUA", "59'", "08'", '07"', "QUI", "--", "André de Santo André", "foi para o IME", "Rossi saiu"]
alunos = {}

# Read all wikITA pages. Pages using table: 1959, 1963, 1994 and 2004
for year in years:
    if (int(year) % 10) == 1: 
        if year == '2021': print('Lendo páginas wikITA das turmas', int(year), '-', int(year)+4)
        else: print('Lendo páginas wikITA das turmas', int(year), '-', int(year)+9)
    html = BeautifulSoup(req.get(url[year]).text, 'lxml')
    if year in ['1959', '1963', '1994', '2004']:
        table = pd.read_html(url[year])[map_year[year]]
        for i in range(len(table)):
            alunos[table.loc[i,'Nome']] = [table.loc[i,'Curso'], table.loc[i,'Apelido'], year, '']
    else:
        for tag in html.find_all('li'):
            if tag.text.find('(')>0:
                txt = [x.strip() for x in re.split('[()]', tag.text.replace('\n', ''))]
                if len(txt)>3: txt = txt[:3]
                txt.append(year)
                if txt[2].find('alec')>=0:
                    txt[2] = ""
                    txt.append('sim')
                else: txt.append('')
                alunos[txt[0].strip()] = txt[1:]
                
# Resolve inconsistencies for different page formats
print('Eliminando inconsistencias')
df = pd.DataFrame(alunos).T.reset_index()
df.columns = ['Aluno', 'Curso', 'Apelido', 'Turma', 'Falecido']
df.drop(df.index[[3673]], inplace=True)
df.loc[df['Curso']=="", 'Curso'] = 'FUND'
df['Curso'] = [x[0] for x in df['Curso'].str.split()]
df.loc[df.Curso.str.find('alec')>0, ['Falecido', 'Curso']] = ['sim', 'FUND']
df['Curso'] = df['Curso'].apply(lambda x: map_curso[x] if x in map_curso else x)
df.loc[df.Curso.isin(map_saiu), ['Curso', 'Apelido']] = ['FUND', '']

# Save final dataframe
df.to_csv("alunos_exalunos_ITA.csv", encoding = 'latin-1', errors = 'ignore')
print('Fim: Arquivo alunos_exalunos_ITA.csv criado')