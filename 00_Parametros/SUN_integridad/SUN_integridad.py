# -*- coding: utf-8 -*-
"""
Started on Fri Aug 11 11:10:05 2017

@author: carlos.arana
"""

'''
Verifica cuantas ciudades del subsistema Principal del SUN se encuentran en un dataset.
De las ciudades que se encuentran en el SUN, verifica que existan todos los municipios que componen la ciudad.
para cada ciudad en el dataset, verifica que existan registros para todos los municipios que componen la ciudad. 

El algoritmo espera las siguientes entradas:
dataframe_sun:  dataframe con claves sun y claves mun, creado con 
                la funcion "asignar_sun" disponible en https://github.com/Caranarq/SUN

'''

import pandas as pd
module_path = r'D:\PCCS\01_Dmine\00_Parametros\SUN'
import sys
if module_path not in sys.path:
    sys.path.append(module_path)

from asignar_sun import asignar_sun

def SUN_integridad(dataframe_sun):
    # Importar dataset SUN
    sun = pd.read_csv(r'D:\PCCS\01_Dmine\00_Parametros\sun.csv',
                      dtype={'CVE_SUN':str, 'CVE_ENT': str, 'CVE_MUN': str, 'CVE_LOC': str},
                      encoding='UTF-8',
                      )

    # Asegurar longitudesd e caracteres para claves SUN
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
    cantmun = sun.groupby(by = 'CVE_SUN').agg('count')['CVE_MUN']           # Total en el SUN
    cantdf = sun.groupby(by = 'CVE_SUN').agg('sum')['CHECK']                # Total en el dataframe
    varint = sun.groupby(by = 'CVE_SUN').agg('mean')['VAR_INTEGRIDAD']      # Promedio de la Variable de Integridad

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
    existencia = ['CVE_SUN', 'CVE_ENT', 'CVE_MUN', 'NOM_MUN', 'SUBSIS_PPAL', 'CHECK', 'VAR_INTEGRIDAD']
    existencia = sun[existencia]
    existencia = existencia.set_index(['CVE_SUN'])
    rev_integridad = {'INTEGRIDAD' : integridad,
                      'EXISTENCIA' : existencia}

    return rev_integridad


'''
dataframe_sun = denuncias_std

    pd.merge(integridad, sun['CVE_SUN'])

    sun['CVE_MUN'].isin(munendf)

    sun[sun['CVE_SUN'] == '061']['CVE_SUN'] = '062'

sum(sun['check'])
len(sun['CVE_MUN'])

dataframe_sun = test2

munendf = test2.groupby(by = 'CVE_SUN').agg('count')['CVE_MUN'] # Total en el dataframe

sun.head()
test2 = asignar_sun(test)
list(sun)
test2.head()

test2[test2['']]
len(test)
len(test2['CVE_SUN'] )

test2['CVE_SUN'].isnull()


df = pd.DataFrame({'Col1': ['Bob', 'Joe', 'Bill', 'Mary', 'Joe'],
                   'Col2': ['Joe', 'Steve', 'Bob', 'Bob', 'Steve'],
                   'Col3': np.random.random(5)})

df2 = pd.DataFrame({'Col1': ['Bob', 'Joe', 'Bill', 'Joe'],
                   'Col2': ['Joe', 'Steve', 'Bob', 'Steve'],
                   'Col3': np.random.random(4)})

muns_in_sun = list(sun['CVE_MUN'])
muns_in_ds = dataframe_sun['CVE_MUN'].unique()

x = 0
unique = []
Repeat = []
for i in muns_in_sun:
    if i in unique:
        Repeat.append(i)
    else:
        unique.append(i)
    print('{} - {}'.format(x, i))
    x += 1


test.head()

repeats = sun[sun['CVE_MUN'].isin(Repeat)]

len(muns_in_sun)
len(set(muns_in_sun))

list(muns_in_ds)

len(sun['CVE_MUN'].unique())
pd.merge(df, df2 on = )

sum(sun['CVE_MUN'].isin(x))

len(sun['CVE_MUN'].unique())

df.head()

sun.head()

list(cantmun)
np.unique(dataframe_sun[['CVE_SUN', 'CVE_MUN']])

cantmun
    return df
sun.head(1)

type(sun['CVE_SUN'])

cantmun
##########################
np.unique()

cantmun.head()
list(munendf)

test = pd.read_csv(r'D:\PCCS\01_Analysis\01_DataAnalysis\00_Parametros\flota_vehicular_municipal.csv',
                      dtype={'CVE_SUN':str, 'CVE_ENT': str, 'CVE_MUN': str, 'CVE_LOC': str},
                      encoding='mbcs',
                      )
test = test.drop('NOM_SUN', axis = 1)
test = test.drop('CVE_SUN', axis = 1)
test = test.drop('Unnamed: 0', axis = 1)


test.head()
dataframe_sun = test

list(test)

cols = ['CVE_MUN', 'NOM_MUN']

test[cols].head()

x = test['CVE_MUN'].unique()
np.shape(x)

repes = pd.DataFrame(Repeat, columns = ['CVE_MUN'])
repes.to_csv('SUN_Repeats.csv')

import os; os.getcwd()
'''


