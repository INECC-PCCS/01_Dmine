# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 11:44:16 2017

@author: carlos.arana
"""

'''
Descripcion: Mineria de datos de vehiculos registrados.

'''

# Librerias Utilizadas
import os
import pandas
import datetime
import numpy as np
import urllib
import zipfile

# Ubicacion y descripcion de la fuente
fuente = r'http://www.beta.inegi.org.mx/proyectos/registros/economicas/accidentes/'
describe_fuente = 'Informacion disponible en http://sc.inegi.org.mx/cobdem/ ' \
                  '\n > Ruta: ' \
                  '\n > Proyecto e indice de contenidos ' \
                  '\n > Aprovechamiento de registros administrativos > Estadísticas económicas' \
                  '\n > Estadísticas de transporte ' \
                  '\n > Accidentes de tránsito terrestre en zonas urbanas y suburbanas (1997 - 2015)' \
                  '\n > Consultar información de: > Total de accidentes de tránsito' \
                  '\n > Pestaña 1. Variables [Seleccionar "Zona donde ocurrió el accidente"]' \
                  '\n > Pestaña 2. Años a consultar [Seleccionar Todos]' \
                  '\n > Pestaña 3. Área geográfica [Ver Municipios] [Seleccionar Todos]' \
                  '\n > [Actualizar Consulta]' \
                  '\n > [Expandir Columnas]' \
                  '\n > [Expandir renglones]' \
                  '\n > [Exportar datos a Excel]'

fecha_mineria = datetime.datetime.now()


# Descargar bases de datos de accidentes
dir_local_base = r'D:\PCCS\00_RawData\01_CSV\Accidentes'
dir_local_sub = r'\zip'
URLBASE = 'http://www.beta.inegi.org.mx/contenidos/proyectos/registros/economicas/accidentes/microdatos'

URLS = [
    r'/1997/atus_97_dbf.zip', r'/1998/atus_98_dbf.zip', r'/1999/atus_99_dbf.zip', r'/2000/atus_00_dbf.zip',
    r'/2001/atus_01_dbf.zip', r'/2002/atus_02_dbf.zip', r'/2003/atus_03_dbf.zip', r'/2004/atus_04_dbf.zip',
    r'/2005/atus_05_dbf.zip', r'/2006/atus_06_dbf.zip', r'/2007/ATUS_07_dbf.zip', r'/2008/ATUS_08_dbf.zip',
    r'/2009/ATUS_09_dbf.zip', r'/2010/ATUS_10_dbf.zip', r'/2011/ATUS_11_dbf.zip', r'/2012/atus_12_dbf.zip',
    r'/2013/atus_13_dbf.zip', r'/2014/atus_14_dbf.zip', r'/2015/atus_15_dbf.zip'
]

archivos = {}
for i in URLS:
    localfile = i.split('/')[2]
    anio = i.split('/')[1]
    destino = dir_local_base+dir_local_sub+'\\'+localfile
    URL = URLBASE+i
    print('Descargando {} ... ... ... ... ... '.format(localfile))
    urllib.request.urlretrieve(URL, destino)
    archivos[anio]= destino
    print('se descargó {}'.format(localfile))

# Descomprimir archivos
unzipdirs = {}
for k, v in archivos.items():
    targetdir = dir_local_base+'\\'+k
    if not os.path.isdir(targetdir):
        os.makedirs(targetdir)
    zip_ref = zipfile.ZipFile(v, 'r')
    zip_ref.extractall(targetdir)
    zip_ref.close()
    unzipdirs[k] = targetdir
    print('Se descomprimio {}'.format(v))

# Convertir archivos .dbf a dataframe
x = 0
dbfs = {}
for k, v in unzipdirs.items():
    for file in os.listdir(v):
        if file.endswith('.dbf') or file.endswith('.DBF'):
            path_to_dbf = r'{}\{}'.format(v,file)
            dbf_to_py = Dbf5(path_to_dbf, codec='mbcs')
            ds_from_dbf = dbf_to_py.to_dataframe()
            dbfs[k] = ds_from_dbf
            print('Done: {}.{} --- {} --- {}'.format(x, k, v, file))
    x +=1


for k, v in dbfs.items():
    print('***\n{}\n{}\n{}'.format(k, list(v), len(v)))



# Descripcion del dataset
descripcion = {
    'Nombre del Dataset'   : 'Vehiculos de motor registrados en circulación',
    'Descripcion del dataset' : 'Numero de Vehiculos de motor registrados en circulación. Incluye automoviles,'
                                'Camiones para pasajeros, Camiones y camionetas para carga y motocicletas',
    'Fuente'    : 'SIMBAD - Sistema Estatal y municipal de Base de Datos (INEGI)',
    'URL_Fuente': 'http://sc.inegi.org.mx/cobdem/',
    'Obtencion de dataset' : describe_fuente,
    'Desagregacion' : 'Municipal',
    'Disponibilidad temporal' : '1980 a 2016',
    'Repositorio de mineria' : 'https://github.com/INECC-PCCS/MV01',
    'Notas' : 'S/N'
}

# Armar pestaña de metadatos
metadatos = pandas.DataFrame.from_dict(descripcion, orient='index')
metadatos = metadatos.rename(columns = {0:'Descripcion'})

# Exportar a excel
writer = pandas.ExcelWriter(r'D:\PCCS\01_Dmine\00_Parametros\MV01\MV01.xlsx')
dataset_b.to_excel(writer, sheet_name = 'DATOS')
metadatos.to_excel(writer, sheet_name = 'Metadatos')
writer.close()


'''
Codigo de pruebas 
'''

# Librerias utilizadas
import pandas as pd
from simpledbf import Dbf5

# Descargar y descomprimir la base de datos del Sistema Urbano Nacional en formato SHP
dir_local_base = r'D:\PCCS\00_RawData\01_CSV\Accidentes'
dir_local_sub = r'\zip'
localfile = 'atus_15_dbf.zip'
destino = dir_local+dir_local_sub+'\\'+localfile
URL = r'http://www.beta.inegi.org.mx/contenidos/proyectos/registros/economicas/accidentes/microdatos/2015/atus_15_dbf.zip'



os.getcwd()

zip_ref = zipfile.ZipFile(elzip, 'r')
zip_ref.extractall(dir_local)

SUN_MAIN = r'D:\PCCS\01_Dmine\00_Parametros\sun_main.csv'

# Convertir datos descargados como dbf a Pandas Dataframe.
sundbf = Dbf5(Archivo, codec='mbcs')
sun_df = sundbf.to_dataframe()

# Cargar subsistema principal
SUN_MAIN = pd.read_csv(r'D:\PCCS\01_Dmine\00_Parametros\sun_main.csv',
                      dtype={'CVE_SUN': str,
                             'CVE_ENT': str,
                             'CVE_MUN': str,
                             'CVE_LOC': str,
                             'CVE_SUNMUN': str},
                      encoding='UTF-8',
                      )

# Clasificar por subsistema principal
ciudades = sun_df['CVE_SUN']
ciudades = ciudades.apply(lambda x: str(x).zfill(3))
listamain = SUN_MAIN['CVE_SUN'].tolist()
sun_df['SS_PPAL'] = ciudades.apply((lambda x: x in listamain))
