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
M.ClaveParametro = 'P1006'
M.NombreParametro = 'Número de municipios con aplicación de programas locales orientados a la GIRSU'
M.DescParam = 'Número de municipios que cuentan con algún programa orientado a la gestión integral de residuos ' \
              'sólidos urbanos'
M.UnidadesParam = 'Numero de municipios'
M.TituloParametro = 'MUNRSU'                              # Para nombrar la columna del parametro
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
M.Agregacion = 'Este parámetro utiliza la variable "p13" de la base de datos del Censo Nacional de Gobiernos ' \
               'Municipales y Delegacionales 2015, que indica para cada municipio si este cuenta con programas ' \
               'orientados a la gestion integral de los Residuos Solidos Urbanos (RSU). Se transformaron los valores ' \
               'de la columna de modo que: ' \
               '\n1 = Cuenta con programas, ' \
               '\n0 = No Cuenta con programas, ' \
               '\nNone = Informacion no disponible.' \
               'Para agregar la información y construir el parámetro, se promedia el valor de p13 todos los ' \
               'municipios de los que componen cada ciudad del SUN. De este modo, el valor de P1006 indica el ' \
               'numero de los municipios que componen la ciudad, que cuentan con programas orientados a la ' \
               'Gestión de Residuos Solidos Urbanos'

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
existepgrsu = {1:1, 2:0}   # Reemplaza los valores de 1 o 2 con valores lógicos fáciles de usar
par_dataset = dataset['p13'].to_frame(name = M.ClaveParametro)
par_dataset[M.ClaveParametro] = par_dataset[M.ClaveParametro].map(existepgrsu)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
