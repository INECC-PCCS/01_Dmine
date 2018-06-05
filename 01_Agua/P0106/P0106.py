# -*- coding: utf-8 -*-
"""
Started on wed, thu 17th, 2018
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
M.ClaveParametro = 'P0106'
M.NombreParametro = 'Demanda Bioquimica de Oxigeno'
M.DescParam = 'Demanda Bioquimica de Oxigeno medida a 5 días'
M.UnidadesParam = 'mg/l'
M.TituloParametro = 'DBO5'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2017'
M.TipoInt = 1       # 1: Binaria; 2: Multivariable, 3: Integral

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'mean'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'P0106'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Estaciones de monitoreo y datos de Demanda Bioquimica de Oxigeno a 5 días'
M.ClaveDataset = 'CONAGUA'
M.ActDatos = '2017'
M.Agregacion = 'Se prometió el valor de DBO para las estaciones de monitorieo que existen en los municipios ' \
               'que componen cada ciudad del SUN'

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
list(dataset)

# Generar dataset para parámetro y Variable de Integridad
var1 = 'dbo'
par_dataset = dataset[var1]
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)

