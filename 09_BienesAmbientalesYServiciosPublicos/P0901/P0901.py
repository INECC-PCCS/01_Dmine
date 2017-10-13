# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:00:05 2017

@author: carlos.arana

Descripcion:
Creacion de parametro P0901 "Denuncias recibidas en materia ambiental"
"""

# Librerias Utilizadas
import pandas as pd
import numpy as np

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\00_Parametros'
if module_path not in sys.path:
    sys.path.append(module_path)

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
DocumentarParametro | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/DocumentarParametro
"""

# Documentacion del Parametro ---------------------------------------------------------------------------------------
# Descripciones del Parametro
ClaveParametro = 'P0901'
DescParam = 'Numero de denuncias recibidas en materia ambiental, por municipio, de 1994 a 2014'
UnidadesParam = 'unidades'
NombreParametro = 'Denuncias Recibidas en Materia Ambiental'
TituloParametro = 'Denuncias_Ambiental'          # Para nombrar la columna del parametro

# Descripciones del proceso de Minería
DirFuente = r'D:\PCCS\01_Dmine\00_Parametros\BS01'
DSBase = r'"BS01.xlsx", disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/BS01'
NomDataset = r'Acciones seleccionadas en materia ambiental'
DescDataset = r'Datos de Árboles plantados, Superficie reforestada, Volumen de basura recolectada, ' \
              r'Denuncias recibidas en materia ambiental y Licencias Ambientales Únicas vigentes'
ContenidoHojaDatos = 'Numero de denuncias recibidas en materia ambiental, por municipio, de 1994 a 2014'
Notas = ''
DescVarIntegridad = 'La variable de integridad para esta parametro es el porcentaje de años ' \
                    'que cuentan con informacion, por municipio'
NomFuente = 'SIMBAD - Sistema Estatal y municipal de Base de Datos (INEGI)'
UrlFuente = r'http://sc.inegi.org.mx/cobdem/'
ActDatos = '2014'

# Descripciones generadas desde la clave del parámetro
ClaveDimension = ClaveParametro[1:3]
NomDimension = AsignarDimension(ClaveDimension)['nombre']
DirDimension = ClaveDimension + "_" + AsignarDimension(ClaveDimension)['directorio']
RepoMina = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/{}/{}'.format(DirDimension, ClaveParametro)
DirDestino = r'D:\PCCS\01_Dmine\{}'.format(ClaveDimension+"_"+AsignarDimension(ClaveDimension)['directorio'])

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Dataset Inicial
dataset = pd.read_excel(DirFuente + r'\BS01.xlsx', sheetname="DATOS", dtype={'CVE_MUN': str})
dataset.set_index('CVE_MUN', inplace=True)

# Seleccionar Columnas de Denuncias
Denuncias = [x for x in list(dataset) if 'Denuncias recibidas en materia amb' in x]

# renombrar columnas al año que corresponden
anios = list(range(1994, 2015))
registros = []
for i in anios:
    registros.append('DENUNCIAS_AMB_{}'.format(i))
denuncias_ma = dataset[Denuncias]
denuncias_ma.columns = registros

# Total de denuncias por municipios y Variable de Integridad.
faltantes = denuncias_ma.isnull().sum(axis=1)
denuncias_ma['DENUNCIAS_AMB'] = denuncias_ma.sum(axis=1)
denuncias_ma['NUM_ANIOS_FALTANTES'] = faltantes
denuncias_ma['VAR_INTEGRIDAD'] = faltantes.apply(lambda x: (21-x)/21)
var_denuncias = list(denuncias_ma)

# Consolidar datos por ciudad
denuncias_ma['CVE_MUN'] = denuncias_ma.index
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'NOM_ENT']
DatosLimpios = asignar_sun(denuncias_ma, vars=variables_SUN)
OrdenColumnas = (variables_SUN + var_denuncias)[:30]
DatosLimpios = DatosLimpios[OrdenColumnas]    # Reordenar las columnas

# Revision de integridad
integridad_parametro = SUN_integridad(DatosLimpios)
info_completa = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 1) # Para generar grafico de integridad
info_sin_info = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 0) # Para generar grafico de integridad
info_incomple = 135 - info_completa - info_sin_info                 # Para generar grafico de integridad

# Construccion del Parametro
param_dataset = DatosLimpios.set_index('CVE_SUN')
param_dataset['CVE_SUN'] = param_dataset.index
param = param_dataset.groupby(by='CVE_SUN').agg('sum')['DENUNCIAS_AMB']     # Total de denuncias
intparam = param_dataset.groupby(by='CVE_SUN').agg('mean')['VAR_INTEGRIDAD']     # Total de denuncias
std_nomsun = param_dataset['CVE_SUN'].map(str)+' - '+param_dataset['NOM_SUN']   # Nombres estandar CVE_SUN + NOM_SUN
std_nomsun.drop_duplicates(keep='first', inplace=True)
Parametro = pd.DataFrame()
Parametro['CIUDAD'] = std_nomsun
Parametro['P0901'] = param
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
