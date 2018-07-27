# -*- coding: utf-8 -*-
"""
Started on fri, apr 08th, 2018

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
M.ClaveParametro = 'P0714'
M.NombreParametro = 'Salarios Minimos Generales'
M.DescParam = 'Salarios Minimos Generales publicados por la Comision Nacional de los Salarios Minimos'
M.UnidadesParam = 'Pesos Mexicanos Diarios'
M.TituloParametro = 'SMG'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2011'
M.TipoInt = 1       # 1: Binaria; 2: Multivariable, 3: Integral

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'min'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'SMG_{}'.format(M.PeriodoParam)
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Salarios minimos Generales por area geografica para el periodo {}'.format(M.PeriodoParam)
M.ClaveDataset = 'CONASAMI'
M.ActDatos = M.PeriodoParam
M.Agregacion = 'Se asignó a cada ciudad del SUN el menor de los salarios mínimos de los municipios que la componen'

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
var1 = 'SMG_{}'.format(M.PeriodoParam)
par_dataset = dataset[var1]
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
