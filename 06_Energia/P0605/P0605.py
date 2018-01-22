# -*- coding: utf-8 -*-
"""
Started on thu, dec 12nd, 2017

@author: carlos.arana

"""

# Librerias utilizadas
import pandas as pd
import sys
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)
from VarInt.VarInt import VarInt
from classes.Meta import Meta
from Compilador.Compilador import compilar

"""
Las librerias locales utilizadas renglones arriba se encuentran disponibles en las siguientes direcciones:
SCRIPT:             | DISPONIBLE EN:
------              | ------------------------------------------------------------------------------------
VarInt              | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/VarInt
Meta                | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/Classes
Compilador          | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/Compilador
"""

# Documentacion del Parametro ---------------------------------------------------------------------------------------
# Descripciones del Parametro
M = Meta
M.ClaveParametro = 'P0605'
M.NombreParametro = 'Viviendas con panel solar'
M.DescParam = 'Porcentaje de viviendas particulares habitadas que cuentan con panel solar'
M.UnidadesParam = 'Porcentaje'
M.TituloParametro = 'VIV_CS'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 2

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'mean'

# Descripciones del proceso de Minería
M.nomarchivodataset = '23'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Datos disponibles por municipio para 2015, utilizados para la construcción del parametro'
M.ClaveDataset = 'EI2015'
M.ActDatos = '2015'
M.Agregacion = 'Promedio del porcentaje de viviendas viviendas que disponen de panel solar ' \
             'Para agregar la información y construir el parámetro, se promedian los ' \
             'valores para los municipios que componen una Ciudad del SUN. En la agregación de datos ' \
             'municipales a ciudades del SUN se han excluido los Municipos en los que la muestra de la Encuesta ' \
             'Intercensal fue clasificada como insuficiente.'
M.getmetafromds = 1

# Descripciones generadas desde la clave del parámetro
Meta.fillmeta(M)

M.Notas = ''

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname=M.nomarchivodataset, dtype={'CVE_MUN': str})
dataset.set_index('CVE_MUN', inplace=True)

# Generar dataset para parámetro y Variable de Integridad
dataset = dataset[~dataset['Municipio'].str.contains('\*\*')]   # Excluir municipios con ** muestra insuficiente
dataset = dataset[dataset['Tipo de equipamiento'].str.contains('Panel solar')]

colummas = ['Dispone_de_Equipamiento']                 # Columnas que se utilizan para construir el parámetro
dataset = dataset[colummas]
par_dataset = dataset
par_dataset = par_dataset.rename(columns = {'Dispone_de_Equipamiento' : M.ClaveParametro})
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo = 1)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
