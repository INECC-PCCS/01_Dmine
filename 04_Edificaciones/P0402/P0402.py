# -*- coding: utf-8 -*-
"""
Started on fri, dec 1st, 2017

@author: carlos.arana

"""
# Librerias utilizadas
import pandas as pd
import numpy as np
import sys

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)

from SUN.asignar_sun import asignar_sun
from VarInt.VarInt import VarInt
from SUN_integridad.SUN_integridad import SUN_integridad
from PCCS_variables.PCCS_variables import variables
from ParametroEstandar.ParametroEstandar import ParametroEstandar
from AsignarDimension.AsignarDimension import AsignarDimension
from DocumentarParametro.DocumentarParametro import DocumentarParametro

"""
Las librerias locales utilizadas renglones arriba se encuentran disponibles en las siguientes direcciones:
SCRIPT:             | DISPONIBLE EN:
------              | ------------------------------------------------------------------------------------
asignar_sun         | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN
VarInt              | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/VarInt
SUN_integridad      | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN_integridad
variables           | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/PCCS_variables
ParametroEstandar   | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/ParametroEstandar
AsignarDimension    | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/AsignarDimension
DocumentarParametro | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/DocumentarParametro
"""

# Documentacion del Parametro ---------------------------------------------------------------------------------------
# Descripciones del Parametro
ClaveParametro = 'P0403'
NombreParametro = 'Viviendas con drenaje'
DescParam = 'Porcentaje de viviendas particulares habitadas que disponen de drenaje por ciudad'
UnidadesParam = 'Porcentaje'
TituloParametro = 'VIV_DRENAJE'                              # Para nombrar la columna del parametro
PeriodoParam = '2015'
DescVarIntegridad = 'La variable de integridad municipal para esta Dataset es binaria: \n' \
                    '1 =  El municipio cuenta con informacion \n0 = El municipio no cuenta con información'

# Descripciones del proceso de Minería
nomarchivodataset = '26'
ArchivoDataset = nomarchivodataset + '.xlsx'
ContenidoHojaDatos = 'Datos disponibles por municipio para 2015, utilizados para la construcción del parametro'
ClaveDataset = 'EI2015'
ActDatos = '2015'
Agregacion = 'Promedio de porcentaje de viviendas que desalojan a red pública, fosa septica o tanque septico'

# Descripciones generadas desde la clave del parámetro
DirFuente = r'D:\PCCS\01_Dmine\Datasets\{}'.format(ClaveDataset)
DSBase = '"{}.xlsx", disponible en ' \
         'https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/{}'.format(ArchivoDataset, ClaveDataset)
ClaveDimension = ClaveParametro[1:3]
NomDimension = AsignarDimension(ClaveDimension)['nombre']
DirDimension = ClaveDimension + "_" + AsignarDimension(ClaveDimension)['directorio']
RepoMina = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/{}/{}'.format(DirDimension, ClaveParametro)
DirDestino = r'D:\PCCS\01_Dmine\{}'.format(ClaveDimension+"_"+AsignarDimension(ClaveDimension)['directorio'])

# Cargar metadatos del dataset
metadataset = pd.read_excel(DirFuente + '\\' + ArchivoDataset,
                        sheetname="METADATOS")
metadataset.set_index('Metadato', inplace=True)
metadataset = metadataset['Descripcion']

# Descripciones generadas desde los metadatos del dataset.
NomDataset = metadataset['Nombre del Dataset']
DescDataset = metadataset['Descripcion del dataset']
DispTemp = metadataset['Disponibilidad Temporal']
PeriodoAct = metadataset['Periodo de actualizacion']
DesagrMax = metadataset['Nivel de Desagregacion']
Notas = 'Para la obtención del parámetro se suma la el porcentaje de viviendas cuyo drenaje desaloja a Red pública ' \
        'con el porcentaje de viviendas cuyo. drenaje desaloja a Fosa séptica o Tanque séptico. El resultado de esta' \
        'suma se multiplica por el porcentaje de Viviendas que cuentan con Drenaje y el parámetro es el ' \
        'producto de esta multiplicación. De esta manera, se excluyen del parámetro las viviendas cuyo drenaje ' \
        'desaloja a Río, Lago o mar. En la agregación de datos municipales a ciudades del SUN se han excluido los' \
        'Municipos en los que la muestra de la Encuesta Intercensal fue insuficiente'
NomFuente = metadataset['Fuente']
UrlFuente = metadataset['URL_Fuente']

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(DirFuente + '\\' + ArchivoDataset,
                        sheetname=nomarchivodataset, dtype={'CVE_MUN': str})
dataset.set_index('CVE_MUN', inplace=True)

# Generar dataset para parámetro y Variable de Integridad
dataset = dataset[~dataset['Municipio'].str.contains('\*\*')]   # Excluir municipios con ** muestra insuficiente
colummas = ['Viviendas particulares habitadas',                 # Culumnas que se utilizan para construi el parámetro
            'Drenaje_Total',
            'Drenaje_desaloja_a_Red_publica',
            'Drenaje_desaloja_a_Fosa_Septica_o_Tanque_Septico']
dataset = dataset[colummas]
par_dataset = dataset['Drenaje_Total'] * (                      # Construccion del Parámetro
              dataset['Drenaje_desaloja_a_Red_publica'] + dataset['Drenaje_desaloja_a_Fosa_Septica_o_Tanque_Septico']
              ) / 100
par_dataset = par_dataset.to_frame(name = ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo = 2)

