# -*- coding: utf-8 -*-
"""
Started on tue, feb 06th, 2018

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
M.ClaveParametro = 'P1005'
M.NombreParametro = 'Número de vehículos utilizados para la recolección de residuos sólidos urbanos'
M.DescParam = 'Número de vehículos utilizados para la recolección de residuos sólidos urbanos'
M.UnidadesParam = 'Numero de vehiculos'
M.TituloParametro = 'VRRSU'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Datos disponibles por municipio para 2015, utilizados para la construcción del parametro'
M.ClaveDataset = 'CNGMD'
M.ActDatos = '2015'
M.Agregacion = 'Este parámetro utiliza la variable "P6_3_2_1_3" de la base de datos del Censo Nacional de Gobiernos ' \
               'Municipales y Delegacionales 2015, que indica el numero de vehiculos utilizados para la recoleccion ' \
               'de sus Residuos Solidos Urbanos (RSU) de cada municipio.' \
               '\nPara agregar la información y construir el parámetro, se suma el valor de P6_3_2_1_3 de todos los ' \
               'municipios de los que componen cada ciudad del SUN. De este modo, el valor de P1005 indica el ' \
               'numero de vehiculos utilizados para la recoleccion de RS en cada ciudad del SUN.'

M.getmetafromds = 1

# Descripciones generadas desde la clave del parámetro
Meta.fillmeta(M)

M.Notas = 's/n'

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname=M.nomarchivodataset, dtype={'CVE_MUN': 'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.apply(pd.to_numeric).where((pd.notnull(dataset)), None)
dataset = dataset.rename_axis('CVE_MUN')

# Generar dataset para parámetro y Variable de Integridad
par_dataset = dataset['P6_3_2_1_3'].to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
