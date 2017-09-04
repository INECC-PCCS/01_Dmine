# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:51:53 2017

@author: Carlos Arana Matus
"""

# librerías usadas
from __future__ import division
import pandas as pd
from pandas import DataFrame
from pyGDsandbox.dataIO import df2dbf
from dbfread import DBF
from os import listdir
from shutil import copyfile


# Importacion de Datos para su analisis
data = pd.read_csv(r".\01_Analysis\01_DataAnalysis\04_Agua\scripts\test.csv")
data.head()
data.shape

# Agrupación de todos los municipios según su clave SUN.
zm = data.groupby("cve_sun").count()
print("Zonas metropolitanas en total: ",zm.shape[0])


# Agrupación según clave SUN con todas las variables con valor diferente a "NaN".
zm_sinNaN = data.dropna().groupby("cve_sun").count()
print("Zonas metropolitanas sin valores 'NaN': ",zm_sinNaN.shape[0])

# Lista de claves SUN de las ciudades sin 'NaNs' para filtrar.
cves_sinNaN = zm_sinNaN.index.tolist()

# Filtro de ciudades con la lista anterior.
zm = zm.loc[zm.index.isin(cves_sinNaN)]

# ¿Qué ciudades tienen la información completa para todos sus municipios?()
(zm_sinNaN / zm)[:10]

# Municipios por ciudad con información completa entre el total de los municipios que existen en esa ciudad.
zm = zm_sinNaN / zm
# Filtar aquellas ciudades cuyos municipios cuentan con toda la información disponible.
zm = zm[zm['_id'] == 1]
zm

# Isolar datos para el estudio
muns = data.loc[data['cve_sun'].isin(zm.index.tolist())]
muns.head()

# Lista de variables
for i,a in enumerate(muns.columns):
    print(i,a)

muns.columns

# Variables descriptivas de cada caso a analizar
info_mun = ['entidad','municipio','cve_ent','cve_mun','cve_sun']

# Analisis de disponibilidad y acceso
disponibilidadYacceso = ['total_disponibilidadYacceso','entubada_total','entubada_dentro_de_vivienda',
                         'entubada_fuera_de_vivienda_dentro_de_terreno','acarreo_total','acarreo_llave_comunitaria',
                         'acarreo_otra_vivienda','acarreo_pipa','acarreo_pozo','acarreo_rio_lago_arroyo',
                         'acarreo_lluvia','acarreo_no_especificado']
disponibilidadYacceso += info_mun
disponibilidadYacceso = muns[disponibilidadYacceso]
disponibilidadYacceso.head()

# Lista de la información
for i,a in enumerate(disponibilidadYacceso.columns):
    print(i,a)

# Exportar a CSV
disponibilidadYacceso.to_csv('dispyacc.csv', sep=",")
muns.to_csv('mun.csv', sep=",")
.to_csv('', sep=",")

# INDICADORES.
# Los siguientes indicadores fueron formulados a partir de los indicadores descritos en los Objetivos de desarrollo Sustentable de la ONU.

# 6.1.1 - Proporción de población utilizando servicios saludables de Agua Potable
# Fuentes de información:
# Población: Sistema Urbano Nacional 2010
# Agua: Mineria de datos de Daniel Urencio
#

# Crear una copia de los archivos de Información geográfica para realizar el análisis de agua
for i in listdir(r'./00_RawData/00_Geo/SUN/SHP/2010SUN/'):
    if 'ZM_2010' in i:
        copyfile(r'./00_RawData/00_Geo/SUN/SHP/2010SUN/{}'.format(i),r'./01_Dmine/02_GIS/01_Agua/{}'.format(i))

# Cargar información geográfica en un Pandas Dataframe.
GeoLoad = DBF(r'./00_RawData/00_Geo/SUN/SHP/2010SUN/ZM_2010.dbf', load=True)
GeoData = DataFrame.from_dict(GeoLoad.records)

GeoLoad.fields

# Combinar datos de agua con información geográfica
aguadbf = GeoData.merge(disponibilidadYacceso, 'left', left_on='CVE_MUN1', right_on='cve_mun')

# Montar el análisis de Agua
Columnas = ['CVE_MUN1', 'CVE_SUN', 'total_disponibilidadYacceso']
df2dbf(aguadbf,r'./01_Dmine/02_GIS/01_Agua/ZM_2010.dbf', Columnas)


print('La base de datos tiene {} filas y {} columnas'.format(data.shape[0], data.shape[1]))

muns.columns


pd.DataFrame.set_index(['A', 'B'])

    (['a', 'b', 'c', 'd', 'e', 'f'])
