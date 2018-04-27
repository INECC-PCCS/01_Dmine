# -*- coding: utf-8 -*-
"""
Started on wed, apr 25th, 2018

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
M.ClaveParametro = 'P0701'
M.NombreParametro = 'Longitud total de la red de carreteras del municipio (excluyendo las autopistas)'
M.DescParam = 'Longitud total de la red de carreteras del municipio (excluyendo las autopistas)'
M.UnidadesParam = 'km'
M.TituloParametro = 'LCarr'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2016'
M.TipoInt = 2

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = 'Long_Carreteras'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Longitud de la red carretera por municipio según tipo de camino y superficie'
M.ClaveDataset = r'AGEO\2017'
M.ActDatos = '2016'
M.Agregacion = 'Se sumó la longitud de la red carretera para los municipios que integran cada ciudad del SUN. Se' \
               ' excluyeron las vialidades de terracería, las Brechas Mejoradas y la red carretera clasificada como ' \
               '"Troncal Federal, Pavimentada", pues incluye tanto caminos libres como de cuota'

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

# Generar dataset para parámetro y Variable de Integridad
dsvar = ['AEP', 'AER', 'CRP', 'CRR']
    # AEP: Alimentadoras Estatales, Pavimentada: También conocidas con el nombre de carreteras secundarias, tienen como propósito principal servir de acceso a las carreteras troncales. Comprende caminos de dos, cuatro o más carriles.
    # AER: Alimentadoras Estatales, Revestida: También conocidas con el nombre de carreteras secundarias, tienen como propósito principal servir de acceso a las carreteras troncales.
    # CRP: Caminos Rurales, Pavimentado.
    # CRR: Caminos Rurales, Revestido.

par_dataset = dataset[dsvar].sum(axis=1, skipna=True)
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
