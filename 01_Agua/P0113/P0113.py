# -*- coding: utf-8 -*-
"""
Started on wed, oct 25th, 2017

@author: carlos.arana

Descripcion:

"""

import pandas as pd
import numpy as np
import sys

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)

from SUN.asignar_sun import asignar_sun

from SUN.CargaSunPrincipal import getsun
from SUN_integridad.SUN_integridad import SUN_integridad
from PCCS_variables.PCCS_variables import variables
from ParametroEstandar.ParametroEstandar import ParametroEstandar
from AsignarDimension.AsignarDimension import AsignarDimension
from DocumentarParametro.DocumentarParametro import DocumentarParametro

"""
Las librerias locales utilizadas renglones arriba se encuentran disponibles en las siguientes direcciones:
SCRIPT:             | DISPONIBLE EN:
------              | ------------------------------------------------------------------------------------
asignar_sun         | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN
SUN_integridad      | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN_integridad
variables           | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/PCCS_variables
ParametroEstandar   | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/ParametroEstandar
AsignarDimension    | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/AsignarDimension
DocumentarParametro 1 https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/DocumentarParametro
"""

# Documentacion del Parametro ---------------------------------------------------------------------------------------
# Descripciones del Parametro
ClaveParametro = 'P0113'
DescParam = 'Consumo'
UnidadesParam = 'l/h/d'
NombreParametro = 'Consumo'
TituloParametro = 'Consumo'                              # Para nombrar la columna del parametro

# Descripciones del proceso de Minería
ClaveDataset = 'Pigoo'
NomDataset = r'Programa de Indicadores de Gestión de Organismos Operadores'
DescDataset = r'Indicadores municipales generados por los Organismos Operadores de agua, recolectados por el ' \
              r'Instituto Mexicano De Tecnologia del Agua y la Secretaría de Medio Ambiente y Recursos Naturales'
ContenidoHojaDatos = ''
Notas = 'S/N'
DescVarIntegridad = 'La variable de integridad municipal para esta Dataset es binaria: \n' \
                    '1 =  El municipio cuenta con informacion \n0 = El municipio no cuenta con información'
NomFuente = 'Programa de Indicadores de Gestión de Organismos Operadores'
UrlFuente = 'http://www.pigoo.gob.mx/index.php?option=com_content&view=article&id=674&Itemid=1677'
ActDatos = '2015'
DispTemp = '2002 a 2015'
PeriodoAct = 'Anual'
DesagrMax = 'Municipal'

# Descripciones generadas desde la clave del parámetro
DirFuente = r'D:\PCCS\01_Dmine\Datasets\{}'.format(ClaveDataset)
DSBase = '"{}.csv", disponible en ' \
         'https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/{}'.format(ClaveDataset, ClaveDataset)
ClaveDimension = ClaveParametro[1:3]
NomDimension = AsignarDimension(ClaveDimension)['nombre']
DirDimension = ClaveDimension + "_" + AsignarDimension(ClaveDimension)['directorio']
RepoMina = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/{}/{}'.format(DirDimension, ClaveParametro)
DirDestino = r'D:\PCCS\01_Dmine\{}'.format(ClaveDimension+"_"+AsignarDimension(ClaveDimension)['directorio'])

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Dataset Inicial
dataset = pd.read_csv(DirFuente + r'\{}.csv'.format(ClaveDataset),
                        header = 3,
                        dtype={'CVE_MUN': str})
dataset = dataset[dataset['indicador'] == 'Consumo (l/h/d)']

dataset.set_index('CVE_MUN', inplace=True)

pigoo_geo = pd.read_excel(r'D:\PCCS\01_Dmine\Datasets\Pigoo\pigoo_start.xlsx',
                          sheetname="datos")
d2 = pd.merge(dataset, pigoo_geo[['Nombre- PIGOO', 'CVE_MUN']], how='left', left_on='ciudad', right_on='Nombre- PIGOO')

# Elegir dato más actual y convertir a dataset
dataset = dataset['2015']
proxy = pd.DataFrame()
proxy['Total_Parametro'] = dataset
dataset = proxy

# Total de accidentes por municipio y Variable de Integridad.
faltantes = dataset.isnull()
dataset[TituloParametro] = dataset.sum(axis=1)
y = len(list(dataset))-1      # y representa el numero de variables que se utilizan para construir el parámetro
dataset['FALTANTES'] = faltantes
dataset['VAR_INTEGRIDAD'] = faltantes.apply(lambda x: (y - x) / y)
variables_dataset = list(dataset)

# Consolidar datos por ciudad
dataset['CVE_MUN'] = dataset.index
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'NOM_ENT']
DatosLimpios = asignar_sun(dataset, vars=variables_SUN)
OrdenColumnas = (variables_SUN + variables_dataset)
DatosLimpios = DatosLimpios[OrdenColumnas]    # Reordenar las columnas

# Revision de integridad
integridad_parametro = SUN_integridad(DatosLimpios)
info_completa = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 1)      # Para generar grafico de integridad
info_sin_info = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 0)      # Para generar grafico de integridad
info_incomple = 135 - info_completa - info_sin_info                             # Para generar grafico de integridad

# Construccion del Parametro
param_dataset = DatosLimpios.set_index('CVE_SUN')
param_dataset['CVE_SUN'] = param_dataset.index
param = param_dataset.groupby(by='CVE_SUN').agg('sum')[TituloParametro]         # Total de Area Verde por Ciudad
intparam = param_dataset.groupby(by='CVE_SUN').agg('mean')['VAR_INTEGRIDAD']    # Integridad por ciudad
std_nomsun = param_dataset['CVE_SUN'].map(str)+' - '+param_dataset['NOM_SUN']   # Nombres estandar CVE_SUN + NOM_SUN
std_nomsun.drop_duplicates(keep='first', inplace=True)
Parametro = pd.DataFrame()
Parametro['CIUDAD'] = std_nomsun
Parametro[ClaveParametro] = param
Parametro['INTEGRIDAD'] = intparam
Parametro = Parametro.sort_index()

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
    'Disponibilidad Temporal': DispTemp,
    'Periodo de actualizacion': PeriodoAct,
    'Nivel de Desagregacion': DesagrMax,
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
