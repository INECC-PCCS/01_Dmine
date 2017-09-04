# -*- coding: utf-8 -*-
"""
DESCRIPCION: Script para asignar claves y nombres de ciudades de acuerdo con el Sistema Urbano Nacional
Fuente de la información: Catálogo del Sistema Urbano Nacional
Started on Fri Aug  4 12:54:13 2017

@author: carlos.arana
"""
'''
Espera los siguientes parametros:
dataframe: pandas dataframe al que se desean asignar claves geoestadisticas
CVE_MUN: str, Nombre de la columna en dataframe que contiene la clave geoestadística a nivel municipal (5 DIGITOS)
vars = [list] columnas del catalogo geoestadístico que se unirán.

Crea las siguientes columnas:
CVE_SUN: Clave de 3 digitos del SUN
NOM_MUN: Nombre de la ciudad a la que pertenece el municipio, de acuerdo con el SUN
TIPO_SUN: Tipo de ciudad, de acuerdo con la clasificacion definida en el SUN

NOTA ACLARATORIA:
Las ciudades 'San Jose del Cabo' y 'Cabo San Lucas' forman parte del subsistema principal y se encuentran dentro
de un mismo municipio. Para poder analizarlas de manera separada, sería necesario contar con un nivel de desagregación 
por localidad. Para la mayoría de los datasets, el nivel máximo de desagregación es municipal, por lo que para este 
análisis, se han considerado como una misma ciudad:

CVE_SUN     CVE_MUN     NOM_SUN             CVE_SUN(Norm)   NOM_SUN(Normalizado)
061         03008       San José del Cabo   062             Cabo San Lucas
062         03008       Cabo San Lucas      062             Cabo San Lucas

'''


from pandas import read_csv as rcsv
import pandas as pd

def asignar_sun(dataframe, CVE_MUN = 'CVE_MUN', vars = ['CVE_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN']):
    sun = rcsv(r'D:\PCCS\01_Dmine\00_Parametros\sun_main.csv',
                      dtype={'CVE_SUN': str,
                             'CVE_ENT': str,
                             'CVE_MUN': str,
                             'CVE_LOC': str,
                             'CVE_SUNMUN': str},
                      encoding='UTF-8',
                      )
    sun['CVE_SUN'] = sun['CVE_SUN'].apply('{:0>3}'.format)
    sun['CVE_ENT'] = sun['CVE_ENT'].apply('{:0>2}'.format)
    sun['CVE_MUN'] = sun['CVE_MUN'].apply('{:0>5}'.format)

    print('Catalogo de variables. Default vars = {}'.format(vars))
    print(list(sun))
    if 'CVE_MUN' not in vars: vars.append('CVE_MUN')

    dataframe.rename(columns={CVE_MUN : 'CVE_MUN'}, inplace = True) # Estandariza el nombre de la columna de clave geoestadistica
    sun.drop_duplicates('CVE_SUNMUN', keep='first', inplace = True) # Quita los municipios que en el dataset aparecen duplicados por estar subdivididos en localidades
    sun = sun[vars]
    dataframe = pd.merge(dataframe, sun, on='CVE_MUN')

    return dataframe

'''
dataframe = denuncias_ma
writer = pd.ExcelWriter(r'test_asignar_sun.xlsx')
dataframe.to_excel(writer, sheet_name = 'dataframe')
sun.to_excel(writer, sheet_name = 'sun')
writer.save()

list(sun)
'''