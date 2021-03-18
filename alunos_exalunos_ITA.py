from bs4 import BeautifulSoup 
import requests as req 
import re
import pandas as pd
url = "http://aeitaonline.com.br/wiki/index.php?title=Turma_de_"
years = [str(year) for year in range(1951, 2026)]
alunos = {}

# read all pages os all years except 1959, 1963, 1994, 2004
for year in years:
    url_full = url + year
    if year == '1982': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Turma_de_1982_completa'
    if year == '1985': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Formandos_da_Turma_1985'
    if year == '1990': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Nojentos'
    if year == '2005': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Formandos_da_Turma_2005'
    if year == '2009': url_full = 'http://aeitaonline.com.br/wiki/index.php?title=Formandos_da_Turma_2009'
    web = req.get(url_full)
    html = BeautifulSoup(web.text, 'lxml')
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

# read pages of years 1959, 1963, 1994, 2004
years = ['1959', '1963', '1994', '2004']
for year in years:
    map_year = {'1959':0, '1963':1, '1994':0, '2004':2, '2005':1}
    table = pd.read_html(url + year)[map_year[year]]
    for i in range(len(table)):
        alunos[table.loc[i,'Nome']] = [table.loc[i,'Curso'], table.loc[i,'Apelido'], year, '']
            
df = pd.DataFrame(alunos).T.reset_index()
df.columns = ['Aluno', 'Curso', 'Apelido', 'Turma', 'Falecido']

# resolve inconsistencies for different page formats
df.drop(df.index[[560,2900, 559, 4515, 4514, 4613, 4614, 3455, 4740, 4741, 4846, 4847]], inplace=True)
df.loc[df['Curso']=="", 'Curso'] = 'FUND'
df['Curso'] = [x[0] for x in df['Curso'].str.split()]
df.loc[df.Curso.str.find('alec')>0, 'Falecido'] = 'sim'
df.loc[df.Curso.str.find('alec')>0, 'Curso'] = ''
map_curso = {'Computação':'COMP', 'Eletrônica': 'ELE', 'Aeronáutica': 'AER', 'Mecânica':'MEC', 'Infra':'INFRA', 'Eletronica':'ELE', 'IN':'FUND', 'Saiu':'FUND', 'Desligado':'FUND'}
df['Curso'] = df['Curso'].apply(lambda x: map_curso[x] if x in map_curso else x)
df['Curso'] = df['Curso'].apply(lambda x: "FUND" if x in ["IN", "Saiu", "Desligado"] else x)
df['Curso'] = df['Curso'].apply(lambda x: "" if x in ["Turma", "École", "MIT/EUA", "59'", "08'", '07"', "QUI", "--"] else x)
df.loc[df['Curso']=="", 'Curso'] = 'FUND'
df['Apelido'] = df['Apelido'].apply(lambda x: "" if x=="." else x)
map_saiu = ['André de Santo André saiu no segundo ano', 'foi para o IME antes das aulas do ITA começarem', 'Rossi saiu em 1986']
df.loc[df.Curso.isin(map_saiu), 'Curso'] = 'FUND'
df['Apelido'] = df['Apelido'].apply(lambda x: "" if x in map_saiu else x)

# save final dataframe
df.to_csv("alunos_exalunos_ITA.csv", encoding = 'latin-1', errors = 'ignore')
