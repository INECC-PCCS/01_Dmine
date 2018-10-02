# -*- coding: utf-8 -*-
"""
Started on mon, aug 27th, 2018
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
M.ClaveParametro = 'P0813'
M.NombreParametro = 'Homicidios intencionales'
M.DescParam = 'Número de homicidios intencionales'
M.UnidadesParam = 'Homicidios'
M.TituloParametro = 'NHI'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2016'
M.TipoInt = 1       # 1: Binaria; 2: Multivariable, 3: Integral

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'count'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'defunciones'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Homicidios intencionales registrados en el año {}'.format(M.PeriodoParam)
M.ClaveDataset = 'INEGI\\Defunciones'
M.ActDatos = M.PeriodoParam
M.Agregacion = 'Se contó el número de homicidios registrados dentro de los municipios que componen las ciudades ' \
               'del SUN en el año {}'.format(M.PeriodoParam)

# Descripciones generadas desde la clave del parámetro
M.getmetafromds = 1
Meta.fillmeta(M)

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname='DATOS', dtype={'CVE_MUN_OCURR': 'str'})
dataset.set_index('CVE_MUN_OCURR', inplace=True)
dataset = dataset.rename_axis('CVE_MUN')
dataset.head(2)
list(dataset)

# Generar dataset para parámetro y Variable de Integridad
anio = 'ANIO_OCUR'
var1 = 'CAUSA_DEF'
dataset = dataset[dataset[anio] == int(M.PeriodoParam)]
par_dataset = dataset[var1]
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
