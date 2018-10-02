# -*- coding: utf-8 -*-
"""
Started on mon, mar 05th, 2018

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
M.ClaveParametro = 'P0402'
M.NombreParametro = 'Viviendas que aprovechan energía solar'
M.DescParam = 'Viviendas que aprovechan energía solar, por medio del uso de paneles fotovoltaicos o ' \
              'calentadores solares'
M.UnidadesParam = 'Porcentaje'
M.TituloParametro = 'VSol'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 2       # 1: Binaria; 2: Multivariable, 3: Integral

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'mean'

# Descripciones del proceso de Minería
M.nomarchivodataset = '23'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Viviendas que cuentan con calentador solar o panel fotovoltaico (2015)'
M.ClaveDataset = 'EI2015'
M.ActDatos = '2014'
M.Agregacion = 'Este parámetro se construye a partir de 2 variables de la encuesta intercensal: ' \
               'Porcentajes de viviendas que cuentan con Calentador Solar y Porcentaje de viviendas que cuentan con ' \
               'Panel fotovoltaico. Debido a que el parametro está definidi como "Viviendas que cuentan con uno u ' \
               'otro equipamiento", se elige el valor superior entre ambas variables para cada municipio, ya que ' \
               'sumar ambos crearía duplicidades (Caso "Una vivienda cuenta con Panel solar Y Calentador Solar) y ' \
               'promediarlos significaría una pérdida de información. Una vez elegido el valor superior entre ambas ' \
               'variables, para agregar los datos y crear el parámetro se promedian los porcentajes para los ' \
               'municipios que componen cada ciudad del SUN.'

# Descripciones generadas desde la clave del parámetro
M.getmetafromds = 1
Meta.fillmeta(M)

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname='23', dtype={'CVE_MUN': 'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.rename_axis('CVE_MUN')
dataset.head(2)
dataset['Tipo de equipamiento'].unique()

# Generar dataset para parámetro y Variable de Integridad
dataset = dataset[~dataset['Municipio'].str.contains('\*\*')]   # Excluir municipios con ** muestra insuficiente

eq1 = 'Calentador solar de agua'
eq2 = 'Panel solar'
var1 = dataset[dataset['Tipo de equipamiento'].str.contains(eq1)]
var2 = dataset[dataset['Tipo de equipamiento'].str.contains(eq2)]

par_dataset = pd.DataFrame()
par_dataset['Dispone de calentador solar'] = var1['Dispone_de_Equipamiento']
par_dataset['Dispone de panel solar'] = var2['Dispone_de_Equipamiento']
dataset = par_dataset

par_dataset = par_dataset.max(axis = 1).to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
