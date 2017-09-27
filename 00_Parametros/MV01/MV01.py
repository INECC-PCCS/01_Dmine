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
import urllib
import pandas
import datetime
import numpy as np

# Ubicacion y descripcion de la fuente
fuente = r'El dataset se genera por medio de interaccion humana con el SIMBAD. No tiene API para interfaz con sistemas'
describe_fuente = 'Informacion disponible en http://sc.inegi.org.mx/cobdem/ ' \
                  '\n > Ruta: ' \
                  '\n > Proyecto e indice de contenidos ' \
                  '\n > Aprovechamiento de registros administrativos > Estadísticas económicas' \
                  '\n > Estadísticas de transporte > Vehiculos de motor registrados en circulación' \
                  '\n > Pestaña 1. Variables [Seleccionar Clase de Vehiculo] (Todos)' \
                  '\n > Pestaña 2. Años a consultar [Seleccionar Todos]' \
                  '\n > Pestaña 3. Área geográfica [Ver Municipios] [Seleccionar Todos]' \
                  '\n > [Actualizar Consulta]' \
                  '\n > [Expandir Columnas]' \
                  '\n > [Expandir renglones]' \
                  '\n > [Exportar datos a Excel]'

fecha_mineria = datetime.datetime.now()

print(fecha_mineria.strftime('%c'))

# Rutas de archivo
archivo_raw = r'D:\PCCS\00_RawData\01_CSV\MV01.xlsx'

dataset = pandas.read_excel(archivo_raw, skiprows = 2, header=1, dtype={'Clave':str})
dataset.head()  # El dataset contiene datos de 1980 a 2016

## Eliminacion de renglones sin informacion util
# Eliminar renglones con resument estatal
res_est = dataset['Clave'].str.len() != 2
# Eliminar renglones vacios y guardar nuevo dataset
dataset_b = dataset[res_est].dropna(how='all')

# Estandarizar nombre de columna de clave municipal
dataset_b.rename(columns = {'Clave':'CVE_MUN'}, inplace = True)

# Reemplazar valores no disponibles y confidenciales por NaN
dataset_b.replace('ND', np.nan, inplace = True) # "ND" = No Disponible
dataset_b.replace('C', np.nan, inplace = True)  # "C" = Cifra no publicable, por el principio de confidencialidad de la Ley de Información Estadística y Geográfica.
dataset_b.replace('NS', np.nan, inplace = True) # "NS" = No Significativo

# Eliminar renglones etiquetados como "Otros Municipios", "Estados Unidos de America", "Otros paises"
dataset_b.set_index('CVE_MUN', inplace = True)
droprows = ['32996', '32997', '32998', '33991', '33992', '33993']
dataset_b = dataset_b.drop(droprows)

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

