# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:45:27 2017

@author: carlos.arana
"""

'''
Descripcion:
Script para revisar variables existentes en un dataset.
El script revisa, a partir de una lista, si las variables se encuentran previamente identificadas
en el proyecto de la PCCS (En el archivo PCCS_variables.csv). Si la variable existe, le asigna la 
definición previamente establecida y almacena ambos valores en un diccionario.
Si no existe, pide la definición al usuario, la guarda en 'PCCS_variables.csv' y almacena la variable
y su descripción en un diccionario.
Regresa una Pandas.Series a partir del diccionario almacenado.
'''

# Librerias Utilizadas
import csv
import pandas

def variables(lista):
    archivovariablescsv = r'D:\PCCS\01_Dmine\Scripts\PCCS_variables\PCCS_variables.csv'
    with open(archivovariablescsv, 'r') as thefile:
        reader = csv.reader(thefile)
        dictvariables = {}
        for row in reader:
            if row == []: continue
            k, v = row
            dictvariables[k] = v

    # Creacion de nuevo diccionario para actualizar variables del archivo maestro
    actualizacion_variables = dictvariables

    actualizacion_variables['TIPO_SUN']
    # Diccionario para almacenar el metadato
    metavariables = {}

    for i in lista:
        if i in dictvariables.keys():
            print(i)
            metavariables[i] = dictvariables[i]
            continue
        else:
            mensaje = 'La variable "{}" no existe en el proyecto. Escribe su descripcion o ' \
                      '[SSALIR] Sin guardar' \
                      '[GSALIR] y guardar:'.format(i)
            hacer = input(mensaje)
            if hacer == 'SSALIR':
                raise ValueError('Script terminado por el usuario')
            elif hacer == 'GSALIR':
                print('Se guardaron las descripciones capturadas')
                break
            else:
                actualizacion_variables[i] = hacer
                metavariables[i] = hacer

    with open(archivovariablescsv, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in actualizacion_variables.items():
            writer.writerow([key, value])

    return pandas.DataFrame.from_dict(metavariables, orient='index').rename(columns={0:'DESCRIPCION'})