# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:55:22 2017

@author: carlos.arana
"""

'''
Descripcion: Creación de dataset para el parámetro P0904 "Uso de Suelo y Vegetacions"
Informacion disponible para 2015
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
DirFuente = r'D:\PCCS\01_Dmine\00_Parametros\BS02'
DirDestino = r'D:\PCCS\01_Dmine\09_BienesAmbientalesYServiciosPublicos'
ClaveParametro = 'P0904'
NombreParametro = 'Uso de Suelo y Vegetacion'
ContenidoDatos = 'Area verde y urbana por clave SUN'     # Contenido de la hoja 'Datos'
Notas = 'Las areas verdes de un municipio son todas aquellas que en el dataset original aparecen como Agricultura, ' \
        'Pastizal, Bosque, Selva, Matorral Xerófilo, Otros Tipos de Vegetacion, Vegetación Secundaria\n Las Areas ' \
        'Urbanas son aquellas especificamente etiquetadas de este modo. Los Cuerpos de Agua y Areas sin vegetación ' \
        'no se toman en consideracion para el análisis'
RepoMina = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/09_BienesAmbientalesYServiciosPublicos/P0904'
DescVarIntegridad = 'La variable de integridad para esta Dataset es el porcentaje variables que cuentan con informacion' \
                    'para cada municipio'

# Dataset Inicial
dataset = pd.read_excel(DirFuente + r'\BS02.xlsx', sheetname="DATOS", dtype={'CVE_MUN':str})
dataset.set_index('CVE_MUN', inplace = True)

# Escluir columnas que no se utilizarán
del dataset['Áreas sin vegetación']
del dataset['Cuerpos de agua']
del dataset['Nombre']

Columnas_verde = list(dataset)[2:9]
dataset_v = dataset[Columnas_verde]

# Total de area verde por municipios y Variable de Integridad.
faltantes = dataset.isnull().sum(axis = 1)
dataset['AREA_VERDE'] = dataset_v.sum(axis=1)

dataset.head()

# Calculo de Variable de Integridad.
dataset['NUM_ANIOS_FALTANTES'] = faltantes
dataset['VAR_INTEGRIDAD'] = faltantes.apply(lambda x: (11 - x) / 11)
variables_dataset = list(dataset)

# Consolidar datos por ciudad
dataset['CVE_MUN'] = dataset.index
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'NOM_ENT']

DatosLimpios = asignar_sun(dataset, vars = variables_SUN)
OrdenColumnas = (variables_SUN + variables_dataset)[:19]
DatosLimpios = DatosLimpios[OrdenColumnas]    # Reordenar las columnas

# Revision de integridad
integridad_parametro = SUN_integridad(DatosLimpios)
info_completa = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 1) # Para generar grafico de integridad
info_sin_info = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 0) # Para generar grafico de integridad
info_incomple = 135 - info_completa - info_sin_info                 # Para generar grafico de integridad

# Construccion del Parametro
param_dataset = DatosLimpios.set_index('CVE_SUN')
param_dataset['CVE_SUN'] = param_dataset.index
param = param_dataset.groupby(by='CVE_SUN').agg('sum')['AREA_VERDE']     # Total de Area Verde por Ciudad
param2 = param_dataset.groupby(by='CVE_SUN').agg('sum')['Áreas urbanas']    # Total de Area Urbana por Ciudad
param3 = param_dataset.groupby(by='CVE_SUN').agg('sum')['Superficie continental (Kilómetros cuadrados)']    # Total de Superficie Continental
intparam = param_dataset.groupby(by='CVE_SUN').agg('mean')['VAR_INTEGRIDAD']     # Integridad por ciudad
std_nomsun = param_dataset['CVE_SUN'].map(str)+' - '+param_dataset['NOM_SUN']   # Nombres estandar CVE_SUN + NOM_SUN
std_nomsun.drop_duplicates(keep='first', inplace = True)
Parametro = pd.DataFrame()
Parametro['CIUDAD'] = std_nomsun
Parametro['AREA_CONTINENTAL'] = param3
Parametro['AREA_VERDE'] = param
Parametro['AREA_URB'] = param2
Parametro['INTEGRIDAD'] = intparam
Parametro = Parametro.sort_index()
list(Parametro)
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
    'DATOS' : ContenidoDatos,
    'INTEGRIDAD' : 'Revision de integridad de la información POR CLAVE DEL SUN. Promedio de VAR_INTEGRIDAD de los municipios que componen una ciudad. Si no se tiene información para el municipio, VAR_INTEGRIDAD es igual a cero',
    'EXISTENCIA' : 'Revision de integridad de la información POR MUNICIPIO.'
}

d_mineria = {
    '  ': np.nan,
    'DESCRIPCION DEL PROCESO DE MINERIA:' : np.nan,
    'Nombre del Dataset' : NombreParametro,
    'Descripcion del dataset' : 'Arboles Plantados, por municipio, de 1994 a 2014',
    'Fuente'    : 'SIMBAD - Sistema Estatal y municipal de Base de Datos (INEGI)',
    'URL_Fuente': 'http://sc.inegi.org.mx/cobdem/',
    'Dataset base' : '"BS01.xlsx", disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/BS01' ,
    'Repositorio de mineria' : RepoMina,
    'Notas' : Notas,
    'VAR_INTEGRIDAD' : DescVarIntegridad,
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
}

# Crear archivo de Excel
ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro)