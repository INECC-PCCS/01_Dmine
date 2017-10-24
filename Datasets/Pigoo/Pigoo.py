# -*- coding: utf-8 -*-
"""
Started on Tue Oct 17 10:23:02 2017

@author: carlos.arana

Descripcion;
Analisis exploratorio al Dataset de indicadores de Gestion de los organismos Operadores de agua de la Republica Mexicana
"""


# Librerias Utilizadas
import os
import pandas as pd
import datetime
import zipfile
from simpledbf import Dbf5

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)
from SUN.asignar_sun import asignar_sun
from SUN_integridad.SUN_integridad import SUN_integridad

# Ubicacion y descripcion de la fuente
fuente = r'D:\PCCS\01_Dmine\Datasets\Pigoo\CiudadesPIGOO_ClaveInegi.xlsx'
describe_fuente = 'Archivo con claves geoestadísticas asignadas por personal de INEGI'
fecha_mineria = datetime.datetime.now()

archivos = {}



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

'''
Preproceso
'''

import pandas as pd

# Cargar archivo
pigoo_inegi = r'D:\PCCS\01_Dmine\Datasets\Pigoo\CiudadesPIGOO_ClaveInegi.xlsx'
pigoo_inegi_df = pd.read_excel(pigoo_inegi, sheetname='OOAPAS-PIGOO', index_col=0,
                      dtype={'Clave-Estado-Inegi': str,
                             'Clave-Municipio-Inegi': str,
                             'Clave-Localidad-Inegi': str})

# Crear CVE_MUN y CVE_SUN
pigoo_inegi_df['CVE_MUN'] = pigoo_inegi_df['Clave-Estado-Inegi'].map(str) + pigoo_inegi_df['Clave-Municipio-Inegi']
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'NOM_ENT']
pigoo_sun = asignar_sun(pigoo_inegi_df, vars=variables_SUN)
pigoo_sun['VAR_INTEGRIDAD'] = 1

# Revisar Integridad
integridad_pigoo = SUN_integridad(pigoo_sun)

# Exportar a excel
writer = pd.ExcelWriter(r'D:\PCCS\01_Dmine\Datasets\Pigoo\pigoo_start.xlsx')     # Proxy de libro
pigoo_sun.to_excel(writer, sheet_name ='datos')
integridad_pigoo['INTEGRIDAD'].to_excel(writer, sheet_name ='integridad')
integridad_pigoo['EXISTENCIA'].to_excel(writer, sheet_name ='existencia')
writer.close()


integridad_pigoo.keys()