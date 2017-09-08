# -*- coding: utf-8 -*-
"""
Started on Thu Sep  7 16:46:39 2017
@author: carlos.arana
"""

'''
Descripcion:
Script para crear proxies de parametros.
Proxies Creados a partir de la lista de parametros disponibles al 
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

for indecs, row in lista.iterrows():
    DirBase = r'D:\PCCS\01_Dmine'
    SubDir = '{}_{}'.format(row['ClaveDimension'], AsignarDimension(row['ClaveDimension'])['directorio'])
    DirDestino = '{}_{}\{}'.format(DirBase, SubDir, indecs)
    if not os.path.isdir(DirDestino):       # Crea un Directorio si es que no existe
        os.makedirs(DirDestino)
    if not indecs in HojaIndice.index:      # Crea un proxy de informacion para un solo parametro
        DatosIndice = pd.DataFrame(index=[indecs],
                                   data={
                                       'NOM_PARAMETRO': row['Nombre Parametro'],
                                       'ARCHIVO_LOCAL': 'proxy',
                                       'URL_MINERIA': 'proxy'
                                   })
        HojaIndice.loc[DatosIndice.iloc[0].name] = DatosIndice.iloc[0]  # Escribe el proxy en el indice
    if not indecs in HojaParametros:


    print(DirDestino)

HojaParametros


def HazProxy(ID_PARAMETRO):
    indice = HojaParametros.index
    ProxyValores = random.sample(range(100,1000), 135)
    Proxy = pd.Series(data=ProxyValores, index=indice, name=ID_PARAMETRO)
    return Proxy

'P0901' in list(HojaParametros)

HojaIndice.loc['P0901']