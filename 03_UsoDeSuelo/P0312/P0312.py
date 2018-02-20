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
M.ClaveParametro = 'P0312'        # La fuente de los datos es la misma que la del parametro P0309
M.NombreParametro = 'Total de viviendas particulares habitadas'
M.DescParam = 'Viviendas particulares habitadas de cualquier clase: casa independiente, departamento en edificio, ' \
              'vivienda o cuarto en vecindad, vivienda o cuarto de azotea, local no construido para habitación, ' \
              'vivienda móvil, refugios o clase no especificada, incluyendo viviendas particulares sin información ' \
              'de ocupantes.'
M.UnidadesParam = 'Numero de viviendas'
M.TituloParametro = 'TVIVPARHAB'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2010'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Datos disponibles por municipio para 2010, utilizados para la construcción del parametro'
M.ClaveDataset = 'CPV'
M.ActDatos = '2010'
M.Agregacion = 'Este parámetro utiliza la variable "TVIVPARHAB" de la base de datos del Censo Nacional de Poblacion y' \
               'Vivienda 2010, que indica las Viviendas particulares habitadas de cualquier clase: casa ' \
               'independiente, departamento en edificio, vivienda o cuarto en vecindad, vivienda o cuarto de azotea, ' \
               'local no construido para habitación, vivienda móvil, refugios o clase no especificada, incluyendo ' \
               'viviendas particulares sin información de ocupantes.' \
               '\nPara agregar la información y construir el parámetro, se suma el valor de TVIVPARHAB de todos los ' \
               'municipios de los que componen cada ciudad del SUN. De este modo, el valor de P0312 indica el ' \
               'numero total de Viviendas Particulares Habitadas en cada ciudad del SUN.'

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
par_dataset = dataset['TVIVPARHAB'].to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
