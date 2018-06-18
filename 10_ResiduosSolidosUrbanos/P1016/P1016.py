# -*- coding: utf-8 -*-
"""
Started on mon, jun 11st, 2018
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
M.ClaveParametro = 'P1016'
M.NombreParametro = 'Número de estaciones de transferencia en la Ciudad'
M.DescParam = 'Número de estaciones de transferencia dentro de los municipios en los que se ubica una Ciudad'
M.UnidadesParam = 'Estacion'
M.TituloParametro = 'etrnsf'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 3       # 1: Binaria; 2: Multivariable, 3: Integral

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'count'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'P1016'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Nombre y funciones de las estaciones de tranferencia'
M.ClaveDataset = 'INEGI'
M.ActDatos = '2015'
M.Agregacion = 'Se contó el numero de estaciones de tranferencia dentro de cada municipio. Luego se sumó el numero ' \
               'de estaciones de tranferencia dentro de los municipios de cada ciudad'

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
var1 = 'Nombre E-Transf'
par_dataset = dataset[var1]
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
