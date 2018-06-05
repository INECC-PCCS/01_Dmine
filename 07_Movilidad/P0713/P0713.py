# -*- coding: utf-8 -*-
"""
Started on tue, feb 21st, 2018

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
M.ClaveParametro = 'P0713'
M.NombreParametro = 'Vialidades con rampa para discapacitados'
M.DescParam = 'Numero de Manzanas por municipio según disponibilidad de rampa para silla de ruedas en sus vialidades'
M.UnidadesParam = 'Numero de manzanas'
M.TituloParametro = 'Mrampa'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2014'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Manzanas por municipio según disponibilidad de rampa para silla de ruedas en sus vialidades'
M.ClaveDataset = 'CLEU'
M.ActDatos = '2014'
M.Agregacion = 'Se clasificó el total de manzanas por municipio segun la disponibilidad de rampa para silla de ruedas' \
               ' en alguna de ' \
               'sus vialidades. Se agregaron a una sola columna las manzanas en donde alguna o todas sus ' \
               'vialidades disponen de rampa. Para la agregación de datos' \
               'municipales a ciudades del SUN, se suma el numero de manzanas que disponen de banqueta en todos los ' \
               'municipios que integran cada ciudad del SUN'

# Descripciones generadas desde la clave del parámetro
M.getmetafromds = 1
Meta.fillmeta(M)

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname='DATOS', dtype={'CVE_MUN': 'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.rename_axis('CVE_MUN')
dataset.head(2)

# Generar dataset para parámetro y Variable de Integridad
rt = 'Rampa en Todas las vialidades'
ra = 'Rampa en Alguna vialidad'
par_dataset = dataset[rt]+dataset[ra]
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)

