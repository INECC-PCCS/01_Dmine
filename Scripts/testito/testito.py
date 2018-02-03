
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
