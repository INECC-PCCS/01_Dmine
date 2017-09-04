# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 17:47:11 2017

@author: carlos.arana
"""

'''
Descripci.on: Mineria de datos de numero de denuncias ambientales recibidas.

'''

# Librerias Utilizadas
import os
import urllib
import pandas
import datetime
import numpy as np

# Ubicacion y descripcion de la fuente
fuente = r'http://sc.inegi.org.mx/cobdem/descargaformatosservlet?tipo=1&archivo=SIMBAD_42677_20170824043758489.xlsx'
describe_fuente = 'Informacion encontrada en http://sc.inegi.org.mx/cobdem/ ' \
                  '\n > Ruta: ' \
                  '\n > Proyecto e indice de contenidos ' \
                  '\n > Integracion de destadisticas - Medio Ambiente ' \
                  '\n > Acciones seleccionadas en materia ambiental [Seleccionar todas]' \
                  '\n > Pestaña 2. Años a consultar [Seleccionar Todos]' \
                  '\n > Pestaña 3. Área geográfica [Ver Municipios]' \
                  '\n > [Actualizar Consulta]' \
                  '\n > [Expandir Columnas]' \
                  '\n > [Expandir renglones]' \
                  '\n > [Exportar datos a Excel]'

fecha_mineria = datetime.datetime.now()

print(fecha_mineria.strftime('%c'))

# Rutas de archivo
archivo_raw = r'D:\PCCS\00_RawData\01_CSV\BS01.xlsx'

if not os.path.isfile(archivo_raw):
    urllib.request.urlretrieve(fuente, archivo_raw)

dataset = pandas.read_excel(archivo_raw, skiprows = 2, header=1)
dataset.head()

## Eliminacion de renglones sin informacion util
# Eliminar renglones con resument estatal
res_est = dataset['Clave'].str.len() != 2
# Eliminar renglones vacios y guardar nuevo dataset
dataset_b = dataset[res_est].dropna()

# Estandarizar nombre de columna de clave municipal
dataset_b.rename(columns = {'Clave':'CVE_MUN'}, inplace = True)

# Reemplazar valores no disponibles y confidenciales por NaN
dataset_b.replace('ND', np.nan, inplace = True) # "ND" = No Disponible
dataset_b.replace('C', np.nan, inplace = True)  # "C" = Cifra no publicable, por el principio de confidencialidad de la Ley de Información Estadística y Geográfica.
dataset_b.replace('NS', np.nan, inplace = True) # "NS" = No Significativo

# Descripcion del dataset
descripcion = {
    'Nombre del Dataset'   : 'Acciones seleccionadas en materia ambiental',
    'Descripcion del dataset' : ', '.join(list(dataset_b)[2:7]),
    'Fuente'    : 'SIMBAD - Sistema Estatal y municipal de Base de Datos (INEGI)',
    'URL_Fuente': 'http://sc.inegi.org.mx/cobdem/',
    'Obtencion de dataset' : describe_fuente,
    'Desagregacion' : 'Municipal',
    'Disponibilidad temporal' : '1994 a 2013',
    'Repositorio de mineria' : 'https://github.com/INECC-PCCS/BS01',
    'Notas' : 'Para las columnas con nombres repetidos, la primer aparicion corresponde a 1994'
}

# Armar pestaña de metadatos
metadatos = pandas.DataFrame.from_dict(descripcion, orient='index')
metadatos = metadatos.rename(columns = {0:'Descripcion'})

# Exportar a excel
writer = pandas.ExcelWriter(r'D:\PCCS\01_Dmine\00_Parametros\BS01\BS01.xlsx')
dataset_b.to_excel(writer, sheet_name = 'DATOS')
metadatos.to_excel(writer, sheet_name = 'Metadatos')
writer.close()


df = pandas.DataFrame(np.random.randn(10, 4), columns=[1994, 1995, 1996, 1997])
df['states'] = ['State1', 'State2', 'State3', 'State4', 'State5',
                'State6', 'State7', 'State8', 'State9', 'State10']
df.set_index('states', inplace=True)

pandas.melt(df, id_vars='states',var_name='Year')