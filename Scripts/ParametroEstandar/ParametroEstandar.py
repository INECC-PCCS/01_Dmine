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
IntegridadParametro : [dict] diccionario con los dos dataframe de integridad generados con el script SUN_Integridad

---
El formato de la hoja imita lo mejor posible los colores estándar de identidad gráfica institucional del Gobierno
de la República, periodo 2012 - 2018. Cuando ha sido necesario, se han utilizado tonalidades más claras o más oscuras
de los colores estándar para lograr distinciones en la información presentada.

[Rojo]          = Pantone 200 C             = Hex #BA0C2F = rgb(186,12,47)
[Verde]         = Pantone 356 C             = Hex #007A33 = rgb(0,122,51)
[Gris Oscuro]   = Pantone Cool Gray 10 C    = Hex #63666A = rgb(99,102,106)
[Gris claro ()] = Pantone 877 C (Plata)     = Hex #8A8D8F = rgb(138,141,143)

El manual de identidad se encuentra disponible en
http://www.funcionpublica.gob.mx/manual/Guia_Basica_de_Identidad_Grafica_Institucional.pdf

"""

# Librerias Utilizadas
import pandas as pd
import datetime
import os
import json

def ParametroEstandar(DescParametro,
                      MetaParametro,
                      Parametro,
                      DatosLimpios,
                      integridad_parametro,
                      hoja_datos):

    # Desempacar datos simples ----------------------------------------------------------------------------------------
    ClaveParametro = DescParametro['ClaveParametro']
    NombreParametro = DescParametro['NombreParametro']
    info_completa = DescParametro['info_completa']
    info_sin_info = DescParametro['info_sin_info']
    info_incomple = DescParametro['info_incomple']
    RutaSalida = DescParametro['RutaSalida']

    # Creacion de hojas -----------------------------------------------------------------------------------------------
    writer = pd.ExcelWriter(RutaSalida + r'\{}\{}.xlsx'.format(ClaveParametro, ClaveParametro))     # Proxy de libro
    MetaParametro.to_excel(writer, sheet_name ='METADATOS')
    Parametro.to_excel(writer, sheet_name ='PARAMETRO')
    hoja_datos.to_excel(writer, sheet_name ='DATOS')
    integridad_parametro['INTEGRIDAD'].to_excel(writer, sheet_name ='INTEGRIDAD')
    integridad_parametro['EXISTENCIA'].to_excel(writer, sheet_name ='EXISTENCIA')

    # Declarar hojas para darles formato -------------------------------------------------------------------------
    workbook = writer.book
    metasheet = writer.sheets['METADATOS']
    paramsheet = writer.sheets['PARAMETRO']
    intsheet = writer.sheets['INTEGRIDAD']
    exisheet = writer.sheets['EXISTENCIA']

    # Definicion de colores
    verde = '#007A33'                           # Verde para ciudades con informacion completa
    amarillo = '#A2CEB4'                        # 'Amarillo' para datos incompletos
    rojo = '#BA0C2F'                            # Rojo para ciudades sin datos
    gris_oscuro = '#63666A'                     # Gris para Titulos
    gris_claro = '#8A8D8F'                      # Gris Claro para fondo de encabezados

    # Especificacion de formatos
    texwrap = workbook.add_format({'text_wrap': True})                       # Formato textwrap para datos
    bold = workbook.add_format({'bold': 1, 'border': 0, 'valign': 'top'})    # Formato para Indices
    titulo = workbook.add_format({                                           # Formato para Titulo de la hoja
                                    'bold': 1,
                                    'border': 1,
                                    'valign': 'top',
                                    'pattern' : 1,
                                    'bg_color' : 'white',
                                    'font_color': gris_oscuro,
                                    'font_size': 14,
                                    'border_color': gris_claro
                                })                                           # /Formato para Titulo de la hoja
    encabezado =  workbook.add_format({                                      # Formato para encabezado de datos
                                    'bold': 0,
                                    'border': 0,
                                    'valign': 'top',
                                    'pattern' : 1,
                                    'bg_color' : gris_claro,
                                    'font_color': 'white',
                                    'bottom': 1,
                                    'border_color': gris_claro
                                    })                                       # /Formato para encabezado de datos
    borders = workbook.add_format({'border': 1, 'border_color': gris_claro})   # Formato para tabla sencilla

    # Creacion de Grafico de integridad ------------------------------------------------------------------------------
    headings = ['INTEGRIDAD', 'NO. CIUDADES']                               # Datos para la gráfica
    data = [
        ['INFO. COMPLETA', 'INFO. INCOMPLETA', 'SIN INFO.'],
        [info_completa, info_incomple, info_sin_info]
    ]

    metasheet.write_row('D2', headings, encabezado)                 # Inscripcion de datos de la gráfica en la hoja
    metasheet.write_column('D3', data[0], borders)
    metasheet.write_column('E3', data[1], borders)                  # /Inscripcion de datos de la gráfica en la hoja
    the_chart = workbook.add_chart({'type' : 'pie'})                                # Creación del gráfico
    the_chart.add_series({
        'name' : 'Integridad del Parámetro',
        'categories': '=METADATOS!$D$3:$D$5',
        'values' : '=METADATOS!$E$3:$E$5',
        'data_labels' : {'value' : True, 'legend_key': True},
        'points' :
            [
            {'fill': {'color': verde}}, # Verde parainformacion complete
            {'fill': {'color': amarillo}}, # Amarillo
            {'fill': {'color': rojo}}, # Rojo
            ]
    })
    the_chart.set_title({'name': 'Integridad de datos del parámetro\n{}'.format(NombreParametro.upper())})
    metasheet.insert_chart('D7', the_chart, {'x_offset': 0, 'y_offset': 0})         # /Creación del gráfico

    # Aplicar Formatos -----------------------------------------------------------------------------------------------
    # Crear Titulo y reescribir indice con formato adecuado
    metasheet.merge_range('A1:B1', 'PARÁMETRO: {}'.format(NombreParametro.upper()), titulo)
    metasheet.write_column('A2', list(MetaParametro.index), bold)
    metasheet.merge_range('A2:B2', 'DESCRIPCION DEL PARAMETRO', encabezado)
    metasheet.merge_range('A9:B9', 'DESCRIPCION DEL PROCESO DE MINERIA', encabezado)
    metasheet.merge_range('A23:B23', 'HOJAS INCLUIDAS EN ESTE LIBRO', encabezado)
    metasheet.merge_range('A30:B30', 'DESCRIPCION DE LAS VARIABLES INCLUIDAS EN ESTE LIBRO', encabezado)

    # Formatear Columnas de hoja Metadatos
    c = 9.86        # Tamaño estándar de columna
    metasheet.set_column('A:A', 22.71)
    metasheet.set_column('B:B', 82.57, texwrap)
    metasheet.set_column('D:D', 17.57)
    metasheet.set_column('E:E', 13.29)

    # Formatear Columnas de hoja Parametro
    paramsheet.set_column('B:B', 45.14)
    paramsheet.set_column('C:C', c)
    paramsheet.set_column('D:D', c)

    # Formatear Columnas de hojas Integridad y existencia
    intsheet.set_column('B:B', 40.43)
    intsheet.set_column('C:C', c)
    intsheet.set_column('D:D', c)
    intsheet.set_column('E:E', c)

    exisheet.set_column('A:A', c)
    exisheet.set_column('B:B', c)
    exisheet.set_column('C:C', c)
    exisheet.set_column('D:D', 47)
    exisheet.set_column('E:E', c)

    # Crear archivo de ultima corrida
    filepath = RutaSalida + r'\{}\{}.txt'.format(ClaveParametro, ClaveParametro)
    rundate = datetime.datetime.today().strftime('Último procesado de parametro: %Y/%m/%d \n\n')
    if not os.path.isfile(filepath):
        with open(filepath, 'a') as file:
            file.write(rundate)
    else:
        with open(filepath, 'w') as file:
            file.write(rundate)

    # FIN
    print('Hoja Guardada en {}'.format(RutaSalida + r'\{}\{}.xlsx'.format(ClaveParametro, ClaveParametro)))
    writer.save()
