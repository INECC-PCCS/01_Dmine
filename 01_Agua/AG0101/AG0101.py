# -*- coding: utf-8 -*-
"""
Started on Fri Aug 18 17:18:37 2017

@author: carlos.arana


"""

import os
import urllib
import pandas

# Scripts locales

fuente = r'http://www.pigoo.gob.mx/dashboard/exportar/excel/exportar_consulta_excel.php?tipo=max'
archivo = r'D:\PCCS\01_Analysis\01_DataAnalysis\04_Agua\Docs\pigoo.csv'

if not os.path.isfile(archivo):
    urllib.request.urlretrieve(fuente, archivo)

dataset = pandas.read_csv(archivo, skiprows = 2, header=1)

dataset.head()