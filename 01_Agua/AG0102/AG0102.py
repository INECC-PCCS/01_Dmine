# -*- coding: utf-8 -*-
"""
Started on Tue Aug 15 12:05:32 2017
@author: carlos.arana
"""

'''
Descripcion: Creacion de indicadores desde archivo test.csv (De la encuesta intercensal 2015)
'''

# Librerias utilizadas
import os
import pandas as pd
import sys
os.chdir(r'D:\PCCS\01_Dmine\04_Agua')

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\00_Parametros'
if module_path not in sys.path:
    sys.path.append(module_path)

from SUN.asignar_sun import asignar_sun                     # Disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/SUN
from SUN_integridad.SUN_integridad import SUN_integridad    # Disponible en https://github.com/INECC-PCCS/01_Dmine/tree/master/00_Parametros/SUN_integridad

# Importar datos
data = pd.read_csv("test.csv")
data.rename(columns={'_id':'CVE_MUN'}, inplace=True)
data['CVE_MUN'] = data['CVE_MUN'].apply('{:0>5}'.format)

# Asignar claves SUN
data_std = asignar_sun(data, vars = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'NOM_ENT'])

# Indicadores para AG0102
cols = ['NOM_ENT', 'CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'entubada_total']
AG0102 = data_std[cols].dropna()

    # Revision de integridad para AG0102
AG0102_int = SUN_integridad(AG0102)

    # Creacion de archivo con informacion para AG0102
indicador = 'AG0102'
if not os.path.isdir(indicador):
    os.mkdir(indicador)

writer = pd.ExcelWriter(r'.\{}\{}.xlsx'.format(indicador, indicador))
AG0102.set_index(['CVE_SUN']).sort_index().to_excel(writer, sheet_name = 'DATOS')
AG0102_int['INTEGRIDAD'].sort_index().to_excel(writer, sheet_name = 'INTEGRIDAD')
AG0102_int['EXISTENCIA'].sort_index().to_excel(writer, sheet_name = 'EXISTENCIA')
writer.close()

# Indicadores para AG0106
cols = ['NOM_ENT', 'CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN', 'disponen_red_pública']
AG0106 = data_std[cols].dropna()

    # Revision de integridad para AG0102
AG0106_int = SUN_integridad(AG0106)

    # Creacion de archivo con informacion para AG0102
indicador = 'AG0106'
if not os.path.isdir(indicador):
    os.mkdir(indicador)

writer = pd.ExcelWriter(r'.\{}\{}.xlsx'.format(indicador, indicador))
AG0106.set_index(['CVE_SUN']).sort_index().to_excel(writer, sheet_name = 'DATOS')
AG0106_int['INTEGRIDAD'].sort_index().to_excel(writer, sheet_name = 'INTEGRIDAD')
AG0106_int['EXISTENCIA'].sort_index().to_excel(writer, sheet_name = 'EXISTENCIA')
writer.close()


''' Codigo de prueba (No de produccion)

x=0;
for i in list(data_std):
    print('{} - {}'.format(x, i))
    x += 1
list(cols[i] for i in list(data_std))

for i in cols:
    print(list(data_std)[i])

list(data)[3]

list(data)[cols]

data.head()

'''