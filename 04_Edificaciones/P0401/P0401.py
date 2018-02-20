# -*- coding: utf-8 -*-
"""
Started on tue, feb 09th, 2018

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
M.ClaveParametro = 'P0401'
M.NombreParametro = 'Edificios con certificación LEED'
M.DescParam = 'Edificios que han recibido algún nivel de certificación de Liderazgo en Energía y desarrollo Ambiental' \
              ' (LEED, por sus siglas en ingles) Otorgado por el Consejo de edificios Verdes de Estados Unidos (USGBC' \
              ' por sus suglas en inglés)'
M.UnidadesParam = 'Numero de edificios'
M.TituloParametro = 'LEEDB'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2018'
M.TipoInt = 3

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'count'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'PCCS_leed_projects'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Base de datos de edificios LEED recopilada al 14 de febrero de 2018, en base a la cual se' \
                       'construyó el parámetro'
M.ClaveDataset = 'LEED'
M.ActDatos = '2018'
M.Agregacion = 'Se extrajo la lista de edificios con certificación LEED del sitio web del USGBC. A partir del código ' \
               'postal se ubicó el municipio en el que se encuentra cada edificio y se etiquetó con la clave ' \
               'geoestadística de 5 dígitos de INEGI (columna CVE_MUN en la base de datos de la PCCS). Para ' \
               'construir el parámetro, se clasificó cada edificio por ciudad del SUN con base en su CVE_MUN, y se ' \
               'contó el número de edificios por ciudad.'

M.getmetafromds = 1

# Descripciones generadas desde la clave del parámetro
Meta.fillmeta(M)

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname='DATOS', dtype={'CVE_MUN': 'str', 'CP':'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.rename_axis('CVE_MUN')

# Generar dataset para parámetro y Variable de Integridad
par_dataset = dataset['Building'].to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
