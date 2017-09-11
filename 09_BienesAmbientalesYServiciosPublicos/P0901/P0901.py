# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:00:05 2017

@author: carlos.arana
"""

'''
Descripcion:
Creacion de dataset P0901 "Denuncias recibidas en materia ambiental"
'''

# Librerias Utilizadas
import pandas as pd
import numpy as np

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\00_Parametros'
if module_path not in sys.path:
    sys.path.append(module_path)

from SUN.asignar_sun import asignar_sun                     # Disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/SUN
from SUN_integridad.SUN_integridad import SUN_integridad    # Disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/SUN_integridad
from PCCS_variables.PCCS_variables import variables         # Disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/PCCS_variables
from ParametroEstandar.ParametroEstandar import ParametroEstandar # Disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/PCCS_variables

# Descripciones del Parametro
DirFuente = r'D:\PCCS\01_Dmine\00_Parametros\BS01'
DirDestino = r'D:\PCCS\01_Dmine\09_BienesAmbientalesYServiciosPublicos'
ClaveParametro = 'P0901'
NombreParametro = 'Denuncias Recibidas en Materia Ambiental'
ClaveDimension = ClaveParametro[1:3]
NomDimension = AsignarDimension(ClaveDimension)['nombre']
TituloParametro = ClaveParametro
ActDatos = '2014'

# Dataset Inicial
dataset = pd.read_excel(DirFuente + r'\BS01.xlsx', sheetname="DATOS", dtype={'CVE_MUN':str})
dataset.set_index('CVE_MUN', inplace = True)

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

faltantes = denuncias_ma.isnull().sum(axis = 1)
denuncias_ma['DENUNCIAS_AMB'] = denuncias_ma.sum(axis=1)

denuncias_ma['NUM_ANIOS_FALTANTES'] = faltantes
denuncias_ma['VAR_INTEGRIDAD'] = faltantes.apply(lambda x: (21-x)/21)
var_denuncias = list(denuncias_ma)

# Consolidar datos por ciudad
denuncias_ma['CVE_MUN'] = denuncias_ma.index
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'NOM_ENT']

DatosLimpios = asignar_sun(denuncias_ma, vars = variables_SUN)
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
std_nomsun.drop_duplicates(keep='first', inplace = True)
Parametro = pd.DataFrame()
Parametro['CIUDAD'] = std_nomsun
Parametro['P0901'] = param
Parametro['INTEGRIDAD'] = intparam
Parametro = Parametro.sort_index()

# Lista de Variables
variables_locales = sorted(list(set(list(DatosLimpios) +
                                    list(integridad_parametro['INTEGRIDAD']) +
                                    list(integridad_parametro['EXISTENCIA']) +
                                    list(Parametro))))

metavariables = variables(variables_locales)

# Metadatos
d_hojas = {
    'HOJAS INCLUIDAS EN EL LIBRO' : np.nan,
    'METADATOS' : 'Descripciones y notas relativas al Dataset',
    'PARAMETRO' : 'Dataset resultado de la minería, agregado por clave del Sistema Urbano Nacional, para utilizarse en la construcción de Indicadores',
    'DATOS' : 'Numero de denuncias recibidas en materia ambiental, por municipio, de 1994 a 2014',
    'INTEGRIDAD' : 'Revision de integridad de la información POR CLAVE DEL SUN. Promedio de VAR_INTEGRIDAD de los municipios que componen una ciudad. Si no se tiene información para el municipio, VAR_INTEGRIDAD es igual a cero',
    'EXISTENCIA' : 'Revision de integridad de la información POR MUNICIPIO.'
}

d_mineria = {
    '  ': np.nan,
    'DESCRIPCION DEL PROCESO DE MINERIA:' : np.nan,
    'Nombre del Dataset' : NombreParametro,
    'Descripcion del dataset' : 'Numero de denuncias recibidas en materia ambiental, por municipio, de 1994 a 2014',
    'Fuente'    : 'SIMBAD - Sistema Estatal y municipal de Base de Datos (INEGI)',
    'URL_Fuente': 'http://sc.inegi.org.mx/cobdem/',
    'Dataset base' : '"BS01.xlsx", disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/BS01' ,
    'Repositorio de mineria' : 'https://github.com/INECC-PCCS/01_Dmine/tree/master/09_BienesAmbientalesYServiciosPublicos/P0901',
    'Notas' : 'Sin Notas',
    'VAR_INTEGRIDAD' : 'La variable de integridad para esta Dataset es el porcentaje de años que cuentan con informacion, por municipio',
    ' ' : np.nan,
    'DESCRIPCION DE VARIABLES' : np.nan
}

descripcion_hojas = pd.DataFrame.from_dict(d_hojas, orient='index').rename(columns={0:'DESCRIPCION'})
descripcion_mineria = pd.DataFrame.from_dict(d_mineria, orient='index').rename(columns={0:'DESCRIPCION'})

MetaParametro = descripcion_hojas.append(descripcion_mineria).append(metavariables)

# Diccionario de Descripciones
DescParametro = {
    'ClaveParametro' : ClaveParametro,
    'NombreParametro' : NombreParametro,
    'info_completa' : info_completa,
    'info_sin_info' : info_sin_info,
    'info_incomple' : info_incomple,
    'RutaSalida' : DirDestino,
    'Clave de Dimension': ClaveDimension,
    'Nombre de Dimension': NomDimension,
    'Titulo de Columna': TituloParametro,
    'Actualizacion de datos' : ActDatos
}

# Crear archivo de Excel
ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro)
DocumentarParametro(DescParametro, MetaParametro, Parametro)