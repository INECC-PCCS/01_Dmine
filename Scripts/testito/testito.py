
'''
archivo para pruebas
'''


'test.csv'.endswith('.csv')

def testito():
    print('Test Success!!')


import json
thefile = r'D:\PCCS\01_Dmine\10_ResiduosSolidosUrbanos\P1017\P1017.json'

with open(thefile) as json_data:
    data = json.load(json_data)
    print(json.dumps(data, indent=4, sort_keys=True))

print(data['Metadatos'])


M.name
M.ClaveParametro
M.NombreParametro
M.DescParam
M.UnidadesParam
M.TituloParametro
M.PeriodoParam
M.TipoInt

M.ParDtype
M.TipoVar
M.array
M.TipoAgr

M.nomarchivodataset
M.extarchivodataset
M.ArchivoDataset
M.ContenidoHojaDatos
M.ClaveDataset
M.ActDatos
M.Agregacion
M.DescVarIntegridad
M.DirFuente
M.DSBase
M.ClaveDimension
M.NomDimension
M.DirDimension
M.RepoMina
M.DirDestino

M.NomDataset
M.DescDataset
M.DispTemp
M.PeriodoAct
M.DesagrMax
M.Notas
M.NomFuente
M.UrlFuente

M.getmetafromds
M.NomDataset
M.DescDataset
M.DispTemp
M.PeriodoAct
M.DesagrMax
M.Notas
M.NomFuente
M.UrlFuente
M.ArchivoDataset
M.DirFuente
M.DSBase
M.ClaveDimension
M.NomDimension
M.DirDimension
M.RepoMina
M.DirDestino
M.DescVarIntegridad


def errores(que):
    if que == 1:
        raise AttributeError('se cancela todo')
    print('no se cancelo nada')

data = {'name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'year': [2012, 2012, 2013, 2014, 2014],
        'reports': [4, 24, 31, 2, 3]}
df = pd.DataFrame(data, index = ['Cochice', 'Pima', 'Santa Cruz', 'Maricopa', 'Yuma'])

df.head()
list(df.year.unique())

df = pd.DataFrame([['de', None, None],
                   ['de ditos', 2, 3],
                   [4, None, None],
                   [None, None, 9],
                   ['de', 4, 6]])


def erasedes(x):
    if x == 'de':
        return None
    else:
        pass

df[0] = df[0].apply(lambda x: erasedes(x))


df = pd.DataFrame([['de', None, None],
                   ['de ditos', 2, 3],
                   [4, None, None],
                   [None, None, 9],
                   ['de', 4, 6]])

sr = pd.Series([[None, 4, 6]])


import numpy as np
import json

file = r'D:\testjson.json'
x = {'a' : np.int64(1)}
y = {'a' : np.float64(1)}

with open(file, 'wb') as f:
    json.dump(x, codecs.getwriter('utf-8')(f), ensure_ascii=False)

with open(file, 'wb') as f:
    json.dump(y, codecs.getwriter('utf-8')(f), ensure_ascii=False)


import requests
import pyperclip

quant = input('\n\nCONVERTIR DOLARES A PESOS\no [Enter] para convertir pesos a dolares \n\n---\n\nÂ¿CuÃ¡ntos dolares, corazon?>>> ')
BASEURL = 'https://openexchangerates.org/api/latest.json'
APPID = '?app_id=4d21a13c8485473db4fe16a6d90363e2'
base = 'USD'
convert = 'MXN'
BASECUR = '&base={}'.format(base)
response = requests.get(BASEURL + APPID + BASECUR)
rate = response.json()['rates'][convert]
if quant == '':
    quant = input('\nCONVERTIR PESOS A DOLARES\n---\nÂ¿CuÃ¡ntos pesos, mi amor? >>>')
    base = 'MXN'
    convert = 'USD'
    rate = 1/rate

if '+' in quant:
    quant = sum([float(x) for x in quant.split('+')])

tipodecambio = base+convert
baseinput = float(quant)
conversion = baseinput * rate
t_baseinput = '${:,.4f}'.format(baseinput)
t_conversion = '${:,.4f}'.format(conversion)

print('\nConvertir {} {} a {}'.format(t_baseinput, base, convert))
print('\nTipo de cambio {}{} = {}\n'.format(base, convert, rate))
nextline = '| {} {} = {} {} |'.format(base, t_baseinput, convert, t_conversion)
box = '-'*(len(nextline)-2)
print('|{}|\n{}\n|{}|\n'.format(box, nextline, box))
one = '\n[c] para copiar tipo de cambio {} ({}) o'.format(tipodecambio, rate)
two = '\n[v] para copiar la conversion ({})'.format(t_conversion)

fin = input('\n...\n\nPresiona \n[enter] para terminar\n\no si quieres copiar al clipboard:{}{}'.format(one, two))
if fin == 'c':
    pyperclip.copy(str(rate))
elif fin == 'v':
    pyperclip.copy(str(conversion))

import pandas as pd

df = pd.DataFrame([['00100', 'Alpha', True, None],
                   ['00100', 'Beta', None, None],
                   ['05300', 'Theta', True, None],
                   ['95687', 'Gamma', False, None],
                   ['05300', 'Sigma', None, None]])

df = df.set_index(0)

match = {
    '00100' : '09010',
    '05300' : '09004'
}

df = pd.DataFrame([['00100', 'one.xlsx', 'sheet1'],
                   ['00100', 'two.xlsx', 'sheet2'],
                   ['05300', 'thr.xlsx', 'sheet3'],
                   ['95687', 'fou.xlsx', 'sheet4'],
                   ['05300', 'fiv.xlsx', 'sheet5']],
                  columns=['id', 'file', 'sheet'])

df = df.rename(columns = {0:'A', 1:'B', 2:'C'})

def