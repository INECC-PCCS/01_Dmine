# -*- coding: utf-8 -*-
"""
Started on thu, dec 12nd, 2017

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
M.ClaveParametro = 'P1017'
M.NombreParametro = 'Viviendas que no entregan sus residuos al Servicio Publico de Recolección'
M.DescParam = 'Porcentaje de viviendas que no entregan sus residuos al Servcio Publico de Recoleccion, disponiendo de ' \
            'estos de manera inadecuada'
M.UnidadesParam = 'Porcentaje'
M.TituloParametro = 'RSU_NO_SPR'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 2

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'mean'

# Descripciones del proceso de Minería
M.nomarchivodataset = '19'
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Datos disponibles por municipio para 2015, utilizados para la construcción del parametro'
M.ClaveDataset = 'EI2015'
M.ActDatos = '2015'
M.Agregacion = 'Este parámetro utiliza las variables "Queman_residuos" y "Entierran_residuos_o_tiran_en_otro_lugar". ' \
             'Para agregar la información y construir el parámetro, se suman ambas variables y se promedian los ' \
             'valores para los municipios que componen una Ciudad del SUN. En la agregación de datos ' \
             'municipales a ciudades del SUN se han excluido los Municipos en los que la muestra de la Encuesta ' \
             'Intercensal fue clasificada como insuficiente.'
M.getmetafromds = 1

# Descripciones generadas desde la clave del parámetro
Meta.fillmeta(M)

M.Notas = 'Este parámetro considera las viviendas que no entregan sus residuos a un servicio público de ' \
        'recolección, y que disponen de estos quemándolos o tirándolos en lugares inadecuados (Como puede ser en ' \
        'la calle, baldío o río). El valor indica el porcentaje de viviendas en cada ciudad que cumplen esta ' \
        'condicion (por ejemplo, 0.4619 = 0.4916 % y 50.95 = 50.95 %)'

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname=M.nomarchivodataset, dtype={'CVE_MUN': str})
dataset.set_index('CVE_MUN', inplace=True)

# Generar dataset para parámetro y Variable de Integridad
dataset = dataset[~dataset['Municipio'].str.contains('\*\*')]   # Excluir municipios con ** muestra insuficiente
columnas = list(dataset)[4:6]
dataset = dataset[columnas]
par_dataset = dataset.sum(axis=1)               # Construccion del Parámetro
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
