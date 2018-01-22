# -*- coding: utf-8 -*-
"""
Started on Tue Jan  9 10:52:27 2018

@author: carlos.arana

Descripcion:
    Compilador principal de datos. A partir del input de metadatos y un dataframe estándar, genera la ficha de
    parámetro que incluye:
    1. Archivo .xlsx legible por humanos
    2. Archivo .json legible por sistemas informáticos
    3. Documentacion en archivo integrador de parámetros, tanto excel como .json
    4. Archivo readme.md para lectura web

    Espera el siguiente input:
        1. M [Class]: Metadatos (Clase estándar)
        2. par_dataset [Dataframe]: Datos del parámetro procesados por la función VarInt
        3. variables_dataset [Dataframe]: Variables del parámetro procesadas por la función VarInt

"""

import pandas as pd
import json
import codecs

from SUN.asignar_sun import asignar_sun
from SUN_integridad.SUN_integridad import SUN_integridad
from PCCS_variables.PCCS_variables import variables
from ParametroEstandar.ParametroEstandar import ParametroEstandar
from DocumentarParametro.DocumentarParametro import DocumentarParametro


def compilar(M, dataset, par_dataset, variables_dataset):
    # Revisa si la variable requiere que se especifique el array
    M.TipoVar = M.TipoVar.lower()
    stdvarset = list('cdobn')   #[c]ontinua, [d]iscreta, [o]rdinal, [b]inaria, [n]ominal
    check1 = M.TipoVar in stdvarset     # Revisa si la variable está mal especificada
    check2 = not(M.TipoVar == 'c' or M.TipoVar == 'd')   # Revisa si la variable no requiere array
    check3 = M.array == []      # Revisa si el array está vacío
    if not check1: raise AttributeError('No se reconoce el tipo de variable especificado: {}'.format(M.TipoVar))
    if check2 and check3: raise ValueError('M.array no puede estar vacío para variables del tipo {}'.format(M.TipoVar))

    # Nombrar columna de integridad
    ColIntegridad = M.ClaveParametro.replace("P", "I")

    # Agregar datos por ciudad para parametro
    variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'NOM_ENT']
    DatosLimpios = asignar_sun(par_dataset, vars=variables_SUN)
    OrdenColumnas = (variables_SUN + variables_dataset)
    DatosLimpios = DatosLimpios[OrdenColumnas]    # Reordenar las columnas

    # Consolidar datos por ciudad para hoja_datos
    dataset.columns = [M.ClaveParametro+"_"+i for i in list(dataset)]
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
    param = param_dataset.groupby(level=0).agg(M.TipoAgr)[M.ClaveParametro]         # Agregacion por ciudad
    intparam = param_dataset.groupby(level=0).agg('mean')['VAR_INTEGRIDAD']    # Integridad por ciudad
    Tipo_Sun = integridad_parametro['EXISTENCIA']['TIPO_SUN']
    Tipo_Sun = Tipo_Sun.groupby(Tipo_Sun.index).first()
    std_nomsun = param_dataset['CVE_SUN'].map(str)+' - '+param_dataset['NOM_SUN']   # Nombres estandar CVE_SUN + NOM_SUN
    std_nomsun.drop_duplicates(keep='first', inplace=True)
    Parametro = pd.DataFrame()
    Parametro['CIUDAD'] = std_nomsun
    Parametro['TIPO_SUN'] = Tipo_Sun
    Parametro[M.ClaveParametro] = param
    Parametro[ColIntegridad] = intparam
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
        'DESCRIPCION DEL PARAMETRO': None,
        'Clave': M.ClaveParametro,
        'Nombre del Parametro': M.NombreParametro,
        'Descripcion del Parametro': M.DescParam,
        'Periodo' : M.PeriodoParam,
        'Unidades': M.UnidadesParam
    }

    d_hojas = {
        'METADATOS': 'Descripciones y notas relativas al Dataset',
        'PARAMETRO': 'Dataset resultado de la minería, agregado por clave del Sistema Urbano Nacional, '
                     'para utilizarse en la construcción de Indicadores',
        'DATOS': M.ContenidoHojaDatos,
        'INTEGRIDAD': 'Revision de integridad de la información POR CLAVE DEL SUN. ' 
                      'Promedio de VAR_INTEGRIDAD de los municipios que componen una ciudad. '
                      'Si no se tiene información para el municipio, VAR_INTEGRIDAD es igual a cero',
        'EXISTENCIA': 'Revision de integridad de la información POR MUNICIPIO.',
        '     ': None,
        'DESCRIPCION DE VARIABLES': None
    }

    d_mineria = {
        '  ': None,
        'DESCRIPCION DEL PROCESO DE MINERIA:': None,
        'Nombre del Dataset': M.NomDataset,
        'Descripcion del dataset': M.DescDataset,
        'Disponibilidad Temporal': M.DispTemp,
        'Periodo de actualizacion': M.PeriodoAct,
        'Nivel de Desagregacion': M.DesagrMax,
        'Notas': M.Notas,
        'Fuente': M.NomFuente,
        'URL_Fuente': M.UrlFuente,
        'Dataset base': M.DSBase,
        'Repositorio de mineria': M.RepoMina,
        'Método de Agregación': M.Agregacion,
        'VAR_INTEGRIDAD': M.DescVarIntegridad,
        ' ': None,
        'HOJAS INCLUIDAS EN EL LIBRO': None
    }

    descripcion_parametro = pd.DataFrame.from_dict(d_parametro, orient='index').rename(columns={0: 'DESCRIPCION'})
    descripcion_mineria = pd.DataFrame.from_dict(d_mineria, orient='index').rename(columns={0: 'DESCRIPCION'})
    descripcion_hojas = pd.DataFrame.from_dict(d_hojas, orient='index').rename(columns={0: 'DESCRIPCION'})
    MetaParametro = descripcion_parametro.append(descripcion_mineria).append(descripcion_hojas).append(metavariables)

    # Archivo JSON
    del (d_parametro['DESCRIPCION DEL PARAMETRO'])
    del ([d_mineria['  '], d_mineria[' '], d_mineria['HOJAS INCLUIDAS EN EL LIBRO'],
          d_mineria['DESCRIPCION DEL PROCESO DE MINERIA:']])
    BaseJSON = {}
    JSONVars = metavariables.to_dict()['DESCRIPCION']
    JSONVars = {key:JSONVars[key] for key in [M.ClaveParametro, ColIntegridad]}

    BaseJSON['Metadatos'] = {
        'Descripcion': d_parametro,
        'Memoria Mineria de datos' : d_mineria,
        'Variables': JSONVars,
        'handling': {
            'VarType': M.TipoVar,
            'array': M.array,
            'dtype': M.ParDtype
        }
    }

    BaseJSON['Parametro'] = Parametro[[M.ClaveParametro, ColIntegridad]].to_dict('index')
    jsonfile = M.DirDestino + '\\' + M.ClaveParametro + '\\' + M.ClaveParametro + '.json'

    # Diccionario de Descripciones
    DescParametro = {
        'ClaveParametro': M.ClaveParametro,
        'NombreParametro': M.NombreParametro,
        'info_completa': info_completa,
        'info_sin_info': info_sin_info,
        'info_incomple': info_incomple,
        'RutaSalida': M.DirDestino,
        'Clave de Dimension': M.ClaveDimension,
        'Nombre de Dimension': M.NomDimension,
        'Titulo de Columna': M.TituloParametro,
        'Actualizacion de datos': M.ActDatos,
        'ClaveIntegridad': ColIntegridad
    }

    # Convertir NaN en None
    MetaParametro = MetaParametro.where((pd.notnull(MetaParametro)), None)
    Parametro = Parametro.where((pd.notnull(Parametro)), None)
    DatosLimpios = DatosLimpios.where((pd.notnull(DatosLimpios)), None)
    hoja_datos = hoja_datos.where((pd.notnull(hoja_datos)), None)

    # Crear archivo de Excel, JSON y documentar parametro
    # json.dump(BaseJSON, open(jsonfile, 'w'))
    with open(jsonfile, 'wb') as f:
        json.dump(BaseJSON, codecs.getwriter('utf-8')(f), ensure_ascii=False)
    print('Archivo JSON generado en {}'.format(jsonfile))
    ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro, hoja_datos)
    DocumentarParametro(DescParametro, MetaParametro, Parametro)

