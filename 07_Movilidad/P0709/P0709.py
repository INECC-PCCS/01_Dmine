# -*- coding: utf-8 -*-
"""
Started on Wed Sep 13 15:55:22 2017

@author: carlos.arana

Descripcion: Creación de dataset para el parámetro P0709 "Vehiculos de Pasajeros"
Informacion disponible para 2016
"""

import pandas as pd
import numpy as np
import sys

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)

from SUN.asignar_sun import asignar_sun
from SUN_integridad.SUN_integridad import SUN_integridad
from PCCS_variables.PCCS_variables import variables
from ParametroEstandar.ParametroEstandar import ParametroEstandar
from AsignarDimension.AsignarDimension import AsignarDimension
from DocumentarParametro.DocumentarParametro import DocumentarParametro

"""
Las librerias locales utilizadas renglones arriba se encuentran disponibles en las siguientes direcciones:
SCRIPT:             | DISPONIBLE EN:
------              | ------
asignar_sun         | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN
SUN_integridad      | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN_integridad
variables           | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/PCCS_variables
ParametroEstandar   | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/ParametroEstandar
AsignarDimension    | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/AsignarDimension
DocumentarParametro 1 https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/DocumentarParametro

"""

# Documentacion del Parametro ---------------------------------------------------------------------------------------
# Descripciones del Parametro
ClaveParametro = 'P0709'
DescParam = 'Vehiculos de pasajeros registrados. Datos Disponibles para 2016'
UnidadesParam = 'unidades'
NombreParametro = 'Vehiculos de Pasajeros'
TituloParametro = 'VEHICULOS_PASAJEROS'          # Para nombrar la columna del parametro

# Descripciones del proceso de Minería
DirFuente = r'D:\PCCS\01_Dmine\00_Parametros\MV01'
DSBase = '"MV01.xlsx", disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/MV01'
NomDataset = r'Vehiculos registrados'
DescDataset = r'Numero de vehiculos registrados por municipio entre 1980 y 2016'
ContenidoHojaDatos = 'Numero de Camiones de pasajeros por municipio de 1980 a 2016'   # Contenido de la hoja 'Datos'
Notas = 'Se utiliza únicamente el dato más reciente para construir el parámetro'
DescVarIntegridad = 'La variable de integridad municipal para esta Dataset es binaria: \n' \
                    '1 =  El municipio cuenta con informacion \n0 = El municipio no cuenta con información'
NomFuente = 'SIMBAD - Sistema Estatal y municipal de Base de Datos (INEGI)'
UrlFuente = 'http://sc.inegi.org.mx/cobdem/'
ActDatos = '2016'

# Descripciones generadas desde la clave del parámetro
ClaveDimension = ClaveParametro[1:3]
NomDimension = AsignarDimension(ClaveDimension)['nombre']
DirDimension = ClaveDimension + "_" + AsignarDimension(ClaveDimension)['directorio']
RepoMina = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/{}/{}'.format(DirDimension, ClaveParametro)
DirDestino = r'D:\PCCS\01_Dmine\{}'.format(ClaveDimension+"_"+AsignarDimension(ClaveDimension)['directorio'])

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Dataset Inicial
dataset = pd.read_excel(DirFuente + r'\MV01.xlsx', sheetname="DATOS", dtype={'CVE_MUN': str})
dataset.set_index('CVE_MUN', inplace=True)

# Elegir columnas de vehiculos de pasajeros
Columnas_raw = [x for x in list(dataset) if 'pasaje' in x]

# Separar datos de camiones de pasajeros y renombrar columnas al año que corresponden
anios = list(range(1980, 2017))
registros = []
for i in anios:
    registros.append('CAM_PASAJEROS_{}'.format(i))

dataset = dataset[Columnas_raw]
dataset.columns = registros

# Vehiculos de pasajeros y Variable de Integridad.
dataset[TituloParametro] = dataset['CAM_PASAJEROS_2016']
faltantes = dataset[TituloParametro].isnull()

# Calculo de Variable de Integridad.
dataset['FALTANTES'] = faltantes
dataset['VAR_INTEGRIDAD'] = faltantes.apply(lambda x: int(not x))
variables_dataset = list(dataset)

# Consolidar datos por ciudad
dataset['CVE_MUN'] = dataset.index
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'NOM_ENT']

DatosLimpios = asignar_sun(dataset, vars=variables_SUN)
OrdenColumnas = (variables_SUN + variables_dataset)
DatosLimpios = DatosLimpios[OrdenColumnas]    # Reordenar las columnas

