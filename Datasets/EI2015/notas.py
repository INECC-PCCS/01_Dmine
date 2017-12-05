'''
codigo de pruebas para extraccion de notas de hojas del dataset "Encuesta Intercensal 2015"
'''

# Librerias utilizadas
import pandas as pd
import sys
import urllib
import os
import numpy as np

# Configuracion del sistema
print('Python {} on {}'.format(sys.version, sys.platform))
print('Pandas version: {}'.format(pd.__version__))
import platform; print('Running on {} {}'.format(platform.system(), platform.release()))

# LIGAS PARA DESCARGA DE ARCHIVOS
# Las ligas para descarga tienen una raiz URL común que cambia
# dependiendo del indicador y estado que se busque descargar
url = r'http://www.beta.inegi.org.mx/contenidos/Proyectos/enchogares/' \
      r'especiales/intercensal/2015/tabulados/'
indicador = r'14_vivienda_'
raiz = url+indicador
links = {
    '01' : raiz+'ags.xls',
    '02' : raiz+'bc.xls',
    '03' : raiz+'bcs.xls',
    '04' : raiz+'cam.xls',
    '05' : raiz+'coah.xls',
    '06' : raiz+'col.xls',
    '07' : raiz+'chis.xls',
    '08' : raiz+'chih.xls',
    '09' : raiz+'cdmx.xls',
    '10' : raiz+'dgo.xls',
    '11' : raiz+'gto.xls',
    '12' : raiz+'gro.xls',
    '13' : raiz+'hgo.xls',
    '14' : raiz+'jal.xls',
    '15' : raiz+'mex.xls',
    '16' : raiz+'mich.xls',
    '17' : raiz+'mor.xls',
    '18' : raiz+'nay.xls',
    '19' : raiz+'nl.xls',
    '20' : raiz+'oax.xls',
    '21' : raiz+'pue.xls',
    '22' : raiz+'qro.xls',
    '23' : raiz+'qroo.xls',
    '24' : raiz+'slp.xls',
    '25' : raiz+'sin.xls',
    '26' : raiz+'son.xls',
    '27' : raiz+'tab.xls',
    '28' : raiz+'tamps.xlsz',
    '29' : raiz+'tlax.xls',
    '30' : raiz+'ver.xls',
    '31' : raiz+'yuc.xls',
    '32' : raiz+'zac.xls'
}

# Descarga de archivos a carpeta local
destino = r'D:\PCCS\00_RawData\01_CSV\Intercensal2015\estatal\14. Vivienda'
archivos = {}   # Diccionario para guardar memoria de descarga

for k,v in links.items():
    archivo_local = destino + r'\{}.xls'.format(k)
    if os.path.isfile(archivo_local):
        print('Ya existe el archivo: {}'.format(archivo_local))
        archivos[k] = archivo_local
    else:
        print('Descargando {} ... ... ... ... ... '.format(archivo_local))
        urllib.request.urlretrieve(v, archivo_local) #
        archivos[k] = archivo_local
        print('se descargó {}'.format(archivo_local))

# Función para extraer notas
skiprows = {
    '08',
    '09',
    '19',
    '20',
    '21',
    '23',
    '25',
    '26',
}

archivos.keys()

listahojas = ['02', '08', '09', '19', '20', '21', '23', '25', '26']

skiprows = {
    '02' : 7,   #
    '08' : 7,   # Combustible utilizado para cocinar
    '09' : 7,   # Utilizan leña o carbón para cocinar y distribucion porcentual segun disponibilidad de estufa o fogon
    '19' : 7,   # Forma de eliminación de residuos
    '20' : 8,   # Viviendas que entregan sus residuos al servicio publico y distribucion porcentual por condición de separacion
    '21' : 7,   # Separación y reutilización de residuos
    '23' : 7,   # Disponibilidad y tipo de equipamiento
    '25' : 7,   # Disponibilidad de agua entubada y fuente de abastecimiento
    '26' : 8,   # Disponibilidad de drenaje y lugar de desalojo
}

def getnotes(ruta, skip):
    tempDF = pd.read_excel(ruta, sheetname=hoja, skiprows=skip)  # Carga el dataframe de manera temporal
    c1 = tempDF['Unnamed: 0'].dropna()  # Carga únicamente la columna 1, que contiene las notas, sin valores NaN
    c1.index = range(len(c1))           # Reindexa la serie para compensar los NaN eliminados en el comando anterior
    indice = c1[c1.str.contains('Nota')].index[0]   # Encuentra el renglon donde inician las notas
    rows = range(indice, len(c1))                   # Crea una lista de los renglones que contienen notas
    templist = c1.loc[rows].tolist()                # Crea una lista con las notas
    notas = []
    for i in templist:
        notas.append(i.replace('\xa0', ' '))
    return notas

listanotas = {}
for archivo, ruta in archivos.items():
    print('Procesando {} desde {}'.format(archivo, ruta))
    for hoja in listahojas:
        if hoja not in listanotas.keys():
            listanotas[hoja] = {}
        listanotas[hoja][archivo] = getnotes(ruta, skiprows[hoja])

tempframe = pd.read_excel(archivos['02'], sheetname='02', skiprows=skiprows['02'])
tempframe = tempframe.dropna()

listanotas.values()

templist = []                               # Inicia con una lista vacía
for hoja, dict in listanotas.items():       # Itera sobre el diccionario con todas las notas
    for estado, notas in dict.items():      # Itera sobre el diccionario de estados de cada hoja
        for nota in notas:                  # Itera sobre la lista de notas que tiene cada estado
            if nota not in templist:        # Si la nota no existe en la lista:
                print('Estado: {} / Hoja {} / : Nota: {}'.format(estado, hoja, nota))   # Imprime la nota
                templist.append(nota)       # Agrega la nota al diccionario

