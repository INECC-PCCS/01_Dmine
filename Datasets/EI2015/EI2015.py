# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:03:44 2017

@author: carlos.arana
"""

import os
import pandas as pd
import datetime
import urllib
import zipfile
from simpledbf import Dbf5


# Descargar bases de datos de encuesta intercensal -------------------------------------------------------------------
# Ubicacion y descripcion de la fuente
fuente = r'http://www.beta.inegi.org.mx/proyectos/enchogares/especiales/intercensal/'
describe_fuente = 'Descarga y transformación de microdatos'
fecha_mineria = datetime.datetime.now()

# Descargar bases de datos de accidentes
dir_local_base = r'D:\PCCS\00_RawData\01_CSV\Intercensal2015'
dir_local_sub = r'\zip'
URLBASE = 'http://www.beta.inegi.org.mx/contenidos/proyectos/enchogares/especiales/intercensal/2015'
dataset_destino = 'EI2015'

URLS = [
    r'/doc/eic2015_fd.xls', r'/microdatos/eic2015_01_csv.zip', r'/microdatos/eic2015_02_csv.zip',
    r'/microdatos/eic2015_03_csv.zip', r'/microdatos/eic2015_04_csv.zip', r'/microdatos/eic2015_05_csv.zip',
    r'/microdatos/eic2015_06_csv.zip', r'/microdatos/eic2015_07_csv.zip', r'/microdatos/eic2015_08_csv.zip',
    r'/microdatos/eic2015_09_csv.zip', r'/microdatos/eic2015_10_csv.zip', r'/microdatos/eic2015_11_csv.zip',
    r'/microdatos/eic2015_12_csv.zip', r'/microdatos/eic2015_13_csv.zip', r'/microdatos/eic2015_14_csv.zip',
    r'/microdatos/eic2015_15_csv.zip', r'/microdatos/eic2015_16_csv.zip', r'/microdatos/eic2015_17_csv.zip',
    r'/microdatos/eic2015_18_csv.zip', r'/microdatos/eic2015_19_csv.zip', r'/microdatos/eic2015_20_csv.zip',
    r'/microdatos/eic2015_21_csv.zip', r'/microdatos/eic2015_22_csv.zip', r'/microdatos/eic2015_23_csv.zip',
    r'/microdatos/eic2015_24_csv.zip', r'/microdatos/eic2015_25_csv.zip', r'/microdatos/eic2015_26_csv.zip',
    r'/microdatos/eic2015_27_csv.zip', r'/microdatos/eic2015_28_csv.zip', r'/microdatos/eic2015_29_csv.zip',
    r'/microdatos/eic2015_30_csv.zip', r'/microdatos/eic2015_31_csv.zip', r'/microdatos/eic2015_32_csv.zip'
]

archivos = {}

# Descarga de archivos
for i in URLS:
    localfile = i.split('/')[2]
    anio = i.split('/')[1]
    destino = dir_local_base+dir_local_sub+'\\'+localfile
    URL = URLBASE+i
    if os.path.isfile(destino):
        print('Ya existe el archivo: {}'.format(localfile))
        archivos[anio] = destino
    else:
        print('Descargando {} ... ... ... ... ... '.format(localfile))
        urllib.request.urlretrieve(URL, destino) #
        archivos[anio]= destino
        print('se descargó {}'.format(localfile))

# Descomprimir archivos
unzipdirs = {}
for k, v in archivos.items():
    targetdir = dir_local_base+'\\'+k
    if not os.path.isdir(targetdir):
        os.makedirs(targetdir)
    zip_ref = zipfile.ZipFile(v, 'r') #
    zip_ref.extractall(targetdir) #
    zip_ref.close() #
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

DataSet = pd.concat(dbfs.values(), keys=dbfs.keys())
del(dbfs) #Liberamos la memoria ocupada por dbfs

# Asignar clave geoestadistica municipal estandar de 5 digitos
Estado = DataSet['EDO'].apply(lambda x: str(x).zfill(2)).map(str)
Municipio = DataSet['MPIO'].apply(lambda x: str(x).zfill(3))
DataSet['CVE_MUN'] = Estado + Municipio

# Consolidar numero de accidentes por municipio y por año
DataSet.set_index('CVE_MUN', append=True, inplace=True)
DataSet.reset_index(level=1, inplace=True)
Accidentes_Urbana = DataSet['URBANA'].loc[DataSet['URBANA'] != 0].groupby(level=[0,1]).count()
Accidentes_Suburbana = DataSet['SUBURBANA'].loc[DataSet['SUBURBANA'] != 0].groupby(level=[0,1]).count()
del(DataSet) #Liberamos la memoria ocupada por DataSet

# Hacer columnas para cada año y consolidar dataset de accidentes
Accidentes_Urbana = Accidentes_Urbana.unstack(level=0)
Accidentes_Suburbana = Accidentes_Suburbana.unstack(level=0)

# Descripcion del dataset
descripcion = {
    'Nombre del Dataset'   : 'Accidentes de tránsito en zonas urbanas y suburbanas',
    'Descripcion del dataset' : 'Accidentes de tránsito en zonas urbanas y suburbanas. Información anual y municipal',
    'Fuente'    : 'INEGI (Microdatos)',
    'URL_Fuente': fuente,
    'Obtencion de dataset' : describe_fuente,
    'Desagregacion' : 'Municipal',
    'Disponibilidad temporal' : '1997 a 2015',
    'Repositorio de mineria' : 'https://github.com/INECC-PCCS/{}'.format(dataset_destino),
    'Notas' : 'S/N'
}

# Armar pestaña de metadatos
metadatos = pd.DataFrame.from_dict(descripcion, orient='index')
metadatos = metadatos.rename(columns = {0:'Descripcion'})

# Exportar a excel
writer = pd.ExcelWriter(r'D:\PCCS\01_Dmine\00_Parametros\{}\{}.xlsx'.format(dataset_destino, dataset_destino))
Accidentes_Urbana.to_excel(writer, sheet_name = 'ACCIDENTES_URBANA')
Accidentes_Suburbana.to_excel(writer, sheet_name = 'ACCIDENTES_SUBURBANA')
metadatos.to_excel(writer, sheet_name = 'Metadatos')
writer.close()
