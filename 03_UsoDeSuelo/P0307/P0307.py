# -*- coding: utf-8 -*-
"""
Started on fri, feb 02nd, 2018

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
M.ClaveParametro = 'P0307'
M.NombreParametro = 'Disposiciones normativas sustantivas en materia de desarrollo urbano u ordenamiento territorial'
M.DescParam = 'Municipios que cuentan con Disposiciones normativas sustantivas en materia de desarrollo ' \
              'urbano u ordenamiento territorial vigentes en la  Administraciones Públicas Municipales o ' \
              'Delegacionales, al cierre del año 2014'
M.UnidadesParam = 'cantidad'
M.TituloParametro = 'DSDSOT'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'count'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Datos disponibles por municipio para 2015, utilizados para la construcción del parametro'
M.ClaveDataset = 'CNGMD'
M.ActDatos = '2015'
M.Agregacion = 'Este parámetro utilizan las variables "tema_nis" y "tt_dispo". La clave 41 en "tema_nis" indica ' \
               'si un municipio cuenta con disposiciones sustantivas (DS) en materia de Desarrollo Urbano y ' \
               'Ordenamiento Territorial. tt_dispo indica la cantidad de DS de cada tipo en cada municipio. Para ' \
               'agregar la información y construir el parámetro, se utilizan todos los renglones registrados con ' \
               'la clave 41 en "tema_nis" y se eliminan los renglones marcados como cero (0) o vacíos de ' \
               '"tt_dispo". Los renglones restantes se cuentan de acuerdo a la clave SUN a la que pertenecen.'

M.getmetafromds = 1

# Descripciones generadas desde la clave del parámetro
Meta.fillmeta(M)

M.Notas = 'Este parámetro indica el total de disposiciones normativas sustantivas con las que cuenta cada ciudad'

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname=M.nomarchivodataset, dtype={'CVE_MUN': 'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.rename_axis('CVE_MUN')
dataset = dataset.apply(pd.to_numeric).where((pd.notnull(dataset)), None)
del(dataset['estructu']) #

# Generar dataset para parámetro y Variable de Integridad
dataset = dataset[dataset['tt_dispo'].notnull()]      # Eliminar renglones donde 'tt_dispo' está vacío
dataset = dataset[dataset['tt_dispo'] > 0]            # Eliminar renglones donde 'tt_dispo' es igual a cero
columnas = 'tema_nis'
par_dataset = dataset[columnas].to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Estandarizacion de tipos de datos
dataset = dataset.apply(pd.to_numeric).where((pd.notnull(dataset)), None)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
