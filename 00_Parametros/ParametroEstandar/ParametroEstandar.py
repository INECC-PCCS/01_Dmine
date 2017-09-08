# -*- coding: utf-8 -*-
"""
Started on Fri Sep  1 13:32:58 2017

@author: carlos.arana
"""

'''
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

'''

# Librerias Utilizadas
import pandas as pd

def ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro):

    # Desempacar datos simples
    ClaveParametro = DescParametro['ClaveParametro']
    NombreParametro = DescParametro['NombreParametro']
    info_completa = DescParametro['info_completa']
    info_sin_info = DescParametro['info_sin_info']
    info_incomple = DescParametro['info_incomple']
    RutaSalida = DescParametro['RutaSalida']

    # Proxy de libro
    writer = pd.ExcelWriter(RutaSalida + r'\{}\{}.xlsx'.format(ClaveParametro, ClaveParametro))

    # Creacion de hojas
    MetaParametro.to_excel(writer, sheet_name ='METADATOS')
    Parametro.to_excel(writer, sheet_name ='PARAMETRO')
    DatosLimpios.to_excel(writer, sheet_name ='DATOS')
    integridad_parametro['INTEGRIDAD'].to_excel(writer, sheet_name ='INTEGRIDAD')
    integridad_parametro['EXISTENCIA'].to_excel(writer, sheet_name ='EXISTENCIA')

    # Definir formatos para hoja de metadatos
    metasheet = writer.sheets['METADATOS']
    paramsheet = writer.sheets['PARAMETRO']
    workbook = writer.book
    metaformat = workbook.add_format({'text_wrap': True})

    # Creacion de Grafico de integridad
    the_chart = workbook.add_chart({'type' : 'pie'})
    headings = ['INTEGRIDAD', 'NO. CIUDADES']
    data = [
        ['INFO. COMPLETA', 'INFO. INCOMPLETA', 'SIN INFO.'],
        [info_completa, info_incomple, info_sin_info]
    ]

    bold = workbook.add_format({'bold': 1, 'border': 1, 'valign': 'top'})    # Formato para encabezado de datos
    borders = workbook.add_format({'border': 1})            # Formato para tabla sencilla

    metasheet.write_row('D1', headings, bold)       # Inscripcion de datos en la hoja
    metasheet.write_column('D2', data[0], borders)
    metasheet.write_column('E2', data[1], borders)

    the_chart.add_series({
        'name' : 'Integridad del Parámetro',
        'categories': '=METADATOS!$D$2:$D$4',
        'values' : '=METADATOS!$E$2:$E$4',
        'data_labels' : {'value' : True, 'legend_key': True},
        'points' : [
            {'fill': {'color': '#0CCE6B'}},
            {'fill': {'color': '#F2FF49'}},
            {'fill': {'color': '#FF4242'}},
        ]
    })

    the_chart.set_title({'name': 'Integridad del Dataset\n{}'.format(NombreParametro)})
    metasheet.insert_chart('D6', the_chart, {'x_offset': 0, 'y_offset': 0})

        # Aplicar Formato
    metasheet.set_column('A:A', 22.71)
    metasheet.set_column('B:B', 82.57, metaformat)
    metasheet.set_column('D:D', 17.57)
    metasheet.set_column('E:E', 13.29)
    paramsheet.set_column('B:B', 13.29)

        # Crear Titulo y reescribir indice con formato adecuado
    metasheet.merge_range('A1:B1', 'PARÁMETRO: {}'.format(NombreParametro), bold)
    metasheet.write_column('A2', list(MetaParametro.index), bold)

    # FIN
    print('Hoja Guardada en {}'.format(RutaSalida + r'\{}\{}.xlsx'.format(ClaveParametro, ClaveParametro)))
    writer.save()

