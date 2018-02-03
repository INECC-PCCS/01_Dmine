# -*- coding: utf-8 -*-
"""
Started on wed, jan 24th, 2018

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
M.ClaveParametro = 'P0306'
M.NombreParametro = 'Programas  de modernización catastral '
M.DescParam = 'Municipios que cuentan con un Programa de modernizacion Catastral'
M.UnidadesParam = 'Binario'
M.TituloParametro = 'PMC'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'mean'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'P0306'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Datos disponibles por municipio para 2015, utilizados para la construcción del parametro'
M.ClaveDataset = 'CNGMD'
M.ActDatos = '2015'
M.Agregacion = 'Este parámetro utiliza la variable "prog_mod", que indica si un municipio cuenta con Programa ' \
               'de Modernizacion Catastral. Para agregar la información y construir el parámetro, se verifica cuáles ' \
               'de los municipios que integran una ciudad cuentan con programa de modernizacion catastral. El valor ' \
               'del parámetro indica el porcentaje de municipios de una ciudad que cuentan con Programa de ' \
               'Modernizacion Catastral'

M.getmetafromds = 1

# Descripciones generadas desde la clave del parámetro
Meta.fillmeta(M)

M.Notas = 's/n'

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname=M.nomarchivodataset, dtype={'CVE_MUN': 'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.rename_axis('CVE_MUN')

# Generar dataset para parámetro y Variable de Integridad
columnas = 'prog_mod'
existepcat = {1:True, 2:False, 99:None}   # Reemplaza los valores de 1 o 2 con valores lógicos fáciles de usar
dataset[columnas] = dataset[columnas].map(existepcat)
dataset = dataset[~dataset[columnas].isnull()]   # Elimina los renglones en donde no hay informacion sobre PRC
par_dataset = dataset[columnas].to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