# Agregar datos por ciudad para parametro
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'NOM_ENT']
DatosLimpios = asignar_sun(par_dataset, vars=variables_SUN)
OrdenColumnas = (variables_SUN + variables_dataset)
DatosLimpios = DatosLimpios[OrdenColumnas]    # Reordenar las columnas

# Consolidar datos por ciudad para hoja_datos
dataset.columns = [ClaveParametro+"_"+i for i in list(dataset)]
var_disponibles = list(dataset)
dataset['CVE_MUN'] = dataset.index
hoja_datos = asignar_sun(dataset)
hoja_datos = hoja_datos[(['CVE_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN'] + var_disponibles)].set_index('CVE_MUN')

# Revision de integridad
integridad_parametro = SUN_integridad(DatosLimpios)
info_completa = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 1)      # Para generar grafico de integridad
info_sin_info = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 0)      # Para generar grafico de integridad
info_incomple = 135 - info_completa - info_sin_info                             # Para generar grafico de integridad

# Construccion del Parametro
param_dataset = DatosLimpios.set_index('CVE_SUN')
param_dataset['CVE_SUN'] = param_dataset.index
param = param_dataset.groupby(level=0).agg('mean')[ClaveParametro]         # Agregacion por ciudad
intparam = param_dataset.groupby(level=0).agg('mean')['VAR_INTEGRIDAD']    # Integridad por ciudad
Tipo_Sun = integridad_parametro['EXISTENCIA']['TIPO_SUN']
Tipo_Sun = Tipo_Sun.groupby(Tipo_Sun.index).first()
std_nomsun = param_dataset['CVE_SUN'].map(str)+' - '+param_dataset['NOM_SUN']   # Nombres estandar CVE_SUN + NOM_SUN
std_nomsun.drop_duplicates(keep='first', inplace=True)
Parametro = pd.DataFrame()
Parametro['CIUDAD'] = std_nomsun
Parametro['TIPO_SUN'] = Tipo_Sun
Parametro[ClaveParametro] = param
Parametro['INTEGRIDAD'] = intparam
Parametro = Parametro.sort_index()

# Lista de Variables
variables_locales = sorted(list(set(list(DatosLimpios) +
                                    list(dataset) +
                                    list(integridad_parametro['INTEGRIDAD']) +
                                    list(integridad_parametro['EXISTENCIA']) +
                                    list(Parametro))))
metavariables = variables(variables_locales)

# Metadatos
d_parametro = {
    'DESCRIPCION DEL PARAMETRO': np.nan,
    'Clave': ClaveParametro,
    'Nombre del Parametro': NombreParametro,
    'Descripcion del Parametro': DescParam,
    'Periodo' : PeriodoParam,
    'Unidades': UnidadesParam
}

d_hojas = {
    'METADATOS': 'Descripciones y notas relativas al Dataset',
    'PARAMETRO': 'Dataset resultado de la minería, agregado por clave del Sistema Urbano Nacional, '
                 'para utilizarse en la construcción de Indicadores',
    'DATOS': ContenidoHojaDatos,
    'INTEGRIDAD': 'Revision de integridad de la información POR CLAVE DEL SUN. ' 
                  'Promedio de VAR_INTEGRIDAD de los municipios que componen una ciudad. '
                  'Si no se tiene información para el municipio, VAR_INTEGRIDAD es igual a cero',
    'EXISTENCIA': 'Revision de integridad de la información POR MUNICIPIO.',
    '     ': np.nan,
    'DESCRIPCION DE VARIABLES': np.nan
}

d_mineria = {
    '  ': np.nan,
    'DESCRIPCION DEL PROCESO DE MINERIA:': np.nan,
    'Nombre del Dataset': NomDataset,
    'Descripcion del dataset': DescDataset,
    'Disponibilidad Temporal': DispTemp,
    'Periodo de actualizacion': PeriodoAct,
    'Nivel de Desagregacion': DesagrMax,
    'Notas': Notas,
    'Fuente': NomFuente,
    'URL_Fuente': UrlFuente,
    'Dataset base': DSBase,
    'Repositorio de mineria': RepoMina,
    'Método de Agregación': Agregacion,
    'VAR_INTEGRIDAD': DescVarIntegridad,
    ' ': np.nan,
    'HOJAS INCLUIDAS EN EL LIBRO': np.nan
}

descripcion_parametro = pd.DataFrame.from_dict(d_parametro, orient='index').rename(columns={0: 'DESCRIPCION'})
descripcion_mineria = pd.DataFrame.from_dict(d_mineria, orient='index').rename(columns={0: 'DESCRIPCION'})
descripcion_hojas = pd.DataFrame.from_dict(d_hojas, orient='index').rename(columns={0: 'DESCRIPCION'})
MetaParametro = descripcion_parametro.append(descripcion_mineria).append(descripcion_hojas).append(metavariables)

# Diccionario de Descripciones
DescParametro = {
    'ClaveParametro': ClaveParametro,
    'NombreParametro': NombreParametro,
    'info_completa': info_completa,
    'info_sin_info': info_sin_info,
    'info_incomple': info_incomple,
    'RutaSalida': DirDestino,
    'Clave de Dimension': ClaveDimension,
    'Nombre de Dimension': NomDimension,
    'Titulo de Columna': TituloParametro,
    'Actualizacion de datos': ActDatos
}

# Crear archivo de Excel y documentar parametro
ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro, hoja_datos)
DocumentarParametro(DescParametro, MetaParametro, Parametro)