# -*- coding: utf-8 -*-
"""
Started on Thu Sep  7 16:46:39 2017
@author: carlos.arana
"""

'''
Descripcion:
Script para crear proxies de parametros.
Proxies Creados a partir de la lista de parametros disponibles al 11 de septiembre de 2017


'''
import pandas as pd
import os
import random

module_path = r'D:\PCCS\01_Dmine\00_Parametros'
if module_path not in sys.path:
    sys.path.append(module_path)

from AsignarDimension.AsignarDimension import AsignarDimension

RutaEntrada = r'D:\PCCS\ListaParametros.xlsx'

lista = pd.read_excel(RutaEntrada, sheetname='lista', index_col = 0,
                      dtype={'ClaveDimension' : str})

# Cargar archivo integrador
RutaIntegrador = r'D:\PCCS\01_Dmine\00_Parametros\CatalogoParametros.xlsx'
HojaIndice = pd.read_excel(RutaIntegrador, sheetname='INDICE', index_col = 0)
HojaParametros = pd.read_excel(RutaIntegrador, sheetname='PARAMETROS', index_col = 0)
HojaIntegridad = pd.read_excel(RutaIntegrador, sheetname='INTEGRIDAD', index_col = 0)

# Funciones para creacion de proxies
def HazProxy(ID_PARAMETRO):
    indice = HojaParametros.index
    ProxyValores = random.sample(range(100,1000), 135)
    Proxy = pd.Series(data=ProxyValores, index=indice, name=ID_PARAMETRO)
    return Proxy

def HazProxyIntegridad(ID_PARAMETRO):
    indice = HojaParametros.index
    ProxyValores = np.random.sample(135).tolist()
    Proxy = pd.Series(data=ProxyValores, index=indice, name=ID_PARAMETRO)
    return Proxy.round(decimals=3)

EsProxy = '(Mineria de datos de parametro pendiente)\n\nProxy creado con fines de coordinacion'

for indecs, row in lista.iterrows():
    DirBase = r'D:\PCCS\01_Dmine'
    SubDir = '{}_{}'.format(row['ClaveDimension'], AsignarDimension(row['ClaveDimension'])['directorio'])
    DirDestino = r'{}\{}\{}'.format(DirBase, SubDir, indecs)
    RepoBase = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/'
    SubRepo = '{}{}/{}'.format(RepoBase, SubDir, indecs)
    if not os.path.isdir(DirDestino):       # Crea un Directorio si es que no existe
        os.makedirs(DirDestino)
        readmefile = '{}\README.md'.format(DirDestino)
        Glosa = '#[PROXY] {} - {}\n\n{}'.format(indecs, row['Nombre Parametro'],EsProxy)
        with open(readmefile, 'w') as README:
            README.write(Glosa)

    if not indecs in HojaIndice.index:      # Crea un proxy de informacion para un solo parametro
        DatosIndice = pd.DataFrame(index=[indecs],
                                   data={
                                       'NOM_PARAMETRO': row['Nombre Parametro'],
                                       'ARCHIVO_LOCAL': 'proxy',
                                       'URL_MINERIA': SubRepo
                                   })
        HojaIndice.loc[DatosIndice.iloc[0].name] = DatosIndice.iloc[0]  # Escribe el proxy en el indice
    else: continue
    if not indecs in HojaParametros:        # Crea un proxy del parámetro
        HojaParametros[indecs] = HazProxy(indecs)
        HojaIntegridad[indecs] = HazProxyIntegridad(indecs)
    else: continue
    print('Proxy creado para {} - {}\nCarpeta: {}\nRepo: {}'.format(indecs, row['Nombre Parametro'], DirDestino, SubRepo))

# Guardar archivo integrador
writer = pd.ExcelWriter(RutaEntrada)
HojaIndice.to_excel(writer, sheet_name='INDICE')
HojaParametros.to_excel(writer, sheet_name='PARAMETROS')
HojaIntegridad.to_excel(writer, sheet_name='INTEGRIDAD')
writer.save()
