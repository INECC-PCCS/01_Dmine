# -*- coding: utf-8 -*-
"""
Started on Fri Aug 11 11:10:05 2017

@author: carlos.arana

Descripcion:
Verifica cuantas ciudades del subsistema Principal del SUN se encuentran en un dataset.
De las ciudades que se encuentran en el SUN, verifica que existan todos los municipios que componen la ciudad.
para cada ciudad en el dataset, verifica que existan registros para todos los municipios que componen la ciudad.

El algoritmo espera las siguientes entradas:
dataframe_sun:  dataframe con claves sun y claves mun, creado con
                la funcion "asignar_sun" disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/SUN
"""

import pandas as pd

def SUN_integridad(dataframe_sun):
    # Importar dataset SUN
    sun = pd.read_csv(r'D:\PCCS\01_Dmine\00_Generales\sun_main.csv',
                      dtype={'CVE_SUN':str, 'CVE_ENT': str, 'CVE_MUN': str, 'CVE_LOC': str},
                      encoding='UTF-8',      # Si mbcs falla entonces utiliza UTF-8
                      )

    # Asegurar longitudes de caracteres para claves SUN
    sun['CVE_SUN'] = sun['CVE_SUN'].apply('{:0>3}'.format)
    sun['CVE_ENT'] = sun['CVE_ENT'].apply('{:0>2}'.format)
    sun['CVE_MUN'] = sun['CVE_MUN'].apply('{:0>5}'.format)

    # Obtener municipios que se encuentran en el Dataframe (Sin duplicados)
    dataframe_sun = dataframe_sun.set_index(['CVE_SUN'])
    unicos_df = dataframe_sun['CVE_MUN'].unique()

    # Calculo de integridad
    sun['CHECK'] = sun['CVE_MUN'].isin(unicos_df)
    sun = pd.merge(sun, dataframe_sun[['VAR_INTEGRIDAD', 'CVE_MUN']], on='CVE_MUN')
    sun['VAR_INTEGRIDAD'] = sun['VAR_INTEGRIDAD'].fillna(0)
    cantmun = sun.groupby(by='CVE_SUN').agg('count')['CVE_MUN']           # Total en el SUN
    cantdf = sun.groupby(by='CVE_SUN').agg('sum')['VAR_INTEGRIDAD']       # Total en el dataframe
    varint = sun.groupby(by='CVE_SUN').agg('mean')['VAR_INTEGRIDAD']      # Promedio de la Variable de Integridad

    # Armar dataframe de integridad
    sun_index = sun.set_index('CVE_SUN')
    sun_nom = sun_index['NOM_SUN'].drop_duplicates()
    sun_subsis = sun_index['SUBSIS_PPAL']
    sun_subsis = sun_subsis[~sun_subsis.index.duplicated(keep='first')]
    integridad = pd.DataFrame()
    integridad['NOM_SUN'] = sun_nom
    integridad['SUBSISTEMA'] = sun_subsis
    integridad['CANTMUN'] = cantmun.astype(float)
    integridad['CANTDF'] = cantdf
    integridad['INTEGRIDAD'] = varint

    # Datasets de integridad
    existencia = ['CVE_SUN', 'CVE_ENT', 'CVE_MUN', 'NOM_MUN', 'SUBSIS_PPAL', 'VAR_INTEGRIDAD']
    existencia = sun[existencia]
    existencia = existencia.set_index(['CVE_SUN'])
    rev_integridad = {'INTEGRIDAD': integridad,
                      'EXISTENCIA': existencia}

    return rev_integridad

'''
SUN_integridad(DatosLimpios)
'''

