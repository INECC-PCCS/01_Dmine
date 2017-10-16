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
fuente = r'El dataset se genera por medio de interaccion humana con el SIMBAD. No tiene API para interfaz con sistemas'
describe_fuente = 'Informacion encontrada en http://sc.inegi.org.mx/cobdem/ ' \
                  '\n > Ruta: ' \
                  '\n > Proyecto e indice de contenidos ' \
                  '\n > Integracion de destadisticas - Medio Ambiente ' \
                  '\n > Uso de Suelo y Vegetacion' \
                  '\n > Pestaña 2. Años a consultar [Seleccionar Todos]' \
                  '\n > Pestaña 3. Área geográfica [Ver Municipios]' \
                  '\n > [Actualizar Consulta]' \
                  '\n > [Expandir Columnas]' \
                  '\n > [Expandir renglones]' \
                  '\n > [Exportar datos a Excel]'

fecha_mineria = datetime.datetime.now()

print(fecha_mineria.strftime('%c'))

# Rutas de archivo
archivo_raw = r'D:\PCCS\00_RawData\01_CSV\BS02.xlsx'

dataset = pandas.read_excel(archivo_raw, skiprows = 2, header=1)
dataset.head()

## Eliminacion de renglones sin informacion util
# Eliminar renglones con resument estatal
res_est = dataset['Clave'].str.len() != 2
# Eliminar renglones vacios y guardar nuevo dataset
dataset_b = dataset[res_est].dropna()

dataset_b.head()

# Estandarizar nombre de columna de clave municipal
dataset_b.rename(columns = {'Clave':'CVE_MUN'}, inplace = True)

# Reemplazar valores no disponibles y confidenciales por NaN
dataset_b.replace('ND', np.nan, inplace = True) # "ND" = No Disponible
dataset_b.replace('C', np.nan, inplace = True)  # "C" = Cifra no publicable, por el principio de confidencialidad de la Ley de Información Estadística y Geográfica.
dataset_b.replace('NS', np.nan, inplace = True) # "NS" = No Significativo

# Descripcion del dataset
descripcion = {
    'Nombre del Dataset'   : 'Uso de Suelo y Vegetacion',
    'Descripcion del dataset' : 'Superficie continental, superficie de suelo utilizado para agricultura, '
                                'Superficie de Pastizal, Superficie de bosque, Superficie de selva. '
                                'Superficies en  Kilómetros cuadrados',
    'Fuente'    : 'SIMBAD - Sistema Estatal y municipal de Base de Datos (INEGI)',
    'URL_Fuente': 'http://sc.inegi.org.mx/cobdem/',
    'Obtencion de dataset' : describe_fuente,
    'Desagregacion' : 'Municipal',
    'Disponibilidad temporal' : '2015',
    'Repositorio de mineria' : 'https://github.com/INECC-PCCS/BS01',
    'Notas' : ''
}

# Armar pestaña de metadatos
metadatos = pandas.DataFrame.from_dict(descripcion, orient='index')
metadatos = metadatos.rename(columns = {0:'Descripcion'})

# Exportar a excel
writer = pandas.ExcelWriter(r'D:\PCCS\01_Dmine\00_Parametros\BS02\BS02.xlsx')
dataset_b.to_excel(writer, sheet_name = 'DATOS')
metadatos.to_excel(writer, sheet_name = 'Metadatos')
writer.close()
