# -*- coding: utf-8 -*-
"""
Started on fri, aug 3rd, 2018
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
M.ClaveParametro = 'P0502'
M.NombreParametro = 'Número de empresas con certificado de Industria Limpia'
M.DescParam = 'Numero de empresas que cuentan con una certificación de las emitidas dentro del marco del ' \
              'Programa Nacional de Auditoría Ambiental, emitidas o actualizadas al mes de julio de 2018'
M.UnidadesParam = 'Número de empresas'
M.TituloParametro = 'CIL'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2018'
M.TipoInt = 3       # 1: Binaria; 2: Multivariable, 3: Integral

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'count'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro.replace('P', 'D')
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Listado de empresas certificadas, tipo de certificado y vigencia'
M.ClaveDataset = 'PROFEPA'
M.ActDatos = '2018'
M.Agregacion = 'Se contó el número de empresas certificadas existentes en cada ciudad del SUN'

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
var1 = 'NOMBRE DE LA INSTALACION'
par_dataset = dataset[var1]
# par_dataset = dataset[var1].astype('float')
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
