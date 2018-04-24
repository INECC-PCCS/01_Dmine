# -*- coding: utf-8 -*-
"""
Started on mon, apr 23rd, 2018

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
M.ClaveParametro = 'P0405'
M.NombreParametro = 'Viviendas Verticales'
M.DescParam = 'Numero de viviendas verticales por ciudad'
M.UnidadesParam = 'Numero de viviendas'
M.TituloParametro = 'Vvert'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2018'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'Rep_Viv_Vig'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Viviendas (Tipo, Segmento, ubicacion en PCU)'
M.ClaveDataset = r'SNIIV'
M.ActDatos = '2017'
M.Agregacion = 'Se sumó el total de viviendas verticales vigentes para los municipios que integran cada ciudad del SUN'

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
dataset = dataset[dataset['Tipo de Vivienda'] == 'HORIZONTAL']
dsvar = 'Viviendas'
par_dataset = dataset[dsvar]
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
