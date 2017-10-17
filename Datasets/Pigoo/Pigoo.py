# -*- coding: utf-8 -*-
"""
Started on Tue Oct 17 10:23:02 2017

@author: carlos.arana

Descripcion;
Descarga el Dataset de indicadores de Gestion de los organismos Operadores de agua de la Republica Mexicana
"""

# Librerias Utilizadas
import os
import pandas as pd
import datetime
import urllib
import zipfile
from simpledbf import Dbf5

# Ubicacion y descripcion de la fuente
fuente = r'http://www.beta.inegi.org.mx/proyectos/registros/economicas/accidentes/'
describe_fuente = 'Descarga automatizada desde la URL_fuente'
fecha_mineria = datetime.datetime.now()

# Descargar bases de datos de accidentes
dir_local_base = r'D:\PCCS\00_RawData\01_CSV\Accidentes'
dir_local_sub = r'\zip'
URLBASE = 'http://www.beta.inegi.org.mx/contenidos/proyectos/registros/economicas/accidentes/microdatos'
dataset_destino = 'MV02'

URLS = [
    r'/1997/atus_97_dbf.zip', r'/1998/atus_98_dbf.zip', r'/1999/atus_99_dbf.zip', r'/2000/atus_00_dbf.zip',
    r'/2001/atus_01_dbf.zip', r'/2002/atus_02_dbf.zip', r'/2003/atus_03_dbf.zip', r'/2004/atus_04_dbf.zip',
    r'/2005/atus_05_dbf.zip', r'/2006/atus_06_dbf.zip', r'/2007/ATUS_07_dbf.zip', r'/2008/ATUS_08_dbf.zip',
    r'/2009/ATUS_09_dbf.zip', r'/2010/ATUS_10_dbf.zip', r'/2011/ATUS_11_dbf.zip', r'/2012/atus_12_dbf.zip',
    r'/2013/atus_13_dbf.zip', r'/2014/atus_14_dbf.zip', r'/2015/atus_15_dbf.zip'
]

archivos = {}

# Descarga de archivos
for i in URLS:
    localfile = i.split('/')[2]
    anio = i.split('/')[1]
    destino = dir_local_base+dir_local_sub+'\\'+localfile
    URL = URLBASE+i
    print('Descargando {} ... ... ... ... ... '.format(localfile))
    # urllib.request.urlretrieve(URL, destino) #
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
