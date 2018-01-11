# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 17:21:27 2017

@author: carlos.arana

Descripcion:
Procesa los datos del parámetro para regresar la variable de integridad.
Si la variable  de integridad es del tipo 1 (Binaria), la funcion busca celdas vacías en una sola columna y regresa 0
si la celda esta vacía o 1 si la celda tiene datos.
Si la Variable de Integridad es del tipo 2, la funcion busca celdas vacías en varias columnas y calcula un porcentaje
de integridad en el rango entre 0 y 1, en donde cero es igual a ningun dato (0%) y uno es igual a todos los datos (100%)

Input:
    par_dataset: [pandas dataframe] indexado por CVE_MUN, una sola columna con los datos para construir el parámetro
    dataset: [Pandas dataframe] dataset estandar, indexado por CVE_MUN, contiene toda la serie de datos disponibles,
                unicamente columnas con datos del parametro, evitar columnas de descripciones.
"""

import pandas as pd

def VarInt(par_dataset, dataset, tipo = 1):
    # 'tipo de integridad: [1] para Binaria, [2] para Serie
    if tipo == 1:
        par_dataset['EXISTE'] = ~par_dataset.isnull()   # el simbolo ~ es para invertir los valores de true / false
        par_dataset['VAR_INTEGRIDAD'] = par_dataset['EXISTE'].astype(int)
    if tipo == 2:
        par_dataset['NUM_REGISTROS'] = len(list(dataset))  # ¿Cuantos registros debería tener cada caso?
        par_dataset['REGISTROS_EXISTEN'] = dataset.notnull().sum(axis=1)  # ¿Cuantas registros tienen informacion?
        par_dataset['VAR_INTEGRIDAD'] = par_dataset['REGISTROS_EXISTEN'] / par_dataset['NUM_REGISTROS']

    variables_par_dataset = list(par_dataset)
    par_dataset['CVE_MUN'] = dataset.index
    return par_dataset, variables_par_dataset
