# -*- coding: utf-8 -*-
"""
Started on Fri Sep  1 13:32:58 2017

@author: carlos.arana

Descripcion:
Script para crear hojas estándar de parámetro.
Requiere los siguientes input:
DescParametro : [dict] Diccionario con definiciones basicas del parametro, que incluye:
    ClaveParametro
    NombreParametro
    info_completa
    info_sin_info
    info_incomple
    RutaSalida
MetaParametro : [DataSet] Metadatos del Parámetro
Parametro : [DataSet] El parametro mismo resultante de la minería, por clave del SUN
DatosLimpios : [DataSet] Los datos base para generar el parámetro
IntegridadParametro : [dict] diccionario con los dos datasets de integridad generados con el script SUN_Integridad

---
El formato de la hoja imita lo mejor posible los colores estándar de identidad gráfica institucional del Gobierno
de la República, periodo 2012 - 2018. Cuando ha sido necesario, se han utilizado tonalidades más claras o más oscuras
de los colores estándar para lograr distinciones en la información presentada.

[Rojo]          = Pantone 200 C             = Hex #BA0C2F
[Verde]         = Pantone 356 C             = Hex #007A33
[Gris Oscuro]   = Pantone Cool Gray 10 C    = Hex #63666A
[Gris claro ()] = Pantone 877 C (Plata)     = Hex #8A8D8F

El manual de identidad se encuentra disponible en
http://www.funcionpublica.gob.mx/manual/Guia_Basica_de_Identidad_Grafica_Institucional.pdf

"""

import pandas as pd
import numpy as np

NombreParametro = 'P0618'

df = pd.DataFrame(np.random.randn(10, 2), columns=list('AB'))

# Proxy de libro
writer = pd.ExcelWriter(r'D:\PCCS\01_Dmine\00_Parametros\ParametroEstandar\test.xlsx')

# Creacion de hojas
df.to_excel(writer, sheet_name='METADATOS')

# Definir proxys de formatos para hoja de metadatos
metasheet = writer.sheets['METADATOS']
workbook = writer.book

# Creacion de Grafico de integridad
the_chart = workbook.add_chart({'type': 'pie'})
headings = ['INTEGRIDAD', 'NO. CIUDADES']
data = [
    ['INFO. COMPLETA', 'INFO. INCOMPLETA', 'SIN INFO.'],
    [60, 30, 10]
]

# Definicion de colores
verde = '#007A33'  # Verde para ciudades con informacion completa
amarillo = '#A2CEB4'  # 'Amarillo' para datos incompletos
rojo = '#BA0C2F'  # Rojo para ciudades sin datos
gris_oscuro = '#63666A' #Gris para formatos de datos

bold = workbook.add_format({'bold': 1, 'border': 0, 'valign': 'top'})  # Formato para encabezado de datos
titulo = workbook.add_format({
    'bold': 1,
    'border': 0,
    'valign': 'top',
    'pattern': 1,
    'bg_color': gris_oscuro,
    'font_color': 'white',
    'font_name': 'Soberana Sans'
})  # Formato para encabezado de datos
borders = workbook.add_format({'border': 1})  # Formato para tabla sencilla
metaformat = workbook.add_format({'text_wrap': True})

metasheet.write_row('D1', headings, titulo)  # Inscripcion de datos en la hoja
metasheet.write_column('D2', data[0], borders)
metasheet.write_column('E2', data[1], borders)

the_chart.add_series({
    'name': 'Integridad del Parámetro',
    'categories': '=METADATOS!$D$2:$D$4',
    'values': '=METADATOS!$E$2:$E$4',
    'data_labels': {'value': True, 'legend_key': True},
    'points': [
        {'fill': {'color': verde}},
        {'fill': {'color': amarillo}},
        {'fill': {'color': rojo}},
    ]
})

the_chart.set_title({'name': 'Integridad del Dataset\n{}'.format(NombreParametro)})
metasheet.insert_chart('D6', the_chart, {'x_offset': 0, 'y_offset': 0})

# Aplicar Formato
metasheet.set_column('A:A', 22.71)
metasheet.set_column('B:B', 82.57, metaformat)
metasheet.set_column('D:D', 17.57)
metasheet.set_column('E:E', 13.29)

# Crear Titulo y reescribir indice con formato adecuado
metasheet.merge_range('A1:B1', 'PARÁMETRO: {}'.format(NombreParametro), titulo)
metasheet.write_column('A2', ['Una cosa', 'Otra Cosa', 'Otra Cosa mas', 'pasfsdojk'], titulo)

# FIN
print('Hoja Guardada en {}'.format(r'D:\PCCS\01_Dmine\00_Parametros\ParametroEstandar\test.xlsx'))
writer.save()