# Revision de integridad
integridad_parametro = SUN_integridad(DatosLimpios)
info_completa = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 1) # Para generar grafico de integridad
info_sin_info = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 0) # Para generar grafico de integridad
info_incomple = 135 - info_completa - info_sin_info                 # Para generar grafico de integridad

# Construccion del Parametro
param_dataset = DatosLimpios.set_index('CVE_SUN')
param_dataset['CVE_SUN'] = param_dataset.index
param = param_dataset.groupby(by='CVE_SUN').agg('sum')[TituloParametro]     # Total de Area Verde por Ciudad
intparam = param_dataset.groupby(by='CVE_SUN').agg('mean')['VAR_INTEGRIDAD']     # Integridad por ciudad
std_nomsun = param_dataset['CVE_SUN'].map(str)+' - '+param_dataset['NOM_SUN']   # Nombres estandar CVE_SUN + NOM_SUN
std_nomsun.drop_duplicates(keep='first', inplace=True)
Parametro = pd.DataFrame()
Parametro['CIUDAD'] = std_nomsun
Parametro[ClaveParametro] = param
Parametro['INTEGRIDAD'] = intparam
Parametro = Parametro.sort_index()

# Creacion de documentos de memoria del Parametro --------------------------------------------------------------------
# Lista de Variables
variables_locales = sorted(list(set(list(DatosLimpios) +
                                    list(integridad_parametro['INTEGRIDAD']) +
                                    list(integridad_parametro['EXISTENCIA']) +
                                    list(Parametro))))

metavariables = variables(variables_locales)

# Metadatos
d_parametro = {
    'DESCRIPCION DEL PARAMETRO': np.nan,
    'Clave': ClaveParametro,
    'Nombre del Parametro': NombreParametro,
    'Descripcion del Parametro': DescParam,
    'Unidades': UnidadesParam
}

d_hojas = {
    'METADATOS': 'Descripciones y notas relativas al Dataset',
    'PARAMETRO': 'Dataset resultado de la minería, agregado por clave del Sistema Urbano Nacional, '
                 'para utilizarse en la construcción de Indicadores',
    'DATOS': ContenidoHojaDatos,
    'INTEGRIDAD': 'Revision de integridad de la información POR CLAVE DEL SUN. ' 
                  'Promedio de VAR_INTEGRIDAD de los municipios que componen una ciudad. '
                  'Si no se tiene información para el municipio, VAR_INTEGRIDAD es igual a cero',
    'EXISTENCIA': 'Revision de integridad de la información POR MUNICIPIO.',
    '     ': np.nan,
    'DESCRIPCION DE VARIABLES': np.nan
}

d_mineria = {
    '  ': np.nan,
    'DESCRIPCION DEL PROCESO DE MINERIA:': np.nan,
    'Nombre del Dataset': NomDataset,
    'Descripcion del dataset': DescDataset,
    'Notas': Notas,
    'Fuente': NomFuente,
    'URL_Fuente': UrlFuente,
    'Dataset base': DSBase,
    'Repositorio de mineria': RepoMina,
    'VAR_INTEGRIDAD': DescVarIntegridad,
    ' ': np.nan,
    'HOJAS INCLUIDAS EN EL LIBRO': np.nan
}

descripcion_parametro = pd.DataFrame.from_dict(d_parametro, orient='index').rename(columns={0: 'DESCRIPCION'})
descripcion_mineria = pd.DataFrame.from_dict(d_mineria, orient='index').rename(columns={0: 'DESCRIPCION'})
descripcion_hojas = pd.DataFrame.from_dict(d_hojas, orient='index').rename(columns={0: 'DESCRIPCION'})
MetaParametro = descripcion_parametro.append(descripcion_mineria).append(descripcion_hojas).append(metavariables)

# Diccionario de Descripciones
DescParametro = {
    'ClaveParametro': ClaveParametro,
    'NombreParametro': NombreParametro,
    'info_completa': info_completa,
    'info_sin_info': info_sin_info,
    'info_incomple': info_incomple,
    'RutaSalida': DirDestino,
    'Clave de Dimension': ClaveDimension,
    'Nombre de Dimension': NomDimension,
    'Titulo de Columna': TituloParametro,
    'Actualizacion de datos': ActDatos
}

# Crear archivo de Excel y documentar parametro
ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro)
DocumentarParametro(DescParametro, MetaParametro, Parametro)
