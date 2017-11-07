# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 17:21:27 2017

@author: carlos.arana

Descripcion:
Procesa los datos del parámetro para regresar la variable de integridad.
Si la variable  de integridad es del tipo binario,

Input:
    par_dataset: [pandas dataframe] indexado por CVE_MUN, una sola columna con los datos para construir el parámetro
    dataset: [Pandas dataframe] dataset estandar, indexado por CVE_MUN, contiene toda la serie de datos disponibles,
                unicamente columnas con datos del parametro, evitar columnas de descripciones.
"""

import pandas as pd

def VarInt(par_dataset, dataset, tipo = 1):
    print('tipo de integridad: [1] para Binaria, [2] para Serie')
    if tipo == 1:
        par_dataset['EXISTE'] = ~par_dataset.isnull()   #el simbolo ~ es para invertir los valores de true / false
        par_dataset['VAR_INTEGRIDAD'] = par_dataset['EXISTE'].astype(int)
    if tipo == 2:
        par_dataset['NUM_REGISTROS'] = len(dataset)         # ¿Cuantos registros debería tener cada caso?
        par_dataset['REGISTROS_EXISTEN'] = dataset.head().notnull().sum(axis=1)   # ¿Cuantas registros tienen informacion?
        par_dataset['VAR_INTEGRIDAD'] = par_dataset['REGISTROS_EXISTEN'] / par_dataset['NUM_REGISTROS']

    variables_par_dataset = list(par_dataset)
    par_dataset['CVE_MUN'] = dataset.index
    return par_dataset, variables_par_dataset
