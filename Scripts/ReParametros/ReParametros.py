# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 14:08:14 2017

@author: carlos.arana

Descripcion:
Script para ejecutar todos los scripts de parametro, con el objetivo de repetir las minerias de datos
cuando se modifica alguno de los scripts básicos
"""

import pandas as pd
import os

Fuente = r'D:\PCCS\01_Dmine\00_Parametros\CatalogoParametros.xlsx'
dataset = pd.read_excel(Fuente, sheetname="INDICE")

D1 = dataset.loc[dataset['ARCHIVO_LOCAL'] != r'S/A']
D2 = D1.loc[D1['ARCHIVO_LOCAL'] != 'proxy']

for i in D2['ARCHIVO_LOCAL']:
    i = i.replace('xlsx', 'py')
    print("EJECUTANDO {}...................".format(i))
    exec(open(i).read())
