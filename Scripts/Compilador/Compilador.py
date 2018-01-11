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
        2. Par_Dataset [Dataframe]: Datos del parámetro procesados por la función VarInt
        3. Variables_Dataset [Dataframe]: Variables del parámetro procesadas por la función VarInt

"""

module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)

from classes.Meta import Meta

def compilar(M, Par_Dataset, Variables_Dataset):

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
