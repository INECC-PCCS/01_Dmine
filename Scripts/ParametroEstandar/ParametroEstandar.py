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

# Librerias Utilizadas
import pandas as pd

def ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro):

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
    DatosLimpios.to_excel(writer, sheet_name ='DATOS')
    integridad_parametro['INTEGRIDAD'].to_excel(writer, sheet_name ='INTEGRIDAD')
    integridad_parametro['EXISTENCIA'].to_excel(writer, sheet_name ='EXISTENCIA')

    # Definir formatos para hoja de metadatos -------------------------------------------------------------------------
    workbook = writer.book                      # Declaro el libro para anunciarle los formatos
    metasheet = writer.sheets['METADATOS']      # Declaro la hoja METADATOS para darle formatos
    paramsheet = writer.sheets['PARAMETRO']     # Declaro la hoja PARAMETRO para darle formatos

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
    metasheet.merge_range('A8:B8', 'DESCRIPCION DEL PROCESO DE MINERIA', encabezado)
    metasheet.merge_range('A18:B18', 'HOJAS INCLUIDAS EN ESTE LIBRO', encabezado)
    metasheet.merge_range('A25:B25', 'DESCRIPCION DE LAS VARIABLES INCLUIDAS EN ESTE LIBRO', encabezado)

    # Crear Titulo y reescribir indice con formato adecuado
    metasheet.set_column('A:A', 22.71)
    metasheet.set_column('B:B', 82.57, texwrap)
    metasheet.set_column('D:D', 17.57)
    metasheet.set_column('E:E', 13.29)
    paramsheet.set_column('B:B', 13.29)

    # FIN
    print('Hoja Guardada en {}'.format(RutaSalida + r'\{}\{}.xlsx'.format(ClaveParametro, ClaveParametro)))
    writer.save()

